#!/usr/bin/env python
# encoding: utf-8
"""
aws.py

Created by Jeremiah Shirk on 2012-02-05.
Copyright (c) 2012 Monitis. All rights reserved.
"""

import sys
import os

from boto import ec2
from boto import rds
from boto.ec2 import elb
from boto.ec2 import cloudwatch

def connect_to_cloudwatch(region):
    '''Connect to the specified region and return a cloudwatch object'''
    return cloudwatch.connect_to_region(region)
    
def get_instance_name(instance):
    '''Return the appropriate attribute for an instance name'''
    if isinstance(instance, ec2.elb.loadbalancer.LoadBalancer):
        return instance.name
    elif isinstance(instance, ec2.instance.Instance):
        return instance.id
    elif isinstance(instance,rds.dbinstance.DBInstance):
        return instance.id
    elif isinstance(instance,ec2.volume.Volume):
        return instance.id

def available_metrics(catalog):
    '''Return a list of available metrics from based on the catalog'''
    ret = list()
    for service, instances in catalog.items():
        for instance, metrics in instances.items():
            for metric in metrics:
                ret.append ((
                    metric.namespace,
                    get_instance_name(instance),
                    metric.name))
    return ret

def metrics_catalog(region):
    '''Build a catalog of available metrics'''
    
    conn_ec2 = ec2.connect_to_region(region)
    conn_elb = elb.connect_to_region(region)
    conn_rds = rds.connect_to_region(region)
    conn_cloudwatch = cloudwatch.connect_to_region(region)
    
    catalog = {'ec2':{}, 'ebs':{}, 'elb':{}, 'rds':{}}
    
    # EC2 instances
    for reservation in conn_ec2.get_all_instances():
        for instance in reservation.instances:
            catalog['ec2'][instance] = conn_cloudwatch.list_metrics(
                dimensions={'InstanceId': [instance.id]})

    # EBS Volumes
    for volume in conn_ec2.get_all_volumes():
        catalog['ebs'][volume] = conn_cloudwatch.list_metrics(
            dimensions={'VolumeId': [volume.id]})
    
    # ELB instances
    for balancer in conn_elb.get_all_load_balancers():
        catalog['elb'][balancer] = conn_cloudwatch.list_metrics(
            dimensions={'LoadBalancerName': [balancer.name]})
    
    # RDS instances
    for instance in conn_rds.get_all_dbinstances():
        catalog['rds'][instance] = conn_cloudwatch.list_metrics(
            dimensions={'DBInstanceIdentifier': [instance.id]})

    return catalog

def dimensions(aws_namespace, instance_name):
    '''Return a Dimensions dict to identify a specific resource'''
    dimension_labels = {
        'AWS/EC2': 'InstanceId',
        'AWS/EBS': 'VolumeId',
        'AWS/ELB': 'LoadBalancerName',
        'AWS/RDS': 'DBInstanceIdentifier'}
    try:
        label = dimension_labels[aws_namespace]
    except KeyError:
        return None
    return {label:instance_name}
