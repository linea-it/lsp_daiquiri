"""Testes simples de regressão para o upgrade do Daiquiri."""

from django.conf import settings
from django.core.management import get_commands
from django.test import Client, SimpleTestCase, TestCase
from django.urls import resolve, reverse


class SettingsRegressionTest(SimpleTestCase):
    def test_static_url_customizada(self):
        self.assertEqual(settings.STATIC_URL, "/daiquiri_static/")

    def test_staticfiles_dirs_inclui_assets_linea(self):
        # Logotipos/banners em daiquiri/static/daiquiri/ entram no collectstatic
        dirs = list(settings.STATICFILES_DIRS)
        self.assertIn(settings.BASE_DIR / "static", dirs)

    def test_adapter_database_customizado(self):
        self.assertEqual(settings.ADAPTER_DATABASE, "linea.adapter.PostgreSQLAdapter")

    def test_wagtail_instalado(self):
        self.assertIn("wagtail", settings.INSTALLED_APPS)


class AdapterRegressionTest(SimpleTestCase):
    def test_adapter_importa(self):
        from linea.adapter import PostgreSQLAdapter

        self.assertTrue(hasattr(PostgreSQLAdapter, "DATATYPES"))

    def test_tipos_customizados_presentes(self):
        from linea.adapter import PostgreSQLAdapter

        for datatype in [
            "numeric",
            "decimal",
            "bpchar",
            "char",
            "timestamp",
            "timestamptz",
            "bool",
        ]:
            self.assertIn(datatype, PostgreSQLAdapter.DATATYPES)


class SamlRegressionTest(SimpleTestCase):
    def test_backend_importa(self):
        from linea.saml2 import LineaSaml2Backend

        self.assertTrue(callable(LineaSaml2Backend))

    def test_views_importam(self):
        from linea.views import linea_login, saml2_template_failure

        self.assertTrue(callable(linea_login))
        self.assertTrue(callable(saml2_template_failure))


class UrlRegressionTest(SimpleTestCase):
    def test_javascript_catalog_url(self):
        self.assertEqual(reverse("javascript-catalog"), "/jsi18n/")

    def test_rotas_principais_resolvem(self):
        for path in [
            "/",
            "/query/",
            "/tap/",
            "/metadata/",
            "/conesearch/",
            "/login/",
            "/admin/",
            "/wagtail/",
            "/cms/",
        ]:
            resolve(path)


class LineaAccountPagesTest(TestCase):
    """GET em páginas que renderizam nav + Wagtail (precisa de DB)."""

    databases = {"default"}

    def test_paginas_conta_e_login_linea_respondem(self):
        client = Client()
        for path in (
            "/accounts/login/",
            "/accounts/signup/",
            "/accounts/password/reset/",
            "/login/",
        ):
            with self.subTest(path=path):
                response = client.get(path)
                self.assertIn(
                    response.status_code,
                    (200, 302),
                    msg=f"{path} retornou {response.status_code}",
                )


class CommandsRegressionTest(SimpleTestCase):
    def test_comandos_custom_existem(self):
        commands = get_commands()
        self.assertIn("generate_table_metadata", commands)
        self.assertIn("update_table_metadata", commands)
