# Defines transaction log behavior (append-only)

from abc import ABC, abstractmethod
from typing import Dict, Any


class LogStoreContract(ABC):
    """
    Contract for append-only transaction log storage.
    """


    @abstractmethod
    def write_entry(self, entry: Dict[str, Any]) -> None:
        """
        Persist a transaction log entry.


        Must be atomic and append-only.
        """

        pass

    @abstractmethod
    def read_entry(self, version: int) -> Dict[str, Any]:
        """Read a specific log version."""

        pass
    