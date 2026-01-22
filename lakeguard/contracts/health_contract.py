# Defines table health semantics


from abc import ABC, abstractmethod
from enum import Enum



class HealthState(Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"


class HealthContract(ABC):
    """
    Contract for tracking dataset health.
    """


    @abstractmethod
    def current_state(self) -> HealthState:
        """
        Return current health state.
        """

        pass

    @abstractmethod
    def mark_unhealthy(self, reason: str) -> None:
        """Mark dataset as unhealthy."""

        pass

    