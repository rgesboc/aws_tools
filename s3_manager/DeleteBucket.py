import boto3
import logging
from botocore.exceptions import ClientError, BucketNotEmpty

def delete_bucket(bucket_name):
    s3 = boto3.client('s3')
    try:
        response = s3.delete_bucket(Bucket=bucket_name,)
        if 'ResponseMetadata' in response:
            return True
    except ClientError as e:
        print("Bucket does not exist or is not accessible.")
        logging.error(e)
        return False
    except BucketNotEmpty as bne:
        print("Bucket contains objects and cannot be deleted. Remove the files before deleting.")
        logging.error(bne)
        return False