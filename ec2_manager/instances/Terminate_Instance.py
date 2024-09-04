import boto3
from botocore.exceptions import ClientError

def terminate_instance(instance_id, region_name=None):
    """
    Terminates an EC2 instance.

    :param instance_id: The ID of the instance to terminate.
    :param region_name: AWS region name to use (default is None, which uses the default region from the AWS configuration).
    :return: The response from the terminate_instances API call.
    """
    try:
        ec2 = boto3.client('ec2', region_name=region_name)

        # Terminate the instance
        response = ec2.terminate_instances(InstanceIds=[instance_id])
        print(f"Termination request sent for instance {instance_id}.")
        
        return response

    except ClientError as e:
        print(f"An error occurred while terminating the instance: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")