# Google imports
from google.appengine.ext import db
from google.appengine.ext.db import polymodel

### Helper functions ###
def score(points, submitted_date):
    """
    Reddit "hotness" algorithm from:
    http://www.reddit.com/r/programming/comments/6ph35/reddits_collaborative_filtering_algorithm/c04is8d
    """
    def seconds_since_cutoff(date):
        cutoff = datetime(2005, 12, 8, 7, 46, 43)
        td = date - cutoff
        seconds = td.days * 24 * 60 * 60
        seconds += td.seconds
        seconds += float(td.microseconds) / 1000000
        return seconds

    order = log(max(abs(points), 1), 10)
    sign = 1 if points > 0 else -1 if points < 0 else 0
    age = seconds_since_cutoff(submitted_date)
    return round(order + sign * age / 45000, 7)


### Models ###
class Forum(db.Model):
    title = db.StringProperty()
    moderators = db.StringListProperty()
    sidebar = db.TextProperty()

    @property
    def name(self):
        return self.key().name()


class Comment(polymodel.PolyModel):
    author = db.StringProperty()
    body = db.TextProperty()
    topic_id = db.IntegerProperty()
    parent_id = db.IntegerProperty()
    
    likes = db.StringListProperty()
    
    has_replies = db.BooleanProperty(default=False, indexed=False)
    reply_cache = db.ListProperty(int, indexed=False)
    
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    
    @classmethod
    def get_by_username(cls, username):
        query = cls.all()
        query.filter('author =', username)
        query.order('-created')
        return query.fetch(50)
    
    @property
    def id(self):
        return int(self.key().id())

    @property
    def points(self):
        return len(self.likes)

    def add_reply(self, author, body):
        self.reply_cache = []
        self.has_replies = True
        self.put()
        
        comment = Comment(
            author=author,
            topic_id=self.topic_id,
            parent_id=self.id,
            body=body
        )
        comment.put()
        return comment

    def get_reply_ids(self):
        if self.reply_cache:
            return self.reply_cache
        if not self.has_replies:
            return []

        query = db.GqlQuery('SELECT __key__ FROM Comment ' +
                            'WHERE parent_id = :1 ' +
                            'ORDER BY updated DESC',
                            self.id)
        reply_keys = query.fetch(1000)

        self.reply_cache = [int(key.id()) for key in reply_keys]
        self.put()
        return self.reply_cache


class Topic(Comment):
    title = db.StringProperty()
    forum = db.StringProperty()
    num_comments = db.IntegerProperty(default=0)
    
    @classmethod
    def recent_topics(cls, forum, next=None, limit=20):
        query = cls.all()
        query.filter('forum =', forum)
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
        return self.id
    
    _comments = None
    @property
    def comments(self):
        if not self._comments:
            query = Comment.all().filter('topic_id =', self.id)
            self._comments = query.order('-created').fetch(1000)
        return self._comments
    
    @property
    def comment_graph(self):
        if len(self.comments) != self.num_comments:
            self.num_comments = len(self.comments)
            self.put()
        
        graph = {self.id: self.get_reply_ids()}
        for comment in self.comments:
            graph[comment.id] = comment.get_reply_ids()
        return graph


