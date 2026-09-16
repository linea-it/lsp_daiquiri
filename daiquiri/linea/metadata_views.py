from django.http import Http404
from django.shortcuts import render

from daiquiri.metadata.models import Schema, Table
from daiquiri.metadata.views import SchemaView as DaiquiriSchemaView
from daiquiri.metadata.views import TableView as DaiquiriTableView


def _access_denied(request, schema_name, table_name=None):
    return render(
        request,
        "metadata/access_denied.html",
        {
            "schema_name": schema_name,
            "table_name": table_name,
            "is_anonymous": not request.user.is_authenticated,
        },
        status=403,
    )


class SchemaView(DaiquiriSchemaView):
    def get(self, request, *args, **kwargs):
        schema_name = kwargs["schema_name"]
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            if Schema.objects.filter(name=schema_name).exists():
                return _access_denied(request, schema_name)
            raise


class TableView(DaiquiriTableView):
    def get(self, request, *args, **kwargs):
        schema_name = kwargs["schema_name"]
        table_name = kwargs["table_name"]
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            schema = Schema.objects.filter(name=schema_name).first()
            if schema and Table.objects.filter(schema=schema, name=table_name).exists():
                return _access_denied(request, schema_name, table_name)
            if (
                schema
                and not Table.objects.filter(schema=schema, name=table_name).exists()
            ):
                # schema existe, mas tabela não existe
                # 404 real da tabela
                raise
            if Schema.objects.filter(name=schema_name).exists():
                return _access_denied(request, schema_name)
            raise
