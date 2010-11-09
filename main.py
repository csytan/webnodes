import os
import wsgiref.handlers

import tornado.wsgi

from app import views


settings = {
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'debug': views.DEBUG,
    'cookie_secret': 'hello'
}
application = tornado.wsgi.WSGIApplication([
    (r'/', views.Index),
    (r'/new_site', views.NewSite),
    (r'/submit', views.Submit),
    (r'/community', views.Community),
    (r'/community/(.+)/topics', views.UserTopics),
    (r'/community/(.+)/comments', views.UserComments),
    (r'/community/(.+)', views.User),
    (r'/sign_in', views.SignIn),
    (r'/sign_up', views.SignUp),
    (r'/sign_out', views.SignOut),
    (r'/(\d+)', views.Topic),
    (r'.*', views.NotFound404)
], **settings)


def main():
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == "__main__":
    main()
    