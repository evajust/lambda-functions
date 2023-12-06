#!/usr/bin/env python3

import boto3
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


def notify_success(event: dict) -> None:
    client = boto3.client("codepipeline")
    client.put_job_success_result(jobId=event["CodePipeline.job"]["id"])


def notify_failure(event: dict) -> None:
    client = boto3.client("codepipeline")
    failure_details = {
        "type": "ConfigurationError",
        "message": "URL not found",
    }
    client.put_job_filure_result(
        jobId=event["CodePipeline.job"]["id"], failureDetails=failure_details
    )


def lambda_handler(event: dict, context: dict) -> None:
    client = boto3.client("cloudfront")

    print("event: " + str(event))
    caller_reference = datetime.now().strftime("%Y%m%d%H%M%S%f")
    url = event["CodePipeline.job"]["data"]["actionConfiguration"][
        "configuration"
    ]["UserParameters"]
    invalidation_path = {
        "Paths": {"Quantity": 1, "Items": ["/*"]},
        "CallerReference": caller_reference,
    }

    response = client.list_distributions()
    distribution_list = response["DistributionList"]["Items"]
    for distribution in distribution_list:
        if url in distribution["Aliases"]["Items"]:
            client.create_invalidation(
                DistributionId=distribution["Id"],
                InvalidationBatch=invalidation_path,
            )
            notify_success(event)
