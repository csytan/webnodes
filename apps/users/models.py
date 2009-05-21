# Django imports
from django.template.defaultfilters import slugify

# Google imports
from google.appengine.ext import db

# Appengine patch imports
from ragendja.auth.models import AnonymousUser, User, UserManager


RESERVED_USERNAMES = ['anonymous', 'login', 'logout', 'admin']

class UserManager(UserManager):
    def create_user(self, username, email, password=None):
        "Creates and saves a User with the given username, e-mail and password."
        assert username not in RESERVED_USERNAMES
        assert username == slugify(username)
        if not email:
            user = super(UserManager, self).create_user(username, 'email@email.com', password)
            user.email = None
            user.save()
            return user
        return super(UserManager, self).create_user(username, email, password)

class User(User):
    objects = UserManager()
    badges = db.StringListProperty()
    
    