"""mmb_pf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import (  # pylint: disable = unused-import
    handler403,
    handler404,
    handler500,
)
from django.contrib import admin
from django.contrib.auth import views as accounts
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView
from rest_framework import routers

import addrbook.views_api as addrbook_views_api
from addrbook.views import addrbook_list
from administration import views_api as administration_views_api

from . import views as mmb_pf_views
from . import views_api as mmb_pf_views_api
from .settings import MMB_PF_VERSION

favicon_view = RedirectView.as_view(url="/static/favicon.ico", permanent=True)

admin.site.site_header = f"Портал администрирования ММБ ПФ ({MMB_PF_VERSION})"
admin.site.site_title = "ММБ ПФ"
admin.site.index_title = ""
APIVER = "v1"

# API CUSTOM
api_custom = [
    path(f"api/{APIVER}/main/menu/", mmb_pf_views_api.get_main_menu, name="main_menu"),
    path(f"api/{APIVER}/main/user_status/", mmb_pf_views_api.get_user_status, name="get_user_status"),
    path(
        f"api/{APIVER}/administration/change_my_password/",
        administration_views_api.change_my_password,
        name="administraion_change_my_password",
    ),
    path(f"api/{APIVER}/administration/status/", administration_views_api.get_system_status, name="get_system_status"),
    path(f"api/{APIVER}/administration/cleanup_db/", administration_views_api.cleanup_db, name="cleanup_db"),
    path(f"api/{APIVER}/addrbook/mmb_map/", addrbook_views_api.mmb_map, name="mmb_map"),
    path(f"api/{APIVER}/addrbook/change_mmb_map/", addrbook_views_api.change_mmb_map, name="change_mmb_map"),
    path(f"api/{APIVER}/addrbook/addrbook_info/", addrbook_views_api.addrbook_info, name="addrbook_info"),
    path(
        f"api/{APIVER}/addrbook/change_addrbook_info/",
        addrbook_views_api.change_addrbook_info,
        name="change_addrbook_info",
    ),
]

# API DRF
router = routers.DefaultRouter()
router.register(f"api/{APIVER}/administration/users", administration_views_api.MMBPFUsersViewSet)
router.register(f"api/{APIVER}/addrbook/streets", addrbook_views_api.StreetsViewSet)
router.register(f"api/{APIVER}/addrbook/customsignes", addrbook_views_api.CustomSignesViewSet)
router.register(
    f"api/{APIVER}/administration/participant_card_actions_journal",
    administration_views_api.ParticipantCardActionsJournalViewSet,
)

urlpatterns = [
    # Main pages
    re_path(r"^favicon\.ico", favicon_view),
    # re_path(r"^$", mmb_pf_views.index, name="index"),
    re_path(r"^$", addrbook_list, name="index_as_addrbook_list"),
    re_path(r"^worklog/$", mmb_pf_views.worklog, name="worklog"),
    # API
    path("", include(router.urls)),
    path("", include(api_custom)),
    # Admin
    re_path(r"^accounts/login/", accounts.LoginView.as_view(), name="login"),
    re_path(r"^accounts/logout/", accounts.LogoutView.as_view(), name="logout"),
    path("admin/", admin.site.urls),
    # APPS
    # Administration
    re_path(r"^administration/", include("administration.urls")),
    # Addrbook
    re_path(r"^addrbook/", include("addrbook.urls")),
]

# err pages
handler403 = mmb_pf_views.error_403
handler404 = mmb_pf_views.error_404
handler500 = mmb_pf_views.error_500
