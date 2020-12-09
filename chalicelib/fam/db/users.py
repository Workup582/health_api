import uuid
import typing
from pydantic import BaseModel

from chalicelib.fam import config
from chalicelib.fam.common import aws
from chalicelib.fam.config import tables
from chalicelib.fam.cipher import hash_password, get_current_username, get_query_token
from . import base

table = aws.get_dynamo_table(tables.TABLE_USER)

SOCIAL_PASSWORD = '!'


class AnonymousUser:
    is_authenticated: bool = False

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '<AnonymousUser>'


class User(BaseModel, AnonymousUser, base.DynamoModel):
    username: str
    email: str
    password: str = None
    cleartext_password: str = None
    first_name: str = None
    last_name: str = None
    req_count: int = config.MAX_REQUESTS
    is_active: int = 1
    api_key: str = None

    social_user: typing.Any = None
    is_new: bool = True
    is_authenticated: bool = False

    def __repr__(self):
        return str(self)

    def __str__(self):
        social_repr = f'<SocialUser uid="{self.social_user.uid}">'if self.social_user else 'None'
        return (
            f'<User username="{self.username}" email="{self.email}" password="{self.password}" ' +
            f'cleartext_password="{self.cleartext_password}" first_name="{self.first_name}" ' +
            f'last_name="{self.last_name}" req_count="{self.req_count}" is_active="{self.is_active}" ' +
            f'is_new="{self.is_new}" social_user={social_repr}>'
        )

    @classmethod
    def get_current_user(cls, req):
        username = get_current_username(req)
        return cls.findOne({'username': username})

    @classmethod
    def get_query_user(cls, req):
        api_key = get_query_token(req)

        if not api_key:
            return None

        users = cls.scan(api_key=api_key)

        if not users:
            return None

        return users[0]

    @classmethod
    def get_table(cls):
        return table

    @classmethod
    def to_model(cls, **kwargs):
        return cls(**kwargs, is_new=False)

    def get_key(self):
        return {'username': self.username}

    def to_dict(self, create=False, update=False):
        result = {}

        if self.username and create:
            result['username'] = self.username

        if self.email is not None:
            result['email'] = self.email

        if self.first_name is not None:
            result['first_name'] = self.first_name

        if self.last_name is not None:
            result['last_name'] = self.last_name

        if self.req_count is not None:
            result['req_count'] = self.req_count

        if self.is_active is not None:
            result['is_active'] = self.is_active

        if self.api_key is not None:
            result['api_key'] = self.api_key

        if self.cleartext_password:
            result['password'] = hash_password(self.cleartext_password)
        elif create:
            result['password'] = self.password

        return result

    @classmethod
    def find_by_pk(cls, username: str):
        return cls.findOne({'username': username})

    def create(self, condition=None, attributes=None):
        if not self.api_key:
            self.api_key = uuid.uuid4().hex
            self.req_count = config.MAX_REQUESTS

        super().create(condition, attributes)

        self.cleartext_password = None
        self.is_new = False

        return self

    def update(self, **kwargs):
        super().update(**kwargs)

        self.cleartext_password = None
        self.is_new = False

        return self
