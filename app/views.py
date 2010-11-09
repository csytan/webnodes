import os
import re
import urllib
import urlparse

from lib import markdown2
import tornado.web

import models



DEBUG = os.environ['SERVER_SOFTWARE'].startswith('Dev')


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_key = self.get_secure_cookie('user')
        if user_key:
            return models.User.get_by_key_name(user_key)
            
    def get_login_url(self):
        return '/sign_in'
        
    def get_current_site(self):
        if self.request.host == 'www.webnodes.org' or \
            'front' in self.request.arguments:
            return
        elif DEBUG:
            return models.Site.get_by_key_name('asdf')
        elif '.webnodes.org' in self.request.host:
            subdomain = self.request.host.split('.')[0]
            return models.Site.get_by_key_name(subdomain)
        elif '.latest.webnodes.appspot.com' in self.request.host:
            subdomain = self.request.host.split('.')[0]
            return models.Site.get_by_key_name(subdomain)
        else:
            return models.Site.all().filter('domain =', self.request.host).get()
        
    def prepare(self):
        token = self.get_argument('login_token', None)
        if token:
            user = models.User.get_by_token(token)
            if user:
                self.set_secure_cookie('user_id', str(user.id), domain=self.cookie_domain)
            self.redirect(self.request.path)
    
    def send_mail(self, subject, to, body=None, template=None,
            sender='webnodes.org <hello@webnodes.org>', **kwargs):
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
        site = self.get_current_site()
        if site:
            topics = site.topics.order('-score')
        else:
            topics = models.Topic.all()
        self.render('index.html', topics=topics)


class NewSite(BaseHandler):
    def get(self):
        self.render('new_site.html')
    
    def post(self):
        name = self.get_argument('name')
        title = self.get_argument('title')
        domain = self.get_argument('domain', None)
        
        if domain:
            if not domain.startswith('http://'):
                domain = 'http://' + domain
            domain = urlparse.urlparse(domain).netloc
        site = models.Site.create(
            name=name, title=title, domain=domain)
        self.redirect('/')


class Submit(BaseHandler):
    def get(self):
        self.render('submit.html')
        
    def post(self):
        title = self.get_argument('title', None)
        link = self.get_argument('link', None)
        text = self.get_argument('text', None)
        topic = models.Topic(
            site=self.get_current_site(),
            title=title,
            author=self.current_user,
            link=link,
            text=text)
        topic.update_score()
        topic.put()
        
        self.current_user.n_topics = self.current_user.topics.count()
        self.current_user.put()
        
        self.redirect('/' + str(topic.id))


class Community(BaseHandler):
    def get(self):
        site = self.get_current_site()
        self.render('community/community.html', users=site.users.order('-karma').fetch(10))


class User(BaseHandler):
    def get(self, username):
        site = self.get_current_site()
        user = models.User.get_user(site, username)
        if not user:
            raise tornado.web.HTTPError(404)
        self.render('community/user.html', user=user)
        
    @tornado.web.authenticated
    def post(self, username):
        email = self.get_argument('email', None)
        if email != self.current_user.email:
            if email and not models.User.email_valid(email):
                return self.reload(message='check_email', copyargs=True)
            else:
                self.current_user.email = email
        
        password = self.get_argument('password', None)
        if password:
            self.current_user.set_password(password)
        self.current_user.put()
        self.reload(message='updated')


class UserTopics(BaseHandler):
    def get(self, username):
        site = self.get_current_site()
        user = models.User.get_user(site, username)
        if not user:
            raise tornado.web.HTTPError(404)
        self.render('community/user_topics.html', user=user)


class UserComments(BaseHandler):
    def get(self, username):
        site = self.get_current_site()
        user = models.User.get_user(site, username)
        if not user:
            raise tornado.web.HTTPError(404)
        self.render('community/user_comments.html', user=user)


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
        
        self.current_user.n_comments = self.current_user.comments.count()
        self.current_user.put()
        
        topic.n_comments = topic.comments.count()
        topic.put()
        self.reload()


class SignIn(BaseHandler):
    def get(self):
        self.render('sign_in.html')
        
    def post(self):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        next = self.get_argument('next', '/')
        if username and password:
            user = models.User.get_user(
                site=self.get_current_site(),
                username=username)
            if user and user.check_password(password):
                self.set_secure_cookie('user', user.key().name())
                return self.redirect(next if next.startswith('/') else '/')
        self.reload(message='login_error', copyargs=True)


class SignUp(BaseHandler):
    def get(self):
        self.render('sign_up.html')
        
    def post(self):
        username = self.get_argument('username', None)
        email = self.get_argument('email', None)
        password = self.get_argument('password', None)
        next = self.get_argument('next', '/')
        
        if email and not models.User.email_valid(email):
            return self.reload(message='check_email', copyargs=True)
            
        user = models.User.create(
            site=self.get_current_site(),
            username=username,
            email=email,
            password=password)
        if user:
            self.set_secure_cookie('user', user.key().name())
        else:
            return self.reload(message='user_exists', copyargs=True)
        self.redirect(next if next.startswith('/') else '/')


class SignOut(BaseHandler):
    def get(self):
        next = self.get_argument('next', '/')
        self.clear_cookie('user')
        self.redirect(next if next.startswith('/') else '/')


class PasswordReset(BaseHandler):
    def get(self):
        self.render('password_reset.html', email=self.get_argument('email', ''))

    def post(self):
        email = self.get_argument('email', None)
        message = 'not_found'
        if email:
            user = models.User.get_by_email(email)
            if user:
                self.send_mail(
                    to=user.email,
                    subject='Password Reset',
                    current_user=user,
                    template='email/password_reset.txt')
                message = 'emailed'
        self.reload(message=message)
