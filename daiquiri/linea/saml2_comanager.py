import logging
from typing import Any, Optional, Tuple

from django.apps import apps
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Group
from django.core.exceptions import ImproperlyConfigured, MultipleObjectsReturned
from djangosaml2.backends import Saml2Backend
from linea.comanage import Comanage

logger = logging.getLogger("djangosaml2")


class LineaSaml2Backend(Saml2Backend):

    def __init__(self):
        # self.log = logging.getLogger("djangosaml2")

        self.comanage = Comanage(
            service_url=settings.COMANAGE_SERVER_URL,
            user=settings.COMANAGE_USER,
            password=settings.COMANAGE_PASSWORD,
            coid=settings.COMANAGE_COID,
        )

    def _extract_user_identifier_params(
        self, session_info: dict, attributes: dict, attribute_mapping: dict
    ) -> Tuple[str, Optional[Any]]:
        """Retorna o atributo usado na busca do usuário e o valor correspondente.
        O valor pode ser o name_id ou outro atributo SAML da requisição.
        """
        logger.info("-----------------------------------------")
        logger.info("Extract user identifier.")
        logger.info("_extract_user_identifier_params()")
        logger.info("-----------------------------------------")
        # Chave de busca
        user_lookup_key = self._user_lookup_attribute
        logger.info(f"User Lookup Key: {user_lookup_key}")

        # Valor de busca
        user_lookup_value = None
        try:
            if getattr(settings, "SAML_USE_NAME_ID_AS_USERNAME", False):
                if session_info.get("name_id"):
                    logger.info(f"name_id: {session_info['name_id']}")
                    user_lookup_value = session_info["name_id"].text
                else:
                    logger.error(
                        "The nameid is not available. Cannot find user without a nameid."
                    )
            else:
                # Valor do atributo customizado configurado
                user_lookup_value = self._get_attribute_value(
                    user_lookup_key, attributes, attribute_mapping
                )
        except Exception as e:
            logger.error("Failed to extract user identifier.")
            logger.error(e)
            return user_lookup_key, None

        logger.info(
            f"User Lookup Value: {user_lookup_value} Type: {type(user_lookup_value)}"
        )
        if (
            user_lookup_value is None
            or user_lookup_value == "None"
            or user_lookup_value == ""
        ):
            logger.error("No identifier to search in COmanager.")
            return user_lookup_key, None

        # Usa o identificador SAML (eppn) para consultar o COmanage LIneA
        # e obter o UID LDAP do usuário.
        try:
            eppn = user_lookup_value
            self.eppn = eppn

            logger.info("Retriving ldap uid from COmanage.")
            ldap_uid = self.comanage.get_ldap_uid(identifier=eppn)
            logger.info(f"LDAP UID: {ldap_uid}")

            user_lookup_value = self.clean_user_main_attribute(ldap_uid)
            logger.info(f"User Lookup Value: {user_lookup_value}")

            return user_lookup_key, user_lookup_value

        except Exception as e:
            logger.error(e)
            return user_lookup_key, None

    def clean_user_main_attribute(self, main_attribute: Any) -> Any:
        """Normaliza o valor que identifica o usuário (substitui '.' por '_')."""
        main_attribute = main_attribute.replace(".", "_")
        return main_attribute

    def is_authorized(
        self,
        attributes: dict,
        attribute_mapping: dict,
        idp_entityid: str,
        assertion_info: dict,
        **kwargs,
    ) -> bool:
        """Autorização customizada com base nos atributos SAML. Padrão: permitir."""
        logger.info("-----------------------------------------")
        logger.info("Checks if the user is authorized")
        logger.info("is_authorized()")
        logger.info("-----------------------------------------")

        # Chave de busca
        user_lookup_key = self._user_lookup_attribute
        logger.info(f"User Lookup Key: {user_lookup_key}")

        # Valor de busca
        user_lookup_value = None
        try:
            # Valor do atributo customizado configurado
            user_lookup_value = self._get_attribute_value(
                user_lookup_key, attributes, attribute_mapping
            )
        except Exception as e:
            logger.error("Failed to extract user identifier.")
            logger.error(e)
            return user_lookup_key, None

        logger.info(
            f"User Lookup Value: {user_lookup_value} Type: {type(user_lookup_value)}"
        )
        if (
            user_lookup_value is None
            or user_lookup_value == "None"
            or user_lookup_value == ""
        ):
            logger.error("No identifier to search in COmanager.")
            return False

        # Consulta o COmanage; se houver registro, o usuário pode prosseguir com o login.
        # Sem registro, o login é interrompido. Na LIneA assume-se registro no COmanage
        # inclusive para usuários de outras instituições.
        try:
            # Utiliza o identificador de usuario do SAML (eppn)
            # para fazer uma consulta ao COmanage do LIneA
            # e descobrir UID do LDAP para este usuario.
            eppn = user_lookup_value

            logger.info("Retriving ldap uid from COmanage.")
            ldap_uid = self.comanage.get_ldap_uid(identifier=eppn)
            logger.info(f"LDAP UID: {ldap_uid}")

            return True

        except Exception as e:
            logger.error(e)
            logger.error("Credentials not found in COmanage.")
            return False

    def user_can_authenticate(self, user) -> bool:
        """
        Rejeita usuários com is_active=False. Modelos sem esse atributo são aceitos.
        """
        is_active = getattr(user, "is_active", None)
        return is_active or is_active is None

    def save_user(self, user, *args, **kwargs):
        user = super().save_user(user, *args, **kwargs)
        # Sincroniza grupos do usuário
        self.setup_groups(user)
        return user

    def setup_groups(self, user):
        logger.info("Setup User Groups")

        # Grupo saml2 para marcar login via djangosaml2
        groups = ["saml2"]

        # Recupera os grupos do usuário no COmanage
        try:
            logger.info("Retriving User Groups from COmanage.")
            personid = self.comanage.get_co_person_id(identifier=self.eppn)
            cogroups = self.comanage.get_groups(personid)

            for group in cogroups:
                groups.append(group["Name"])

        except Exception as e:
            msg = f"Failed on retrive groups from COmanage. Error: {e}"
            logger.error(msg)

        # Remove o usuário dos grupos que não vieram do COmanage
        for group in user.groups.all():
            if group.name not in groups:
                group.user_set.remove(user)
                logger.info(f"User has been removed from the group {group.name}")

        # Adiciona o usuário aos grupos retornados pelo COmanage / SAML
        for g in groups:
            group, created = Group.objects.get_or_create(name=g)
            user.groups.add(group)

        logger.info("User has been added to the following groups")
        logger.info(f"Groups: {groups}")

        return user
