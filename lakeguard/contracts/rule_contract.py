# Defines data quality rule expectations.


from abc import ABC, abstractmethod
from typing import Any


class RuleContract(ABC):
    """
    Contract for a single data quality or SLA rule.
    """


    @abstractmethod
    def evaluate(self, dataset: Any) -> bool:
        """
        Evaluate rule against dataset.


        Returns True if rule passes
        """

        pass

    