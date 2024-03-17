import uuid


class UUIDGenerator:
    _namespace = uuid.NAMESPACE_DNS

    @staticmethod
    def generate(s: str):
        return uuid.uuid5(UUIDGenerator._namespace, s)
