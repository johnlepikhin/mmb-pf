# from django.contrib.auth.decorators import permission_required
import shutil

from django.http import JsonResponse

from administration.models import MainMenu, SystemSettings
from mmb_pf.settings import BASE_DIR


# @permission_required('administration.view_main_menu', raise_exception=True)
# @get_main_menu_cache
def get_main_menu(request, ic="0"):
    """
    TAKE:
    RETURN:
        main menu depends from user rigts
        [{}]
    """
    main_menu = []
    main_menu_qs = None

    if request.method != "GET":
        return JsonResponse({"msg": "Некорректный метод запроса, разрешён только GET"}, status=405, safe=False)

    values = ["name", "menu_type", "tid", "icon", "items", "permission"]
    main_menu_qs = MainMenu.objects.filter(disabled=False).values(*values).order_by("order")

    for menu_obj in main_menu_qs:
        if menu_obj["permission"] and not request.user.has_perm(menu_obj["permission"]):
            continue
        del menu_obj["permission"]
        main_menu.append(menu_obj)

    return JsonResponse(main_menu, safe=False)


# @permission_required('administration.view_main_menu', raise_exception=True)
# @get_user_status_cache
def get_user_status(request):
    """
    TAKE:
    RETURN:
        status of user
    """
    result = {
        "username": request.user.username,
        "is_staff": request.user.is_staff,
        "is_superuser": request.user.is_superuser,
        "groups": [],
    }
    for group in request.user.groups.all():
        result["groups"].append(group.name)

    return JsonResponse(result, safe=False)


# @permission_required('administration.view_main_menu', raise_exception=True)
# @get_system_status_cache
def get_system_status(request):
    """
    TAKE:
    RETURN:
        status of system
    """
    result = {
        "cfg": {
            "refresh_time": SystemSettings.objects.get_option(name="main_page_info_refresh_time", default=3600),
        },
        "disk": {"total": 0, "used": 0, "free": 0},
    }

    if request.method != "GET":
        return JsonResponse({"msg": "Некорректный метод запроса, разрешён только GET"}, status=405, safe=False)

    # DISK
    total, used, free = shutil.disk_usage(BASE_DIR)
    result["disk"]["total"] = total
    result["disk"]["used"] = used
    result["disk"]["free"] = free

    return JsonResponse(result, safe=False)
