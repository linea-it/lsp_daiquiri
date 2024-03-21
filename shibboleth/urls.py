# Correção Temporaria do django-shibboleth-remoteuser Incompativel com Vesão 4.x do Django.
# Enquanto o PR https://github.com/Brown-University-Library/django-shibboleth-remoteuser/pull/93
# Não é feito Merge. Criei uma copia local do arquivo com a correção. e durante a criação do container
# Substituo o arquivo na pasta de instalação do Shibboleth dentro do container.
# /usr/local/lib/python3.9/site-packages/shibboleth/urls.py
import django
from django.urls import re_path

from .views import ShibbolethLoginView, ShibbolethLogoutView, ShibbolethView

app_name = "shibboleth"

urlpatterns = [
    re_path(r"^login/$", ShibbolethLoginView.as_view(), name="login"),
    re_path(r"^logout/$", ShibbolethLogoutView.as_view(), name="logout"),
    re_path(r"^$", ShibbolethView.as_view(), name="info"),
]
