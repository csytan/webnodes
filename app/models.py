from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api import users


from lib import feedparser

class Topic(db.Model):
    title = db.StringProperty()
    tags = db.StringListProperty()
    root_id = db.IntegerProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    
    @property
    def id(self):
        return self.key().id()
    
    @classmethod
    def create(cls, title, body):
        topic = cls(title=title)
        topic.put()
        
        comment = Comment.create(topic=topic, body=body)
        comment.put()
        
        topic.root_id = int(comment.key().id())
        topic.put()
        return topic
    
    @classmethod
    def hot_topics(cls):
        query = cls.all().order('-created')
        return query.fetch(100)
        
    def get_comments(self):
        query = Comment.all().filter('topic =', self)
        comments = query.order('-rating').fetch(1000)
        
        graph = {}
        for comment in comments:
            graph[comment.id] = comment.get_reply_ids()
            
        if not self.root_id in graph:
            root = Comment.get_by_id(self.root_id)
            graph[self.root_id] = root.get_reply_ids()
        return comments, graph


class Comment(db.Model):
    topic = db.ReferenceProperty(Topic)
    reply_to = db.SelfReferenceProperty()
    author = db.UserProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    body = db.TextProperty()
    rating = db.IntegerProperty(default=0)
    
    has_replies = db.BooleanProperty(default=False)
    reply_cache = db.ListProperty(int)
    
    @property
    def id(self):
        return int(self.key().id())
    
    @classmethod
    def create(cls, body, parent=None, topic=None):
        if parent:
            parent.reply_cache = []
            parent.has_replies = True
            parent.put()
            topic = parent.topic
        body = feedparser._sanitizeHTML(body, 'utf-8')
        comment = cls(
            topic=topic,
            reply_to=parent,
            author=users.get_current_user(),
            body=body
        )
        comment.put()
        return comment
    
    def get_reply_ids(self):
        if self.reply_cache:
            return self.reply_cache
        elif not self.has_replies:
            return []
        
        query = Comment.all()
        query.filter('reply_to =', self)
        query.order('-updated')
        replies = query.fetch(1000)
        
        self.reply_cache = [reply.id for reply in replies]
        self.put()
        return self.reply_cache
    
