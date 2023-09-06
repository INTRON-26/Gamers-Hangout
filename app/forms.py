from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError 
from app.model import Gamer 
from flask import request

class RegisterForm(FlaskForm):
    gamertag = StringField('Gamertag',validators = [DataRequired(), Length(min = 2, max = 30)])
    password = PasswordField('Password',validators= [DataRequired()])
    confirmpwd = PasswordField('Confirm Password',validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Join')

    def validate_gamer(self, gamertag):
        gamer = Gamer.query.filter_by(gamertag = gamertag.data).first()
        if gamer:
            raise ValidationError('Gamer-tag already exists!')

class LoginForm(FlaskForm):
    gamertag = StringField('Gamertag',validators = [DataRequired(), Length(min = 2, max = 30)])
    password = PasswordField('Password',validators= [DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class UpdateForm(FlaskForm):
    gamertag = StringField('Gamertag',validators = [DataRequired(), Length(min = 2, max = 30)])
    image = FileField('Update Profile picture',validators = [FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Update')

    def validate_gamer(self, gamertag):
        if gamertag.data != current_user.gamertag:
            gamer = Gamer.query.filter_by(gamertag=gamertag.data).first()
            if gamer:
                raise ValidationError('Gamer-tag already exists!')
            

class PostForm(FlaskForm):
    title = StringField('Title',validators = [DataRequired()])
    content = TextAreaField('Content', validators = [DataRequired()])
    image = FileField('Add Media to your post',validators = [FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Post')
