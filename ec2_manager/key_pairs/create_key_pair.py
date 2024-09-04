import boto3
from botocore.exceptions import ClientError

def create_ec2_key_pair(keyname, keytype='rsa', tagspecifications=None, keyformat='pem'):
    """
    Create a key pair for an EC2 instance.

    :param keyname: Name of the key pair.
    :param keytype: Type of the key pair. Choices are 'rsa' (default) or 'ed25519'.
    :param tagspecifications: List of dictionaries for tag specifications. Each dict should have 'ResourceType' and 'Tags'.
    :param keyformat: Format of the key pair. Choices are 'pem' (default) or 'ppk'.
    :return: The key pair object.
    """
    ec2_client = boto3.client('ec2')

    try:
        # Validate keytype and keyformat
        if keytype not in ['rsa', 'ed25519']:
            raise ValueError("Invalid keytype. Choose 'rsa' or 'ed25519'.")
        if keyformat not in ['pem', 'ppk']:
            raise ValueError("Invalid keyformat. Choose 'pem' or 'ppk'.")

        # Create key pair
        response = ec2_client.create_key_pair(
            KeyName=keyname,
            KeyType=keytype  # 'rsa' or 'ed25519'
        )

        key_pair_id = response['KeyPairId']
        key_material = response['KeyMaterial']

        # Print key material to save it to a file
        if keyformat == 'pem':
            key_file_extension = '.pem'
        else:
            key_file_extension = '.ppk'
            # Convert PEM to PPK format if needed using the puttygen command
            import subprocess
            ppk_file = keyname + '.ppk'
            with open(keyname + '.pem', 'w') as pem_file:
                pem_file.write(key_material)
            subprocess.run(['puttygen', keyname + '.pem', '-o', ppk_file, '-O', 'ppk'], check=True)
            # Optionally remove the pem file after conversion
            import os
            os.remove(keyname + '.pem')

        # Save the key material to a file
        with open(keyname + key_file_extension, 'w') as key_file:
            key_file.write(key_material)
        print(f"Key pair '{keyname}' created and saved to '{keyname + key_file_extension}'")

        # Add tags to the key pair
        if tagspecifications:
            for tag_spec in tagspecifications:
                ec2_client.create_tags(
                    Resources=[key_pair_id],
                    Tags=tag_spec['Tags']
                )
                print(f"Tags added to key pair '{keyname}': {tag_spec['Tags']}")

        return response

    except ClientError as e:
        print(f"An error occurred: {e}")
    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")