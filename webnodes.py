# Python imports
import os

# Appengine imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

# Local imports
import reddit



class MainHandler(webapp.RequestHandler):
    path = os.path.join(os.path.dirname(__file__), 'templates','base.html')
    
    def get(self):
        context = reddit.get_thread_data('http://www.reddit.com/r/science/comments/866ss/forty_years_after_the_start_of_belyaev_experiment/')
        html = template.render(self.path, context)
        self.response.out.write(html)

class RedditHandler(webapp.RequestHandler):
    path = os.path.join(os.path.dirname(__file__), 'templates','base.html')

    def get(self):
        context = reddit.get_thread_data('http://www.reddit.com/r/science/comments/866ss/forty_years_after_the_start_of_belyaev_experiment/')
        html = template.render(self.path, context)
        self.response.out.write(html)

class RedditThreadHandler(webapp.RequestHandler):
    path = os.path.join(os.path.dirname(__file__), 'templates','base.html')

    def get(self, link):
        context = reddit.get_thread_data(link)
        html = template.render(self.path, context)
        self.response.out.write(html)

application = webapp.WSGIApplication([
        ('/reddit/(.+)', RedditThreadHandler),
        ('/reddit/', RedditHandler),
        ('/', MainHandler)
    ], debug=True)



def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
