# Created by Oleksandr Sorochynskyi
# On 19/10/2019

from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect

"""
Middeware to force check user authentication for all views
that are not decorated with `auth_exempt` decorator.
"""

"""
The name of the attribute to be set by `auth_exempt`.
May change in the future due to naming conflicts with
Django/other libraries.
"""
_AUTH_EXEMPT_ATTR = 'auth_exempt'

def auth_exempt(value=True):
    """
    Exempt a view from requiring user authentication.

    Should work for both class-based views, and function views
    since `AuthRequiredMiddleware` checks `view.view_class`.
    """
    def _set_auth_exempt(view):
        setattr(view, _AUTH_EXEMPT_ATTR, value)
        return view
    return _set_auth_exempt

class AuthRequiredMiddleware(object):
    """
    Middleware that checks if the user is authenticated.

    Requires the `user` attribute to be defined in request.
    Thus it depends on AuthenticationMiddleware, and template context_processor
    'django.contrib.auth.context_processors.auth'. AuthenticationMiddleware also
    needs to be above this class in `settings.MIDDLEWARE`.

    To exempt a view from requiring authentication decorate
    it with `auth_exempt` decorator.

    If the user is not authenticated redirects to a page
    named 'login'. To override this behavior override
    the `redirect_to` class attribute.
    """

    redirect_to = reverse_lazy('login')

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user'), """
            The Login Required middleware needs to be after AuthenticationMiddleware.
            Also make sure to include the template context_processor:
            'django.contrib.auth.context_processors.auth'."""
        auth_exempt = (
            (hasattr(view_func, _AUTH_EXEMPT_ATTR) and
                view_func.auth_exempt) or
            # If it was generated form a class view
            (hasattr(view_func, "view_class") and
                hasattr(view_func.view_class, _AUTH_EXEMPT_ATTR) and
                view_func.view_args.auth_exempt)
        )
        if not (auth_exempt or request.user.is_authenticated):
            # Check if we're redirecting FROM self.redirect_to
            if request.path == self.redirect_to:
                raise ImproperlyConfigured("""
                    {target} is not auth_exempt.
                    Will cause infinite redirects.
                    Perhaps add auth_exempt decorator to view handling {target}.
                    """.format(
                        target=request.path
                    ))
            return HttpResponseRedirect(self.redirect_to)
        return None

    # What follows is boilerplate code required to be valid middleware
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response    

