from flask_wtf import FlaskForm
from wtforms import  SubmitField, StringField
from wtforms.validators import DataRequired

class CreatePostForm(FlaskForm):
    img = StringField('Image URL: ', validators=[DataRequired()])
    caption = StringField('Password: ', validators=[DataRequired()])
    location = StringField('Location: ')
    submit_btn = SubmitField('Create Post')