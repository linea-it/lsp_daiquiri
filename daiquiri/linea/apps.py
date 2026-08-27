from django.apps import AppConfig


class LineaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "linea"

    def ready(self):
        from daiquiri.jobs.viewsets import JobViewSet
        from daiquiri.query.viewsets import QueryJobViewSet
        from linea.authentication import ServiceJWTAuthentication

        for viewset in (JobViewSet, QueryJobViewSet):
            if ServiceJWTAuthentication not in viewset.authentication_classes:
                viewset.authentication_classes = (
                    ServiceJWTAuthentication,
                    *viewset.authentication_classes,
                )
