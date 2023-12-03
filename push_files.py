#!/usr/bin/env python3

import boto3
from zipfile import ZipFile
import pathlib
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor


def push_lambda_files(file):
    function_name = file.name.split('.')[0]
    in_mem_archive = BytesIO()
    with ZipFile(in_mem_archive, 'w') as zip_archive:
        with open(file, 'rb') as f:
            zip_archive.writestr('lambda_function.py', f.read())

    client = boto3.client('lambda')
    client.update_function_code(FunctionName=function_name,
                                ZipFile=in_mem_archive.getvalue())


def main():
    file_list = pathlib.Path().glob('./lambda-functions/*')
    worker_pool = ThreadPoolExecutor(max_workers=2)
    for file in file_list:
        worker_pool.submit(push_lambda_files(file))


if __name__ == "__main__":
    main()
