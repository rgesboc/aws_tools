import boto3

def enable_delete_on_termination(instance_id, region_name='us-east-2'):
    # Initialize the EC2 client
    ec2 = boto3.client('ec2', region_name=region_name)

    try:
        # Describe the instance to get the block device mappings
        response = ec2.describe_instances(InstanceIds=[instance_id])
        instance = response['Reservations'][0]['Instances'][0]

        # Loop through the block device mappings
        for volume in instance.get('BlockDeviceMappings', []):
            if 'Ebs' in volume:
                volume_id = volume['Ebs']['VolumeId']
                print(f"Enabling DeleteOnTermination for Volume ID: {volume_id}")

                # Modify the volume attribute to enable DeleteOnTermination
                ec2.modify_instance_attribute(
                    InstanceId=instance_id,
                    BlockDeviceMappings=[
                        {
                            'DeviceName': volume['DeviceName'],
                            'Ebs': {
                                'DeleteOnTermination': True
                            }
                        }
                    ]
                )
                print(f"Set DeleteOnTermination to True for Volume ID: {volume_id}")

    except Exception as e:
        print(f"An error occurred: {e}")