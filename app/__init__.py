
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login.login_manager import LoginManager
#from flask_openid import OpenID
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT
from config import MAIL_PASSWORD, MAIL_USERNAME

app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

#oid = OpenID(app, os.path.join(basedir, 'tmp'))

if not app.debug:
    import logging
    """
    from logging.handlers import SMTPHandler
    
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
    
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 
                               'noreply@'+MAIL_SERVER, ADMINS, 
                               "microblog failure", credentials)
    
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
    
    """
    
    from logging.handlers import RotatingFileHandler
    
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a',
                                       1*1024*1024, 10)
    fmt = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    file_handler.setFormatter(fmt)
    file_handler.setLevel(logging.ERROR)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog setartup')
    

from app import views, models



