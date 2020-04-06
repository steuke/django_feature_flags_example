import logging
from typing import Dict

from django.conf import settings
from optimizely import optimizely
from optimizely.optimizely import Optimizely

from feature_flags.providers import FeatureFlagProvider

logger = logging.getLogger(__name__)


class OptimizelyProvider(FeatureFlagProvider):
    _optimizely_client: Optimizely = None

    def __init__(self, sdk_key=None):
        if not sdk_key:
            raise ValueError(
                "You must supply a valid Optimizely SDK-key. Did you remember to set settings.OPTIMIZELY_SDK_KEY?")
        logger.info(f"Initializing Optimizely feature flag client.")
        try:
            self._optimizely_client = optimizely.Optimizely(sdk_key=sdk_key)
            # You can change the default-setting like this:
            # self._optimizely_client.config_manager.set_blocking_timeout(20)
            self._optimizely_client.config_manager.set_update_interval(settings.OPTIMIZELY_UPDATE_INTERVAL_SECONDS)
        except Exception:
            logger.exception("Unexpected failure when trying to initialize Optimizely feature flag client.")

    def is_feature_enabled(self, feature_name: str, user_id: str = None, attributes: Dict = None):
        return self._optimizely_client.is_feature_enabled(feature_key=feature_name, user_id=user_id,
                                                          attributes=attributes)
