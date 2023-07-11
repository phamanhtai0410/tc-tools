# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from resources.health_check import HealthCheck
from resources.hello import HelloWorld
# from resources.iapi import iapi_resources
from resources.auth import auth_api
from resources.admin import admin_api
from resources.analytics import analytics_api
from resources.metadata import metadata_api
from resources.score import ScoreResource

api_resources = {
    '/hello': HelloWorld,
    '/common/health_check': HealthCheck,
    '/score': ScoreResource,
    # **{f'/iapi{k}': val for k, val in iapi_resources.items()},
    **{f'/auth{k}': val for k, val in auth_api.items()},
    **{f'/admin{k}': val for k, val in admin_api.items()},
    **{f'/analytics{k}': val for k, val in analytics_api.items()},
    **{f'/metadata{k}': val for k, val in metadata_api.items()},
}
