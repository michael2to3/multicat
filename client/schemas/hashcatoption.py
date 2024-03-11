import enum


class HashcatOption(enum.Enum):
    HASH_TYPE = "-m"
    ATTACK_MODE = "-a"
    WORDLIST_FILE = "--wordlist"
    MASK = "--mask"
    RULES_FILE = "-r"
    QUIET = "--quiet"
    STATUS = "--status"
    STATUS_TIMER = "--status-timer"
    MACHINE_READABLE = "--machine-readable"
    OUTFILE = "-o"
    OUTFILE_FORMAT = "--outfile-format"
    USERNAME = "--username"
    SESSION = "--session"
    RESTORE = "--restore"
    POTFILE_PATH = "--potfile-path"
