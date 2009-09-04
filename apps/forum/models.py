# Google imports
from google.appengine.ext import db
from google.appengine.ext.db import polymodel


### Models ###
class Comment(polymodel.PolyModel):
    author = db.StringProperty()
    body = db.TextProperty()
    topic_id = db.IntegerProperty()
    parent_id = db.IntegerProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    
    @classmethod
    def get_by_author(cls, author):
        query = cls.all()
        query.filter('author =', author)
        query.order('-created')
        return query.fetch(50)
    
    @property
    def id(self):
        return int(self.key().id())
    
    def add_reply(self, author, body):
        comment = Comment(
            author=author,
            topic_id=self.topic_id,
            parent_id=self.id,
            body=body
        )
        comment.put()
        return comment


class Topic(Comment):
    title = db.StringProperty()
    forum = db.StringProperty()
    num_comments = db.IntegerProperty(default=0)
    
    @classmethod
    def topics_by_author(cls, author, next=None, limit=20):
        query = cls.all()
        query.filter('author =', author)
        if next is not None:
            next_topic = cls.get_by_id(int(next))
            query.filter('created <', next_topic.created)
        query.order('-created')
        topics = query.fetch(limit)
        
        if len(topics) == limit:
            next = topics[-1].id
        else:
            next = None
        return topics, next
    
    @property
    def topic_id(self):
        return int(self.key().id())
    
    def replies(self):
        """Adds the .replies to each comment for display as tree"""
        query = Comment.all()
        query.filter('topic_id =', self.id)
        query.order('created')
        comments = query.fetch(1000)
        
        if self.num_comments != len(comments):
            self.num_comments = len(comments)
            self.put()
        
        ids = {self.id: self}
        self.replies = []
        
        for comment in comments:
            ids[comment.id] = comment
            comment.replies = []
            
        for comment in comments:
            parent = ids[comment.parent_id]
            parent.replies.append(comment)
        
        return self.replies

