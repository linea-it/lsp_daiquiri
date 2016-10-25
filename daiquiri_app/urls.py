from django.conf.urls import include, url
from django.contrib import admin
from django.views.i18n import javascript_catalog

from daiquiri_core.views import home

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^auth/', include('daiquiri_auth.urls_auth')),
    url(r'^accounts/', include('daiquiri_auth.urls_accounts')),
    url(r'^metadata/', include('daiquiri_metadata.urls')),
    url(r'^serve/', include('daiquiri_serve.urls')),
    url(r'^query/', include('daiquiri_query.urls')),
    url(r'^contact/', include('daiquiri_contact.urls')),
    url(r'^uws/', include('daiquiri_jobs.urls', namespace='uws')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^jsi18n/$', javascript_catalog, name='javascript-catalog'),
]
