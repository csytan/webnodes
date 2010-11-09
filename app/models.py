import cgi
import datetime
import hashlib
import re
import uuid

from google.appengine.ext import db



### Functions ###
def prefetch_refprop(entities, prop):
    ref_keys = [prop.get_value_for_datastore(x) for x in entities]
    ref_entities = dict((x.key(), x) for x in db.get(set(ref_keys)))
    for entity, ref_key in zip(entities, ref_keys):
        prop.__set__(entity, ref_entities[ref_key])
    return entities


### Models ###
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


class Site(BaseModel):
    title = db.StringProperty(indexed=False)
    domain = db.StringProperty()
    
    @classmethod
    def create(cls, name, title=None, domain=None):
        name = name.lower()
        assert name.isalnum()
        def txn():
            if cls.get_by_key_name(name):
                return None
            site = cls(key_name=name,
                domain=domain,
                title=title if title else name)
            site.put()
            return site
        return db.run_in_transaction(txn)


class User(BaseModel):
    site = db.ReferenceProperty(Site, collection_name='users')
    email = db.EmailProperty()
    password = db.StringProperty(indexed=False)
    url_login_token = db.StringProperty()
    karma = db.IntegerProperty(default=0)
    
    @classmethod
    def create(cls, site, username, password, email=None):
        """User key_name stored as "site_key_name:username"
        """
        username = username.lower()
        assert username.isalnum()
        if email:
            email = email.strip().lower()
        key_name = site.key().name() + ':' + username
        def txn():
            if cls.get_by_key_name(key_name):
                return None
            user = cls(key_name=key_name, site=site, email=email)
            user.set_password(password)
            user.put()
            return user
        return db.run_in_transaction(txn)
        
    @classmethod
    def get_user(cls, site, username, password=None):
        key_name = site.key().name() + ':' + username
        user = cls.get_by_key_name(key_name)
        if user and user.check_password(password):
            return user
    
    @staticmethod
    def email_valid(email):
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
        
    def gravatar(self, size=None, default='identicon'):
        email = self.email if self.email else ''
        return 'http://www.gravatar.com/avatar.php' + \
            '?gravatar_id=' + hashlib.md5(email).hexdigest() + \
            '&default=' + default + ('&size=' + str(size) if size else '')
            
    @property
    def name(self):
        return self.key().name().split(':')[1]


class Topic(BaseModel):
    site = db.ReferenceProperty(Site, collection_name='topics')
    author = db.ReferenceProperty(User, collection_name='topics')
    author_name = db.StringProperty(indexed=False)
    title = db.StringProperty(indexed=False)
    link = db.StringProperty()
    text = db.TextProperty(default='')
    points = db.IntegerProperty(default=1)
    score = db.FloatProperty()
    n_comments = db.IntegerProperty(default=0)
    
    def update_score(self, gravity=1.8):
        """Adapted from http://amix.dk/blog/post/19574"""
        now = datetime.datetime.utcnow()
        hour_age = (now - self.created).seconds / 60.0
        self.score = self.points / pow(hour_age + 2, gravity)
        
    def update_comment_count(self):
        self.n_comments = self.comment_set.count(1000)
    
    def replies(self):
        """Fetches the topic's comments & sets each comment's 'replies' attribute"""
        keys = {}
        comments = self.comment_set.order('-score').fetch(1000)
        for comment in comments:
            keys[str(comment.key())] = comment
            comment.replies = []
        for comment in comments:
            parent_key = Comment.reply_to.get_value_for_datastore(comment)
            parent = keys.get(str(parent_key))
            if parent:
                parent.replies.append(comment)
        replies = [c for c in comments if not c.reply_to]
        #prefetch_refprop(replies, Comment.author)
        return replies


class Comment(BaseModel):
    author = db.ReferenceProperty(User, collection_name='comments')
    author_name = db.StringProperty(indexed=False)
    topic = db.ReferenceProperty(required=True)
    text = db.TextProperty()
    reply_to = db.SelfReferenceProperty(collection_name='reply_to_set')
    points = db.IntegerProperty(default=1)
    score = db.FloatProperty()
    


