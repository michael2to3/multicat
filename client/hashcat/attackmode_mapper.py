from schemas import AttackMode


class AttackModeMapper:
    _mapping: dict[AttackMode, int] = {
        AttackMode.DICTIONARY: 0,
        AttackMode.COMBINATOR: 1,
        AttackMode.MASK: 3,
        AttackMode.HYBRID_DICT_MASK: 6,
        AttackMode.HYBRID_MASK_DICT: 7,
    }

    @classmethod
    def to_int(cls, attack_mode: AttackMode) -> int | None:
        return cls._mapping.get(attack_mode)

    @classmethod
    def from_int(cls, mode_int: int) -> AttackMode:
        for mode, val in cls._mapping.items():
            if val == mode_int:
                return mode
        raise ValueError(f"Invalid attack mode integer: {mode_int}")
