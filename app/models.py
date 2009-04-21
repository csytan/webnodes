from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api import users


from lib import feedparser

# TODO: move html sanitization into view

### Helper functions ###
class Group(db.Model):
    name = db.StringProperty()
    description = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    
    @property
    def url_name(self):
        return self.key().name()
        
    @classmethod
    def newest_groups(cls):
        return cls.all().order('-created').fetch(20)


class Vote(db.Model):
    direction = db.IntegerProperty() # 1 or -1
    

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
    

class Tag(db.Model):
    group = db.ReferenceProperty(Group)
    count = db.IntegerProperty(default=0)
    
    @property
    def name(self):
        return self.key().name()
        
    @classmethod
    def top_tags(cls):
        query = cls.all().order('-count')
        return query.fetch(1000)
        
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

class TaggableMixin(db.Model):
    tags = db.StringListProperty()
    
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

class Topic(TaggableMixin, VotableMixin):
    group = db.ReferenceProperty(Group, required=True)
    title = db.StringProperty()
    root_id = db.IntegerProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    
    @property
    def id(self):
        return self.key().id()
    
    @classmethod
    def create(cls, group, title, body, tags=None):
        group = Group.get_by_key_name(group)
        topic = cls(group=group, title=title, tags=tags)
        topic.put()
        
        comment = Comment.create(topic=topic, body=body)
        comment.put()
        
        topic.root_id = int(comment.key().id())
        topic.put()
        
        Tag.increment_tags(topic.tags)
        return topic
    
    @classmethod
    def hot_topics(cls, group):
        group = Group.get_by_key_name(group)
        query = cls.all()
        query.filter('group =', group).order('-created')
        return query.fetch(100)
        
    @classmethod
    def topics_by_tag(cls, tag, group):
        group = Group.get_by_key_name(group)
        query = cls.all()
        query.filter('group =', group).filter('tags=', tag)
        query.order('-created')
        return query.fetch(1000)
        
    def comment_graph(self):
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
    
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)

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
    
