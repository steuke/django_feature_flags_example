from typing import List

from django.http import HttpRequest

from feature_flags.providers import is_feature_enabled

_features: List["Feature"] = []


def _register_feature(feature):
    _features.append(feature)


def _is_feature_enabled(feature: str, request: HttpRequest) -> bool:
    is_enabled = is_feature_enabled(feature_name=feature, request=request)
    return is_enabled


class Feature:
    def __init__(self, name: str):
        self.name: str = name
        _register_feature(self)

    def is_enabled(self, request: HttpRequest = None) -> bool:
        return _is_feature_enabled(self.name, request=request)

    def __repr__(self):
        return f"({self.name}, {self.is_enabled()})"


class UnknownFeature(Exception):
    pass
