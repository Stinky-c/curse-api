class CurseForgeException(Exception):
    """Base for all CurseForge Exceptions"""

    def __init__(self, error: str) -> None:
        self.error = error


class MissingImportException(Exception):
    """Missing one or more imports"""


class APIBannedException(CurseForgeException):
    """Mod has been API banned, and is unreachable"""
