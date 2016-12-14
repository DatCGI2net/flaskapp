
from app import db
from flask_login.mixins import UserMixin
import md5

class User(UserMixin, db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64), index=False, unique=False)
    social_id = db.Column(db.String(64), nullable=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

    def __repr__(self):
        
        return '<User %r>' % (self.nickname)
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return  True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        
        try:
            return unicode(self.id)
        
        except NameError:
            return str(self.id)
        
        
    def avatar(self, size):
        #(md5(self.email.encode('utf-8')).hexdigest(), size)
        ##           md5(self.email.encode('utf-8')).hexdigest()
        
        bas64_str= md5.new(self.email.encode('utf-8')).hexdigest()
        url = 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (bas64_str,
                                                               size)
        return url
        
        
class Post(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        
        return '<Post %r>' % (self.body)
    
    
    
    