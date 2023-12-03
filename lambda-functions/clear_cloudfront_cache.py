#!/usr/bin/env python3

import boto3
import sys
from datetime import datetime

client = boto3.client('cloudfront')

caller_reference = datetime.now().strftime('%Y%m%d%H%M%S%f')
url = sys.argv[1]
invalidation_path = {'Paths': {
                         'Quantity': 1,
                         'Items': ['/*']
                         },
                     'CallerReference': caller_reference
                     }

distribution_list = client.list_distributions()['DistributionList']['Items']
for distribution in distribution_list:
    if url in distribution['Aliases']['Items']:
        response = client.create_invalidation(
                DistributionId=distribution['Id'],
                InvalidationBatch=invalidation_path)
