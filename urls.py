from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to, direct_to_template
from gallery.views import *

## The served urls
#
#  Most of the important variables are passed through URLS to make the resulting pages
#  bookmarkable and searchengine-friendly
urlpatterns = patterns('',
    ## The home page
    (r'^$', index, {'template': 'gallery/index.html'}),
    ## See the photos you have uploaded
    (r'^yourphotos/$', index, {'template': 'gallery/index.html', 'home':True}),
    ## See the photos uploaded by a specific uder
    (r'^user/(?P<user>\w*)/$', index, {'template': 'gallery/index.html'}),
    ## See the photos tagged with a specific tag
    (r'^tag/(?P<tag>\w*)/$', index, {'template': 'gallery/index.html'}),

    ## Edit your photoes infos
    (r'^edit/(?P<id>\d*)/$', edit, {'template': 'gallery/edit.html'}),
    ## Delete your photoes
    (r'^delete/(?P<id>\d*)/$', delete, {'template': '/gallery/index.html'}),

    ## register yourself as a user
    (r'^register/$', register, {'template': 'gallery/register.html'}),
    ## login
    (r'^login/$', login_view, {'template': 'gallery/login.html'}),
    ## change your password
    (r'^changepasswd/$', change_password, {'template': 'gallery/changepasswd.html'}),
    ## logout
    (r'^logout/$', logout_view, {}),

    ## the URL where the actual photoes are
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/mauro/documenti/progetti/django/djangogallery/media/'}),

    ## the administration interface
    (r'^admin/', include('django.contrib.admin.urls')),
)
