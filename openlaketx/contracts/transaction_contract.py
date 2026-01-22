# Defines what a transaction is, not how it's implemented

from abc import ABC, abstractmethod
from typing import Any, Dict


class TransactionContract(ABC):
    """
    Contract for a transactional write operation in OpenLakeTx

    A transaction represents a single atomic intent to mutate table state.
    """


    @abstractmethod
    def begin(self) -> None:
        """Initialize a new transaction context."""

        pass

    @abstractmethod
    def commit(self, metadata: Dict[str, Any]) -> None:

        """
        Atomatically commit the transaction.


        Must guarantee:
        - All or Nothing visibility
        - Snapshot immutability
        """

        pass


    @abstractmethod
    def abort(self, reason: str) -> None:
        """
        Abort the transaction safely.


        Partial writes must never be exposed.
        """

        pass
    