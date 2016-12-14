from flask_wtf.form import Form
from wtforms.fields.core import StringField, BooleanField
from wtforms.validators import DataRequired, Length
from wtforms.fields.simple import TextAreaField
from app.models import User


class LoginForm(Form):
    
    nickname = StringField('nickname', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    
   
class EditForm(Form):
    
    nickname = StringField('nickname',
                           validators=[DataRequired()])
    about_me = TextAreaField('about_me',
                             validators=[Length(min=0,
                                                max=140)])
    def __init__(self, original_nickname, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.original_nickname = original_nickname
        
        
    
    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        
        user = User.query.filter_by(nickname=self.nickname.data).first()
        
        if user is not None:
            
            self.nickname.errors.append('This nickname is already used')
            return False
        
        return True
     