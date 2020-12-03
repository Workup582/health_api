from social_core.pipeline.partial import partial


@partial
def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    print("require_email >>> strategy", strategy)
    print("require_email >>> details", details)
    print("require_email >>> user", user)
    print("require_email >>> is_new", is_new)
    print("require_email >>> ars", args)
    print("require_email >>> kwargs", kwargs)

    if kwargs.get('ajax') or user and user.email:
        return
    elif is_new and not details.get('email'):
        email = strategy.request_data().get('email')
        if email:
            details['email'] = email
        else:
            current_partial = kwargs.get('current_partial')
            return strategy.redirect('/email?partial_token={0}'.format(current_partial.token))
