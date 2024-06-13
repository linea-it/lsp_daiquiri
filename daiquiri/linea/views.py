from django.conf import settings
from django.shortcuts import render


def linea_login(request):
    """View function for home page of site."""

    context = {
        "AUTH_SAML2_LOGIN_URL_CAFE": settings.AUTH_SAML2_LOGIN_URL_CAFE,
        "AUTH_SAML2_LOGIN_URL_CILOGON": settings.AUTH_SAML2_LOGIN_URL_CILOGON,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, "core/linea_login.html", context=context)
