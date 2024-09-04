# Import the boto3 library
import boto3
import logging
from botocore.exceptions import ClientError

# Instantiate a boto3 resource for S3 and name your bucket
def create_bucket(bucket_name, region='us-east-2'):
    try:
        if region is None:
            s3_client = boto3.client('s3', region_name = region)
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationContraint': 'us-east-2'})
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationContraint': region}
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False    
    return True


# Check if bucket exists
# Create the bucket if it does NOT exist

def check_bucket(bucket_name, ):






# Create 'file_1' and 'file_2'


# UPLOAD 'file_1' to the new bucket



# READ and print the file from the bucket




# UPDATE 'file_1' in the bucket with new content from 'file_2'





# DELETE the file from the bucket



# DELETE the bucket (the bucket should be empty.)


