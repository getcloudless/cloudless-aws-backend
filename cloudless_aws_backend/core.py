# -*- coding: utf-8 -*-
from . import helpers

import json
from jsonschema import validate
import boto3
from moto import mock_ec2

### Initialize Resources ###

RESOURCE_TYPES = {}
RESOURCE_SCHEMAS = {}

def register_resource_types():

    # TODO: Replace this with resource type "registration" to invert the control
    def register_resource_type(resource_type, schema_path, create_function,
            delete_function, get_function):
        with open(schema_path) as model_raw:
            model = json.loads(model_raw.read())
        # TODO: Throw a better error message
        assert resource_type == model["title"]
        RESOURCE_TYPES[model["title"]] = {
                "create": create_function,
                "delete": delete_function,
                "get": get_function}
        RESOURCE_SCHEMAS[model["title"]] = model

    register_resource_type("VirtualMachine", "cloudless-core-model/models/virtual-machine.json",
            create_virtual_machine, delete_virtual_machine, get_virtual_machine)
    # TODO: Private networks
    register_resource_type("PrivateNetwork", "cloudless-core-model/models/private-network.json",
            None, None, None)

### VirtualMachine Resource Type ###

def create_virtual_machine(resource_definition):
    ec2 = boto3.client('ec2')
    return ec2.run_instances(ImageId="ami-0cbcac3d89df9334d",
            MaxCount=1,
            MinCount=1,
            InstanceType=resource_definition["instance_type"])

def delete_virtual_machine(resource_definition):
    pass

def get_virtual_machine(resource_definition):
    ec2 = boto3.client('ec2')
    reservations = ec2.describe_instances()["Reservations"]
    instances = [instance for reservation in reservations for instance in reservation["Instances"]]
    virtual_machines = [{"instance_type": instance["InstanceType"]} for instance in instances]
    return virtual_machines[0]

### Query Actions ###

def create(resources, plan=False):
    for resource_type, resource_definition in resources:
        # TODO: Ordering, dependency analysis, etc.
        validate(instance=resource_definition, schema=RESOURCE_SCHEMAS[resource_type])
        return RESOURCE_TYPES[resource_type]["create"](resource_definition)

def delete(resources, plan=False):
    for resource_type, resource_definition in resources:
        validate(instance=resource_definition, schema=RESOURCE_SCHEMAS[resource_type])
        return RESOURCE_TYPES[resource_type]["delete"](resource_definition)

def get(resources, plan=False):
    for resource_type, resource_definition in resources:
        validate(instance=resource_definition, schema=RESOURCE_SCHEMAS[resource_type])
        return RESOURCE_TYPES[resource_type]["get"](resource_definition)

ACTIONS = {
    "CREATE": create,
    "DELETE": delete,
    "GET": get
}

### User API ###

def plan(action, resources):
    if not RESOURCE_TYPES:
        register_resource_types()
    return ACTIONS[action](resources, plan=True)

def apply(action, resources):
    if not RESOURCE_TYPES:
        register_resource_types()
    return ACTIONS[action](resources)
