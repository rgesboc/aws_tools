import boto3
import logging

def list_objects(input_bucket):
    s3 = boto3.client('s3')

    try:
        response = s3.list_objects(Bucket=input_bucket)

        doc_names = []
        for items in response['Contents']:
            doc_names.append(items['Key'])
    # Exception for wrong bucket name or not accessible
    except s3.exceptions.NoSuchBucket as nsb:
        logging.error(nsb)
        return False, None  
    # Exception for no contents within the bucket
    except KeyError as ke:
        logging.error(ke)
        return False, None
    return True, doc_names