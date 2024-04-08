import logging

from schemas import AttackMode, HashcatDiscreteTask, HashcatStep, HashType

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
    def _generate_straight_tasks(step: HashcatStep) -> HashcatDiscreteTask:
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
