from flask_login import UserMixin
from . import db, login_manager
from . import config
from .utils import current_time


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()


class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)

    def get_id(self):
        return self.username


class Wordle(db.Document):
    user = db.ReferenceField(User, required=True)
    grid = db.StringField(required=True, max_length=55)
    date = db.StringField(required=True)
    wordle_day = db.IntField(required=True)
    guesses = db.StringField(required=True, min_length=1, max_length=1)
