import uuid
import traceback
from datetime import datetime
from chalicelib.fam.common import aws
from chalicelib.fam.config import tables

table = aws.get_dynamo_table(tables.TABLE_ERRORS) if tables.TABLE_ERRORS else None


def put(error):
    print(error)

    if not table:
        return

    return table.put_item(
        Item={
            'uid': uuid.uuid4().hex,
            'message': str(error),
            'traceback': traceback.format_tb(error.__traceback__),
            'date': str(datetime.now())
        }
    )
