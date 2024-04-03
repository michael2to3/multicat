from schemas import AttackMode, HashcatStep, Steps, HashType, HashcatDiscreteStraightTask

class DiscreteTasksGenerator:
    def __init__(self, model: Steps):
        self.model: Steps = model

    def yield_discrete_tasks_from_step(self, step: HashcatStep):
        # TODO: remove fixed calculation
        step.options.attack_mode = AttackMode.DICTIONARY

        match step.options.attack_mode:
            case AttackMode.DICTIONARY:
                if len(step.rules) == 0:
                    for wordlist in step.wordlists:
                        yield HashcatDiscreteStraightTask(
                            job_id=-1,
                            hash_type=HashType(
                                hashcat_type=-1, human_readable="unnamed"
                            ),
                            hashes=list(),
                            wordlist1=wordlist,
                        )
                else:
                    for wordlist in step.wordlists:
                        for rule in step.rules:
                            yield HashcatDiscreteStraightTask(
                                job_id=-1,
                                hash_type=HashType(
                                    hashcat_type=-1, human_readable="unnamed"
                                ),
                                hashes=list(),
                                wordlist1=wordlist,
                                rule=rule,
                            )

            case _:
                raise NotImplementedError("Not implemented")

    def yield_discrete_tasks(self):
        for step in self.model.steps:
            for task in self.yield_discrete_tasks_from_step(step):
                yield task
