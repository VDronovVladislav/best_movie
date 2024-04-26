import os
import random

from flask import render_template, session, flash
from flask import request

from . import app, db
from .forms import MovieForm
from .models import Movie


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Вью-функция стартовой страницы."""
    return render_template('index.html')


@app.route('/start_tournament', methods=['POST'])
def start_tournament():
    """Вью-функция страницы соревнования."""
    try:
        tournament_list = session['tournament_list']
        winners_list = session['winners_list']
        chosen_film_id = int(request.form['chosen_film'])
        winners_list.append(chosen_film_id)
        session['winners_list'] = winners_list
        if not tournament_list:
            if len(winners_list) == 1:
                winner = Movie.query.get(winners_list[0])
                return render_template('winner.html', winner=winner)
            else:
                tournament_list.extend(winners_list)
                winners_list.clear()
                session['winners_list'] = winners_list
                session['tournament_list'] = tournament_list
        left_film_id = random.choice(tournament_list)
        tournament_list.remove(left_film_id)
        right_film_id = random.choice(tournament_list)
        tournament_list.remove(right_film_id)
        session['tournament_list'] = tournament_list
        left_film = Movie.query.get(left_film_id)
        right_film = Movie.query.get(right_film_id)
        return render_template(
                'choice.html', left_film=left_film, right_film=right_film
            )
    except KeyError:
        film_count = int(request.form['filmCount'])
        session['tournament_list'] = [
            movie.id for movie in Movie.query.limit(film_count).all()
        ]
        session['winners_list'] = []
        session['temporary_list'] = []
        tournament_list = session['tournament_list']
        winners_list = session['winners_list']
        left_film_id = random.choice(tournament_list)
        tournament_list.remove(left_film_id)
        right_film_id = random.choice(tournament_list)
        tournament_list.remove(right_film_id)
        session['tournament_list'] = tournament_list
        left_film = Movie.query.get(left_film_id)
        right_film = Movie.query.get(right_film_id)
        return render_template(
            'choice.html', left_film=left_film, right_film=right_film
        )


@app.route('/add', methods=['POST', 'GET'])
def add_movie_view():
    """Вью-функция добавления фильма."""
    form = MovieForm()
    if form.validate_on_submit():
        image = form.image.data
        name = form.name.data
        if Movie.query.filter_by(name=name).first():
            flash('Этот фильм уже добавлен! '
                  'Попробуйте ввести оригинальное название.')
            return render_template('add_movie.html', form=form)
        if not image:
            flash('У фильма должен быть постер!')
            return render_template('add_movie.html', form=form)
        filename = image.filename
        image.save(os.path.join(app.config['DOWNLOAD_FOLDER'], filename))
        movie = Movie(
            name=form.name.data,
            image=filename
        )
        db.session.add(movie)
        db.session.commit()
    return render_template('add_movie.html', form=form)
