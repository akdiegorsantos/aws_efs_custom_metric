# -*- coding: utf-8 -*-
''' This lambda function can be used to create a CloudWatch custom metric
named SizeInBytes to help you tracking the metered size of EFS file
systems. '''

import os

import boto3

# Make sure you set the environment variables 'filesystemid' and 'region' in
# the lambda function otherwise we cannot proceed.
INFO = {'filesystemid': os.environ.get('filesystemid'),
        'region': os.environ.get('region')}

for index, (key, value) in enumerate(INFO.items()):
    if not value:
        raise SystemError('Environment variable not found: {}'.format(key))


def efs_get_size():
    ''' EFS boto3 client '''
    client = boto3.client('efs', region_name=INFO['region'])
    response = client.describe_file_systems(FileSystemId=INFO['filesystemid'])
    output = response['FileSystems'][0]['SizeInBytes']['Value']
    return output


def cloudwatch_put_metric():
    ''' CloudWatch boto3 client '''
    client = boto3.client('cloudwatch', region_name=INFO['region'])
    response = client.put_metric_data(MetricData=[
        {
            'MetricName': 'SizeInBytes',
            'Dimensions': [
                {
                    'Name': 'FileSystemId',
                    'Value': INFO['filesystemid']
                },
            ],
            'Unit': 'None',
            'Value': efs_get_size()
        },
    ], Namespace='Custom/EFS')
    return response


def handler(event, context):
    ''' Populate our custom CloudWatch metric SizeInBytes '''
    return {'message': cloudwatch_put_metric()}
