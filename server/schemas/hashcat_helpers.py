import yaml
from pydantic import parse_obj_as
from .hashcat_request import HashcatStep


def hashcat_step_constructor(loader, node):
    value = loader.construct_mapping(node, deep=True)
    return parse_obj_as(HashcatStep, value)


def hashcat_step_loader():
    loader = yaml.SafeLoader
    loader.add_constructor("!hashcatstep", hashcat_step_constructor)
    return loader
