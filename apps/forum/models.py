# Google imports
from google.appengine.ext import db
from google.appengine.api import memcache


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


### Custom Properties ###
from google.appengine.ext import db
from google.appengine.api import datastore_types
from django.utils import simplejson
class JSONProperty(db.Property):
    def get_value_for_datastore(self, model_instance):
        value = super(JSONProperty, self).get_value_for_datastore(model_instance)
        return db.Text(self._deflate(value))
    def validate(self, value):
        return self._inflate(value)
    def make_value_from_datastore(self, value):
        return self._inflate(value)
    def _inflate(self, value):
        if value is None:
            return {}
        if isinstance(value, unicode) or isinstance(value, str):
            return simplejson.loads(value)
        return value
    def _deflate(self, value):
        return simplejson.dumps(value)
    data_type = datastore_types.Text


### Models ###
class Tag(db.Model):
    count = db.IntegerProperty(default=0)
    
    @property
    def name(self):
        return self.key().name()
        
    @classmethod
    def top_tags(cls):
        return cls.all().order('-count').fetch(50)
        
    @classmethod
    def increment(cls, tag_names):
        """Increments the tag count by one"""
        tags = cls.get_by_key_name(tag_names)

        save_tags = []
        for name, tag in zip(tag_names, tags):
            if not tag:
                tag = Tag(key_name=name)
            tag.count += 1
            save_tags.append(tag)
        db.put(save_tags)


class Group(db.Model):
    title = db.StringProperty()
    moderators = db.StringListProperty()

    @property
    def name(self):
        return self.key().name()

class Comment(db.Model):
    author = db.StringProperty()
    body = db.TextProperty()
    topic_id = db.IntegerProperty()
    parent_id = db.IntegerProperty()
    
    points = db.IntegerProperty(default=0)
    
    has_replies = db.BooleanProperty(default=False, indexed=False)
    reply_cache = db.ListProperty(int, indexed=False)
    
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    
    @property
    def id(self):
        return int(self.key().id())

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

        query = Comment.all(keys_only=True)
        query.filter('parent_id =', self.id)
        query.order('-updated')
        reply_keys = query.fetch(1000)

        self.reply_cache = [int(key.id()) for key in reply_keys]
        self.put()
        return self.reply_cache


class Topic(Comment):
    title = db.StringProperty()
    group = db.StringProperty()
    tags = db.StringListProperty()
    num_comments = db.IntegerProperty(default=0)
    history = JSONProperty()
    
    @classmethod
    def recent_topics(cls, group):
        query = cls.all()
        query.filter('group =', group)
        query.order('-created')
        return query.fetch(50)
        
    @classmethod
    def topics_by_tag(cls, tag):
        query = cls.all().filter('tag =', tag)
        query.order('-created')
        return query.fetch(50)
    
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


