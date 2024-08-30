from datetime import datetime, timezone
from pathlib import Path

import yaml
from django.core.management.base import BaseCommand

from daiquiri.core.constants import ACCESS_LEVEL_PRIVATE
from daiquiri.metadata.models import Schema


class Command(BaseCommand):
    help = "Updates table metadata from yml file."

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--local",
    #         action="store_true",
    #         dest="local",
    #         default=False,
    #         help="Does not download the files, uses the local files in /data/asteroid_table",
    #     )

    def add_arguments(self, parser):
        parser.add_argument(
            "schema",
            help="schema to be updated, there must be a yml file for the schema in the utils/fixtures directory",
        )

    def handle(self, *args, **options):
        self.stdout.write("Teste Update Metadata")
        print(f"Schema: {options['schema']}")
        fixtures_path = Path.cwd().joinpath("fixtures")
        print(f"Fixtures Path: {fixtures_path}")

        schema_yml = fixtures_path.joinpath(f"{options['schema']}.yml")
        print(f"Schema YML: {schema_yml}")

        if not schema_yml.exists():
            self.stdout.write(f"File {schema_yml} not found.")
            return

        with open(schema_yml, "r") as file:
            schemas = yaml.safe_load(file)

        schema_data = schemas[0]

        print(f"Geting daiquiri model for schema: {schema_data['name']}")
        try:
            schema_obj = Schema.objects.get(name=schema_data["name"])
            schema_obj.title = schema_data.get("title", "").strip()
            schema_obj.description = schema_data.get("description", "").strip()
            schema_obj.long_description = schema_data.get(
                "long_description", ""
            ).strip()
            schema_obj.attribution = schema_data.get("attribution", "").strip()
            schema_obj.license = schema_data.get("license", "PD").strip()
            schema_obj.doi = schema_data.get("doi", "").strip()
            schema_obj.order = schema_data.get("order", None)
            schema_obj.published = schema_data.get("published", None)
            schema_obj.updated = schema_data.get("updated", None)
            schema_obj.access_level = schema_data.get(
                "access_level", ACCESS_LEVEL_PRIVATE
            ).strip()
            schema_obj.metadata_access_level = schema_data.get(
                "metadata_access_level", ACCESS_LEVEL_PRIVATE.strip()
            )
            schema_obj.save()

            print(
                f"Updated schema metadata. ID: [{schema_obj.id}] Name: [{schema_obj.name}]"
            )
        except Exception as e:
            print(f"Error updating schema metadata: {schema_data['name']}")
            raise e

        schema_obj.refresh_from_db()

        # Iterate over schema table and update metadata
        for table_data in schema_data["tables"]:
            try:
                table_obj = schema_obj.tables.get(name=table_data["name"])
                table_obj.title = table_data["title"]
                table_obj.description = table_data["description"]
                table_obj.long_description = table_data.get("long_description", "")
                table_obj.attribution = table_data.get("attribution", "")
                table_obj.license = table_data.get("license", "PD")
                table_obj.doi = table_data.get("doi", "")
                table_obj.order = table_data.get("order", None)
                table_obj.published = table_data.get("published", None)
                table_obj.updated = table_data.get("updated", None)
                table_obj.access_level = table_data.get(
                    "access_level", ACCESS_LEVEL_PRIVATE
                ).strip()
                table_obj.metadata_access_level = table_data.get(
                    "metadata_access_level", ACCESS_LEVEL_PRIVATE.strip()
                )
                table_obj.save()

                print(
                    f"    Updated table metadata. ID: [{table_obj.id}] Name: [{table_obj.name}]"
                )
            except Exception as e:
                print(f"    Error updating table metadata: {table_data['name']}")
                raise e

            table_obj.refresh_from_db()

            # Iterate over table columns and update metadata
            print(f"    QTD Columns: {len(table_data['columns'])}")
            for column_data in table_data["columns"]:
                try:
                    column_obj = table_obj.columns.get(name=column_data["name"])
                    column_obj.description = column_data.get("description", "")
                    column_obj.unit = column_data.get("unit", "")
                    column_obj.ucd = column_data.get("ucd", "")
                    column_obj.order = column_data.get("order", None)
                    column_obj.save()

                    print(
                        f"        Updated column metadata. ID: [{column_obj.id}] Name: [{column_obj.name}]"
                    )
                except Exception as e:
                    print(
                        f"        Error updating column metadata: {column_data['name']}"
                    )
                    raise e
