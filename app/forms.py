from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.models import User


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(8, 120)])
    name = StringField('Name', validators=[DataRequired(), Length(4, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(),
                                                              EqualTo('password')])
    accept_policy = BooleanField('I accept Privacy Policy')
    submit = SubmitField('Register')

    def validate_accept_policy(self, accept_policy):
        if not accept_policy.data:
            raise ValidationError('Please, accept Privacy Policy before submitting the form.')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(),
                                                              EqualTo('password')])
    submit = SubmitField('Reset')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Request')


class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    bio = TextAreaField('About me', validators=[Length(min=0, max=300)])
    submit = SubmitField('Save')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    new_password2 = PasswordField('Confirm New Password', validators=[DataRequired(),
                                                                      EqualTo('new_password')])
    submit = SubmitField('Save')

