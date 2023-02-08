# taskForce

Sometimes many ephemeral servers are required to perform a slow task quicker by distributing the load over multiple instances, such as port scanning, hash brute-forcing, etc.

This repository contains scripts that automate the deployment of servers and then execute Ansible Playbooks against them.

The Playbook files need to be located in the same directory where the deployment script is.

## AWS

The script `aws.py` makes the best usage of features like Spot Instances (super cheap idle resources) and Termination as the default shutdown behaviour.

## Linode

## Digital Ocean

