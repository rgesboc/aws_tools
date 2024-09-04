from setuptools import setup, find_packages

setup(
    name='aws_tools',
    version='0.1.0',
    description='A collection of utilities for managing AWS services',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/aws_tools',
    packages=find_packages(include=['ec2_manager', 'ec2_manager.*',
                                    's3_manager', 's3_manager.*',
                                    'ecs_manager', 'ecs_manager.*',
                                    'lambda_manager', 'lambda_manager.*']),
    install_requires=[
        'boto3==1.26.0',  # AWS SDK for Python
        # Add other dependencies here
    ],
    extras_require={
        'dev': [
            'pytest==7.3.0',  # For testing
            'mypy==1.4.1',    # For type checking
            'flake8==6.1.0'  # For linting
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
