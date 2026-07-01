import asyncio

from flask import Blueprint, abort, current_app, redirect, render_template

from yacut import db
from yacut.forms import FileUploadForm, URLForm
from yacut.models import URLMap
from yacut.utils import get_short_link, get_unique_short_id
from yacut.yandex_disk import upload_files

bp = Blueprint('views', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    short_link = None
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if custom_id:
            short_id = custom_id
        else:
            short_id = get_unique_short_id()
        url_map = URLMap(
            original=form.original_link.data,
            short=short_id,
        )
        db.session.add(url_map)
        db.session.commit()
        short_link = get_short_link(short_id)
    return render_template('index.html', form=form, short_link=short_link)


@bp.route('/files', methods=['GET', 'POST'])
def file_upload_view():
    form = FileUploadForm()
    uploaded_files = []
    if form.validate_on_submit():
        token = current_app.config['DISK_TOKEN']
        files_data = [
            (file.read(), file.filename)
            for file in form.files.data
        ]
        download_urls = asyncio.run(upload_files(files_data, token))
        for (_, filename), download_url in zip(files_data, download_urls):
            short_id = get_unique_short_id()
            url_map = URLMap(original=download_url, short=short_id)
            db.session.add(url_map)
            uploaded_files.append({
                'filename': filename,
                'short_link': get_short_link(short_id),
            })
        db.session.commit()
    return render_template(
        'files.html',
        form=form,
        uploaded_files=uploaded_files,
    )


@bp.route('/<short_id>')
def redirect_view(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        abort(404)
    return redirect(url_map.original)
