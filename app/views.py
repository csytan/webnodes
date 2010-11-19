import cgi
import datetime
import logging
import os
import re
import urllib
import urlparse

from google.appengine.ext import blobstore
from google.appengine.ext import db

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
            relative_date=self.relative_date,
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
        # vimeo and youtube embed
        value = re.sub('^http://(?:www\.)?vimeo.com/(\d+)', r'VIMEO:\1', value, re.MULTILINE)
        value = re.sub('^http://www.youtube.com/watch\?v=([^&]+)\S?', r'YOUTUBE:\1', value, re.MULTILINE)
        # automatic hyperlinks
        #value = re.sub(r'(^|\s)(http:\/\/\S+)', r'\1\[\2\]', value)
        html = markdown2.markdown(value, safe_mode='escape')
        html = re.sub(r'VIMEO:(\d+)', 
            r'<iframe src="http://player.vimeo.com/video/\1" class="vimeo" frameborder="0"></iframe>', html)
        html = re.sub(r'YOUTUBE:([\w|-]+)', 
            r'<iframe src="http://www.youtube.com/embed/\1?hd=1" class="youtube" frameborder="0"></iframe>', html)
        html = html.replace('<a href=', '<a rel="nofollow" href=')
        return html
        
    @staticmethod
    def relative_date(date):
        td = datetime.datetime.now() - date
        if td.days == 1:
            return '1 day ago'
        elif td.days:
            return str(td.days) + ' days ago'
        elif td.seconds / 60 / 60 == 1:
            return '1 hour ago'
        elif td.seconds > 60 * 60:
            return str(td.seconds / 60 / 60) + ' hours ago'
        elif td.seconds / 60 == 1:
            return '1 minute ago'
        elif td.seconds > 60:
            return str(td.seconds / 60) + ' minutes ago'
        else:
            return str(td.seconds) + ' seconds ago'


class Index(BaseHandler):
    def get(self):
        page = self.get_argument('page', '')
        page = abs(int(page)) if page.isdigit() else 0
        topics = self.current_site.hot_topics(page=page)
        next_page = page + 1 if len(topics) == 20 else None
        self.render('index.html', topics=topics, next_page=next_page)


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
    @tornado.web.authenticated
    def get(self):
        self.render('submit.html')
        
    @tornado.web.authenticated
    def post(self):
        slug = self.get_argument('slug', None)
        title = self.get_argument('title', None)
        text = self.get_argument('text', '')
        
        if not title:
            return self.reload(message='no_title', copyargs=True)
        if not slug or slug != self.slugify(slug):
            return self.reload(message='check_slug', copyargs=True)
        if not text:
            return self.reload(message='no_text', copyargs=True)
        
        topic = models.Topic.create(
            name=slug,
            site=self.current_site,
            title=title,
            author=self.current_user,
            text=text)
        if not topic:
            return self.reload(message='topic_exists', copyargs=True)
        
        self.current_user.n_topics = self.current_user.topics.count()
        self.current_user.put()
        self.redirect('/' + topic.name)
        
    @staticmethod
    def slugify(value):
        """
        Normalizes string, converts to lowercase, removes non-alpha characters,
        and converts spaces to hyphens.
        http://code.djangoproject.com/svn/django/trunk/django/template/defaultfilters.py
        """
        import unicodedata
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
        value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
        return re.sub('[-\s]+', '-', value)


class Topic(BaseHandler):
    def get(self, name):
        topic = models.Topic.get_topic(self.current_site, name)
        if not topic:
            raise tornado.web.HTTPError(404)
        self.render('topic.html', topic=topic, replies=topic.replies())
        
    def render_comments(self, comments):
        return self.render_string('_comment.html', comments=comments)
        
    def post(self, name):
        topic = models.Topic.get_topic(self.current_site, name)
        if not topic: raise tornado.web.HTTPError(404)
        
        reply_to = self.get_argument('reply_to', None)
        if reply_to:
            reply_to = models.Comment.get_by_id(int(reply_to))
            
        comment = models.Comment(
            author=self.current_user,
            topic=topic,
            reply_to=reply_to,
            text=self.get_argument('text'))
        topic.n_comments += 1
        if self.current_user:
            self.current_user.n_comments += 1
        db.put([topic, comment, self.current_user] if self.current_user else [topic, comment])
        
        parent_author = reply_to.author if reply_to else topic.author
        if parent_author and parent_author != comment.author:
            message = models.Message(to=parent_author, type='comment_reply', comment=comment)
            parent_author.n_messages += 1
            db.put([message, parent_author])
            
        self.redirect(self.request.path + '#c' + str(comment.id))


class TopicEdit(BaseHandler):
    @tornado.web.authenticated
    def get(self, name):
        topic = models.Topic.get_topic(self.current_site, name)
        self.render('topic_edit.html', topic=topic)
        
    @tornado.web.authenticated
    def post(self, name):
        topic = models.Topic.get_topic(self.current_site, name)
        if topic.can_edit(self.current_user):
            topic.title = self.get_argument('title')
            topic.text = self.get_argument('text', '')
            topic.put()
        self.redirect('/' + name)


