import boto3
import ListBuckets
import OutputToTerminal
import CheckBucket
import ListObjects
import CheckAndCreateBucket
import DeleteBucket
import ReadFile
import UpdateFile
import CreateBucket
import os
import DeleteFile
import Upload

if __name__ == '__main__':
    
    bucket_name = "aws-python-test-91202test4532"
    full_file_name = r'C:\Users\rober\Documents\Python\python_aws_class\My Code\AWS_Services\S3\howdy.txt'
    file_name = os.path.basename(full_file_name)
    region = 'us-east-2'

    # List all bucketsk
    all_buckets = ListBuckets.list_all_buckets()
    if len(all_buckets) > 0:
        print("Buckets Available to you:")
        OutputToTerminal.list_output(all_buckets)
    else:
        print("You don't have access to any buckets")

    # Check if bucket exists and accessible
    available = CheckBucket.check_bucket(bucket_name)
    if available == True:
        print("\nThe bucket is accessible.\n")
    elif available == False:
        print("\nThe bucket is not accessible or does not exist.\n")

    # Create bucket
    bucket_creation = CreateBucket.create_bucket(bucket_name, region)
    
    if bucket_creation == True:
        print(f"Bucket {bucket_name} has been created in region {region}\n")
    else:
        print(f"Failure to create bucket {bucket_name} in region {region}\n")

    # Check is bucket exists. If not, create bucket
    check_and_create = CheckAndCreateBucket.check_and_create_bucket(bucket_name, region)

    if check_and_create == True:
        print(f"Bucket '{bucket_name}' already exists and is accessible.\n")
    else:
        print(f"Bucket {bucket_name} does not exist. It has been created in {region}\n")

    # Upload a file to a bucket
    upload_success = Upload.upload_file(full_file_name, bucket_name, file_name)

    if upload_success == True:
        print(f"Upload {file_name} to {bucket_name} was successful.\n")
    else:
        print(f"Upload {file_name} to {bucket_name} was unsuccessful.\n")

    # Check valid bucket and list objects within
    valid_bucket_list_obj = ListObjects.list_objects(bucket_name)

    if valid_bucket_list_obj[0] == True:
        print("Documents in the bucket are:")
        OutputToTerminal.list_output(valid_bucket_list_obj[1])
    else:
        print("No documents in this bucket.")

    # Read file within a bucket
    file_read = ReadFile.read_file(bucket_name, file_name)

    if file_read[0] == True:
        print(f"\n{bucket_name} contains the file {file_name} with the contents:\n{file_read[1]}")
    else:
        print(f"\nBucket name '{bucket_name}' or file name '{file_name}' is incorrect or cannot be accessed. Cannot read File in Bucket")

    # Update file in a bucket
    update_success = UpdateFile.update_file(bucket_name, full_file_name, file_name)
    
    if update_success == True:
        print(f"\nUpdate of file '{file_name}' to bucket '{bucket_name}' was successful.\n")
    else:
        print(f"\nUpdate of file '{file_name}' to bucket '{bucket_name}' was unsuccessful.\n")

    # # Delete File
    # delete_success = DeleteFile.delete_s3_file(bucket_name, file_name)
    # if delete_success == True:
    #     print(f"File '{file_name}' was deleted from bucket '{bucket_name}'.")
    # else:
    #     print(f"File '{file_name}' was unable to be deleted from bucket '{bucket_name}'.")

    # Delete all files in a bucket
    delete_all_files_success = DeleteFile.delete_mult_s3_files(bucket_name, valid_bucket_list_obj[1])
    if delete_all_files_success == True:
        print(f"Successfully deleted the following objects from bucket {bucket_name}:")
        OutputToTerminal.list_output(valid_bucket_list_obj[1])
    else: 
        print(f"Did not successfully delete all of the objects in the bucket {bucket_name}\n")
    # Delete Bucket
    delete_bucket = DeleteBucket.delete_bucket(bucket_name)
    
    if delete_bucket == True:
        print(f"\nBucket {bucket_name} has been deleted.")
    else:
        print(f"\nBucket {bucket_name} was not able to be deleted.")