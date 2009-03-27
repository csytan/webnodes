from google.appengine.ext import db
from google.appengine.api import memcache



# ideas:
# ability to make private replies to a comment
# community dictionary support 
    # namespace search (tlnet -> gamers -> wikipedia)
# translations between words

class User(db.Model):
    favorites = db.ListProperty(db.Key)
    email = db.EmailProperty()

class Topic(db.Model):
    name = db.StringProperty()
    tags = db.StringListProperty()



class Comment(db.Model):
    topic = db.ReferenceProperty(Topic)
    reply_to = db.SelfReferenceProperty()
    author = db.UserProperty()
    added = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    body = db.TextProperty()
    rating = db.IntegerProperty(default=0)
    
    def id(self):
        return self.key().id()
    
    def add_reply(self, body):
        pass
    
    def get_replies(self, sort='-rating'):
        query = Comment.all()
        query.filter('reply_to =', self)
        query.order(sort)
        return query.fetch()
    
    def fetch_subgraph(self, width=10, depth=20, max=50):
        """Fetches a subgraph of comments"""
        replies = [reply.id for reply in self.get_replies()]
        subgraph = {comment.id: replies}
    
        while replies and depth > 0 and max >= len(subgraph):
            depth -= 1
            next_replies = []
            for reply in replies[:width]:
                next_replies.extend(graph.get(reply, []))
            replies = next_replies

        return subgraph
    

    
