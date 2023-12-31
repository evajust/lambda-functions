import boto3
import logging
from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)


class Visitor:
    def __init__(self, dyn_resource):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dyn_resource = dyn_resource
        self.table = self.dyn_resource.Table("portfolio_db")

    def add_visitor(self) -> int:
        """
        Increases the visitor counter by one.
        """
        try:
            current_value = self.table.get_item(Key={"id": "view_count"})
            value = current_value["Item"]["value"] + 1
            self.table.put_item(Item={"id": "view_count", "value": value})
            return value
        except ClientError as e:
            logger.error(
                "Failed due to %s: %s",
                e.response["Error"]["Code"],
                e.response["Error"]["Message"],
            )
        except Exception as e:
            print(e)


def lambda_handler(event: dict, context: dict) -> dict:
    dyn_resource = boto3.resource("dynamodb")
    counter = Visitor(dyn_resource)
    value = counter.add_visitor()
    return {"statusCode": 200, "body": value}

lambda_handler({}, {})
