import os
import wsgiref.handlers

import tornado.wsgi

import views
import models


app_settings = models.Settings.get_settings()

settings = {
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'debug': views.DEBUG,
    'cookie_secret': app_settings.cookie_secret,
    'login_url': '/sign_in',
    'xsrf_cookies': True,
}
application = tornado.wsgi.WSGIApplication([
    (r'/', views.Index),
    (r'/favicon\.ico', views.Favicon),
    (r'/new_site', views.NewSite),
    (r'/submit', views.Submit),
    (r'/vote', views.Vote),
    (r'/account', views.Account),
    (r'/inbox', views.Inbox),
    (r'/sign_in', views.SignIn),
    (r'/sign_up', views.SignUp),
    (r'/sign_out', views.SignOut),
    (r'/users', views.Users),
    (r'/users/(.+)/topics', views.UserTopics),
    (r'/users/(.+)/comments', views.UserComments),
    (r'/users/(.+)', views.UserProfile),
    (r'/comments/(\d+)/edit', views.CommentEdit),
    (r'/(.+)/edit', views.TopicEdit),
    (r'/(.+)/versions', views.TopicVersions),
    (r'/community_edit', views.CommunityEdit),
    (r'/(.+)', views.Topic)
], **settings)


def main():
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == "__main__":
    main()
    