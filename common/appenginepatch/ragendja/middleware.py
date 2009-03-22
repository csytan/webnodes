# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.utils.cache import patch_cache_control

LOGIN_REQUIRED_PREFIXES = getattr(settings, 'LOGIN_REQUIRED_PREFIXES', ())
NO_LOGIN_REQUIRED_PREFIXES = getattr(settings, 'NO_LOGIN_REQUIRED_PREFIXES', ())

class LoginRequiredMiddleware(object):
    """
    Redirects to login page if request path begins with a
    LOGIN_REQURED_PREFIXES prefix. You can also specify
    NO_LOGIN_REQUIRED_PREFIXES which take precedence.
    """
    def process_request(self, request):
        for prefix in NO_LOGIN_REQUIRED_PREFIXES:
            if request.path.startswith(prefix):
                return None
        for prefix in LOGIN_REQUIRED_PREFIXES:
            if request.path.startswith(prefix) and \
                    not request.user.is_authenticated():
                return redirect_to_login(request.get_full_path())
        return None

class NoHistoryCacheMiddleware(object):
    """
    If user is authenticated we disable browser caching of pages in history.
    """
    def process_response(self, request, response):
        if 'Expires' not in response and \
                'Cache-Control' not in response and \
                hasattr(request, 'session') and \
                request.user.is_authenticated():
            patch_cache_control(response,
                no_store=True, no_cache=True, must_revalidate=True, max_age=0)
        return response
