import importlib
import os
import pkgutil

__all__ = []


def import_recursive(package_name):
    package = importlib.import_module(package_name)
    package_file = package.__file__
    if package_file is None:
        return
    current_dir = os.path.dirname(package_file)
    for loader, module_name, is_pkg in pkgutil.walk_packages([current_dir]):
        if module_name != "__init__":
            module_full_name = f"{package_name}.{module_name}"
            if is_pkg:
                import_recursive(module_full_name)
            else:
                module = importlib.import_module(module_full_name)
                for attribute_name in dir(module):
                    if not attribute_name.startswith("_"):
                        globals()[attribute_name] = getattr(module, attribute_name)
                        __all__.append(attribute_name)


current_package_name = __name__
if __name__ == "__main__":
    current_package_name = __name__.rpartition(".")[0]

import_recursive(current_package_name)
