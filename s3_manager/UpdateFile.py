import boto3
import logging
from botocore.exceptions import ClientError
import os
import ListObjects

def update_file(bucket, file_name, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # Grab a list of all objects in the bucket
    total_objects = ListObjects.list_objects(bucket)

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Check if the file exists
    if total_objects[0] == True and object_name in total_objects[1]:
        # Upload the file
        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            print(f"The bucket name '{bucket}' is not accessible or the file to upload, '{object_name}', is incorrect")
            return False
        return True
    # If the file doesn't exist, return False
    else:
        print(f"The file '{object_name}' does not exist in bucket '{bucket}'")
        return False 