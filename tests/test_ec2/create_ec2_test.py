import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import logging

# Add the project root directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import the function and logger setup
from ec2_manager.instances.create_ec2 import create_instance
from logging_config import setup_test_logger

LOG_DIR='test_logs\\ec2'
LOG_FILE='test_create.log'
ERROR_LOG_FILE = 'test_create_error.log'

class TestCreateInstance(unittest.TestCase):

    @patch('boto3.resource')
    @patch('ec2_manager.instances.find_instance.find_instance_by_name')
    @patch('ec2_manager.ami.latest_amazon_linux_ami.get_latest_amazon_linux_ami', return_value='ami-12345678')
    @patch('ec2_manager.key_pairs.create_key_pair.create_ec2_key_pair')
    def test_create_instance(self, mock_create_key_pair, mock_get_latest_ami, mock_find_instance, mock_boto3_resource):
        # Set up mock return values
        mock_instance = MagicMock()
        mock_instance.id = 'i-1234567890abcdef0'
        mock_instance.wait_until_running = MagicMock()
        mock_instance.load = MagicMock()
        
        mock_ec2 = MagicMock()
        mock_ec2.create_instances.return_value = [mock_instance]
        mock_boto3_resource.return_value = mock_ec2
        
        mock_find_instance.return_value = (None, None, False)  # Simulate instance does not exist
        
        # Call the function
        instance_id = create_instance(
            instance_name='test-instance',
            region_name='us-east-1',
            ami_id=None,
            instance_type='t2.micro',
            key_name=None,
            security_group_id='sg-12345678',
            subnet_id='subnet-12345678',
            min_count=1,
            max_count=1,
            user_tags={'Environment': 'Test'}
        )
        
        # Verify the instance ID is returned
        self.assertEqual(instance_id, 'i-1234567890abcdef0')
        
        # Check logs
        log_file_path = os.path.join(LOG_DIR, LOG_FILE)
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as log_file:
                logs = log_file.read()
            
            self.assertIn('Checking if instance test-instance exists...', logs)
            self.assertIn('Instance test-instance does not exist. Proceeding with creation.', logs)
            self.assertIn('No AMI ID provided. Fetching the latest Amazon Linux AMI.', logs)
            self.assertIn('No key name provided. Creating a new key pair.', logs)
            self.assertIn('Launching instance with name: test-instance', logs)
            self.assertIn('Waiting for the instance test-instance to start...', logs)
            self.assertIn('EC2 instance test-instance created with ID: i-1234567890abcdef0', logs)
        else:
            self.fail(f'Log file {log_file_path} not found.')

    def tearDown(self):
        # Retrieve the logger used in the tests
        logger = logging.getLogger()

        # Flush and close all handlers associated with this logger
        for handler in logger.handlers[:]:
            handler.acquire()
            try:
                handler.flush()  # Ensure all data is written to the file
                handler.close()  # Close the handler
                logger.removeHandler(handler)  # Remove the handler from the logger
            finally:
                handler.release()

        # Only clean up logs if the test was successful
        if self._outcome.success:
            log_file_path = os.path.join(LOG_DIR, LOG_FILE)
            error_log_file_path = os.path.join(LOG_DIR, ERROR_LOG_FILE)
            
            # Remove the main log file if it exists
            if os.path.exists(log_file_path):
                os.remove(log_file_path)
                
            # Remove the error log file if it exists
            if os.path.exists(error_log_file_path):
                os.remove(error_log_file_path)

if __name__ == '__main__':
    unittest.main()