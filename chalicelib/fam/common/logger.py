from functools import wraps
import logging

logger = logging.getLogger('fam')
logger.setLevel(logging.DEBUG)


LOG_FUNCTION_ARGS = True
LOG_FUNCTION_RESULT = True


def log_call(name=None):
    name = f'{name}:: ' if name else ''

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if LOG_FUNCTION_ARGS:
                logger.info(f'{name}{f.__name__}, args: {str(args)}, kwargs: {str(kwargs)}')

            result = f(*args, **kwargs)

            if LOG_FUNCTION_RESULT:
                logger.info(f'{name}{f.__name__}, result: {str(result)}')

            return result
        return wrapper
    return decorator
