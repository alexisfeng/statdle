from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
    Regexp
)


from .models import User


class SearchForm(FlaskForm):
    search_query = IntegerField("Query", validators=[InputRequired(), NumberRange(min=1, max=9999)])
    submit = SubmitField("Search")


class WordlePasteForm(FlaskForm):
    text = TextAreaField(
        "Wordle", validators=[InputRequired(), Length(min=20, max=71)]
    )
    submit = SubmitField("Submit Wordle")

class WordleManualForm(FlaskForm):
    wordle_day = IntegerField("Wordle day", validators=[InputRequired(), NumberRange(min=1, max=9999)])
    guesses = StringField("Guesses", validators=[InputRequired(), Length(min=1, max=1)])
    submit = SubmitField("Submit Wordle")

    def validate_guesses(self, guesses):
        valid_guesses = ["1","2","3","4","5","6","X"]
        print(guesses)
        if guesses.data not in valid_guesses:
            raise ValidationError("Invalid number of guesses!")
    

class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField(
        "Password", 
        validators=[
            InputRequired(),
            Length(min=8, message="Password be at least 8 characters"),
            Regexp("^(?=.*[a-z])", message="Password must have a lowercase character."),
            Regexp("^(?=.*[A-Z])", message="Password must have an uppercase character.")
        ]
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Log In")


class UpdatePasswordForm(FlaskForm):
    current_password = PasswordField("Current Password", validators=[InputRequired()])
    new_password = PasswordField(
        "New Password", 
        validators=[
            InputRequired(),
            Length(min=8, message="Password be at least 8 characters."),
            Regexp("^(?=.*[a-z])", message="Password must have a lowercase character."),
            Regexp("^(?=.*[A-Z])", message="Password must have an uppercase character.")
        ]
    )
    confirm_password = PasswordField(
        "Confirm New Password", validators=[InputRequired(), EqualTo("new_password")]
    )
    submit = SubmitField("Update password")
