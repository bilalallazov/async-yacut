import re

from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, URLField
from wtforms.validators import DataRequired, Length, Optional, ValidationError

from yacut.models import URLMap
from yacut.utils import DUPLICATE_MSG, RESERVED_SHORT_IDS


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле.')],
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Optional(), Length(max=16)],
    )

    def validate_custom_id(self, field):
        if not field.data:
            return
        if len(field.data) > 16:
            raise ValidationError(
                'Длина короткой ссылки не должна превышать 16 символов.'
            )
        if not re.match(r'^[a-zA-Z0-9]+$', field.data):
            raise ValidationError(
                'Указано недопустимое имя для короткой ссылки'
            )
        if field.data in RESERVED_SHORT_IDS:
            raise ValidationError(DUPLICATE_MSG)
        if URLMap.query.filter_by(short=field.data).first():
            raise ValidationError(DUPLICATE_MSG)


class FileUploadForm(FlaskForm):
    files = MultipleFileField(
        'Файлы',
        validators=[DataRequired(message='Выберите хотя бы один файл.')],
    )
