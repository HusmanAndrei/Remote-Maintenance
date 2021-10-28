

def create_table(dynamodb, table_name):
    """
    create table, throws error if already exists
    :param dynamodb:
    :param table_name:
    :return:
    """

    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                "AttributeName": "uuid",
                "KeyType": "HASH"  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "uuid",
                "AttributeType": "S"
            }
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 1,
            "WriteCapacityUnits": 1
        }
    )
    return table

