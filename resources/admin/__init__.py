from resources.admin.users import AdminUsersResource
from resources.admin.users_by_id import AdminUsersByIdResource
from resources.admin.vertical_keyword_group import AdminVerticalKeywordGroupResource
from resources.admin.vertical_keyword_group_by_id import AdminVerticalKeywordGroupByIdResource
from resources.admin.follower_group import AdminFollowerGroupResource
from resources.admin.follower_group_by_id import AdminFollowerGroupByIdResource
from resources.admin.follower_watch import AdminFollowerWatchResource
from resources.admin.relevant_group import AdminRelevantResource
from resources.admin.relevant_group_by_id import AdminRelevantGroupByIdResource
from resources.admin.vertical import AdminVerticalResource
from resources.admin.vertical_by_id import AdminVerticalByIddResource
from resources.admin.global_setting import AdminGlobalSettingResource
from resources.admin.favourite_account import AdminFavouriteAccountResource


admin_api = {
    '/users': AdminUsersResource,
    '/users/<string:user_id>': AdminUsersByIdResource,
    '/vertical_keyword_group': AdminVerticalKeywordGroupResource,
    '/vertical_keyword_group/<string:vertical_keyword_group_id>': AdminVerticalKeywordGroupByIdResource,
    '/follower_group': AdminFollowerGroupResource,
    '/follower_group/<string:follower_group_id>': AdminFollowerGroupByIdResource,
    '/follower_watch': AdminFollowerWatchResource,
    '/favourite_account': AdminFavouriteAccountResource,
    '/relevant_group': AdminRelevantResource,
    '/relevant_group/<string:relevant_group_id>': AdminRelevantGroupByIdResource,
    '/vertical': AdminVerticalResource,
    '/vertical/<string:vertical_id>': AdminVerticalByIddResource,
    '/global_setting': AdminGlobalSettingResource,
}
