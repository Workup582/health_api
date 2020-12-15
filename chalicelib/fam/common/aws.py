import boto3

from chalicelib.fam import config


def get_session():
    if not boto3.DEFAULT_SESSION:
        if config.ENV == 'development' or config.ENV == 'local':
            boto3.setup_default_session(
                aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
                region_name=config.AWS_REGION)
        else:
            boto3.setup_default_session()

    return boto3.DEFAULT_SESSION


def get_dynamo_table(table_name):
    return boto3.resource('dynamodb').Table(table_name)
