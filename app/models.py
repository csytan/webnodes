from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api import users


class Topic(db.Model):
    title = db.StringProperty()
    tags = db.StringListProperty()
    root_comment_id = db.StringProperty()
    
    @classmethod
    def hot_topics(cls):
        pass
        
    def comments_by_rating(self):
        query = Comment.all().filter('topic =', self)
        comments = query.order('-rating').fetch()
        graph = {}
        for comment in comments:
            graph[comment.id] = comment.get_replies()
        
        #add root if not there
        return comments, graph


class Comment(db.Model):
    topic = db.ReferenceProperty(Topic)
    reply_to = db.SelfReferenceProperty()
    author = db.UserProperty()
    added = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    body = db.TextProperty()
    rating = db.IntegerProperty(default=0)
    
    replies_rating = db.ListProperty(int)
    replies_date = db.ListProperty(int)
    
    
    def id(self):
        return self.key().id()
    
    def add_reply(self, body):
        reply = Comment(
            topic=self.topic,
            reply_to=self,
            author=users.get_current_user(),
            body=body
        )
        reply.put()
        
        self.replies_rating = None
        self.replies_date = None
        self.put()
        return reply
    
    def get_reply_ids(self):
        query = Comment.all()
        query.filter('reply_to =', self)
        query.order('-updated')
        replies = query.fetch()
        
        if sort == '-rating':
            self.replies_rating = [reply.id for reply in replies]
        else:
            self.replies_date = [reply.id for reply in replies]
        return replies

    
