# Django imports
from django.template.defaultfilters import slugify

# Google imports
from google.appengine.ext import db
from google.appengine.api import memcache


# TODO: move html sanitization into view

class KeyReferenceProperty(db.Property):
    def __init__(self, ref_class, **kwargs):
        self.ref_class = ref_class
        db.Property.__init__(self, **kwargs)
    def get_value_for_datastore(self, model_instance):
        model = db.Property.get_value_for_datastore(self, model_instance)
        return str(model.key().name())
    def make_value_from_datastore(self, value):
        return self.ref_class.get_by_key_name(value)
    data_type = basestring

class IdReferenceProperty(db.Property):
    def __init__(self, ref_class, **kwargs):
        self.ref_class = ref_class
        db.Property.__init__(self, **kwargs)
    def get_value_for_datastore(self, model_instance):
        model = db.Property.get_value_for_datastore(self, model_instance)
        return int(model.key().id())
    def make_value_from_datastore(self, value):
        return self.ref_class.get_by_id(value)
    data_type = int
    
### Helper functions ###



### Models ###
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
    author = db.StringProperty()
    title = db.StringProperty()
    root_id = db.IntegerProperty()
    num_comments = db.IntegerProperty(default=0)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    
    @property
    def id(self):
        return int(self.key().id())
    
    @classmethod
    def create(cls, author, title, body, tags=None):
        if tags:
            tags = [str(slugify(tag)) for tag in tags]
        else:
            tags = []
            
        topic = cls(
            author=author,
            title=title,
            tags=tags
        )
        topic.put()
        
        comment = Comment(author=author, topic=topic, body=body)
        comment.put()
        
        topic.root_id = comment.id
        topic.put()
        
        Tag.increment_tags(topic.tags)
        return topic
    
    @classmethod
    def hot_topics(cls):
        return cls.all().order('-created').fetch(50)
        
    @classmethod
    def topics_by_tag(cls, tag):
        query = cls.all().filter('tags =', tag)
        query.order('-created')
        return query.fetch(50)
        
    def comment_graph(self):
        query = Comment.all().filter('topic =', self)
        comments = query.order('-created').fetch(1000)
        
        # update number of comments
        if len(comments) != self.num_comments:
            self.num_comments = len(comments)
            self.put()
        
        graph = {}
        for comment in comments:
            graph[comment.id] = comment.get_reply_ids()
            
        if not self.root_id in graph:
            root = Comment.get_by_id(self.root_id)
            graph[self.root_id] = root.get_reply_ids()
        return comments, graph


class Comment(VotableMixin):
    author = db.StringProperty(default='anonymous')
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
    
    def add_reply(self, author, body):
        self.reply_cache = []
        self.has_replies = True
        self.put()
        
        comment = Comment(
            author=author,
            topic=self.topic,
            parent_comment=self,
            body=body
        )
        comment.put()
        return comment
    
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
    
