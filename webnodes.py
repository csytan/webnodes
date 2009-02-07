# Python imports
import os

# Appengine imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

# Local imports
from models import Comment


import reddittree

class CommentHandler(webapp.RequestHandler):
    path = os.path.join(os.path.dirname(__file__), "templates", "base.html")
    
    def get(self, id):
        comment = Comment.get_by_id(int(id))
        self.response.out.write(template.render(self.path, comment.context))

    def post(self, id):
        content = self.request.get("content")
        
        if id:
            reply_to = Comment.get_by_id(int(id))
        else:
            reply_to = None
            
        comment = Comment(content=content, reply_to=reply_to)
        comment.put()
        self.response.out.write(template.render(self.path, comment.context))

class RepliesHandler(webapp.RequestHandler):
    def get(self, id):
        pass
        
    def post(self, id):
        content = self.request.get("content")
        


class MainHandler(webapp.RequestHandler):
    path = os.path.join(os.path.dirname(__file__), 'templates','base.html')
    
    def get(self):
        context = {"graph":reddittree.graph, "comments":reddittree.comments, "root":"root"}
        self.response.out.write(template.render(self.path, context))



application = webapp.WSGIApplication([
        ('/comments/(\d*)', CommentHandler),
        ('/', MainHandler)
    ], debug=True)



def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
