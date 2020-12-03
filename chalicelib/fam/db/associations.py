from .social_auth import SocialAuth
from .users import User


def populate_association(social_auth: SocialAuth = None, user: User = None):
    if not social_auth and not user:
        raise ValueError('At least social auth or user must be passed to populate link')

    if social_auth:
        social_auth.user = User.findOne({'username': social_auth.username})

        if social_auth.user:
            social_auth.user.social_user = social_auth
    else:
        raise NotImplementedError('Cannot find social auth by user')
