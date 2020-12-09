from social_core.storage import UserMixin, BaseStorage
from chalicelib.fam.db import users, social_auth, associations
from chalicelib.fam.common.logger import log_call
from botocore.exceptions import ClientError


class DynamoDBUserStorage(UserMixin):
    current_user = None

    @classmethod
    @log_call(name='DynamoDBUserStorage')
    def get_username(cls, user):
        """Return the username for given user"""
        return user.username

    @classmethod
    # @log_call(name='DynamoDBUserStorage')
    def username_max_length(cls):
        """Return the max length for username"""
        return 512

    @classmethod
    @log_call(name='DynamoDBUserStorage')
    def user_model(cls):
        """Return the user model"""
        return users.User

    @classmethod
    @log_call(name='DynamoDBUserStorage')
    def changed(cls, user: users.User):
        """The given user instance is ready to be saved"""
        user.update()

        cls.current_user = user

        return user

    @classmethod
    @log_call(name='DynamoDBUserStorage')
    def user_exists(cls, username: str):
        """
        Return True/False if a User instance exists with the given arguments.
        Arguments are directly passed to filter() manager method.
        """
        user = users.User.find_by_pk(username)
        return bool(user)

    @classmethod
    @log_call(name='DynamoDBUserStorage')
    def create_user(cls, username: str, email: str = None):
        """Create a user with given username and (optional) email"""
        user = users.User(username=username, email=email, password=users.SOCIAL_PASSWORD)
        return user.create()

    @classmethod
    @log_call(name='DynamoDBUserStorage')
    def get_user(cls, pk):
        """Return user instance for given id"""
        return users.User.find_by_pk(pk)

    @classmethod
    @log_call(name='DynamoDBUserStorage')
    def get_social_auth(cls, provider, uid):
        """Return UserSocialAuth for given provider and uid"""
        auth = social_auth.SocialAuth.find_by_pk(uid, provider)

        if auth:
            associations.populate_association(social_auth=auth)
            cls.current_user = auth.user

        return auth

    @classmethod
    @log_call(name='DynamoDBUserStorage')
    def get_social_auth_for_user(cls, user: users.User):
        """Return all the UserSocialAuth instances for given user"""
        auths = social_auth.SocialAuth.query(username=user.username)

        for auth in auths:
            associations.populate_association(social_auth=auth)
            cls.current_user = auth.user

        return auths

    @classmethod
    @log_call(name='DynamoDBUserStorage')
    def create_social_auth(cls, user, uid, provider, **kwargs):
        """Create a UserSocialAuth instance for given user"""
        auth = social_auth.SocialAuth(uid=uid, provider=provider, username=user.username, extra_data=kwargs, user=user)
        auth.create()
        associations.populate_association(social_auth=auth)

        return auth

    @classmethod
    @log_call(name='DynamoDBUserStorage')
    def allowed_to_disconnect(cls, user, backend_name, association_id=None):
        """Return if it's safe to disconnect the social account for the given user"""
        return True

    @classmethod
    @log_call(name='DynamoDBUserStorage')
    def disconnect(cls, name, user, association_id=None):
        """Disconnect the social account for the given user"""
        raise NotImplementedError('Implement in subclass')

    @classmethod
    @log_call(name='DynamoDBUserStorage')
    def get_users_by_email(cls, email):
        """Return users instances for given email address"""
        values = users.User.scan(email=email)
        return values or []


class DynamoDBStorage(BaseStorage):
    user = DynamoDBUserStorage

    @classmethod
    @log_call(name='DynamoDBStorage')
    def is_integrity_error(cls, exception):
        return (
            isinstance(exception, ClientError) and
            getattr(exception, 'response', {}).get('Error', {}).get('Code') == 'ConditionalCheckFailedException'
        )
