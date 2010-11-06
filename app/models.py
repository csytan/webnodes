import cgi
import datetime
import hashlib
import re
import uuid

from google.appengine.ext import db


class BaseModel(db.Model):
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    
    def __eq__(self, other):
        if hasattr(other, 'key'):
            return self.key() == other.key()
        return False
    def __ne__(self, other):
        if hasattr(other, 'key'):
            return self.key() != other.key()
        return True
        
    @property
    def id(self):
        return self.key().id()


class User(BaseModel):
    email = db.EmailProperty()
    password = db.StringProperty(indexed=False)
    name = db.StringProperty()
    url_login_token = db.StringProperty()
    is_admin = db.BooleanProperty(default=False)
    
    @classmethod
    def create(cls, email, password=None):
        email = email.strip().lower()
        if cls.all().filter('email =', email).count(1):
            return None
        user = cls(email=email)
        user.set_name()
        if password:
            user.set_password(password)
        user.put()
        if cls.all().filter('email =', email).count(2) == 2:
            user.delete()
            return None
        return user
        
    @classmethod
    def check_email(cls, email):
        email_re = '^([\w\!\#$\%\&\'\*\+\-\/\=\?\^\`{\|\}\~]+\.)*[\w\!\#$\%\&\'\*\+\-\/\=\?\^\`{\|\}\~]+@((((([a-z0-9]{1}[a-z0-9\-]{0,62}[a-z0-9]{1})|[a-z])\.)+[a-z]{2,6})|(\d{1,3}\.){3}\d{1,3}(\:\d{1,5})?)$'
        if email and re.search(email_re, email):
            return True
        return False
        
    @classmethod
    def get_by_email(cls, email):
        email = email.strip().lower()
        return cls.all().filter('email =', email).get()
        
    @classmethod
    def get_by_token(cls, token):
        return cls.all().filter('url_login_token =', token).get()
        
    @property
    def login_token(self):
        if not self.url_login_token:
            self.url_login_token = str(uuid.uuid4()).replace('-', '')
            self.put()
        return self.url_login_token
        
    def set_name(self, name=None):
        if not name:
            name = self.email.split('@')[0]
        self.name = cgi.escape(name)[:25]
    
    def set_password(self, raw_password):
        assert len(raw_password) > 0 and len(raw_password) <= 20
        raw_password = raw_password.encode('utf-8')
        salt = str(uuid.uuid4()).replace('-', '')
        hsh = hashlib.sha1(salt + raw_password).hexdigest()
        self.password = 'sha1$' + salt + '$' + hsh
        
    def check_password(self, raw_password):
        if not self.password: return False
        raw_password = raw_password.encode('utf-8')
        algo, salt, hsh = str(self.password).split('$')
        return hsh == hashlib.sha1(salt + raw_password).hexdigest()
        
    @property
    def gravatar(self, size=None, default='identicon'):
        return 'http://www.gravatar.com/avatar.php' + \
            '?gravatar_id=' + hashlib.md5(self.email).hexdigest() + \
            '&default=' + default + ('&size=' + str(size) if size else '')


class Topic(BaseModel):
    title = db.StringProperty(indexed=False)
    body = db.TextProperty(default='')
    author = db.ReferenceProperty(User)
    votes = db.IntegerProperty(default=1)
    score = db.FloatProperty()
    
    def update_score(self, vote, gravity=1.8):
        """Adapted from http://amix.dk/blog/post/19574"""
        now = datetime.datetime.utcnow()
        date = datetime.datetime.utcfromtimestamp(self.created)
        hour_age = (now - date).seconds / 60.0
        self.score = (self.votes + vote - 1) / pow(hour_age + 2, gravity)
        
    
