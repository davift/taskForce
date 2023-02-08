#!/usr/bin/python3
import os
import boto3
import botocore.exceptions
import random

# Checking for AWS Configuration Files
os.system('clear')
if not os.path.isfile(os.path.expanduser('~/.aws/config')):
    print('~/.aws/config does not exist.')
    exit()
if not os.path.isfile(os.path.expanduser('~/.aws/credentials')):
    print('~/.aws/credentials does not exist.')
    exit()

#
# Connect to EC2 with default region
#
 
ec2 = boto3.client('ec2')
config = {}

# Inheriting Configuration Variables
with open(os.path.expanduser('~/.aws/config')) as f:
    for line in f:
        if "=" in line:
            key, value = line.strip().split("=")
            config[key.strip()] = value.strip()

# Get the list of regions
regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
print("\nSelect a target REGION:\n")
i = 0
for region in regions:
    i = i + 1
    if config['region'] == region:
        default = i
    print('[', i, ']', region)

try:
    choice = int(input("\nEnter your choice [" + str(default) + "]: "))
except:
    choice = 0
if choice > 0 and choice <= i:
    config['region'] = regions[choice - 1]

#
# Connect to EC2 with selected region
#

ec2 = boto3.client('ec2', region_name=config['region'])

# Get the list of key pairs
key_pairs = ec2.describe_key_pairs()['KeyPairs']
print("\nSelect a KEY PAIR:\n")
i = 0
for key_pair in key_pairs:
    i = i + 1
    print('[', i, ']', key_pair['KeyName'])

try:
    choice = int(input("\nEnter your choice [1]: "))
except:
    choice = 0
if choice > 0 and choice <= i:
    config['key_pair'] = key_pairs[choice - 1]['KeyName']
else:
    config['key_pair'] = key_pairs[0]['KeyName']

# Get the list of security groups
security_groups = ec2.describe_security_groups()['SecurityGroups']
print("\nSelect a SECURITY GROUP:\n")
i = 0
for security_group in security_groups:
    i = i + 1
    print('[', i, ']', security_group['GroupId'], security_group['GroupName'])

try:
    choice = int(input("\nEnter your choice [1]: "))
except:
    choice = 1
if choice > 0 and choice <= i:
    config['security_group'] = security_groups[choice - 1]['GroupId']

# Get the list of VPCs
vpcs = ec2.describe_vpcs()['Vpcs']
print("\nSelect a VPC:\n")
i = 0
for vpc in vpcs:
    i = i + 1
    if vpc['IsDefault']:
        default = i
    print('[', i, ']', vpc['VpcId'])

try:
    choice = int(input("\nEnter your choice [" + str(default)+ "]: "))
except:
    choice = default
if choice > 0 and choice <= i:
    config['vpc'] = vpcs[choice - 1]['VpcId']

# Get the list of subnets for the default VPC
subnets = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [config['vpc']]}])['Subnets']
print("\nSelect a SUBNET:\n")
i = 0
for subnet in subnets:
    i = i + 1
    print('[', i, ']', subnet['SubnetId'])

try:
    choice = int(input("\nEnter your choice [any]: "))
except:
    choice = 0
if choice > 0 and choice <= i:
    config['subnet'] = subnets[choice - 1]['SubnetId']
else:
    config['subnet'] = ''

#
# EC2 Deployment
#

ec2 = boto3.client('ec2', region_name='ca-central-1')
ec2_config = {}

# List all the available AMIs
response = ec2.describe_images(Owners=['amazon'])
print("\nSelect an Ubuntu 20.04 TLS IMA:\n")
i = 0
imageids = {}
images = response['Images']
for image in sorted(images, key=lambda x: x['Name'], reverse=True):
    if 'ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server'.casefold() in image['Name'].casefold():
        i = i + 1
        imageids[i -1] = image['ImageId']
        print('[', i, ']', image['ImageId'], image['Name'])
        if i == 5:
            break

try:
    choice = int(input("\nEnter your choice [1]: "))
except:
    choice = 0
if choice > 0 and choice <= i:
    ec2_config['image'] = imageids[choice - 1]
else:
    ec2_config['image'] = imageids[0]

# Quantity
try:
    choice = int(input("\nNumber of instances [1]: "))
except:
    choice = 0
if choice > 0 and choice <= 10:
    ec2_config['quantity'] = choice
