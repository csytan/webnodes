# Python imports
import re
import os
import wsgiref.handlers

# Tornado imports
import tornado.wsgi
import tornado.web

# Local imports
import models
import markdown2



class Topics(tornado.web.RequestHandler):
    def get(self):
        topics = models.Topic.all().order('-updated').fetch(100)
        self.render('topics.html', topics=topics)
        
    def post(self):
        topic = models.Topic(
            author=self.get_argument('author', None),
            title=self.get_argument('title', None),
            body=self.get_argument('body', None)
        )


class Topic(tornado.web.RequestHandler):
    def get(self, id):
        topic = models.Topic.get_by_id(int(id))
        self.render('topic.html', markdown=self.markdown, topic=topic)
        
    @staticmethod
    def markdown(value):
        # real line breaks
        value = re.sub(r'(\S ?)(\r\n|\r|\n)', r'\1  \n', value)
        # automatic hyperlinks
        value = re.sub(r'(^|\s)(http:\/\/\S+)', r'\1<\2>', value)
        html = markdown2.markdown(value, safe_mode='escape')
        return html.replace('<a href=', '<a rel="nofollow" href=')


settings = {
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'debug': os.environ['SERVER_SOFTWARE'].startswith('Dev')
}
application = tornado.wsgi.WSGIApplication([
    (r'/', Topics),
    (r'/(.+)', Topic)
], **settings)


def main():
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == "__main__":
    main()

