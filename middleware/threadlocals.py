try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()
##  The current user
def get_current_user():
    return getattr(_thread_locals, 'user', None)

## Threadlocals
#
#  http://code.djangoproject.com/wiki/CookBookThreadlocalsAndUser
#  Middleware that gets various objects from the request object and saves them in thread local storage.
class ThreadLocals(object):

    def process_request(self, request):
        _thread_locals.user = getattr(request, 'user', None)