import os
import wsgiref.handlers

import tornado.wsgi

from app import views


settings = {
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'debug': views.DEBUG,
    'cookie_secret': 'hello',
    'login_url': '/sign_in',
    'xsrf_cookies': True,
}
application = tornado.wsgi.WSGIApplication([
    (r'/', views.Index),
    (r'/new_site', views.NewSite),
    (r'/submit', views.Submit),
    (r'/vote', views.Vote),
    (r'/community', views.Community),
    (r'/community/edit', views.CommunityEdit),
    (r'/account', views.Account),
    (r'/inbox', views.Inbox),
    (r'/sign_in', views.SignIn),
    (r'/sign_up', views.SignUp),
    (r'/sign_out', views.SignOut),
    (r'/users/(.+)/topics', views.UserTopics),
    (r'/users/(.+)/comments', views.UserComments),
    (r'/users/(.+)', views.UserProfile),
    (r'/(\d+)', views.Topic),
    (r'.*', views.NotFound404)
], **settings)


def main():
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == "__main__":
    main()
    