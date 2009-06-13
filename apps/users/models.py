# Django imports
from django.template.defaultfilters import slugify

# Google imports
from google.appengine.ext import db
from django.contrib.auth import models

RESERVED_USERNAMES = ['anonymous', 'login', 'logout', 'admin']


class User(db.Model):
    password = db.StringProperty()
    email = db.EmailProperty()
    messages = db.StringListProperty()
    last_login = db.DateTimeProperty()
    date_joined = db.DateTimeProperty(auto_now_add=True)
    is_active = db.BooleanProperty(default=True)
    is_staff = db.BooleanProperty(default=False)
    is_superuser = db.BooleanProperty(default=False)

    @classmethod
    def create(cls, username, password, email=None):
        "Creates and saves a User with the given username, e-mail and password."
        assert username not in RESERVED_USERNAMES
        assert username == slugify(username)
        assert not cls.get_by_key_name(username)
        user = cls(
            key_name=username,
            email=email
        )
        user.set_password(password)
        user.save()
        return user

    @property
    def id(self):
        return self.key().name()

    @property
    def username(self):
        return self.key().name()

    def get_and_delete_messages(self):
        messages = self.messages
        self.messages = []
        self.put()
        return messages

    is_anonymous = models.User.is_anonymous.im_func
    is_authenticated = models.User.is_authenticated.im_func
    get_full_name = models.User.get_full_name.im_func
    set_password = models.User.set_password.im_func
    check_password = models.User.check_password.im_func
    set_unusable_password = models.User.set_unusable_password.im_func
    has_usable_password = models.User.has_usable_password.im_func
    #get_group_permissions = models.User.get_group_permissions.im_func



class ModelBackend(object):
    def authenticate(self, username=None, password=None):
        return User.get_by_key_name(username)

    def get_user(self, user_id):
        return User.get_by_key_name(user_id)