import boto3
import CreateBucket
import CheckBucket

def check_and_create_bucket(input_bucket, region='us-east-2'):
    s3 = boto3.client('s3')
    bucket_exists = CheckBucket.check_bucket(input_bucket)

    if bucket_exists == True:
        return True
    else:
        CreateBucket.create_bucket(input_bucket, region)
        return False