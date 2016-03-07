from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView

from daiquiri_auth.views import login

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^login/', login, name='login'),
    url(r'^admin/', include(admin.site.urls)),
]
