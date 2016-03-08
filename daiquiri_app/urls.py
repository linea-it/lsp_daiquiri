from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='core/home.html'), name='home'),
    url(r'^auth/', include('daiquiri_auth.urls')),
    url(r'^%s/' % settings.LOGIN_URL.strip('/'), 'daiquiri_auth.views.login', name='login'),
    url(r'^%s/' % settings.LOGOUT_URL.strip('/'), 'daiquiri_auth.views.logout', name='logout'),
    url(r'^admin/', include(admin.site.urls)),
]
