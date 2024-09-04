import boto3
from botocore.exceptions import ClientError

def stop_instance(instance_id, hibernate=False, region_name = 'us-east-2'):
    """
    Stops one EC2 instance. Optionally hibernates the instance instead of stopping.

    :param instance_id: The ID of the instance to stop
    :param hibernate: Determines whether to hibernate the instance instead of stopping it. False is default.
    :param region_name: The region the instance is running. Default will try us-east-2.
    :return: The response from the stop_instances API call.
    """
    try:
        # Create the EC2 client with the specified region, defaulting to 'us-east-2' if none is provided
        ec2 = boto3.client('ec2',region_name=region_name)

        # Check to see if hibernate is a boolean
        if not isinstance(hibernate, bool):
            raise ValueError(f"The hibernate value provided was not a boolean. {hibernate} was provided.")
        
        # Call the EC2 stop_instances method with the correct parameters
        response = ec2.stop_instances(
            InstanceIds=[
                instance_id,
            ],
            Hibernate=hibernate
        )

        # Return response for further inspection if necessary
        return response

    except ClientError as e:
        print(f"An error occurred: {e}")
    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")  


def stop_mult_instances(instance_ids, hibernate=False, region_name='us-east-2'):
    """
    Stops one or more EC2 instances. Optionally hibernates instances instead of stopping.

    :param instance_ids: List of instance IDs to stop.
    :param hibernate: Determines whether to hibernate the instance instead of stopping it. False is default.
    :param region_name: The region the instances are running. Default will try us-east-2.
    :return: The response from the stop_instances API call.
    """
    try:
        # Create the EC2 client with the specified region, defaulting to 'us-east-2' if none is provided
        ec2 = boto3.client('ec2', region_name=region_name)

        # Ensure hibernate is a boolean value
        if not isinstance(hibernate, bool):
            raise ValueError(f"The hibernate value provided was not a boolean. {hibernate} was provided.")

        # Ensure instance_ids is a list
        if not isinstance(instance_ids, list):
            raise ValueError(f"instance_ids must be a list. {instance_ids} was provided.")

        # Call the EC2 stop_instances method with the correct parameters
        response = ec2.stop_instances(
            InstanceIds=instance_ids,
            Hibernate=hibernate 
        )

        # Return response for further inspection if necessary
        return response

    except ClientError as e:
        print(f"An error occurred: {e}")
    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")