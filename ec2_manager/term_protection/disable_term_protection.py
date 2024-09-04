import boto3
from botocore.exceptions import ClientError

def disable_termination_protection(instance_id, region_name=None):
    """
    Disables termination protection for an EC2 instance.

    :param instance_id: The ID of the instance to modify.
    :param region_name: AWS region name to use (default is None, which uses the default region from the AWS configuration).
    :return: The response from the modify_instance_attribute API call.
    """
    try:
        ec2 = boto3.client('ec2', region_name=region_name)

        # Disable termination protection
        response = ec2.modify_instance_attribute(InstanceId=instance_id, DisableApiTermination={'Value': False})
        print(f"Termination protection has been disabled for instance {instance_id}.")
        
        return response

    except ClientError as e:
        print(f"An error occurred while disabling termination protection: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")