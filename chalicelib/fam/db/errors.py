from datetime import datetime
from chalicelib.fam.common import aws
from chalicelib.fam.config import tables

table = aws.get_dynamo_table(tables.TABLE_ERRORS) if tables.TABLE_ERRORS else None


def put(error):
    if not table:
        print(error)
        return

    return table.put_item(
        Item={
            'message': str(error),
            'traceback': error.__traceback__,
            'date': str(datetime.now())
        }
    )
