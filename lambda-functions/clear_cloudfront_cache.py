#!/usr/bin/env python3

import boto3
import sys
from datetime import datetime
import json
import logging


logger = logging.getLogger(__name__)


def lambda_handler(event, context):
    client = boto3.client('cloudfront')

    print("event: " + str(event))
    print("context: " + str(context))
    caller_reference = datetime.now().strftime('%Y%m%d%H%M%S%f')
    url = sys.argv[1]
    invalidation_path = {'Paths': {
                             'Quantity': 1,
                             'Items': ['/*']
                             },
                         'CallerReference': caller_reference
                         }

    response = client.list_distributions()
    distribution_list = response['DistributionList']['Items']
    for distribution in distribution_list:
        if url in distribution['Aliases']['Items']:
            response = client.create_invalidation(
                    DistributionId=distribution['Id'],
                    InvalidationBatch=invalidation_path)
            return {
                'statusCode': 200,
                'body': json.dumps(response)
            }
