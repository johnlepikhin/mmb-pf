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


# @permission_required("addrbook.view_addrbook", raise_exception=True)
def participant_card(request, participant_id):
    return render(
        request,
        "addrbook/participant_card.html",
        {
            "participant_id": participant_id,
            "history": request.user.has_perm("administration.view_participantcardactionsjournal"),
        },
    )


# @permission_required("addrbook.view_addrbook", raise_exception=True)
def participant_card_edit(request, participant_id):
    return render(
        request,
        "addrbook/participant_card_edit.html",
        {
            "participant_id": participant_id,
        },
    )
