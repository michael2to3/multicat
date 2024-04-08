from abc import ABC, abstractmethod

from schemas import (
    HashcatDiscreteCombinatorTask,
    HashcatDiscreteHybridTask,
    HashcatDiscreteMaskTask,
    HashcatDiscreteStraightTask,
    HashcatDiscreteTask,
    HashcatStep,
    HashType,
)


class HashcatTaskFactory(ABC):
    @abstractmethod
    def create_task(self, step: HashcatStep) -> HashcatDiscreteTask:
        pass


class StraightTaskFactory(HashcatTaskFactory):
    def create_task(self, step: HashcatStep):
        return HashcatDiscreteStraightTask(
            job_id=-1,
            hash_type=HashType(hashcat_type=-1, human_readable="Straight Task"),
            hashes=[],
            wordlist1=step.wordlists[0],
            rule=step.rules[0] if step.rules else "",
        )


class CombinatorTaskFactory(HashcatTaskFactory):
    def create_task(self, step: HashcatStep):
        return HashcatDiscreteCombinatorTask(
            job_id=-1,
            hash_type=HashType(hashcat_type=-1, human_readable="Combinator Task"),
            hashes=[],
            wordlist1=step.wordlists[0],
            wordlist2=step.wordlists[1] if len(step.wordlists) > 1 else "",
            left="",
            right="",
        )


class MaskTaskFactory(HashcatTaskFactory):
    def create_task(self, step: HashcatStep):
        return HashcatDiscreteMaskTask(
            job_id=-1,
            hash_type=HashType(hashcat_type=-1, human_readable="Mask Task"),
            hashes=[],
            mask=step.masks[0],
        )


class HybridTaskFactory(HashcatTaskFactory):
    def create_task(self, step: HashcatStep):
        return HashcatDiscreteHybridTask(
            job_id=-1,
            hash_type=HashType(hashcat_type=-1, human_readable="Hybrid Task"),
            hashes=[],
            wordlist1=step.wordlists[0],
            mask=step.masks[0],
            wordlist_mask=True,
        )
