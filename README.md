# Lambda function to monitor Amazon Elastic File System (EFS) size

## What is it?

This lambda function can be used to create a CloudWatch custom metric named SizeInBytes to help you tracking the metered size of EFS file systems.

## Prerequisites

Create the execution role (IAM Role) **lambda_basic_execution** to be used by the lambda function, and attached the below AWS managed IAM policies to this IAM role:
 
Policy ARN: arn:aws:iam::aws:policy/CloudWatchFullAccess

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "autoscaling:Describe*",
                "cloudwatch:*",
                "logs:*",
                "sns:*"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
```

Policy ARN: arn:aws:iam::aws:policy/AmazonElasticFileSystemReadOnlyAccess

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "ec2:DescribeAvailabilityZones",
                "ec2:DescribeNetworkInterfaceAttribute",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeSubnets",
                "ec2:DescribeVpcAttribute",
                "ec2:DescribeVpcs",
                "elasticfilesystem:Describe*",
                "kms:ListAliases"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
```

## Usage

- Amazon Linux 2017.09
- Ubuntu 16.04
 
Launch a new instance or use an existing one that has an attached IAM Role with administrator permissions (like the AWS managed AdministratorAccess) to download the lambda function and deploy it from this instance.
 
Modify the config.yaml file to match your environment configuration, run and deploy the lambda function using one of the below two methods:

1. SSH into an existing instance run the below commands:

```bash
region="eu-west-1"
filesystem_id="fs-d617b81f"
mkdir ~/venv; cd $_
git clone https://github.com/diesant/aws_efs_custom_metric
virtualenv -p /usr/bin/python2.7 aws_efs_custom_metric; cd $_
source bin/activate
pip install -r requirements.txt
sed -i "s:eu-west-1:${region}:g; s:fs-d617b81f:${filesystem_id}:g" config.yaml
lambda deploy
```

2. Launch a new instance and use the below user_data (change the environment variables to match your configuration and attach the administrator IAM role to this instance):

```bash 
#!/bin/bash
su - ec2-user -c '
region="eu-west-1"
filesystem_id="fs-d617b81f"
mkdir ~/venv; cd $_
git clone https://github.com/diesant/aws_efs_custom_metric
virtualenv -p /usr/bin/python2.7 aws_efs_custom_metric; cd $_
source bin/activate
sed -i "s:eu-west-1:${region}:g; s:fs-d617b81f:${filesystem_id}:g" config.yaml
pip install -r requirements.txt
lambda deploy
'
```

At this point the lambda function may work fine and you just need to create a CloudWatch Rule to schedule an event to trigger this function hourly. The below example shows how to create the CloudWatch rule using the AWS CLI:


```bash 
aws events put-rule --name SizeInBytes --schedule-expression 'rate(5 minutes)'
```

The below example shows how to descrite the CloudWatch rule using the AWS CLI:

```bash
aws events describe-rule --name SizeInBytes
{
    "ScheduleExpression": "rate(5 minutes)",
    "Name": "SizeInBytes",
    "State": "ENABLED",
    "Arn": "arn:aws:events:eu-west-1:525708436736:rule/SizeInBytes",
    "Description": "SizeInBytes"
}
```

For more information about this matter, please refer to [Tutorial: Schedule AWS Lambda Functions Using CloudWatch Events](http://docs.aws.amazon.com/AmazonCloudWatch/latest/events/RunLambdaSchedule.html)