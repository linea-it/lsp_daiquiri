import logging

from django.conf import settings
from django.contrib.auth.models import Group

from shibboleth.middleware import ShibbolethRemoteUserMiddleware


class ShibbolethMiddleware(ShibbolethRemoteUserMiddleware):
    def make_profile(self, user, shib_meta):
        """
        This is here as a stub to allow subclassing of ShibbolethRemoteUserMiddleware
        to include a make_profile method that will create a Django user profile
        from the Shib provided attributes.  By default it does nothing.
        """
        log = logging.getLogger("shibboleth")
        log.debug(settings.MIDDLEWARE)
        log.debug(settings.AUTHENTICATION_BACKENDS)
        log.debug(settings.SHIBBOLETH_ATTRIBUTE_MAP)

        # Usar essa url depois de logado para ver os atributos disponiveis
        # https://userquery-dev.linea.org.br/Shibboleth.sso/Session

        log.info("Shibboleth::make_profile()")
        log.debug(f"Shib Meta: {shib_meta}")
        log.debug(f"User: {user}")

        # Guardar o email do usuario
        user.email = shib_meta["email"]
        log.info("Updated user email")

        user.save()

        try:
            # Adicionar o usuario ao grupo Shibboleth
            group, created = Group.objects.get_or_create(name="Shibboleth")
            user.groups.add(group)
            log.info("Added user to Shibboleth group")
        except Exception as e:
            log.error("Failed on add user to group shibboleth. Error: %s" % e)

        log.debug("--------------------------")

        return
