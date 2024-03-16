from .hashcat_request import StepsModel


def get_unique_name_hashcatrules(session, desired_name):
    counter = 0
    unique_name = desired_name
    while True:
        if not session.query(StepsModel).filter_by(name=unique_name).first():
            return unique_name
        counter += 1
        unique_name = f"{desired_name}{counter}"
