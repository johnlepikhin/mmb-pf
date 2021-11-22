import json
import re

from django.contrib.auth import password_validation, update_session_auth_hash
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse

from .models import MMBPFUsers


@permission_required("administration.change_my_password", raise_exception=True)
def change_my_password(request):
    """
    Current user password changer

    """
    if request.method != "POST":
        return JsonResponse({"msg": "Некорректный метод запроса, только POST"}, status=405, safe=False)

    try:
        request_body = json.loads(request.body)
    except Exception:
        return JsonResponse({"msg": "Некорректное тело запроса, только JSON"}, status=422, safe=False)
    if not request_body:
        return JsonResponse({"msg": "Запрос без параметров для изменения"}, status=422, safe=False)

    # check fields
    fields = {
        "old_password": "re:^.{4,}$",
        "new_password": "re:^.{4,}$",
    }
    for field in request_body:
        if not field in fields:
            return JsonResponse({"msg": f'Поле "{field}" некорректное для данного запроса'}, status=422, safe=False)
        check_type = fields[field]
        if re.match(r"^re:.+", check_type):
            regexp = re.match(r"^re:(.+)$", check_type).group(1)
            if not re.match(regexp, str(request_body[field])):
                return JsonResponse(
                    {"msg": f'Поле "{field}" имеет неверный формат или значение'}, status=422, safe=False
                )

    try:
        user_obj = MMBPFUsers.objects.get(id=request.user.id)
    except:
        return JsonResponse({"msg": "Ошибка запроса базы данных"}, status=422, safe=False)

    # check
    if user_obj.check_password(request_body["old_password"]):
        try:
            password_validation.validate_password(password=request_body["new_password"], user=user_obj)
        except Exception as exc:
            err_str = " ".join(exc)
            return JsonResponse({"msg": f"{err_str}"}, status=422, safe=False)

        user_obj.set_password(request_body["new_password"])
        user_obj.save()
        update_session_auth_hash(request, user_obj)
    else:
        return JsonResponse({"msg": "Введён некорректный текущий пароль"}, status=422, safe=False)

    return JsonResponse({"msg": "Изменения сохранены"}, status=200, safe=False)
