# from django.contrib.auth.decorators import permission_required


from django.http import JsonResponse

from administration.models import MainMenu

from .common_services import check_api_request
from .mmb_pf_memcache import get_main_menu_cache, get_user_status_cache


# @permission_required('administration.view_main_menu', raise_exception=True)
@get_main_menu_cache
@check_api_request({"methods": ["GET"]})
def get_main_menu(request):
    """
    TAKE:
    RETURN:
        main menu depends from user rigts
        [{}]
    """
    main_menu = []
    main_menu_qs = None

    values = ["name", "menu_type", "tid", "icon", "items", "permission"]
    main_menu_qs = MainMenu.objects.filter(disabled=False).values(*values).order_by("order")

    for menu_obj in main_menu_qs:
        if menu_obj["permission"] and not request.user.has_perm(menu_obj["permission"]):
            continue
        del menu_obj["permission"]
        main_menu.append(menu_obj)

    return JsonResponse(main_menu, safe=False)


# @permission_required('administration.view_main_menu', raise_exception=True)
@get_user_status_cache
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

    return JsonResponse(result)
