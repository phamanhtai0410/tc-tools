from resources.analytics.vertical import AnalyticsVerticalResource
from resources.analytics.vertical_result import AnalyticsVerticalResultResource
from resources.analytics.vertical_run import AnalyticsVerticalRunResource
from resources.analytics.vertical_logs import AnalyticsVerticalLogsResource
from resources.analytics.vertical_by_id import AnalyticsVerticalByIdResource
from resources.analytics.vertical_result_export import AnalyticsVerticalResultExportResource
from resources.analytics.accounts_filtered import AccountsFilteredResource
from resources.analytics.keyword_url import KeywordURLResource
from resources.analytics.friendship import AccountFriendShipResource
from resources.analytics.account_profile_link import AccountProfileLinkResource
from resources.analytics.follower_you_follow import FollowerYouFollowLinkResource


analytics_api = {
    '/vertical': AnalyticsVerticalResource,
    '/vertical/run': AnalyticsVerticalLogsResource,
    '/vertical/<string:analytics_vertical_id>': AnalyticsVerticalByIdResource,
    '/vertical/run/<string:analytics_vertical_id>': AnalyticsVerticalRunResource,
    '/vertical/result': AnalyticsVerticalResultResource,
    '/vertical/result/export': AnalyticsVerticalResultExportResource,
    '/vertical/accounts_filtered': AccountsFilteredResource,
    '/vertical/keyword_url': KeywordURLResource,
    '/vertical/account_friendship': AccountFriendShipResource,
    '/vertical/account_profile_link': AccountProfileLinkResource,
    '/vertical/follower_you_follow': FollowerYouFollowLinkResource,
}