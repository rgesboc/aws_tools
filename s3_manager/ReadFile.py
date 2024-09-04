import boto3
import logging
from botocore.exceptions import ClientError

def read_file(input_bucket, file_name):
    s3 = boto3.resource('s3')
    try:
        obj = s3.Object(input_bucket, file_name)
        body = obj.get()['Body'].read()
    except ClientError as e:
        logging.error(e)
        return False, None
    return True, body