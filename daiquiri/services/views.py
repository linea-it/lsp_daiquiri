from django.shortcuts import render


SERVICE_PAGES = [
    {"slug": "overview", "label": "Overview", "url_name": "overview"},
    {
        "slug": "query-interface",
        "label": "Query interface",
        "url_name": "query_interface",
    },
    {
        "slug": "direct-download",
        "label": "Download",
        "url_name": "direct_download",
    },
    {
        "slug": "scripted-access",
        "label": "Scripted access",
        "url_name": "scripted_access",
    },
    {
        "slug": "adql-postgresql",
        "label": "ADQL, PostgreSQL",
        "url_name": "adql_postgresql",
    },
]


def render_service_page(request, template_name, current_page, page_title):
    context = {
        "service_pages": SERVICE_PAGES,
        "current_service_page": current_page,
        "page_title": page_title,
    }
    return render(request, template_name, context=context)


def overview(request):
    return render_service_page(
        request,
        "services/overview.html",
        current_page="overview",
        page_title="Services at LIneA",
    )


def query_interface(request):
    return render_service_page(
        request,
        "services/query_interface.html",
        current_page="query-interface",
        page_title="Query interface",
    )


def direct_download(request):
    return render_service_page(
        request,
        "services/direct_download.html",
        current_page="direct-download",
        page_title="Direct download",
    )


def scripted_access(request):
    return render_service_page(
        request,
        "services/scripted_access.html",
        current_page="scripted-access",
        page_title="Scripted access",
    )


def adql_postgresql(request):
    return render_service_page(
        request,
        "services/adql_postgresql.html",
        current_page="adql-postgresql",
        page_title="ADQL and PostgreSQL",
    )