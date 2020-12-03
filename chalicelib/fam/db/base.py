from boto3.dynamodb.conditions import Key

from .errors import put as log_error


class DynamoModel:
    @classmethod
    def get_table(cls):
        raise NotImplementedError('get_table must be implemented in derived class')

    def get_key(self):
        raise NotImplementedError('get_key must be implemented in derived class')

    def to_dict(self, create=False, update=False):
        raise NotImplementedError('get_key must be implemented in derived class')

    @classmethod
    def to_model(cls, **kwargs):
        return cls(**kwargs)

    @classmethod
    def findOne(cls, key):
        try:
            obj = cls.get_table().get_item(Key=key)
            item = obj.get('Item')

            if not item:
                raise ValueError(f'Not found: {str(key)}: {str(obj)}')

            return cls.to_model(**item)
        except Exception as ex:
            log_error(ex)

        return None

    def create(self, condition=None, attributes=None):
        args = {'Item': self.to_dict(create=True)}

        if condition:
            args['ConditionExpression'] = condition

        if attributes:
            args['ExpressionAttributeValues'] = attributes

        self.get_table().put_item(**args)

        return self

    @classmethod
    def delete(cls, key):
        return cls.get_table().delete_item(Key=key)

    @classmethod
    def query(cls, **kwargs):
        try:
            key = None

            for sub_key, value in kwargs.items():
                if not key:
                    key = Key(sub_key).eq(value)
                else:
                    key = key & Key(sub_key).eq(value)

            obj = cls.get_table().query(KeyConditionExpression=key)
            results = obj.get('Items')

            if not results:
                raise ValueError(f'Not found: {str(key)}: {str(obj)}')

            return [cls.to_model(**result) for result in results]
        except Exception as ex:
            log_error(ex)

        return None

    @classmethod
    def scan(cls, **kwargs):
        try:
            key = None

            for sub_key, value in kwargs.items():
                if not key:
                    key = Key(sub_key).eq(value)
                else:
                    key = key & Key(sub_key).eq(value)

            obj = cls.get_table().scan(FilterExpression=key)
            results = obj.get('Items')

            if not results:
                raise ValueError(f'Not found: {str(key)}: {str(obj)}')

            return [cls.to_model(**result) for result in results]
        except Exception as ex:
            log_error(ex)

        return None

    def update(self, **kwargs):
        update_expression = []
        update_values = {}

        fields = {**self.to_dict(), **kwargs}

        for index, (field, value) in enumerate(fields.items()):
            update_expression.append(f'{field}=:_{field}')
            update_values[f':_{field}'] = value

            setattr(self, field, value)

        update_expression = 'SET ' + ', '.join(update_expression)

        self.get_table().update_item(
            Key=self.get_key(),
            UpdateExpression=update_expression,
            ExpressionAttributeValues=update_values,
            ReturnValues="UPDATED_NEW"
        )
