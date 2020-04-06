import logging
from typing import Dict

from django.http import HttpRequest

logger = logging.getLogger(__name__)


class FeatureFlagProvider:
    def is_feature_enabled(self, feature_name: str, user_id: str = None, attributes: Dict = None):
        raise NotImplementedError("You must override FeatureFlagProvider.is_feature_enabled()")


def _attributes_from_request(request: HttpRequest) -> Dict:
    if not request:
        return dict()
    attributes = dict()
    try:
        attributes["is_staff"] = request.user.is_staff
        return attributes
    except Exception:
        logger.exception(
            "Unexpected exception while trying to parse http-request for feature-attributes."
        )
        return dict()


def is_feature_enabled(feature_name: str, request: HttpRequest) -> bool:
    from django.conf import settings
    is_enabled = False
    attributes = _attributes_from_request(request)
    try:
        is_enabled = settings.FEATURE_FLAG_PROVIDER.is_feature_enabled(
            feature_name=feature_name, user_id="dontcare", attributes=attributes
        )
        logger.info(f"Feature '{feature_name}' is enabled={is_enabled}")
    except Exception:
        logger.exception(f"Exception while trying to check feature-flag state for '{feature_name}'")
    return is_enabled
