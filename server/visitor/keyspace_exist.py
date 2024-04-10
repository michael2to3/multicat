from typing import TYPE_CHECKING, Callable

from sqlalchemy.orm import scoped_session

from models import (
    Keyspace,
    KeyspaceCombinator,
    KeyspaceHybrid,
    KeyspaceMask,
    KeyspaceStraight,
)

if TYPE_CHECKING:
    from schemas import (
        KeyspaceBase,
        KeyspaceCombinatorSchema,
        KeyspaceHybridSchema,
        KeyspaceMaskSchema,
        KeyspaceStraightSchema,
    )

from .ikeyspace import IKeyspaceVisitor


class KeyspaceExistVisitor(IKeyspaceVisitor):
    _session: scoped_session
    _callback: Callable[[bool], None]

    def __init__(self, session: scoped_session, callback: Callable[[bool], None]):
        self._session = session
        self._callback = callback

    def configure_straight(self, schema: "KeyspaceStraightSchema"):
        self._make_query(KeyspaceStraight, schema)

    def configure_combinator(self, schema: "KeyspaceCombinatorSchema"):
        self._make_query(KeyspaceCombinator, schema)

    def configure_mask(self, schema: "KeyspaceMaskSchema"):
        self._make_query(KeyspaceMask, schema)

    def configure_hybrid(self, schema: "KeyspaceHybridSchema"):
        self._make_query(KeyspaceHybrid, schema)

    def _make_query(self, model: "Keyspace", schema: "KeyspaceBase"):
        keyspace_data = {
            k: v for k, v in schema.model_dump(exclude={"value", "attack_mode"}).items()
        }
        query = self._session.query(model).filter_by(**keyspace_data)
        self._callback(query.first() is not None)
