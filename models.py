from google.appengine.ext import db

import pickle
import copy

class User(db.Expando):
    favorites = db.ListProperty(db.Key)
    email = db.EmailProperty()

class CommentGraph(db.Expando):
    """Stores the comment graph as comment ids (attributes) and lists
    containing replies.
    E.g. 
    >>> graph.comment_A
    ['comment_B', 'comment_C']
    >>> graph.comment_B
    ['comment_D', 'commentE']
    """

class Topic(db.Expando):
    """
    The comment graph is cached to enable quick fetching of entities
    from the datastore.
    
        
    """
    graph_rating = db.ReferenceProperty(CommentGraph) # sorted by rating
    graph_newest = db.ReferenceProperty(CommentGraph)
    
    @transaction
    @staticmethod
    def update_replies(comment):
        topic = comment.topic
        setattr(topic.graph_newest, comment.id, sorted(comment.newest))
        
        def rating_cmp(x, y):
            return x.rating - y.rating
        setattr(topic.graph_rating, comment.id, sorted(comment.replies, rating_cmp))
    
    
    def get_replies(self, comment, sort="rating", width=10, depth=20, max=50):
        """Fetches a subgraph of comments"""       
        if sort == "rating":
            graph = self.graph_rating
        elif sort == "date":
            graph = self.graph_rating
        
        replies = getattr(graph, comment.id, [])
        subgraph = {comment.id: replies}
        
        while replies and depth > 0 and max >= len(subgraph):
            depth -= 1
            next_replies = []
            for reply in replies[:width]:
                subgraph[reply] = getaget(reply, [])
                next_replies.extend(graph.get(reply, []))
            replies = next_replies
            
        return subgraph

class Comment(db.Expando):
    topic = db.StringProperty()
    reply_to = db.SelfReferenceProperty(collection_name="replies")
    #author = db.UserProperty()
    added = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    content = db.TextProperty()
    rating = db.IntegerProperty(default=0)
    #tags = db.StringListProperty()
        
    @property
    def id(self):
        return str(self.key().id())
    
