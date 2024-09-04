import boto3
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from ec2_manager.ami.latest_amazon_linux_ami import get_latest_amazon_linux_ami
from ec2_manager.key_pairs.create_key_pair import create_ec2_key_pair
from ec2_manager.instances.find_instance import find_instance_by_name
from botocore.exceptions import ClientError
from logging_config import setup_test_logger

LOG_DIR='test_logs\\ec2'
LOG_FILE='test_create.log'
ERROR_LOG_FILE = 'test_create_error.log'

def create_instance(instance_name, region_name='us-east-2', ami_id=None, instance_type='t2.micro', key_name=None, security_group_id=None, subnet_id=None, min_count=1, max_count=1, user_tags=None):
    # Setup the Logger
    logger=setup_test_logger(LOG_DIR,LOG_FILE,ERROR_LOG_FILE)

    # Initialize the EC2 resource
    ec2 = boto3.resource('ec2', region_name = region_name)
    instances = ec2.instances.all()
    
    logger.info(f"Checking if instance {instance_name} exists...")
    instance_exists = find_instance_by_name(instance_name, region_name)

    if not instance_exists[2]:
        logger.info(f"Instance {instance_name} does not exist. Proceeding with creation.")

        # Initialize ami_id if none was provided
        if ami_id == None:
            logger.info("No AMI ID provided. Fetching the latest Amazon Linux AMI.")
            ami_id = get_latest_amazon_linux_ami(region_name)

        # Initialized key_name if none was provided
        if key_name == None:
            logger.info("No key name provided. Creating a new key pair.")
            tags = [{'ResourceType': 'key-pair', 'Tags': [{'Key': 'Name', 'Value': instance_name + " EC2 Key Pair"}]}]
            create_ec2_key_pair(instance_name+" EC2 Key Pair", tagspecifications=tags)
        
        # Initialize default tag
        default_tag = {
            'Key': 'Name',
            'Value': instance_name
        }

        # Merge the default tag with the user tag if provided
        if user_tags:
            if not isinstance(user_tags, dict):
                logger.error("user_tags must be a dictionary")
                raise ValueError("user_tags must be a dictionary")
            for key, value in user_tags.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    logger.error("Both tag keys and values must be strings.")
                    raise ValueError("Both tag keys and values must be strings.")
                tags.append({'Key': key, 'Value': value})

        # Launch a new EC2 instance if it hasn't already been created
        try:
            logger.info(f"Launching instance with name: {instance_name}")
            new_instance = ec2.create_instances(
                ImageId = ami_id,
                InstanceType=instance_type,
                KeyName=key_name,
                SecurityGroupIds=[security_group_id] if security_group_id else [],
                SubnetId=subnet_id if subnet_id else None,
                MinCount=min_count,
                MaxCount=max_count,
                TagSpecifications=[
                    {
                        'ResourceType': 'instance',
                        'Tags': tags
                    }
                ]
            )[0] # Get the first instance from the list of instances

            # Wait for the instance to run
            logger.info(f"Waiting for the instance {instance_name} to start...")
            new_instance.wait_until_running()
            new_instance.load() # Refresh the instance attributes to get the latest state

            # Print the instance ID
            logger.info(f"EC2 instance {instance_name} created with ID: {new_instance.id}")
            for handler in logger.handlers[:]:
                handler.close()
                logger.removeHandler(handler)
            return new_instance.id
            
        except ClientError as e:
            logger.error(f"An error occurred: {e}", exc_info=True)
            for handler in logger.handlers[:]:
                handler.close()
                logger.removeHandler(handler)
            return None
    else:
        logger.info(f"Instance named '{instance_name}' already exists.")
        for handler in logger.handlers[:]:
                handler.close()
                logger.removeHandler(handler)
        return None