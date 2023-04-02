from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from addrbook.models import Teams
from administration.models import MMBPFUsers, SystemSettings

from .settings import INSTANCE_PREF


def get_system_status_cache(func):
    """
    DECORATOR !
    @get_system_status_cache
    def method():

    Decorator for caching system status result
    RETURN cached object for user group
    """

    def system_status_cache(self, **kwargs):
        group_id = "0"
        try:
            # if user included in several groups - will concat them ids
            group_id = "".join(map(str, self.user.groups.all().values_list("id", flat=True)))
        except Exception:
            # do not fail if user without groups or auth system is off
            pass

        cache_name = f"{INSTANCE_PREF}-system_status_cache_{group_id}"
        cache_data = cache.get(cache_name)
        if not cache_data:
            cache_data = func(self, **kwargs)
            cache.set(
                cache_name,
                cache_data,
                SystemSettings.objects.get_option(name="main_menu_cache_ttl", default=3600),
            )

        return cache_data

    return system_status_cache


def get_main_menu_cache(func):
    """
    DECORATOR !
    @get_main_menu_cache
    def method():

    Decorator for caching main menu result
    RETURN cached object for user group
    """

    def main_menu_cache(self, **kwargs):
        group_id = "0"
        try:
            # if user included in several groups - will concat them ids
            group_id = "".join(map(str, self.user.groups.all().values_list("id", flat=True)))
        except Exception:
            # do not fail if user without groups or auth system is off
            pass

        cache_name = f"{INSTANCE_PREF}-main_menu_cache_{group_id}"
        cache_data = cache.get(cache_name)
        if not cache_data:
            cache_data = func(self, **kwargs)
            cache.set(
                cache_name,
                cache_data,
                SystemSettings.objects.get_option(name="main_menu_cache_ttl", default=3600),
            )

        return cache_data

    return main_menu_cache


def get_user_status_cache(func):
    """
    DECORATOR !
    @get_user_status_cache
    def method():

    Decorator for caching user status result
    RETURN cached object for user status
    """

    def user_status_cache(self, **kwargs):
        user_id = self.user.id

        cache_name = f"{INSTANCE_PREF}-user_status_cache_{user_id}"
        cache_data = cache.get(cache_name)
        if not cache_data:
            cache_data = func(self, **kwargs)
            cache.set(
                cache_name,
                cache_data,
                SystemSettings.objects.get_option(name="user_status_cache_ttl", default=3600),
            )

        return cache_data

    return user_status_cache


@receiver(post_save, sender=MMBPFUsers)
@receiver(post_save, sender=Teams)
def clear_addrbook_cache(sender, instance, **kwargs):
    cache_name = f"{INSTANCE_PREF}-addrbook_cache"
    cache.delete(cache_name)
