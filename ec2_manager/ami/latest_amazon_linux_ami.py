import boto3

def get_latest_amazon_linux_ami(region_name='us-east-1'):
    # Create a session using the specified region
    session = boto3.Session(region_name=region_name)
    ec2 = session.client('ec2')

    # Define the filters for the AMI search
    filters = [
        {'Name': 'name', 'Values': ['amzn2-ami-hvm-*-x86_64-gp2']},  # Amazon Linux 2 AMIs
        {'Name': 'state', 'Values': ['available']},  # Filter for available AMIs
        {'Name': 'owner-id', 'Values': ['137112412989']}  # Amazon Linux 2 AMI owner ID
    ]

    # Retrieve the AMI images based on the filters
    response = ec2.describe_images(Filters=filters, Owners=['137112412989'])
    
    # Sort the AMIs based on creation date to get the latest one
    images = sorted(response['Images'], key=lambda x: x['CreationDate'], reverse=True)

    # Get the latest AMI ID
    latest_ami_id = images[0]['ImageId'] if images else None

    return latest_ami_id

# # Example usage
# latest_ami_id = get_latest_amazon_linux_ami('us-east-1')  # You can change the region as needed
# print(f'The latest Amazon Linux 2 AMI ID is: {latest_ami_id}')