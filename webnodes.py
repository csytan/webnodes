# Python imports
import os

# Appengine imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

# Local imports
import reddit


class RedditHandler(webapp.RequestHandler):
    path = os.path.join(os.path.dirname(__file__), 'templates','hot_topics.html')

    def get(self):
        context = {'topics': reddit.hot_topics()}
        html = template.render(self.path, context)
        self.response.out.write(html)

class RedditThreadHandler(webapp.RequestHandler):
    path = os.path.join(os.path.dirname(__file__), 'templates','index.html')

    def get(self, link):
        context = reddit.get_thread_data(link)
        html = template.render(self.path, context)
        self.response.out.write(html)

application = webapp.WSGIApplication([
        ('/', RedditHandler),
        ('/reddit/', RedditHandler),
        ('/reddit/(.+)', RedditThreadHandler),
    ], debug=True)



def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
