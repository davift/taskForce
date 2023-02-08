# taskForce

Sometimes many ephemeral servers are required to perform a slow task quicker by distributing the load over multiple instances, such as port scanning, hash brute-forcing, etc.

This repository contains scripts that automate the deployment of servers and then execute Ansible Playbooks against them.

The Playbook files need to be located in the same directory where the deployment script is.

## AWS

The script `aws.py` makes the best usage of features like Spot Instances (super cheap idle resources) and Termination as the default shutdown behaviour.

```
Select a target REGION:

[ 1 ] ap-south-1
[ 2 ] eu-north-1
[ 3 ] eu-west-3
[ 4 ] eu-west-2
[ 5 ] eu-west-1
[ 6 ] ap-northeast-3
[ 7 ] ap-northeast-2
[ 8 ] ap-northeast-1
[ 9 ] ca-central-1
[ 10 ] sa-east-1
[ 11 ] ap-southeast-1
[ 12 ] ap-southeast-2
[ 13 ] eu-central-1
[ 14 ] us-east-1
[ 15 ] us-east-2
[ 16 ] us-west-1
[ 17 ] us-west-2

Enter your choice [9]: 

Select a KEY PAIR:

[ 1 ] Sandbox
[ 2 ] Production
[ 3 ] Secured

Enter your choice [1]: 

Select a SECURITY GROUP:

[ 1 ] sg-05d1b75bf555c24ab default
[ 2 ] sg-089cadbe22226e389 Deny-All
[ 3 ] sg-0b8333d12c2d33f79 Test

Enter your choice [1]: 

Select a VPC:

[ 1 ] vpc-9cab99f5

Enter your choice [1]: 

Select a SUBNET:

[ 1 ] subnet-30d88c59
[ 2 ] subnet-5fd0db66
[ 3 ] subnet-e110bfb1

Enter your choice [any]: 

Select an Ubuntu 20.04 TLS IMA:

[ 1 ] ami-09e2c09f31b90da99 ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-20230207
[ 2 ] ami-0b71701f667d37ddf ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-20230112
[ 3 ] ami-07a69147786eb0731 ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-20221212
[ 4 ] ami-0521101504f19ff6a ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-20221206
[ 5 ] ami-0859074604ca21d57 ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-20221201

Enter your choice [1]: 

Number of instances [1]: 
[ 1 ] t3.nano 2 vCPU 0.5 GB
[ 2 ] t3.micro 2 vCPU 1 GB
[ 3 ] t3.small 2 vCPU 2 GB
[ 4 ] t3.medium 2 vCPU 4 GB
[ 5 ] t3.large 2 vCPU 8 GB
[ 6 ] t3.xlarge 4 vCPU 16 GB
[ 7 ] t3.2xlarge 8 vCPU 32 GB

Instance type [t3.small]: 

Disk size in GB [10]: 

Public IP(s):

3.99.51.134

[ 1 ] nginx.yml

Chose one Playbook to run [none]: 1

PLAY [all] *******************************************************************************************************

TASK [Gathering Facts] *******************************************************************************************
ok: [3.99.51.134]

TASK [apt-get update] ********************************************************************************************
ok: [3.99.51.134]

TASK [install nginx] *********************************************************************************************
changed: [3.99.51.134]

TASK [start nginx] ***********************************************************************************************
ok: [3.99.51.134]

PLAY RECAP *******************************************************************************************************
3.99.51.134                : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 
```

## Linode

## Digital Ocean

