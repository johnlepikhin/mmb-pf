from django.core.cache import cache

from administration.models import SystemSettings

from .settings import BASE_DIR

this_instance_pref = str(BASE_DIR).replace("/", "-")


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

        cache_name = f"{this_instance_pref}-system_status_cache_{group_id}"
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

        cache_name = f"{this_instance_pref}-main_menu_cache_{group_id}"
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

        cache_name = f"{this_instance_pref}-user_status_cache_{user_id}"
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


def scheduler_tasks_counter_cache(**kwargs):
    """
    CACHE:
        Name: scheduler_tasks_counter
        Increment its counter every time when called
    TAKE:
        increment_task='', # [OPTIONAL], Increment counter of defined task name

    RETURN:
        return cache data (create new one if not existed)
    """
    known_tasks = ["mail_for_send"]
    if "increment_task" in kwargs and not kwargs["increment_task"] in known_tasks:
        raise ValueError(f"task {kwargs['increment_task']} is unknown")

    cache_name = f"{this_instance_pref}-scheduler_tasks_counter"
    cache_data = cache.get(cache_name)

    if not cache_data:
        cache_data = {}
        for task_name in known_tasks:
            cache_data[task_name] = {
                "count": 0,
            }
    else:
        if "increment_task" in kwargs:
            cache_data[kwargs["increment_task"]]["count"] += 1

    cache.set(cache_name, cache_data)

    return cache_data
