from app import app, lm, db
from flask import render_template, flash, redirect, url_for, request, g
from app.forms import LoginForm, EditForm
from app.models import User
from flask.globals import session
from flask_login import login_manager
from flask_login.utils import login_user, current_user, login_required,\
    logout_user
from app.oauth import OAuthSignIn
import flask
from datetime import date, datetime


@app.route('/user/<nickname>')
def user(nickname):
    
    user = User.query.filter_by(nickname=nickname).first()
    
    if user is None:
        flash('%s is not found' % (nickname))
        
        return redirect(url_for('index'))
    
    posts = [{'author':user, 'body': 'Post one'},
             {'author':user, 'body': 'Post two'}]
    return render_template('user.html', title='User', user=user,
                           posts=posts)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
@app.route('/index')
@login_required
def index():
    
    user = {'nickname': 'Dat'}
    return render_template('index.html', user=user, title='Hello')



@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if g.user is not None and g.user.is_authenticated:
        
        return redirect(url_for('index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        """
        flash('Login requested for OpenID="%s", remember_me=%s' % 
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
        """
        ##return oid.try_login(form.openid.data, ask_for=['nickname','email'])
        
        user = User.query.filter_by(nickname=form.nickname.data, 
                                    password=form.password.data).first()
                                    
        if user is not None:
            login_user(user, form.remember_me.data)
            
            
            flash('Logged in successfully.')

            next = request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            
            #if not is_safe_url(next):
            #    return flask.abort(400)
    
            return redirect(next or url_for('index'))
            
        
    return render_template('login.html', form=form,
                           title='Sign In',
                           providers=app.config['OPENID_PROVIDERS'])
    
@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    
    form = EditForm(g.user.nickname)
    
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        
        db.session.add(g.user)
        db.session.commit()
        
        flash('Your changes have been saved successfully!')
        return redirect(url_for('index'))
    
    
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
        
    return render_template('edit.html', form=form)
        
@app.before_request
def before_request():
    g.user = current_user
    
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
    
    

def after_login(resp):
    
    if resp.email is None or resp.email == "":
        flash("Invalid login. Please try again.")
        return redirect(url_for('login'))
    
    user = User.query.filter_by(email=res.email).first()
    
    if user is None:
        nickname = resp.nickname
        
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
            
        user = User(nickname=nickname, email=resp.email)
        
        db.session.add(user)
        db.session.commit()
        
    remember_me = False
    
    if 'remember_me' in sesssion:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
        
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    ##OAuthSignIn
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()



@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))


@app.errorhandler(404)
def not_found_error(error):
    
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    
    return render_template('500.html'), 500

