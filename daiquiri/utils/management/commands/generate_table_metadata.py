import csv
import re
from datetime import datetime, timezone
from pathlib import Path

import yaml
from daiquiri.core.constants import ACCESS_LEVEL_PRIVATE
from daiquiri.metadata.models import Schema
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generate table yml metadata from database."

    def add_arguments(self, parser):
        parser.add_argument(
            "schema",
            help="schema name to be processed, need to pre registered in the daiquiri database",
        )

        parser.add_argument(
            "table",
            help="table name to be processed, need to pre registered in the daiquiri database",
        )

        parser.add_argument(
            "--columns_file",
            help="csv file with descriptions and ucds for columns",
        )

    def parse_column_name(self, nome_coluna: str) -> str:
        """
        Versão mais simples focada nos padrões específicos do seu CSV.
        """
        if not nome_coluna:
            return nome_coluna

        # Insere underscore antes de qualquer letra maiúscula que tenha letra minúscula antes
        # mas preserva os underscores existentes
        nome_temp = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", nome_coluna)

        # Converte para lowercase
        nome_padronizado = nome_temp.lower()

        return nome_padronizado

    def load_columns_csv(self, columns_csv_file):
        """Carrega todas as colunas do CSV em memória"""
        try:
            columns = {}
            with open(columns_csv_file, "r", newline="", encoding="utf-8") as arquivo:
                leitor = csv.DictReader(arquivo)

                for linha in leitor:
                    nome = self.parse_column_name(linha["name"])
                    columns[nome] = {
                        "name": linha["name"],
                        "data_type": linha["data_type"],
                        "unit": linha["unit"],
                        "description": linha["description"],
                        "ucd": linha["ucd"],
                        "order": linha["order"],
                        "principal": linha["principal"],
                    }

            return columns
        except FileNotFoundError:
            print(f"Erro: Arquivo '{columns_csv_file}' não encontrado.")
        except Exception as e:
            print(f"Erro ao processar o arquivo: {e}")

    def handle(self, *args, **options):
        self.stdout.write("Generate Metadata")

        schema = options["schema"]
        table = options["table"]
        print(f"Schema: {schema}")
        print(f"Table: {table}")
        fixtures_path = Path.cwd().joinpath("fixtures")
        print(f"Fixtures Path: {fixtures_path}")

        schema_yml = fixtures_path.joinpath(f"{schema}.yml")
        print(f"Schema YML: {schema_yml}")

        columns_attributes = {}
        columns_csv_filename = options.get("columns_file")
        if columns_csv_filename:
            columns_csv_file = fixtures_path.joinpath(columns_csv_filename)
            print(f"Columns CSV File: {columns_csv_file}")
            columns_attributes = self.load_columns_csv(columns_csv_file)

        schema_data = {}

        schema_obj = Schema.objects.get(name=schema)
        schema_data["name"] = schema_obj.name
        schema_data["title"] = schema_obj.title
        schema_data["description"] = schema_obj.description
        schema_data["long_description"] = schema_obj.long_description
        schema_data["attribution"] = schema_obj.attribution
        schema_data["order"] = schema_obj.order
        schema_data["license"] = schema_obj.license
        schema_data["doi"] = schema_obj.doi
        schema_data["related_identifiers"] = schema_obj.related_identifiers
        schema_data["utype"] = schema_obj.utype
        schema_data["published"] = (
            schema_obj.published.isoformat() if schema_obj.published else None
        )
        schema_data["updated"] = (
            schema_obj.updated.isoformat() if schema_obj.updated else None
        )
        schema_data["access_level"] = schema_obj.access_level
        schema_data["metadata_access_level"] = schema_obj.metadata_access_level
        schema_data["groups"] = [group.name for group in schema_obj.groups.all()]

        # Tables metadata
        for table_obj in schema_obj.tables.filter(name=table):
            table_data = {}
            table_data["name"] = table_obj.name
            table_data["title"] = table_obj.title
            table_data["description"] = table_obj.description
            table_data["long_description"] = table_obj.long_description
            table_data["attribution"] = table_obj.attribution
            table_data["order"] = table_obj.order
            table_data["license"] = table_obj.license
            table_data["doi"] = table_obj.doi
            table_data["related_identifiers"] = table_obj.related_identifiers
            table_data["utype"] = table_obj.utype
            table_data["published"] = (
                table_obj.published.isoformat() if table_obj.published else None
            )
            table_data["updated"] = (
                table_obj.updated.isoformat() if table_obj.updated else None
            )
            table_data["access_level"] = table_obj.access_level
            table_data["metadata_access_level"] = table_obj.metadata_access_level
            table_data["groups"] = [group.name for group in table_obj.groups.all()]

            # Columns metadata
            columns_data = []
            for column_obj in table_obj.columns.all():
                column_data = {}
                column_data["name"] = column_obj.name
                column_data["ucd"] = column_obj.ucd
                column_data["unit"] = column_obj.unit
                column_data["description"] = column_obj.description
                column_data["order"] = column_obj.order

                if column_obj.name in columns_attributes:
                    column_attr = columns_attributes[column_obj.name]
                    column_data["ucd"] = column_attr.get(
                        "ucd", column_data["ucd"]
                    ).strip()
                    column_data["unit"] = column_attr.get(
                        "unit", column_data["unit"]
                    ).strip()
                    column_data["description"] = column_attr.get(
                        "description", column_data["description"]
                    ).strip()

                columns_data.append(column_data)

            table_data["columns"] = columns_data
            schema_data.setdefault("tables", []).append(table_data)

        with open(schema_yml, "w") as file:
            yaml.dump([schema_data], file, sort_keys=False, indent=2)

        if not schema_yml.exists():
            self.stdout.write(f"File {schema_yml} not created.")
            return

        self.stdout.write(f"Metadata YML file created: {schema_yml}")
