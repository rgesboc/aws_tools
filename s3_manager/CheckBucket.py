import boto3
from botocore.exceptions import ClientError
import logging

def check_bucket(input_bucket):
    s3 = boto3.client('s3')
    try:
        response = s3.head_bucket(Bucket=input_bucket)
        if 'ResponseMetadata' in response:
            return True
    except ClientError as e:
        print(e)
        return False   