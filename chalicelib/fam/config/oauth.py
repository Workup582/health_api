SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/auth/logged-in/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/auth/login-error/'
SOCIAL_AUTH_LOGIN_URL = '/auth/login-url/'

SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/auth/new-users-redirect-url/'
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/auth/new-association-redirect-url/'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/auth/account-disconnected-redirect-url/'
SOCIAL_AUTH_INACTIVE_USER_URL = '/auth/inactive-user/'

# SOCIAL_AUTH_USER_MODEL = 'chalicelib.fam.db.users.User'

SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.linkedin.LinkedinOAuth2',
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    # 'chalicelib.fam.common.pipeline.require_email',
    'social_core.pipeline.mail.mail_validation',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    # 'social_core.pipeline.debug.debug'
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '144880288954-8v1u8qac75gink8f8mtled1rhoqcet4r.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'TKSpcMe_3RoLLNNfDic447ho'

SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = '86j75o0p2o8ots'
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = 'JeKDjugiZKbxRr5P'
SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA = [('id', 'id'), ('firstName', 'first_name'), ('lastName', 'last_name'),
                                          ('emailAddress', 'email_address')]
SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ['r_liteprofile', 'r_emailaddress']
SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = ['emailAddress']
