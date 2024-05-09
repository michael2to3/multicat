from celery import signature, chord

import schemas
import models

from hashcat_distributor.keyspace_tasks_generator import KeyspaceTasksGenerator


class BruteforceTasksGenerator:
    @staticmethod
    def send_bruteforce_tasks(
        steps: schemas.Steps, job: models.Job, hash_type: models.HashType
    ):
        tasks = []
        for keyspace in KeyspaceTasksGenerator.generate_keyspace_tasks(steps):
            task_data = schemas.HashcatDiscreteTask(
                job_id=job.id,
                hash_type=schemas.HashType(
                    hashcat_type=hash_type.hashcat_type,
                    human_readable=hash_type.human_readable,
                ),
            )
            tasks.append(
                signature(
                    "client.run_hashcat",
                    args=(task_data.model_dump(), keyspace.model_dump()),
                )
            )

        callback = signature(
            "server.bruteforce_finished",
            queue="server",
            kwargs={
                "job_id": job.id,
            },
        )

        chord(tasks)(callback)
