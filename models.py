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


class Topic(BaseModel):
    author = db.StringProperty(default='anonymous')
    title = db.StringProperty()
    body = db.TextProperty()
    
    def replies(self):
        """Fetches the topic's comments & sets each comment's 'replies' attribute"""
        keys = {}
        comments = self.comment_set.order('-created').fetch(1000)
        for comment in comments:
            keys[str(comment.key())] = comment
            comment.replies = []
        for comment in comments:
            parent_key = Comment.reply_to.get_value_for_datastore(comment)
            parent = keys.get(str(parent_key))
            if parent:
                parent.replies.append(comment)
        return [c for c in comments if not c.reply_to]


class Comment(BaseModel):
    author = db.StringProperty(default='anonymous')
    topic = db.ReferenceProperty(required=True)
    reply_to = db.SelfReferenceProperty(collection_name='reply_to_set')
    body = db.TextProperty()
    
    