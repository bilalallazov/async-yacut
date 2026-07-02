from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, URLField
from wtforms.validators import DataRequired, Length, Optional, ValidationError

from yacut.constants import SHORT_ID_MAX_LENGTH
from yacut.exceptions import InvalidAPIUsage
from yacut.validators import validate_custom_id


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле.')],
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Optional(), Length(max=SHORT_ID_MAX_LENGTH)],
    )

    def validate_custom_id(self, field):
        if not field.data:
            return
        try:
            validate_custom_id(field.data)
        except InvalidAPIUsage as error:
            raise ValidationError(error.message) from error


class FileUploadForm(FlaskForm):
    files = MultipleFileField(
        'Файлы',
        validators=[DataRequired(message='Выберите хотя бы один файл.')],
    )
