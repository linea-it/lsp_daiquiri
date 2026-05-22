import difflib
from pathlib import Path

import yaml
from django.core.management.base import BaseCommand, CommandError

from daiquiri.core.constants import ACCESS_LEVEL_PRIVATE
from daiquiri.metadata.models import Column, Schema, Table


class Command(BaseCommand):
    help = "Atualiza metadados de tabelas a partir de um arquivo YAML."

    def add_arguments(self, parser):
        parser.add_argument(
            "schema",
            help="schema name; must match fixtures/<name>.yml under the app cwd (e.g. mpc_sbn → mpc_sbn.yml)",
        )

    def handle(self, *args, **options):
        self.stdout.write("Update Metadata")
        print(f"Schema: {options['schema']}")
        fixtures_path = Path.cwd().joinpath("fixtures")
        print(f"Fixtures Path: {fixtures_path}")

        schema_yml = fixtures_path.joinpath(f"{options['schema']}.yml")
        print(f"Schema YML: {schema_yml}")

        if not schema_yml.exists():
            available = (
                sorted(p.stem for p in fixtures_path.glob("*.yml"))
                if fixtures_path.is_dir()
                else []
            )
            guess = difflib.get_close_matches(
                options["schema"], available, n=1, cutoff=0.55
            )
            msg = f"Arquivo não encontrado: {schema_yml}"
            if available:
                msg += f". YAMLs em {fixtures_path}: {', '.join(available)}"
            if guess:
                msg += f". Sugestão: `manage.py update_table_metadata {guess[0]}`"
            raise CommandError(msg)

        with open(schema_yml, "r") as file:
            schemas = yaml.safe_load(file)

        schema_data = schemas[0]

        print(f"Geting daiquiri model for schema: {schema_data['name']}")
        try:
            schema_obj = Schema.objects.get(name=schema_data["name"])
        except Schema.DoesNotExist as exc:
            raise CommandError(
                f'O schema "{schema_data["name"]}" não existe na base de metadados '
                f"(daiquiri.metadata.Schema). O comando só preenche títulos/descrições "
                f"a partir do YAML; o registro inicial precisa existir.\n\n"
                f"Faça antes: Management → Metadata management → Create new schema entry, "
                f'name = "{schema_data["name"]}", com "Automatically discover tables and columns" '
                f"ativado (e o schema/tabelas já criados no PostgreSQL).\n\n"
                f"Ver compose/local/README.md, secção «Registro de Catalogos/Tabelas»."
            ) from exc

        schema_obj.title = schema_data.get("title", "").strip()
        schema_obj.description = schema_data.get("description", "").strip()
        schema_obj.long_description = schema_data.get("long_description", "").strip()
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
            "metadata_access_level", ACCESS_LEVEL_PRIVATE
        ).strip()
        schema_obj.save()

        print(
            f"Updated schema metadata. ID: [{schema_obj.id}] Name: [{schema_obj.name}]"
        )

        schema_obj.refresh_from_db()

        # Percorre as tabelas do schema e atualiza os metadados
        for table_data in schema_data["tables"]:
            try:
                table_obj = schema_obj.tables.get(name=table_data["name"])
            except Table.DoesNotExist as exc:
                known = list(
                    schema_obj.tables.order_by("name").values_list("name", flat=True)
                )
                raise CommandError(
                    f'Não existe tabela "{table_data["name"]}" nos metadados do schema '
                    f'"{schema_obj.name}". Tabelas registradas no Daiquiri: '
                    f"{known if known else '(nenhuma — a descoberta não criou tabelas)'}.\n\n"
                    "Os nomes no YAML têm de coincidir com os nomes no PostgreSQL e com as "
                    "entradas em Metadata management.\n\n"
                    "Se a lista está vazia ou falta `main`: edite o schema em "
                    "Management → Metadata management, confirme que "
                    '"Automatically discover tables and columns" está ativo, grave de novo '
                    "(com o schema e tabelas já existentes na base `data`).\n\n"
                    "No PostgreSQL de dados pode confirmar nomes com:\n"
                    f"  SELECT tablename FROM pg_tables WHERE schemaname = '{schema_obj.name}';"
                ) from exc

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
                "metadata_access_level", ACCESS_LEVEL_PRIVATE
            ).strip()
            table_obj.save()

            print(
                f"    Updated table metadata. ID: [{table_obj.id}] Name: [{table_obj.name}]"
            )

            table_obj.refresh_from_db()

            # Percorre as colunas da tabela e atualiza os metadados
            print(f"    QTD Columns: {len(table_data['columns'])}")
            for column_data in table_data["columns"]:
                try:
                    column_obj = table_obj.columns.get(name=column_data["name"])
                except Column.DoesNotExist as exc:
                    col_names = list(
                        table_obj.columns.order_by("name").values_list(
                            "name", flat=True
                        )
                    )
                    preview = col_names[:25]
                    suffix = " …" if len(col_names) > 25 else ""
                    raise CommandError(
                        f'Coluna "{column_data["name"]}" não existe nos metadados da tabela '
                        f'"{schema_obj.name}.{table_obj.name}". '
                        f"Colunas registradas ({len(col_names)}): {preview}{suffix}\n\n"
                        "Alinhe o YAML às colunas descobertas (nomes em minúsculas no PG) ou "
                        "volte a gravar o schema com descoberta automática."
                    ) from exc

                column_obj.description = column_data.get("description", "")
                column_obj.unit = column_data.get("unit", "")
                column_obj.ucd = column_data.get("ucd", "")
                column_obj.order = column_data.get("order", None)
                column_obj.save()

                print(
                    f"        Updated column metadata. ID: [{column_obj.id}] Name: [{column_obj.name}]"
                )
