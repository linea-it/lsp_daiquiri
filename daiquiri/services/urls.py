from django.urls import path

from . import views

app_name = "services"

urlpatterns = [
    path("", views.overview, name="overview"),
    path("query-interface/", views.query_interface, name="query_interface"),
    path("direct-download/", views.direct_download, name="direct_download"),
    path("scripted-access/", views.scripted_access, name="scripted_access"),
    path("adql-postgresql/", views.adql_postgresql, name="adql_postgresql"),
]