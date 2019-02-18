from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    bio = TextAreaField('About me', validators=[Length(min=0, max=300)])
    submit = SubmitField('Save')