from resources.health_check import HealthCheck
from resources.hello import HelloWorld
# from resources.iapi import iapi_resources
from resources.auth import auth_api
from resources.check_keyword import CheckResource
from resources.admin import admin_api
from resources.analytics import analytics_api
from resources.metadata import metadata_api
from resources.score import ScoreResource
from resources.output_list import OutputListResource
from resources.outut_list_by_timestamp import OutputListByTimestampResource
from resources.enable_crawl_flag import EnableCrawlFlagResource
from resources.ip_logger import IpLoggerResource
api_resources = {
    '/hello': HelloWorld,
    '/common/health_check': HealthCheck,
    '/score': ScoreResource,
    '/output_list': OutputListResource,
    '/enable_crawl_flag': EnableCrawlFlagResource,
    '/check_keyword':CheckResource,
    '/output_list/<int:timestamp>':OutputListByTimestampResource,
    '/ip':IpLoggerResource,
    # **{f'/iapi{k}': val for k, val in iapi_resources.items()},
    **{f'/auth{k}': val for k, val in auth_api.items()},
    **{f'/admin{k}': val for k, val in admin_api.items()},
    **{f'/analytics{k}': val for k, val in analytics_api.items()},
    **{f'/metadata{k}': val for k, val in metadata_api.items()},
}

