import re

from django.contrib.auth.decorators import permission_required
from django.http.response import JsonResponse
from django.shortcuts import render

# from essystem.drf_api import BaseModelPermissions


@permission_required("administration.view_main_page", raise_exception=True)
def index(request):
    return render(
        request,
        "index.html",
        {},
    )


@permission_required("administration.view_main_page", raise_exception=True)
def worklog(request):
    return render(
        request,
        "worklog.html",
        {},
    )


def error_403(request, exception):
    if re.match(r"^\/api\/v", request.path):
        return JsonResponse({"msg": "У вас нет прав для выполнения данного запроса"}, status=403, safe=False)
    else:
        return render(
            request,
            "error403.html",
            {},
            status=403,
        )


def error_404(request, exception):
    if re.match(r"^\/api\/v", request.path):
        return JsonResponse({"msg": "Данные не найдены"}, status=404, safe=False)
    else:
        return render(
            request,
            "error404.html",
            {},
            status=404,
        )


def error_500(request):
    if re.match(r"^\/api\/v", request.path):
        return JsonResponse({"msg": "Внутри системы что-то пошло не так"}, status=500, safe=False)
    else:
        return render(
            request,
            "error500.html",
            {},
            status=500,
        )
