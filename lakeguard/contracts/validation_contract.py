# Defines what validation means, not how it runs.


from abc import ABC, abstractmethod
from typing import Dict, Any



class ValidationContract(ABC):
    """
    Contract for validating a committed snapshot.
    """


    @abstractmethod
    def validate(self, snapshot_id: int) -> Dict[str, Any]:
        """
        Validate a snapshot.


        Returns a structured validation result.
        """

        pass

    