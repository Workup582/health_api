# Pipeline handler data:

## Signature

`def require_email(strategy, details, user=None, is_new=False, *args, **kwargs): ....`

## Arguments

- strategy: `<chalicelib.fam.oauth.strategy.ChaliceStrategy object at 0x7f52233f4f10>`
- details: `{'username': 'nosuchip', 'email': 'nosuchip@gmail.com', 'fullname': 'XXX', 'first_name': 'XXX', 'last_name': 'YYY'}`
- user: `None`
- is_new: `True`
- ars: `()`
- kwargs:

  ```
  {
      'backend': <social_core.backends.google.GoogleOAuth2 object at 0x7f5223413b80>,
      'pipeline_index': 5,
      'current_partial': <social_core.storage.PartialMixin object at 0x7f5223413d60>,
      'response': {
          'access_token': 'XXXX.......XXXX',
          'expires_in': 3599,
          'scope': 'https://www.googleapis.com/auth/userinfo.profile openid https://www.googleapis.com/auth/userinfo.email',
          'token_type': 'Bearer',
          'id_token': 'YYYY......YYYY',

          'sub': '118253614024394073502',
          'name': 'Alex',
          'given_name': 'Alex',
          'picture': 'https://lh3.googleusercontent.com/a-/AOh14GgD-AI9aogc4rtseBOXJQf2GH5xREuAj6PdFScYGg=s96-c',
          'email': 'nosuchip@gmail.com',
          'email_verified': True,
          'locale': 'en-GB'
      },
      'storage': <chalicelib.fam.oauth.storage.DynamoDBStorage object at 0x7f52233f4ee0>,
      'request': {
          'state': 'xxxxx....xxxxx',
          'code': 'yyyyy......yyyyy',
          'scope': 'email profile openid https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
          'authuser': '0',
          'prompt': 'consent'
      },
      'uid': 'nosuchip@gmail.com',
      'social': None,
      'new_association': True,
      'username': 'nosuchip'
  }
  ```
