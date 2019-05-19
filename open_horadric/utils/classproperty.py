from __future__ import annotations


# noinspection PyPep8Naming
class classproperty(object):
    """
    Source: https://stackoverflow.com/a/3203659
    """

    def __init__(self, get_function):
        self._get_function = get_function

    def __get__(self, owner_self, owner_cls):
        return self._get_function(owner_cls)
