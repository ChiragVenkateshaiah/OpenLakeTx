# Defines lineage tracking guarantees.


from abc import ABC, abstractmethod
from typing import Dict, Any




class LineageContract(ABC):
    """
    Contract for lineage capture across layers.
    """


    @abstractmethod
    def record(self, source: str, target: str, metadata: Dict[str, Any]) -> None:
        """Record lineage relationship"""

        pass

    