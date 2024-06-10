import logging

from django.contrib.auth.models import Group
from djangosaml2.backends import Saml2Backend
from typing import Any, Optional, Tuple

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, MultipleObjectsReturned

from django.contrib import auth
from django.contrib.auth.backends import ModelBackend
from linea.comanage import Comanage

logger = logging.getLogger("djangosaml2")

class LineaSaml2Backend(Saml2Backend):

    def __init__(self):
        self.log = logging.getLogger("saml2")

        self.comanage = Comanage(
            service_url=settings.COMANAGE_SERVER_URL,
            user=settings.COMANAGE_USER,
            password=settings.COMANAGE_PASSWORD,
            coid=settings.COMANAGE_COID,
        )

    def _extract_user_identifier_params(
            self, session_info: dict, attributes: dict, attribute_mapping: dict
        ) -> Tuple[str, Optional[Any]]:
        """Returns the attribute to perform a user lookup on, and the value to use for it.
        The value could be the name_id, or any other saml attribute from the request.
        """
        self.log.info("Extract user identifier")
        # Lookup key
        user_lookup_key = self._user_lookup_attribute
        self.log.debug(f"User Lookup Key: {user_lookup_key}")

        # Lookup value
        if getattr(settings, "SAML_USE_NAME_ID_AS_USERNAME", False):
            if session_info.get("name_id"):
                self.log.debug(f"name_id: {session_info['name_id']}")
                user_lookup_value = session_info["name_id"].text
            else:
                self.log.error(
                    "The nameid is not available. Cannot find user without a nameid."
                )
                user_lookup_value = None
        else:
            # Obtain the value of the custom attribute to use
            user_lookup_value = self._get_attribute_value(
                user_lookup_key, attributes, attribute_mapping
            )

        self.log.debug(f"User Lookup Value: {user_lookup_value}")


        # Utiliza o identificador de usuario do SAML (eppn)
        # para fazer uma consulta ao COmanage do LIneA
        # e descobrir UID do LDAP para este usuario. 
        try:
            eppn = user_lookup_value
            self.eppn = eppn

            self.log.debug("Retriving ldap uid from COmanage.")
            ldap_uid = self.comanage.get_ldap_uid(identifier=eppn)
            self.log.debug(f"LDAP UID: {ldap_uid}")

            return user_lookup_key, ldap_uid

        except Exception as e:
            msg = f"Failed on retrive ldap uid from COmanager. Error: {e}"
            self.log.error(msg)

            user_lookup_value = self.clean_user_main_attribute(user_lookup_value)

            return user_lookup_key, user_lookup_value


    def clean_user_main_attribute(self, main_attribute: Any) -> Any:
        """Hook to clean the extracted user-identifying value. No-op by default."""
        main_attribute = main_attribute.split("@")[0]
        return main_attribute

    def is_authorized(
        self,
        attributes: dict,
        attribute_mapping: dict,
        idp_entityid: str,
        assertion_info: dict,
        **kwargs,
    ) -> bool:
        """Hook to allow custom authorization policies based on SAML attributes. True by default."""
        return True        

    def user_can_authenticate(self, user) -> bool:
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        is_active = getattr(user, "is_active", None)
        return is_active or is_active is None


    def save_user(self, user, *args, **kwargs):
        user = super().save_user(user, *args, **kwargs)
        # Tratamento dos grupos que o usuario pertence
        self.setup_groups(user)        
        return user

    def setup_groups(self, user):
        self.log.debug("Setup User Groups")
        
        # Add a custom group saml for mark this user make login using djangosaml2.
        groups = ["saml2"]

        # Recupera os grupos do usuario
        try:
            self.log.info("Retriving User Groups from COmanage.")
            personid = self.comanage.get_co_person_id(identifier=self.eppn)
            cogroups = self.comanage.get_groups(personid)

            for group in cogroups:
                groups.append(group["Name"])

        except Exception as e:
            msg = f"Failed on retrive groups from COmanage. Error: {e}"
            self.log.error(msg)

        # Remove the user from all groups that are not specified  
        for group in user.groups.all():
            if group.name not in groups:
                group.user_set.remove(user)
                self.log.debug(f"User has been removed from the group {group.name}")

        # Add the user to all groups in the shibboleth metadata
        for g in groups:
            group, created = Group.objects.get_or_create(name=g)
            user.groups.add(group)

        self.log.debug("User has been added to the following groups")
        self.log.debug(f"Groups: {groups}")

        return user
