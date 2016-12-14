#!flask/bin/python

import os

import unittest
from config import basedir
from app import app, db
from app.models import User, Post

from coverage import coverage
from activate_this import base
from datetime import datetime
cov = coverage(branch=True, omit=['tests.py'])

cov.start()


class TestCase(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WFT_CSRF_ENABLED'] = False
        testdb = os.path.join(basedir, 'test.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + testdb

        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    def test_avatar(self):
        
        u = User(nickname='jondoe', email='jondoe@example.com')
        avatar = u.avatar(128)
        
        assert avatar is not None
        
    def test_delete_post(self):
        # create a user and a post
        ##datetime
        u = User(nickname='john', email='john@example.com')
        p = Post(body='test post', author=u, timestamp=datetime.utcnow())
        db.session.add(u)
        db.session.add(p)
        db.session.commit()
        # query the post and destroy the session
        p = Post.query.get(1)
        db.session.remove()
        # delete the post using a new session
        db.session = db.create_scoped_session()
        db.session.delete(p)
        db.session.commit()
        
    def test_user(self):
        # make valid nicknames
        
        # create a user
        u = User(nickname='john', email='john@example.com')
        db.session.add(u)
        db.session.commit()
        assert u.is_authenticated is True
        assert u.is_active is True
        assert u.is_anonymous is False
        assert u.id == int(u.get_id())
    
if __name__ == '__main__':
    try:
        
        unittest.main()
    except:
        pass
    
    cov.stop()
    cov.save()
    print "\n\nCoverage Report:\n"
    cov.report()
    print "HTML version: ", os.path.join(basedir, "tmp/coverage/index.html")
    cov.html_report(directory='tmp/coverage')
    cov.erase()