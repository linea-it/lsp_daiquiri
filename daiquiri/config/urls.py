from django.urls import include, path
from django.contrib import admin
from django.views.generic import TemplateView

from daiquiri.core.views import home
# from django.conf import settings

urlpatterns = [
    path('daiquiri/', home, name='home'),
    path('daiquiri/accounts/', include('daiquiri.auth.urls_accounts')),
    path('daiquiri/auth/', include('daiquiri.auth.urls_auth', namespace='auth')),
    path('daiquiri/conesearch/', include('daiquiri.conesearch.urls', namespace='conesearch')),
    path('daiquiri/contact/', include('daiquiri.contact.urls', namespace='contact')),
    path('daiquiri/datalink/', include('daiquiri.datalink.urls', namespace='datalink')),
    path('daiquiri/files/', include('daiquiri.files.urls', namespace='files')),
    path('daiquiri/metadata/', include('daiquiri.metadata.urls', namespace='metadata')),
    path('daiquiri/oai/', include('daiquiri.oai.urls', namespace='oai')),
    path('daiquiri/registry/', include('daiquiri.registry.urls', namespace='registry')),
    path('daiquiri/serve/', include('daiquiri.serve.urls', namespace='serve')),
    path('daiquiri/stats/', include('daiquiri.stats.urls', namespace='stats')),
    path('daiquiri/query/', include('daiquiri.query.urls', namespace='query')),
    path('daiquiri/tap/', include('daiquiri.tap.urls', namespace='tap')),
    path('daiquiri/uws/', include('daiquiri.uws.urls', namespace='uws')),

    path('daiquiri/robots.txt', TemplateView.as_view(template_name='site/robots.txt', content_type='text/plain'), name='robots'),
    path('daiquiri/layout/', TemplateView.as_view(template_name='wordpress/layout.html'), name='layout'),

    path('daiquiri/admin/', admin.site.urls),

    # Auth Shibboleth
    path('daiquiri/shib/', include("shibboleth.urls", namespace="shibboleth")),
]

# # Add 'prefix' to all urlpatterns
# if settings.BASE_URL != '/':
#     urlpatterns = [path(f'{settings.BASE_URL}', include(urlpatterns))]

handler400 = 'daiquiri.core.views.bad_request'
handler403 = 'daiquiri.core.views.forbidden'
handler404 = 'daiquiri.core.views.not_found'
handler500 = 'daiquiri.core.views.internal_server_error'
