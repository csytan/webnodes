import os
import wsgiref.handlers

import tornado.wsgi

from app import views


settings = {
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'debug': os.environ['SERVER_SOFTWARE'].startswith('Dev')
}
application = tornado.wsgi.WSGIApplication([
    (r'/', views.Index),
    (r'/submit', views.Submit),
    (r'/topics/(\d+)', views.Topic)
], **settings)


def main():
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == "__main__":
    main()
    