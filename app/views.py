import cgi
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
            
    @property
    def current_site(self):
        if not hasattr(self, '_current_site'):
            if DEBUG:
                self._current_site = models.Site.get_by_key_name('asdf')
            elif '.webnodes.org' in self.request.host or \
                '.latest.webnodes.appspot.com' in self.request.host:
                subdomain = self.request.host.split('.')[0]
                self._current_site = models.Site.get_by_key_name(subdomain)
            else:
                self._current_site = models.Site.all().filter('domain =', self.request.host).get()
        return self._current_site
        
    def render_string(self, template_name, **kwargs):
        return super(BaseHandler, self).render_string(
            template_name,
            truncate=self.truncate,
            markdown=self.markdown,
            current_site=self.current_site,
            **kwargs)
    
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
        self.render('index.html', topics=self.current_site.hot_topics())


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
            site=self.current_site,
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
        self.render('community/community.html',
            users=self.current_site.users.order('-karma').fetch(100))


class User(BaseHandler):
    def get(self, username):
        user = models.User.get_user(self.current_site, username)
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
        user = models.User.get_user(self.current_site, username)
        if not user:
            raise tornado.web.HTTPError(404)
        self.render('community/user_topics.html', user=user)


class UserComments(BaseHandler):
    def get(self, username):
        user = models.User.get_user(self.current_site, username)
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
        reply_to = self.get_argument('reply_to', None)
        if reply_to:
            reply_to = models.Comment.get_by_id(int(reply_to))
            
        comment = models.Comment(
            author=self.current_user,
            topic=models.Topic.get_by_id(int(id)),
            reply_to=reply_to,
            text=self.get_argument('text'))
        comment.put()
        
        self.current_user.n_comments = self.current_user.comments.count()
        self.current_user.put()
        
        topic.n_comments = topic.comments.count()
        topic.put()
        self.reload()


class Vote(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        comment_id = self.get_argument('comment_id', None)
        topic_id = self.get_argument('topic_id', None)
        if comment_id:
            comment = models.Comment.get_by_id(int(comment_id))
            if comment.topic.site != self.current_site:
                raise tornado.web.HTTPError(403)
        elif topic_id:
            comment = models.Topic.get_by_id(int(topic_id))
            if comment.site != self.current_site:
                raise tornado.web.HTTPError(403)
        
        if self.current_user.daily_karma > 0 and comment.author != self.current_user:
            way = self.get_argument('way', None)
            if way == 'up' and self.current_user.name not in comment.up_votes:
                comment.points += 1
                comment.up_votes.append(self.current_user.name)
                comment.update_score()
                comment.put()
                self.current_user.daily_karma -= 1
                self.current_user.put()
                if comment.author:
                    comment.author.karma += 1
                    comment.author.put()
            elif way == 'down' and self.current_user.karma >= 100 and \
                    self.current_user.name not in comment.down_votes:
                comment.points -= 1
                comment.down_votes.append(self.current_user.name)
                comment.update_score()
                comment.put()
                self.current_user.daily_karma -= 1
                self.current_user.put()
                if comment.author:
                    comment.author.karma -= 1
                    comment.author.put()
        self.write(str(comment.points) + (' point' if comment.points in (1, -1) else ' points'))


class SignIn(BaseHandler):
    def get(self):
        next = self.get_argument('next', '/')
        token = self.get_argument('login_token', None)
        if token:
            user = models.User.get_by_token(token)
            if user:
                self.set_secure_cookie('user_id', str(user.id))
            return self.redirect(next if next.startswith('/') else '/')
        self.render('sign_in.html')
        
    def post(self):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        next = self.get_argument('next', '/')
        if username and password:
            user = models.User.get_user(
                site=self.current_site,
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
            site=self.current_site,
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
