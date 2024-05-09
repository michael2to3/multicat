import schemas
from schemas import KeyspaceBase
from visitor.hashcatstep_keyspace_tasks import HashcatStepKeyspaceVisitor


class KeyspaceTasksGenerator:
    @staticmethod
    def generate_keyspace_tasks(model: schemas.Steps) -> list[KeyspaceBase]:
        tasks: list[KeyspaceBase] = []

        def callback(_tasks: list[KeyspaceBase]):
            tasks.extend(_tasks)

        generator = HashcatStepKeyspaceVisitor(callback)
        for step in model.steps:
            step.accept(generator)
        return tasks
