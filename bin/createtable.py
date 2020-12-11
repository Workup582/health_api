#!/usr/bin/python

import os
import uuid
import json
import argparse

import boto3

USE_UUID = False

TABLES_KEYS = {
    'USERS_TABLE_NAME': {
        'hash_key': 'username'
    },
    'SOCIAL_AUTH_TABLE_NAME': {
        'hash_key': 'uid',
        'range_key': 'provider'
    }
}


def create_table(table_name_prefix, hash_key, range_key=None):
    table_name = f'{table_name_prefix}-{str(uuid.uuid4())}' if USE_UUID else table_name_prefix
    print(f'Creating table {table_name}')
    client = boto3.client('dynamodb', region_name=os.environ['AWS_REGION'])
    key_schema = [{
        'AttributeName': hash_key,
        'KeyType': 'HASH',
    }]
    attribute_definitions = [{
        'AttributeName': hash_key,
        'AttributeType': 'S',
    }]
    if range_key is not None:
        key_schema.append({'AttributeName': range_key, 'KeyType': 'RANGE'})
        attribute_definitions.append({'AttributeName': range_key, 'AttributeType': 'S'})
    client.create_table(TableName=table_name,
                        KeySchema=key_schema,
                        AttributeDefinitions=attribute_definitions,
                        ProvisionedThroughput={
                            'ReadCapacityUnits': 5,
                            'WriteCapacityUnits': 5,
                        })
    waiter = client.get_waiter('table_exists')
    waiter.wait(TableName=table_name, WaiterConfig={'Delay': 1})
    return table_name


def record_as_env_var(key, value, stage):
    with open(os.path.join('.chalice', 'config.json')) as f:
        data = json.load(f)
        data['stages'].setdefault(stage, {}).setdefault('environment_variables', {})[key] = value
    with open(os.path.join('.chalice', 'config.json'), 'w') as f:
        serialized = json.dumps(data, indent=2, separators=(',', ': '))
        f.write(serialized + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--stage', default='dev')
    args = parser.parse_args()

    config = {}
    current_env = {}
    tables = {}

    with open(os.path.join('.chalice', 'config.json')) as f:
        config = json.load(f)
        current_env = config['stages'][args.stage]
        tables = {
            key: value
            for key, value in current_env['environment_variables'].items()
            if key.endswith('_TABLE_NAME')
        }

    for table_env_var, table_name in tables.items():
        tabke_key_config = TABLES_KEYS[table_env_var]
        create_table(table_name, tabke_key_config['hash_key'], tabke_key_config.get('range_key'))


if __name__ == '__main__':
    main()
