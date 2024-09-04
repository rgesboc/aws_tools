import boto3
import logging
from botocore.exceptions import ClientError

def create_bucket(bucket_name, region='us-east-2'):

    #Check input
    try:
        if region is None:
            s3_client = boto3.client('s3', region_name = region)
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationContraint': 'us-east-2'})
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False    
    return True