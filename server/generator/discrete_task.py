import logging
import itertools
from typing import List

from schemas import AttackMode, HashcatDiscreteTask, HashcatStep, HashType
from schemas.keyspaces import KeyspaceBase, KeyspaceStraightSchema

logger = logging.getLogger(__name__)


class DiscreteTasksGenerator:
    @staticmethod
    def generate_tasks(step: HashcatStep) -> HashcatDiscreteTask:
        logger.info("Generating discrete tasks for step: %s", step.model_dump())
        match step.options.attack_mode:
            case AttackMode.DICTIONARY:
                return DiscreteTasksGenerator._generate_straight_tasks(step)
            case _:
                raise NotImplementedError("Not implemented")

    @staticmethod
    def generate_keyspace_tasks(step: HashcatStep) -> List[KeyspaceBase]:
        # TODO: Remove after yaml loading is fixed
        attack_mode = AttackMode.DICTIONARY

        logger.info("Generating keypsace tasks for step: %s", step.model_dump())

        match attack_mode:
            case AttackMode.DICTIONARY:
                return DiscreteTasksGenerator._generate_keyspace_straight_tasks(step)
            case _:
                raise NotImplementedError("Not implemented")

    @staticmethod
    def _generate_straight_tasks(step: HashcatStep) -> List[HashcatDiscreteTask]:
        tasks = []
        if not step.rules:
            tasks.extend(
                HashcatDiscreteTask(
                    job_id=-1,
                    hash_type=HashType(hashcat_type=-1, human_readable="unnamed"),
                    hashes=[],
                    wordlist1=wordlist,
                )
                for wordlist in step.wordlists
            )
        else:
            for wordlist in step.wordlists:
                for rule in step.rules:
                    tasks.append(
                        HashcatDiscreteStraightTask(
                            job_id=-1,
                            hash_type=HashType(
                                hashcat_type=-1, human_readable="unnamed"
                            ),
                            hashes=[],
                            wordlist1=wordlist,
                            rule=rule,
                        )
                    )
        return tasks

    @staticmethod
    def _generate_keyspace_straight_tasks(step: HashcatStep) -> List[KeyspaceBase]:
        tasks = []
        for wordlist, rule in zip(step.wordlists, step.rules or itertools.repeat("")):
            tasks.append(
                KeyspaceStraightSchema(
                    wordlist1=wordlist,
                    rule=rule,
                    value=0,
                )
            )
        return tasks
