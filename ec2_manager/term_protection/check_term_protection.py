import boto3
from botocore.exceptions import ClientError

def check_termination_protection(instance_id, region_name=None):
    """
    Checks if termination protection is enabled for an EC2 instance.

    :param instance_id: The ID of the instance to check.
    :param region_name: AWS region name to use (default is None, which uses the default region from the AWS configuration).
    :return: A boolean indicating whether termination protection is enabled.
    """
    try:
        ec2 = boto3.client('ec2', region_name=region_name)

        # Check if termination protection is enabled
        response = ec2.describe_instance_attribute(InstanceId=instance_id, Attribute='disableApiTermination')
        termination_protection = response['DisableApiTermination']['Value']
        
        if termination_protection:
            print(f"Termination protection is enabled for instance {instance_id}.")
        else:
            print(f"Termination protection is not enabled for instance {instance_id}.")
        
        return termination_protection

    except ClientError as e:
        print(f"An error occurred while checking termination protection: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None