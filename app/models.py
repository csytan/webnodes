from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api import users


from lib import feedparser

class Tag(db.Model):
    num_topics = db.IntegerProperty(default=0)
    
    @property
    def name(self):
        return self.key().name()

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
        comments = query.order('-created').fetch(1000)
        
        graph = {}
        for comment in comments:
            graph[comment.id] = comment.get_reply_ids()
            
        if not self.root_id in graph:
            root = Comment.get_by_id(self.root_id)
            graph[self.root_id] = root.get_reply_ids()
        return comments, graph


class Comment(db.Model):
    author = db.UserProperty()
    body = db.TextProperty()
    topic = db.ReferenceProperty(Topic, required=True)
    parent_comment = db.SelfReferenceProperty()
    
    rating = db.IntegerProperty(default=0)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)

    tags = db.StringListProperty()
    has_replies = db.BooleanProperty(default=False)
    reply_cache = db.ListProperty(int)
    
    @property
    def id(self):
        return int(self.key().id())
    
    @classmethod
    def create(cls, body, topic, parent_comment=None):
        if parent_comment:
            parent_comment.reply_cache = []
            parent_comment.has_replies = True
            parent_comment.put()
        
        comment = cls(
            topic=topic,
            parent_comment=parent_comment,
            author=users.get_current_user(),
            body=feedparser._sanitizeHTML(body, 'utf-8')
        )
        comment.put()
        return comment
    
    def add_reply(self, body):
        return Comment.create(
            topic=self.topic,
            parent_comment=self,
            body=body
        )
    
    def get_reply_ids(self):
        if self.reply_cache:
            return self.reply_cache
        elif not self.has_replies:
            return []
        
        query = Comment.all()
        query.filter('parent_comment =', self)
        query.order('-updated')
        replies = query.fetch(1000)
        
        self.reply_cache = [reply.id for reply in replies]
        self.put()
        return self.reply_cache
    
