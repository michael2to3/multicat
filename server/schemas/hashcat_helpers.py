from ruamel.yaml import YAML


from .discrete_task import StraightStep, CombinatorStep, MaskStep, HybridStep


def hashcat_step_loader():
    CLASSES = [
        StraightStep,
        CombinatorStep,
        MaskStep,
        HybridStep,
    ]

    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)

    for x in CLASSES:
        yaml.register_class(x)

    return yaml
