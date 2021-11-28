# from django.contrib.auth.decorators import permission_required
from django.shortcuts import render


# @permission_required("addrbook.view_addrbook", raise_exception=True)
def addrbook_list(request):
    return render(
        request,
        "addrbook/addrbook_list.html",
        {},
    )


# @permission_required("addrbook.view_addrbook", raise_exception=True)
def addrbook_info(request):
    return render(
        request,
        "addrbook/addrbook_info.html",
        {},
    )
