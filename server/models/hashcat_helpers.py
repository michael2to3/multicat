from .hashcat_request import Step


def get_unique_name_hashcatrules(session, desired_name):
    counter = 1
    unique_name = desired_name
    existing_names = (
        session.query(Step.name)
        .filter(Step.name.like(f"{desired_name}%"))
        .all()
    )
    existing_names = set(name[0] for name in existing_names)

    while unique_name in existing_names:
        unique_name = f"{desired_name}{counter}"
        counter += 1

    return unique_name
