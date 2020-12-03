import typing
from pydantic import BaseModel

from chalicelib.fam.common import aws
from chalicelib.fam.config import tables
from . import base

table = aws.get_dynamo_table(tables.TABLE_SOCIAL_AUTH)


class SocialAuth(BaseModel, base.DynamoModel):
    uid: str
    provider: str
    extra_data: dict = None
    username: str = None
    user: typing.Any = None

    def __repr__(self):
        user_repr = f'<User username={self.user.username}>' if self.user else 'None'

        return (
            f'<SocialAuth uid="{self.uid}" provider="{self.provider}" extra_data="{self.extra_data}" ' +
            f'username="{self.username}" user="{user_repr}">'
        )

    @classmethod
    def get_table(cls):
        return table

    def get_key(self):
        return {'uid': self.uid, 'provider': self.provider}

    def to_dict(self, create=False, update=False):
        result = {}

        if self.uid and create:
            result['uid'] = self.uid

        if self.provider and create:
            result['provider'] = self.provider

        if self.extra_data is not None:
            result['extra_data'] = self.extra_data

        if self.username is not None:
            result['username'] = self.username

        return result

    def set_extra_data(self, data):
        self.extra_data = data
        self.update()

        return self

    @classmethod
    def find_by_pk(cls, uid: str, provider: str):
        return cls.findOne({'uid': uid, 'provider': provider})
