"""
Adaptador PostgreSQL que estende o do django-daiquiri.

Mapeia tipos que o adaptador base não trata, para a descoberta de colunas
usar os datatypes TAP/IVOA corretos em vez de cair em 'char'.
"""

from daiquiri.core.adapter.database.postgres import (
    PostgreSQLAdapter as BasePostgreSQLAdapter,
)


class PostgreSQLAdapter(BasePostgreSQLAdapter):
    """Adiciona mapeamento de tipos usados em mpc_sbn.obs_sbn e tabelas similares."""

    DATATYPES = {
        **BasePostgreSQLAdapter.DATATYPES,
        # numérico exato
        "numeric": {"datatype": "double", "arraysize": False},
        "decimal": {"datatype": "double", "arraysize": False},
        # character(n)
        "bpchar": {"datatype": "char", "arraysize": True},
        "char": {"datatype": "char", "arraysize": True},
        # timestamps
        "timestamp": {"datatype": "timestamp", "arraysize": False},
        "timestamptz": {"datatype": "timestamp", "arraysize": False},
        "timestamp without time zone": {"datatype": "timestamp", "arraysize": False},
        "timestamp with time zone": {"datatype": "timestamp", "arraysize": False},
        # boolean
        "bool": {"datatype": "boolean", "arraysize": False},
    }
