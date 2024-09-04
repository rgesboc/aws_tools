import boto3
from botocore.exceptions import ClientError

def check_ebs_volumes(instance_id, region_name='us-east-2'):
    """
    Checks the EBS volumes attached to an EC2 instance to ensure they have DeleteOnTermination set to True.

    :param instance_id: The ID of the instance to check.
    :param region_name: AWS region name to use (default is None, which uses the default region from the AWS configuration).
    :return: A list of volumes with DeleteOnTermination set to False.
    """
    try:
        ec2 = boto3.client('ec2', region_name=region_name)

        # Retrieve instance details
        response = ec2.describe_instances(InstanceIds=[instance_id])
        instance = response['Reservations'][0]['Instances'][0]

        volumes_with_issue = []

        for volume in instance['BlockDeviceMappings']:
            volume_id = volume['Ebs']['VolumeId']
            delete_on_termination = volume['Ebs'].get('DeleteOnTermination', True)
            if not delete_on_termination:
                volumes_with_issue.append(volume_id)
                print(f"Volume {volume_id} has DeleteOnTermination set to False.")
            else:
                print(f"Volume {volume_id} has DeleteOnTermination set to True.")

        if not volumes_with_issue:
            print("All EBS volumes have DeleteOnTermination set to True.")
        
        return volumes_with_issue

    except ClientError as e:
        print(f"An error occurred while checking EBS volumes: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
