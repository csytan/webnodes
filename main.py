# Python imports
import re
import os
import wsgiref.handlers

# Appengine imports
from google.appengine.api import memcache

# Tornado imports
import tornado.wsgi
import tornado.web

# Local imports
import reddit
import markdown2


def markdown(value):
    # real line breaks
    value = re.sub(r'(\S ?)(\r\n|\r|\n)', r'\1  \n', value)
    # automatic hyperlinks
    value = re.sub(r'(^|\s)(http:\/\/\S+)', r'\1<\2>', value)
    html = markdown2.markdown(value, safe_mode='escape')
    return html.replace('<a href=', '<a rel="nofollow" href=')
    

class Topics(tornado.web.RequestHandler):
    def get(self):
        topics = memcache.get('topics')
        if topics is None:
            try:
                topics = reddit.topics()
            except:
                return self.render('error.html')
            memcache.add('topics', topics, 10)
        self.render('topics.html', topics=topics)


class Topic(tornado.web.RequestHandler):
    def get(self, id):
        topic = memcache.get('topic:' + id)
        if topic is None:
            try:
                topic = reddit.topic(id)
            except:
                return self.render('error.html')
            memcache.add('topic:' + id, topic, 10)
        self.render('topic.html', markdown=markdown, **topic)


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
    