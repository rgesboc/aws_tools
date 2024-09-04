import boto3
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError, EndpointConnectionError, BotoCoreError
from logging_config import setup_logger

LOG_DIR='logs\\ec2'
LOG_FILE='find_instance.log'
ERROR_LOG_FILE = 'find_instance_error.log'

def find_instance_by_name(instance_name, region_name='us-east-2'):
    """
    Check if an EC2 instance with a specific Name tag already exists.
    
    :param instance_name: The name of the instance to find
    :param region_name: AWS region to use
    :return: The ID of the existing instance if found, None otherwise
    """
    # Setup the logger
    logger=setup_logger(LOG_DIR, LOG_FILE, ERROR_LOG_FILE)
    try:
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
                    logger.info(f"Instance name '{instance_name}' with ID '{instance.id}' exists.")
                    return instance_name, instance.id, True
        
        logger.info(f"No instance named '{instance_name}' found.")
        return None, None, False
    
    except (NoCredentialsError, PartialCredentialsError) as cred_error:
        logger.error("AWS credentials not found or incomplete. Please configure your credentials properly.", exc_info=True)
        return None, None, False

    except BotoCoreError as botocore_err:
        logger.error(f"An unexpected error occurred with Boto3: {botocore_err}", exc_info=True)
        return None, None, False