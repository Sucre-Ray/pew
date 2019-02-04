import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # SQLALCHEMY_DATABASE_URI = 'mysql://<username>:<password>@<server_name>/<db_name>'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'