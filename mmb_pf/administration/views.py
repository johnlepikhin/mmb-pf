from django.contrib.auth.decorators import permission_required
from django.shortcuts import render


@permission_required("administration.change_my_password", raise_exception=True)
def change_my_password(request):
    return render(
        request,
        "administration/change_my_password.html",
        {},
    )
