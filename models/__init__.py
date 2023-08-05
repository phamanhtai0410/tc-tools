# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""

from config import Config
from connect import connect_db, redis_cluster
from lib import DaoModel

__models__ = ['UsersModel', 'SessionsModel']

UsersModel = DaoModel(col=connect_db.db.users, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)
SessionsModel = DaoModel(col=connect_db.db.sessions, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)

VerticalModel = DaoModel(col=connect_db.db.vertical, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)
VerticalKeywordGroupModel = DaoModel(col=connect_db.db.vertical_keyword_group, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)
RelevantGroupModel = DaoModel(col=connect_db.db.relevant_group, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)
FollowerGroupModel = DaoModel(col=connect_db.db.follower_group, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)
AnalyticsModel = DaoModel(col=connect_db.db.analytics, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)
AnalyticsLogsModel = DaoModel(col=connect_db.db.analytics_logs, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)
CrawlerTasksModel = DaoModel(col=connect_db.db.crawler_tasks, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)

TweetsFilteredModel = DaoModel(col=connect_db.db.tweets_filtered, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)
AccountsFilteredModel = DaoModel(col=connect_db.db.accounts_filtered, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)
AccountsFilteredDetailModel = DaoModel(col=connect_db.db.accounts_filtered_detail, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)
AnalyticsResultsModel = DaoModel(col=connect_db.db.analytics_results, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)
KeywordSearchLinkModel = DaoModel(col=connect_db.db.keyword_search_link, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)
FollowWatchModel = DaoModel(col=connect_db.db.follow_watch, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)
FavouriteAccountModel = DaoModel(col=connect_db.db.favourite_account, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)
GlobalSettingModel = DaoModel(col=connect_db.db.global_setting, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)
ExcludeAccountModel = DaoModel(col=connect_db.db.exclude_account, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)
OutputListModel = DaoModel(col=connect_db.db.output_results, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)

IpLogsModel = DaoModel(col=connect_db.db.ip_logs, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)