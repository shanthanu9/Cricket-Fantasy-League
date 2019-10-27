from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    # TODO: Login via email
    # TODO: Verify if the entered email is correct
    # TODO: Support password reset.. (maybe too ambitous)

class RegistrationFrom(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register Now')

    # All `validate_*` functions are taken as custom validators by WTForms

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username taken. Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('An account is already there with the given email ID.')

class TeamSelectionForm(FlaskForm):
    # TODO: Replace label with correct player name
    # t1_players = [BooleanField('player') for i in range(11)]
    # t2_players = [BooleanField('player') for i in range(11)]
    t1_players = FieldList(BooleanField('team1', min_entries=3, max_entries=11))
    t2_players = FieldList(BooleanField('team2', min_entries=0, max_entries=11))

# TODO: Team selection form