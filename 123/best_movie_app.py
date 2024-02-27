import os
from pprint import pprint
from PIL import Image

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired, Length
from flask import Flask, render_template, send_from_directory, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename



app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['SECRET_KEY'] = 'MY SECRET KEY'

db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    image = db.Column(db.String(255))

    def get_image_path(self):
        return os.path.join(app.config['UPLOAD_FOLDER'], self.image)


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


@app.route('/', methods=['GET', 'POST'])
def index_view():
    return render_template('index.html')


@app.route('/start_tournament', methods=['POST', 'GET'])
def start_tournament():
    movie = Movie.query.get(4)
    return render_template('choice.html', movie=movie)


@app.route('/add', methods=['POST', 'GET'])
def add_movie_view():
    form = MovieForm()
    if form.validate_on_submit():
        image = form.image.data
        if image:
            filename = image.filename
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            movie = Movie(
                name=form.name.data,
                image=filename
            )
            db.session.add(movie)
            db.session.commit()
            return 'Фильм успешно добавлен!'
    return render_template('add_movie.html', form=form)


if __name__ == '__main__':
    app.run()
