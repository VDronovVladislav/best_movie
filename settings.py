import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DOWNLOAD_FOLDER = 'best_movie_app/static/images'
    UPLOAD_FOLDER = 'static/images'
    SECRET_KEY = os.getenv('SECRET_KEY')
