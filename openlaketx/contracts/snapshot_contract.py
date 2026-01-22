# Defines visibility and versioning rules

from abc import ABC, abstractmethod
from typing import Dict, Any


class SnapshotContract(ABC):
    """
    Contract representing an immutable snapshot of table state.
    """


    @abstractmethod
    def snapshot_id(self) -> int:
        """Return the snapshot version identifier."""

        pass


    @abstractmethod
    def metadata(self) -> Dict[str, Any]:
        """Return snapshot-level metadata."""

        pass


    @abstractmethod
    def is_visible(self) -> bool:
        """Determine if snapshot is safe for readers."""

        pass