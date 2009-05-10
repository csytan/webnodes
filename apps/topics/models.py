# Google imports
from google.appengine.ext import db
from google.appengine.api import memcache


### Models ###
class Vote(db.Model):
    direction = db.IntegerProperty() # 1 or -1
    

class Tag(db.Model):
    count = db.IntegerProperty(default=0)
    moderators = db.StringListProperty()
    
    @property
    def name(self):
        return self.key().name()
        
    @classmethod
    def top_tags(cls):
        return cls.all().order('-count').fetch(50)
        
    @classmethod
    def increment_tags(cls, tag_names):
        """Increments the tag count by one"""
        tags = cls.get_by_key_name(tag_names)

        save_tags = []
        for name, tag in zip(tag_names, tags):
            if not tag:
                tag = Tag(key_name=name)
            tag.count += 1
            save_tags.append(tag)
        db.put(save_tags)

class VotableMixin(db.Model):
    points = db.IntegerProperty(default=0)
    score = db.FloatProperty(default=0.0)
    
    @staticmethod
    def seconds_since_cutoff(date):
        cutoff = datetime(2005, 12, 8, 7, 46, 43)
        td = date - cutoff
        seconds = td.days * 24 * 60 * 60
        seconds += td.seconds
        seconds += float(td.microseconds) / 1000000
        return seconds
    
    @staticmethod
    def score(points, submitted_date):
        """
        Reddit "hotness" algorithm from:
        http://www.reddit.com/r/programming/comments/6ph35/reddits_collaborative_filtering_algorithm/c04is8d
        """
        order = log(max(abs(points), 1), 10)
        sign = 1 if points > 0 else -1 if points < 0 else 0
        age = seconds_since_cutoff(submitted_date)
        return round(order + sign * age / 45000, 7)
    
    def vote_up(self):
        user = Users.get_current_user()
        email = user.email()
        if email in self.votes_up:
            self.votes_up.append(email)
        self.put()
    



class Comment(VotableMixin):
    author = db.StringProperty(default='anonymous')
    body = db.TextProperty()
    topic_id = db.IntegerProperty()
    parent_id = db.IntegerProperty()
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
            topic_id=self.id if isinstance(self, Topic) else self.topic_id,
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

        query = Comment.all()
        query.filter('parent_id =', self.id)
        query.order('-updated')
        replies = query.fetch(1000)

        self.reply_cache = [reply.id for reply in replies]
        self.put()
        return self.reply_cache


class Topic(Comment):
    title = db.StringProperty()
    num_comments = db.IntegerProperty(default=0)
    tags = db.StringListProperty()
    
    @classmethod
    def create(cls, author, title, body, tags=None):
        topic = cls(
            author=author,
            title=title,
            body=body,
            tags=[str(slugify(tag)) for tag in tags] if tags else []
        )
        topic.put()
        return topic
    
    @classmethod
    def hot_topics(cls):
        return cls.all().order('-created').fetch(50)
        
    @classmethod
    def topics_by_tag(cls, tag):
        query = cls.all().filter('tags =', tag)
        query.order('-created')
        return query.fetch(50)
        
    def add_tag(self, name):
        if name in self.tags: return
        
        tag = Tag.get_or_insert(name)
        tag.num_tagged += 1
        tag.put()
        
        self.tags.append(name)
        self.put()
    
    def remove_tag(self, name):
        self.tags = [tag for tag in self.tags if tag != name]
        self.put()
        
        
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


