from django.contrib.auth.decorators import permission_required
from django.shortcuts import render


@permission_required("administration.change_self_password", raise_exception=True)
def change_self_password(request):
    return render(
        request,
        "administration/change_self_password.html",
        {},
    )


@permission_required("administration.view_administration", raise_exception=True)
def database_operations(request):
    return render(
        request,
        "administration/database_operations.html",
        {},
    )


@permission_required("administration.view_administration", raise_exception=True)
def participant_card_actions_journal(request):
    return render(
        request,
        "administration/participant_card_actions_journal.html",
        {},
    )
