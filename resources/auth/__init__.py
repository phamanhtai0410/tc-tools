

from resources.auth.login import AuthLoginResource
from resources.auth.me import AuthMeResource


auth_api = {
    '/login': AuthLoginResource,
    '/me': AuthMeResource,
}