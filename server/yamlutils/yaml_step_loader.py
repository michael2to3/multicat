from ruamel.yaml import YAML

from schemas import CombinatorStep, HybridStep, MaskStep, StraightStep


def yaml_step_loader():
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