else:
    ec2_config['quantity'] = 1

# Type
types = ['t3.nano','t3.micro','t3.small','t3.medium','t3.large','t3.xlarge','t3.2xlarge']
cpu = ['2 vCPU','2 vCPU','2 vCPU','2 vCPU','2 vCPU','4 vCPU','8 vCPU']
ram = ['0.5 GB','1 GB','2 GB','4 GB','8 GB','16 GB','32 GB']
i = 0
while i < len(types):
    print('[', i + 1, ']', types[i], cpu[i], ram[i])
    i = i + 1
try:
    choice = int(input("\nInstance type [t3.small]: "))
except:
    choice = 0
if choice > 0 and choice <= i:
    ec2_config['type'] = types[choice - 1]
else:
    ec2_config['type'] = 't3.small'

# Disk
try:
    choice = int(input("\nDisk size in GB [10]: "))
except:
    choice = 0
if choice > 0 and choice <= 100:
    ec2_config['disk'] = choice
else:
    ec2_config['disk'] = 10

#
# Deploying EC2
#

try:
    response = ec2.run_instances(
        ImageId=ec2_config['image'],
        InstanceType=ec2_config['type'],
        KeyName=config['key_pair'],
        SecurityGroupIds=[config['security_group']],
        SubnetId=config['subnet'],
        MinCount=ec2_config['quantity'],
        MaxCount=ec2_config['quantity'],
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/sda1',
                'Ebs': {
                    'VolumeSize': ec2_config['disk'],
                    'VolumeType': 'gp3',
                    'DeleteOnTermination': True
                }
            }
        ],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'SDK Deployment'
                    },
                ]
            },
        ],
        UserData='#!/bin/bash\necho "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCfy2uXMrYKBrBhHvR0hgKudVZPSLbOA/avuRY7Op5XzN7pc3tCLdMz/FeixCdF6hXf8aMEtDNFm6JoJMOZ8c15XmashS+seO3wFvtbWd+Ng/CKpxoNzPMSa/6ODxbtyVGdK5kv+jO9g9IE+gehWAiEyOn0gf0sJDSKeZxjsZdLzkbZ/AH5HSKoZNrmpHkE0gPrv4TYAcuc3VR5zG+E83w3i0O2CAZVUduiL64Crl4kIp7oxhvWxkSXZ5D+SRuqXO09TuVlUjH3zDl2Io0dhatnXZA4tW8wQSuQO/JOwUF74x4cRscdc4insXiCQ2lwOSn3DCeg37aMppY0DNaoLvDL" > /home/ubuntu/.ssh/authorized_keys\nsudo apt update && sudo apt upgrade -y',
        #InstanceInitiatedShutdownBehavior='stop',
        #InstanceInitiatedShutdownBehavior='terminate',
        InstanceMarketOptions={
            'MarketType': 'spot',
            'SpotOptions': {
                'MaxPrice': '0.3',
                'SpotInstanceType': 'one-time',
                'InstanceInterruptionBehavior': 'terminate'
            }
        },
    )
except botocore.exceptions.EndpointConnectionError as e:
    if "no Spot capacity available" in str(e):
        print("!!! No Spot capacity available !!!")
    else:
        raise e

# Inventory
print("\nPublic IP(s):\n")
inventory = open("inventory.list", "wt")
i = 0
while i < ec2_config['quantity']:
    instance_id = response['Instances'][i]['InstanceId']
    waiter = ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance_id])
    instance = ec2.describe_instances(InstanceIds=[instance_id])
    public_ip_address = instance['Reservations'][0]['Instances'][0]['PublicIpAddress']
    print(public_ip_address)
    inventory.write(public_ip_address)
    i = i + 1
inventory.close()

# Playbooks
list = {}
print("")
i = 0
for file in os.listdir('./'):
    if file.endswith('.yml'):
        list[i] = file
        i = i + 1
        print('[', i, ']', file)
if len(list) == 0:
    print("\nNo Playbooks in the current directory.\n")
    exit()

try:
    choice = int(input("\nChose one Playbook to run [none]: "))
except:
    choice = 0
if choice > 0 and choice <= i:
    os.system('ansible-playbook --ssh-common-args \'-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null\' --inventory-file inventory.list ' + list[choice - 1])

print("")
exit()
