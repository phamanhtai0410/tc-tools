# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import string
from datetime import timedelta
from connect import redis_cluster

import jwt
import bcrypt
from pydash import get

from config import Config
from connect import web3_providers, redis_cluster
from exceptions.auth import UsernameOrPasswordNotCorrectEx
from lib import BadRequest
from lib.logger import debug
from lib.security import auth_token_key
from lib.utils import random_str, dt_utcnow
from models import SessionsModel, UsersModel


with open("conf/keys/private.key") as f:
    TOKEN_KEY = f.read()


class AuthService:
    @classmethod
    def _gen_nonce(cls):
        return random_str(size=8, chars=string.digits)

    @classmethod
    def _gen_access_token(cls, session: dict) -> str:
        _key = auth_token_key(user=get(session, "user._id"))
        _payload = {
            "payload": session,
            "iat": dt_utcnow(),  # init time
            "exp": dt_utcnow() + timedelta(seconds=Config.TOKEN_EXPIRE_TIME),
        }
        _access_token = jwt.encode(_payload, TOKEN_KEY, algorithm="RS256")

        # save
        redis_cluster.setex(
            name=_key, time=Config.TOKEN_EXPIRE_TIME, value=_access_token
        )

        return _access_token

    @classmethod
    def login(cls, form_data, headers):
        _username = get(form_data, "username").lower()
        _password = get(form_data, "password")

        _device_id = get(headers, "did")
        _xrip = get(headers, "X-Real-Ip")
        _geoip = get(headers, "Cf-Ipcountry")

        _access_token = AuthService.verify_account(
            username=_username,
            password=_password,
            session={"xrip": _xrip, "device_id": _device_id, "geoip": _geoip},
        )

        return {"access_token": _access_token}

    @classmethod
    def verify_account(cls, username, password, session):
        _user = UsersModel.find_one({"username": username})

        if not _user:
            raise UsernameOrPasswordNotCorrectEx

        _check_pwd = bcrypt.checkpw(
            password=password.encode("utf-8"),
            hashed_password=get(_user, "password").encode("utf-8"),
        )

        if not _check_pwd:
            raise UsernameOrPasswordNotCorrectEx

        _session = {
            **session,
            "user": {
                "_id": str(get(_user, "_id")),
                "username": get(_user, "username"),
                "name": get(_user, "name"),
                "roles": get(_user, "roles"),
            },
        }

        _access_token = AuthService._gen_access_token(session=_session)

        SessionsModel.insert_one(
            {
                **_session,
                "access_token": _access_token,
                "created_by": "tc-tools:services:auth:AuthService:verify_account",
            },
            worker=True,
        )

        return _access_token

    @classmethod
    def get_me(cls, login_info):
        _user = get(login_info, "user")

        return _user
