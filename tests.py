#!flask/bin/python

import os

import unittest
from config import basedir
from app import app, db
from app.models import User

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
        
    
if __name__ == '__main__':
    
    unittest.main()
    
    