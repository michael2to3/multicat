from __future__ import annotations

from typing import Annotated, Union

from pydantic import Field, TypeAdapter
from schemas import KeyspaceBase


def get_keyspace_adapter() -> Annotated:
    return TypeAdapter(
        Annotated[Union[*KeyspaceBase.__subclasses__()], Field(discriminator="type")]
    )
