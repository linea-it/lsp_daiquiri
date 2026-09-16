import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class LineaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "linea"

    def ready(self):
        try:
            from linea.authentication import ServiceJWTAuthentication

            from daiquiri.jobs.viewsets import JobViewSet
            from daiquiri.query.viewsets import QueryJobViewSet

            for viewset in (JobViewSet, QueryJobViewSet):
                if ServiceJWTAuthentication not in viewset.authentication_classes:
                    viewset.authentication_classes = (
                        ServiceJWTAuthentication,
                        *viewset.authentication_classes,
                    )
            logger.info(
                "ServiceJWTAuthentication aplicado com sucesso em JobViewSet e QueryJobViewSet"
            )
        except Exception:
            logger.exception(
                "Falha ao aplicar ServiceJWTAuthentication em JobViewSet e QueryJobViewSet"
            )
