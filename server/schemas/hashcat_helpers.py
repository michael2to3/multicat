import yaml

from .discrete_task import HashcatStep


def hashcat_step_constructor(loader, node):
    value = loader.construct_mapping(node, deep=True)
    return HashcatStep(**value)


def hashcat_step_loader():
    loader = yaml.SafeLoader
    loader.add_constructor("!hashcatstep", hashcat_step_constructor)
    return loader
