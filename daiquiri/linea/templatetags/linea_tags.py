from django import template

from daiquiri.metadata.models import Table

register = template.Library()


@register.simple_tag
def registered_tables():
    """Retorna o conjunto de tabelas registradas nos metadados, no formato "schema.tabela".

    Uso no template:
        {% registered_tables as tables %}
        {% if "lsst_dp2.object" in tables %}...{% endif %}
    """
    return {
        f"{schema}.{table}"
        for schema, table in Table.objects.values_list("schema__name", "name")
    }
