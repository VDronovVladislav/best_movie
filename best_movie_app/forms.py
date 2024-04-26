from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired, Length


class MovieForm(FlaskForm):
    name = StringField(
        'Введите название фильма',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 128)]
    )
    image = FileField(
        'Image File',
        validators=[FileAllowed(['jpg', 'jpeg', 'png'],
                    'Допустимы только изображения в форматах jpg, jpeg, png.')]
    )
    submit = SubmitField('Добавить')
