"""
This file contains helpers related to DynamoDB.
"""

import decimal
import json
import uuid


# Encoder to handle numbers properly
class _DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def get_dynamo_table_item(table):
    """
    :param table: dynamodb table
    :return: DynamoTableItem with preconfigured table
    """
    DynamoTableItem.table = table
    return DynamoTableItem


class DynamoTableItem:
    """
    Wrapper Class for all Interactions with DynamoDB items.
    every items has a uuid which is also the partition key in the table.
    """
    table = None

    def __init__(self, data=None):

        self.data = data

    def __getitem__(self, item):
        return self.data.get(item)

    @classmethod
    def list_all(cls):
        scan_kwargs = {}
        done = False
        start_key = None
        items = []
        while not done:
            if start_key:
                scan_kwargs['ExclusiveStartKey'] = start_key
            response = cls.table.scan(**scan_kwargs)
            items += response.get('Items', [])
            start_key = response.get('LastEvaluatedKey', None)
            done = start_key is None
        return json.loads(json.dumps(items, cls=_DecimalEncoder))

    def create(self):
        if "uuid" in self.data:
            raise KeyError("if uuid is present, the data can not be created a second time")
        self.data["uuid"] = str(uuid.uuid4())
        response = self.table.put_item(
            Item=self.data
        )
        return json.loads(json.dumps(response, cls=_DecimalEncoder))

    def update(self):
        if "uuid" not in self.data:
            raise KeyError("if uuid is not present, the data can not be updated. Create the data at first")
        pass

    def update_sshtunnel(self, url):
        """
        updates item with ssh_url = url
        :param url:
        :return:
        """
        if "uuid" not in self.data:
            raise KeyError("if uuid is not present, the data can not be updated. Create the data at first")
        response = self.table.update_item(
            Key={
                'uuid': self.data["uuid"],
            },
            UpdateExpression="set ssh_url=:s",
            ExpressionAttributeValues={
                ':s': url
            },
            ReturnValues="UPDATED_NEW"
        )
        return response

    def update_request_check(self, should_open, customer_id):
        """
       updates item with is_requested = should_open
       :param should_open: if the connection requests the current item to be opened, it is True, False otherwise
        :return:
        """
        if "uuid" not in self.data:
            raise KeyError("if uuid is not present, the data can not be updated. Create the data at first")
        response = self.table.update_item(
            Key={
                'uuid': self.data["uuid"],
            },
            UpdateExpression="set is_requested=:s, customer_id=:t ",
            ExpressionAttributeValues={
                ':s': should_open,
                ':t': customer_id
            },
            ReturnValues="UPDATED_NEW"
        )
        return response

    def delete(self):

        response = self.table.delete_item(Key={"uuid": self.data["uuid"]})
        return response

    def get(self):
        if "uuid" not in self.data:
            raise KeyError("if uuid is not present, the data can not be updated. Create the data at first")
        item = self.table.get_item(Key={"uuid": self.data["uuid"]})["Item"]
        for k, v in item.items():
            self.data[k] = v
        return item
