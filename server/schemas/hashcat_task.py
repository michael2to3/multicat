from pydantic import BaseModel, UUID5

from .hashcat_request import HashcatStep


class HashcatDiscreteTask(BaseModel):
    owner_id: UUID5
    step: HashcatStep
