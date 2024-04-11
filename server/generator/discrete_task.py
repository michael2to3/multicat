import logging
from typing import List

from schemas import AttackMode, HashcatStep
from schemas.keyspaces import KeyspaceBase, KeyspaceStraightSchema

logger = logging.getLogger(__name__)


class KeyspaceGenerator:
    @staticmethod
    def generate_tasks(step: HashcatStep) -> List[KeyspaceBase]:
        logger.info("Generating discrete tasks for step: %s", step.model_dump())
        match step.options.attack_mode:
            case AttackMode.DICTIONARY:
                return KeyspaceGenerator._straight(step)
            case _:
                raise NotImplementedError("Not implemented")

    @staticmethod
    def _straight(step: HashcatStep) -> List[KeyspaceBase]:
        tasks: List[KeyspaceBase] = []
        if not step.rules:
            tasks.extend(
                KeyspaceStraightSchema(
                    attack_mode=step.options.attack_mode,
                    value=0,
                    wordlist1=wordlist,
                    rule="",
                )
                for wordlist in step.wordlists
            )
        else:
            for wordlist in step.wordlists:
                for rule in step.rules:
                    tasks.append(
                        KeyspaceStraightSchema(
                            attack_mode=step.options.attack_mode,
                            value=0,
                            wordlist1=wordlist,
                            rule=rule,
                        )
                    )
        return tasks
