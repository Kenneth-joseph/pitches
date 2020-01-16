from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,TextAreaField,SubmitField
from wtforms.validators import Required

class Updateprofile(FlaskForm):
    bio=TextAreaField('Briefly describe yourself', validators=Required)
    submit = SubmitField('Update')

class Topicform(FlaskForm):
    title = StringField('Title', validators=[Required()])
    category= SelectField('Category',choices=[('Music','Music'),('Sports','Sports'),('Jobs','Jobs'),('Quotes','Quotes')],validators=[Required()])
    post=TextAreaField('Post', validators=[Required()])
    submit=SubmitField('Share Your Pitch')

class CommentForm(FlaskForm):
    comment = TextAreaField('comment', validators=[Required()])
    submit = SubmitField('post')


