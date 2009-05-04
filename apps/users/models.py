from google.appengine.ext import db
from ragendja.auth.models import AnonymousUser, User, UserManager

class AnonymousUser(AnonymousUser):
    username = 'anonymous'
    
class UserManager(UserManager):
    def create_user(self, username, email, password=None):
        "Creates and saves a User with the given username, e-mail and password."
        assert username != 'anonymous'
        if not email:
            user = super(UserManager, self).create_user(username, 'email@email.com', password)
            user.email = None
            user.save()
            return user
        return super(UserManager, self).create_user(username, email, password)

class User(User):
    objects = UserManager()