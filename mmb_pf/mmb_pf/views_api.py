# from django.contrib.auth.decorators import permission_required


from django.http import JsonResponse

import mmb_pf.mmb_pf_memcache as memcache
from administration.models import MainMenu


# @permission_required('administration.view_main_menu', raise_exception=True)
@memcache.get_main_menu_cache
def get_main_menu(request):
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
@memcache.get_user_status_cache
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
