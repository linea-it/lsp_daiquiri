from django.urls import include, path, re_path
from linea.metadata_views import SchemaView, TableView
from rest_framework import routers

from daiquiri.metadata.views import ManagementView, SchemasView
from daiquiri.metadata.viewsets import (
    AccessLevelViewSet,
    ColumnViewSet,
    FunctionViewSet,
    LicenseViewSet,
    MetaViewSet,
    SchemaViewSet,
    TableViewSet,
)

app_name = "metadata"

router = routers.DefaultRouter()
router.register(r"schemas", SchemaViewSet, basename="schema")
router.register(r"tables", TableViewSet, basename="table")
router.register(r"columns", ColumnViewSet, basename="column")
router.register(r"functions", FunctionViewSet, basename="function")
router.register(r"licenses", LicenseViewSet, basename="license")
router.register(r"accesslevels", AccessLevelViewSet, basename="accesslevel")
router.register(r"meta", MetaViewSet, basename="meta")

urlpatterns = [
    path("api/", include(router.urls)),
    path("management/", ManagementView.as_view(), name="management"),
    re_path(r"^(?P<schema_name>\w+)/$", SchemaView.as_view(), name="schema"),
    re_path(
        r"^(?P<schema_name>\w+)/(?P<table_name>\w+)/$",
        TableView.as_view(),
        name="table",
    ),
    path("", SchemasView.as_view(), name="schemas"),
]
