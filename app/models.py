import cgi
import datetime
import hashlib
import math
import re
import urlparse
import uuid

from google.appengine.api import images
from google.appengine.ext import blobstore
from google.appengine.ext import db



### Functions ###
def prefetch_refprop(entities, prop):
    ref_keys = [prop.get_value_for_datastore(x) for x in entities]
    entities = [e for e, k in zip(entities, ref_keys) if k is not None]
    ref_keys = [k for k in ref_keys if k is not None]
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
        return not self == other
        
    @property
    def id(self):
        return self.key().id()
        
    @property
    def key_name(self):
        return self.key().name()


class Site(BaseModel):
    title = db.StringProperty(indexed=False)
    domain = db.StringProperty()
    favicon = db.StringProperty() # blob_key
    tagline = db.StringProperty(indexed=False, default='')
    about = db.TextProperty(default='')
    
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
        
    def hot_topics(self, page=0):
        topics = self.topics.order('-score').fetch(20, offset=page*20)
        prefetch_refprop(topics, Topic.author)
        return topics


class User(BaseModel):
    site = db.ReferenceProperty(Site, collection_name='users')
    email = db.EmailProperty()
    password = db.StringProperty(indexed=False)
    url_login_token = db.StringProperty()
    karma = db.IntegerProperty(default=1)
    daily_karma = db.IntegerProperty(default=10)
    n_topics = db.IntegerProperty(default=0)
    n_comments = db.IntegerProperty(default=0)
    n_messages = db.IntegerProperty(default=0)
    about = db.TextProperty(default='')
    is_admin = db.BooleanProperty(default=False)
    
    @classmethod
    def create(cls, site, username, password, email=None):
        """User key_name stored as "site_key_name:username"
        """
        username = username.lower()
        assert username.isalnum()
        email = email.strip().lower() if email else None
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
    def get_user(cls, site, username):
        key_name = site.key().name() + ':' + username
        return cls.get_by_key_name(key_name)
    
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
        
    def gravatar(self, size=None):
        hash = hashlib.md5(self.email).hexdigest() if self.email else '0'
        return 'http://www.gravatar.com/avatar/' + hash + \
                '?d=mm' + ('&s=' + str(size) if size else '')
        
    @property
    def name(self):
        return self.key().name().split(':')[1]
        
    @property
    def can_downvote(self):
        return self.is_admin or self.karma >= 100
        
    @property
    def can_remove_topics(self):
        return self.is_admin or self.karma >= 200


class Message(BaseModel):
    to = db.ReferenceProperty(User, collection_name='messages')
    type = db.StringProperty(choices=['welcome', 'comment_reply'])
    comment = db.ReferenceProperty()


class Votable(BaseModel):
    points = db.IntegerProperty(default=1)
    score = db.FloatProperty()
    up_votes = db.StringListProperty() # contains user key_names
    down_votes = db.StringListProperty() # contains user key_names
    
    def update_score(self):
        """Adapted from reddit's algorithm
        http://code.reddit.com/browser/r2/r2/lib/db/sorts.py?rev=4778b17e939e119417cc5ec25b82c4e9a65621b2
        """
        td = self.created - datetime.datetime(1970, 1, 1)
        epoch_seconds = td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)
        order = math.log(max(abs(self.points), 1), 10)
        sign = 1 if self.points > 0 else -1 if self.points < 0 else 0
        seconds = epoch_seconds - 1134028003
        self.score = round(order + sign * seconds / 45000, 7)
        
    def can_vote_up(self, user):
        if (user and user.is_admin) or \
            user and \
            user.daily_karma > 0 and \
            user.name not in self.up_votes and \
            user != self.author:
            return True
        return False
        
    def can_vote_down(self, user):
        if (user and user.is_admin) or \
            user and \
            user.karma >= 100 and \
            user.daily_karma > 0 and \
            user.name not in self.down_votes and \
            user != self.author:
            return True
        return False
        
    def can_edit(self, user):
        td = datetime.datetime.now() - self.created
        if user == self.author and \
            not td.days and td.seconds < 60 * 10:
            return True
        return False


class Topic(Votable):
    site = db.ReferenceProperty(Site, collection_name='topics')
    author = db.ReferenceProperty(User, collection_name='topics')
    editors = db.StringListProperty()
    title = db.StringProperty(indexed=False)
    link = db.StringProperty()
    text = db.TextProperty()
    n_comments = db.IntegerProperty(default=0)
    
    @staticmethod
    def slugify(value):
        """
        Normalizes string, converts to lowercase, removes non-alpha characters,
        and converts spaces to hyphens.
        http://code.djangoproject.com/svn/django/trunk/django/template/defaultfilters.py
        """
        import unicodedata
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
        value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
        return re.sub('[-\s]+', '-', value)

    @classmethod
    def convert_to_wiki(cls):
        puts = []
        topics = cls.all().fetch(1000)
        for topic in topics:
            if topic.key().name():
                continue
            t = cls(
                key_name=cls.slugify(topic.title),
                site=topic.site,
                created=topic.created,
                author=topic.author,
                score=topic.score,
                link=topic.link,
                text=topic.text,
                title=topic.title,
                points=topic.points,
                n_comments=topic.n_comments)
            puts.append(t)
            comments = topic.comments.fetch(1000)
            for comment in comments:
                comment.topic = t
            puts += comments
            db.put(puts)
            topic.delete()
        
    @property
    def link_domain(self):
        netloc = urlparse.urlparse(self.link).netloc
        return netloc.replace('www.', '', 1) if netloc.startswith('www.') else netloc
    
    def replies(self):
        """Fetches the topic's comments & sets each comment's 'replies' attribute"""
        keys = {}
        comments = self.comments.order('-score').fetch(1000)
        for comment in comments:
            keys[str(comment.key())] = comment
            comment.replies = []
        for comment in comments:
            parent_key = Comment.reply_to.get_value_for_datastore(comment)
            parent = keys.get(str(parent_key))
            if parent:
                parent.replies.append(comment)
        replies = [c for c in comments if not c.reply_to]
        prefetch_refprop(replies, Comment.author)
        return replies
        
    def save_edit(self):
        edit = TopicEdit(
            topic=self,
            author=self.author,
            title=self.title,
            link=self.link,
            text=self.text)
        edit.put()


class TopicEdit(BaseModel):
    topic = db.ReferenceProperty(Topic, collection_name='edits')
    author = db.ReferenceProperty(User)
    title = db.StringProperty(indexed=False)
    link = db.StringProperty()
    text = db.TextProperty()


class Comment(Votable):
    author = db.ReferenceProperty(User, collection_name='comments')
    topic = db.ReferenceProperty(Topic, collection_name='comments')
    text = db.TextProperty()
    reply_to = db.SelfReferenceProperty(collection_name='reply_to_set')

