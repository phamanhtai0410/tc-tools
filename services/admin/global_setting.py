# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from pydash import get
import bson
from config import Config

from exceptions.follower_group import FollowerGroupNameExistedEx, FollowerGroupNotExistedEx
from exceptions.request import NotValidObjectIdEx
from lib.utils import dt_utcnow
from models import FollowerGroupModel, GlobalSettingModel
from slugify import slugify


class AdminGlobalSettingService:

    @classmethod
    def get(cls):

        _result = GlobalSettingModel.find_one({
            'key': Config.DEFAULT_GLOBAL_SETTING_KEY
        })

        return _result

    @classmethod
    def update(cls, login_info, form_data):

        _result = GlobalSettingModel.update_one({
            'key': Config.DEFAULT_GLOBAL_SETTING_KEY
        }, {
            **form_data,
            'updated_by': get(login_info, 'user.username')
        })

        return {}
