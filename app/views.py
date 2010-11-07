import re

from lib import markdown2
import tornado.web

import models


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_id = self.get_secure_cookie('user_id')
        if user_id:
            return models.User.get_by_id(int(user_id))
            
    def get_login_url(self):
        return '/sign_in'
        
    def prepare(self):
        token = self.get_argument('login_token', None)
        if token:
            user = models.User.get_by_token(token)
            if user:
                self.set_secure_cookie('user_id', str(user.id), domain=self.cookie_domain)
            self.redirect(self.request.path)
    
    def send_mail(self, subject, to, body=None, template=None,
            sender='Vittyo.com <hello@webnodes.org>', **kwargs):
        if template:
            body = self.render_string(template, **kwargs)
        mail.send_mail(sender=sender, to=to, subject=subject, body=body)
        logging.info('mail sent to: ' + to)
        
    def reload(self, copyargs=False, **kwargs):
        data = {}
        if copyargs:
            for arg in self.request.arguments:
                if arg not in ('_xsrf', 'password', 'password_again'):
                    data[arg] = self.get_argument(arg)
        data.update(kwargs)
        self.redirect(self.request.path + '?' + urllib.urlencode(data))
        
    def get_error_html(self, status_code, **kwargs):
        if status_code in (404, 500): # 503 and 403
            pass
            #return self.render_string(str(status_code) + '.html')
        return super(BaseHandler, self).get_error_html(status_code, **kwargs)
        
    ### Template helpers ###
    @staticmethod
    def truncate(string, n_chars):
        new_str = string[0:n_chars]
        if len(new_str) < len(string):
            new_str += '...'
        return cgi.escape(new_str)
        
    @staticmethod
    def markdown(value):
        # real line breaks
        value = re.sub(r'(\S ?)(\r\n|\r|\n)', r'\1  \n', value)
        value = re.sub(r'\n\n\n', r'\n\n\nLINEBREAK', value)
        # automatic hyperlinks
        value = re.sub(r'(^|\s)(http:\/\/\S+)', r'\1<\2>', value)
        html = markdown2.markdown(value, safe_mode='escape')
        return html.replace('<a href=', '<a rel="nofollow" href=').replace('LINEBREAK', '<br>')


class NotFound404(BaseHandler):
    def get(self):
        raise tornado.web.HTTPError(404)


class Index(BaseHandler):
    def get(self):
        topics = models.Topic.all().order('-score')
        self.render('index.html', topics=topics)


class Submit(BaseHandler):
    def get(self):
        self.render('submit.html')
        
    def post(self):
        title = self.get_argument('title', None)
        link = self.get_argument('link', None)
        text = self.get_argument('text', None)
        topic = models.Topic(title=title,
            author=self.current_user,
            link=link,
            text=text)
        topic.update_score()
        topic.put()
        self.redirect('/topics/' + str(topic.id))


class Topic(BaseHandler):
    def get(self, id):
        topic = models.Topic.get_by_id(int(id))
        self.render('topic.html', topic=topic)
        
    def render_comments(self, comments):
        return self.render_string('_comment.html', comments=comments)
        
    def post(self, id):
        topic = models.Topic.get_by_id(int(id))
        reply_to = self.get_argument('reply_to', None)
        if reply_to:
            reply_to = models.Comment.get_by_id(int(reply_to))
            
        comment = models.Comment(
            author=self.current_user,
            topic=topic,
            reply_to=reply_to,
            text=self.get_argument('text'))
        comment.put()
        topic.update_comment_count()
        topic.put()
        self.redirect('/topics/' + id)