class CommentEdit(BaseHandler):
    @tornado.web.authenticated
    def get(self, id):
        self.render('comment_edit.html', comment=models.Comment.get_by_id(int(id)))
        
    @tornado.web.authenticated
    def post(self, id):
        comment = models.Comment.get_by_id(int(id))
        if comment.can_edit(self.current_user):
            comment.text = self.get_argument('text', '')
            comment.put()
        self.redirect('/' + comment.topic.name + '#c' + id)


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
            topic = models.Topic.get_topic(self.current_site, topic_id)
            if comment.site != self.current_site:
                raise tornado.web.HTTPError(403)
                
        if self.current_user.is_admin or \
                (self.current_user.daily_karma > 0 and comment.author != self.current_user):
            way = self.get_argument('way', None)
            if way == 'up' and self.current_user.is_admin or \
                    self.current_user.name not in comment.up_votes:
                comment.points += 1
                if self.current_user.name not in comment.up_votes:
                    comment.up_votes.append(self.current_user.name)
                comment.update_score()
                comment.put()
                self.current_user.daily_karma -= 1
                self.current_user.put()
                if comment.author:
                    comment.author.karma += 1
                    comment.author.put()
            elif way == 'down' and self.current_user.is_admin or \
                    (self.current_user.karma >= 100 and \
                    self.current_user.name not in comment.down_votes):
                comment.points -= 1
                if self.current_user.name not in comment.down_votes:
                    comment.down_votes.append(self.current_user.name)
                comment.update_score()
                comment.put()
                self.current_user.daily_karma -= 1
                self.current_user.karma -= 1
                self.current_user.put()
                if comment.author:
                    comment.author.karma -= 1
                    comment.author.put()
        self.write(str(comment.points) + (' point' if comment.points in (1, -1) else ' points'))


class CommunityEdit(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('community_edit.html',
            upload_url=blobstore.create_upload_url('/community_edit'))
        
    @tornado.web.authenticated
    def post(self):
        blob_key = re.findall(r'blob-key="*([^;"\s]+)', self.request.body)
        if blob_key:
            blob_info = blobstore.BlobInfo.get(blob_key[0])
            if self.current_site.favicon:
                self.current_site.favicon.delete()
            self.current_site.favicon = str(blob_info.key())
        else:
            self.current_site.title = self.get_argument('title', '')
            self.current_site.tagline = self.get_argument('tagline', '')
            self.current_site.about = self.get_argument('about', '')
        self.current_site.put()
        self.reload(message='updated')


class Account(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('account.html')
        
    @tornado.web.authenticated
    def post(self):
        email = self.get_argument('email', None)
        if email != self.current_user.email:
            if email and not models.User.email_valid(email):
                return self.reload(message='check_email', copyargs=True)
            else:
                self.current_user.email = email
        password = self.get_argument('password', None)
        if password:
            self.current_user.set_password(password)
        self.current_user.about = self.get_argument('about', '')
        self.current_user.put()
        self.reload(message='updated')


class Inbox(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.current_user.n_messages = 0
        self.current_user.put()
        self.render('inbox.html',
            messages=self.current_user.messages.order('-created').fetch(20))


class Users(BaseHandler):
    def get(self):
        self.render('users/users.html', users=self.current_site.users.fetch(100))


class UserProfile(BaseHandler):
    def get(self, username):
        user = models.User.get_user(self.current_site, username)
        if not user:
            raise tornado.web.HTTPError(404)
        self.render('users/profile.html', user=user)


class UserTopics(BaseHandler):
    def get(self, username):
        user = models.User.get_user(self.current_site, username)
        if not user:
            raise tornado.web.HTTPError(404)
        self.render('users/topics.html', user=user)


class UserComments(BaseHandler):
    def get(self, username):
        user = models.User.get_user(self.current_site, username)
        if not user:
            raise tornado.web.HTTPError(404)
        self.render('users/comments.html', user=user)


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
                self.set_secure_cookie('user', user.key_name)
                return self.redirect(next if next.startswith('/') else '/')
        self.reload(message='login_error', copyargs=True)


class SignUp(BaseHandler):
    def get(self):
        self.render('sign_up.html')
        
    def post(self):
        username = self.get_argument('username', None)
        email = self.get_argument('email', None)
        password = self.get_argument('password', None)
        
        if email and not models.User.email_valid(email):
            return self.reload(message='check_email', copyargs=True)
            
        if username and not username.isalnum():
            return self.reload(message='check_username', copyargs=True)
            
        user = models.User.create(
            site=self.current_site,
            username=username,
            email=email,
            password=password)
        if user:
            message = models.Message(to=user, type='welcome')
            message.put()
            self.set_secure_cookie('user', user.key_name)
        else:
            return self.reload(message='user_exists', copyargs=True)
        self.redirect('/inbox')


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
