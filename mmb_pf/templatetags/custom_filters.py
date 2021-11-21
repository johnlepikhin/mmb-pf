import re

from django import template
from django.conf import settings

register = template.Library()


@register.filter(name="get_mmb_pf_version")
def get_mmb_pf_version(version):
    return settings.MMB_PF_VERSION


# change next if it count to accounts/logout
# otherwise it will be login and logout immediately
@register.filter(name="check_next")
def check_next(next):
    returned_next = "/"
    try:
        if not re.search(r"accounts|admin\/logout", next):
            returned_next = next
    except:
        pass
    return returned_next
