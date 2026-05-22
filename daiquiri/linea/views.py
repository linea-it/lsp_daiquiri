import logging

from django.conf import settings
from django.shortcuts import render


def linea_login(request):
    """Página de login LIneA / Rubin (escolha do IdP)."""

    context = {
        "LINEA_LOGIN_URL": settings.LINEA_LOGIN_URL,
        "RUBIN_LOGIN_URL": settings.RUBIN_LOGIN_URL,
    }

    # Renderiza o template com o contexto (URLs de login por IdP)
    return render(request, "core/linea_login.html", context=context)


def saml2_template_failure(request, exception=None, status=403, **kwargs):
    """Renderiza template simples com mensagem de erro SAML2."""
    logger = logging.getLogger("djangosaml2")
    logger.info("------------------------------------------")
    logger.info("saml2_template_failure()")
    logger.info(f"request: {request}")
    logger.info(f"exception: {exception}")
    logger.info(f"status: {status}")
    logger.info(f"kwargs: {kwargs}")

    idp_name = request.session["idp_name"]
    needs_registration = request.session.get("needs_registration", False)
    user_status = request.session.get("user_status")

    logger.info(f"idp_name: {idp_name} type: {type(idp_name)}")
    logger.info(f"needs_registration: {needs_registration}")
    logger.info(f"user_status: {user_status}")

    # Se o usuário não tem uid LIneA, encaminha para a página de registro
    if needs_registration:

        if idp_name == "rubin_oidc":
            logger.info("Redirecting to Rubin registration page.")
            return render(
                request,
                "djangosaml2/rubin_need_registration.html",
                {"exception": exception},
                status=status,
            )

        logger.info("Redirecting to LIneA registration page.")
        return render(
            request,
            "djangosaml2/linea_need_registration.html",
            {"exception": exception},
            status=status,
        )

    # Se o cadastro ainda não foi aprovado, encaminha para a página de aguardando aprovação
    if user_status in ["PendingApproval", "Pending"]:
        logger.info(
            f"User status is {user_status}. Redirecting to waiting aproval error page."
        )
        return render(
            request,
            "djangosaml2/waiting_approval.html",
            {"exception": exception},
            status=status,
        )

    return render(
        request, "djangosaml2/login_error.html", {"exception": exception}, status=status
    )
