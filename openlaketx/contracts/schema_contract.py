# Defines schema enforcement expectations.

from abc import ABC, abstractmethod
from typing import Dict, Any


class SchemaContract(ABC):
    """
    Contract for schema validation and evolution rules.
    """


    @abstractmethod
    def validate(self, schema: Dict[str, Any]) -> None:
        """Validate schema compatibility."""

        pass

    @abstractmethod
    def evolve(self, new_schema: Dict[str, Any]) -> None:
        """
        Apply allowed schema evolution rules.


        Breaking changes must be rejected
        """

        pass
    