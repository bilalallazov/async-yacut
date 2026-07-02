import asyncio

from flask import Blueprint, abort, current_app, redirect, render_template

from yacut.exceptions import InvalidAPIUsage
from yacut.forms import FileUploadForm, URLForm
from yacut.models import URLMap
from yacut.utils import get_short_link
from yacut.yandex_disk import upload_files

bp = Blueprint('views', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    short_link = None
    if form.validate_on_submit():
        try:
            url_map = URLMap.create(
                form.original_link.data,
                form.custom_id.data
            )
        except InvalidAPIUsage as error:
            form.custom_id.errors.append(error.message)
        else:
            short_link = get_short_link(url_map.short)
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
            url_map = URLMap.create(download_url)
            uploaded_files.append({
                'filename': filename,
                'short_link': get_short_link(url_map.short),
            })
    return render_template(
        'files.html',
        form=form,
        uploaded_files=uploaded_files,
    )


@bp.route('/<short_id>')
def redirect_view(short_id):
    url_map = URLMap.get(short_id)
    if url_map is None:
        abort(404)
    return redirect(url_map.original)
