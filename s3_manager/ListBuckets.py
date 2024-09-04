import boto3

def list_all_buckets():
    # Retrieve the list of existing buckets that are owned by the user
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    
    # Add buckets to a list
    buckets = []
    for bucket in response['Buckets']:
        buckets.append(bucket["Name"])

    return buckets
