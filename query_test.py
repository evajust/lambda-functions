#!/usr/bin/python3

import boto3
import logging


logger = logging.getLogger(__name__)


class Visitor:
    def __init__(self, dyn_resource):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dyn_resource = dyn_resource
        self.table = self.dyn_resource.Table('test1')


    def add_visitor(self):
        """
        Increases the visitor counter by one.
        """
        try:
            response = self.table.put_item(Item={'id': 'visitor_count',
                                                 'value': 1})
            print(response)
        except Exception as e:
            logger.error(
                    "Failed due to %s: %s",
                    e.response['Error']['Code'],
                    e.response['Error']['Message'])


def main():
    dyn_resource = boto3.resource('dynamodb')
    counter = Visitor(dyn_resource)
    counter.add_visitor()


if '__main__' in __name__:
    main()
