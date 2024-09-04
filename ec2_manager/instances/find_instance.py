import boto3
from botocore.exceptions import ClientError

def find_instance_by_name(instance_name, region_name='us-east-2'):
    """
    Check if an EC2 instance with a specific Name tag already exists.
    
    :param instance_name: The name of the instance to find
    :param region_name: AWS region to use
    :return: The ID of the existing instance if found, None otherwise
    """
    ec2 = boto3.resource('ec2', region_name=region_name)
    
    # Filter instances based on the Name tag
    instances = ec2.instances.filter(
        Filters=[
            {'Name': 'tag:Name', 'Values': [instance_name]},
            {'Name': 'instance-state-name', 'Values': ['running', 'stopped', 'pending', 'terminated']}
        ]
    )
    
    for instance in instances:
        for tag in instance.tags or []:
            if tag['Key'] == 'Name' and tag['Value'] == instance_name:
                print(f"An instance named '{instance_name}' with ID '{instance.id}' already exists.")
                return instance_name, instance.id, True
    
    print(f"No instance named '{instance_name}' found.")
    return None, None, False