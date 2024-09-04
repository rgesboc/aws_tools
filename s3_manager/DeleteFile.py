import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

# Function to delete a file from an S3 bucket
def delete_s3_file(bucket_name, file_key):
    """
    Delete a file from an S3 bucket.

    :param bucket_name: The name of the S3 bucket.
    :param file_key: The key of the file to be deleted.
    :return: None
    """
    # Create a session using your AWS credentials and region
    session = boto3.Session(profile_name='default')  # Replace 'default' with your AWS profile name if needed
    
    # Get the S3 service resource
    s3 = session.resource('s3')
    
    try:
        # Specify the bucket
        bucket = s3.Bucket(bucket_name)
        
        # Delete the file
        bucket.delete_objects(
            Delete={
                'Objects': [
                    {'Key': file_key}
                ],
                'Quiet': False  # Set to True for a quieter response
            }
        )
    
    except NoCredentialsError:
        print("Error: No AWS credentials found. Please configure your AWS credentials.")
        return False
    
    except PartialCredentialsError:
        print("Error: Incomplete AWS credentials found. Please check your configuration.")
        return False
    
    except ClientError as e:
        # This handles errors returned by the AWS S3 service
        error_code = e.response['Error']['Code']
        if error_code == '404':
            print(f"Error: The file '{file_key}' does not exist in bucket '{bucket_name}'.")
        else:
            print(f"ClientError: {e}")
        return False

    except Exception as e:
        # Handles any other exceptions that may occur
        print(f"An unexpected error occurred: {e}")
        return False
    
    return True

# # Example usage
# bucket_name = 'my-bucket'  # Replace with your bucket name
# file_key = 'path/to/your/file.txt'  # Replace with the path to your file

# delete_s3_file(bucket_name, file_key)

def delete_mult_s3_files(bucket_name, file_keys):
    """
    Delete multiple files from an S3 bucket.

    :param bucket_name: The name of the S3 bucket.
    :param file_keys: A list of keys of the files to be deleted.
    :return: None
    """
    session = boto3.Session(profile_name='default')
    s3 = session.resource('s3')
    
    try:
        bucket = s3.Bucket(bucket_name)
        
        objects = [{'Key': key} for key in file_keys]
        response = bucket.delete_objects(
            Delete={
                'Objects': objects,
                'Quiet': False
            }
        )
    
    except NoCredentialsError:
        print("Error: No AWS credentials found. Please configure your AWS credentials.")
        return False
    
    except PartialCredentialsError:
        print("Error: Incomplete AWS credentials found. Please check your configuration.")
        return False
    
    except ClientError as e:
        print(f"ClientError: {e}")
        return False
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
    return True

# # Example usage
# file_keys = ['path/to/your/file1.txt', 'path/to/your/file2.txt']  # Replace with the paths to your files
# delete_s3_files(bucket_name, file_keys)