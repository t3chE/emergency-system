from enum import Enum, unique
from functools import total_ordering

@unique  # Ensure no duplicate values
@total_ordering  #  Provides all rich comparison methods if we define __lt__
class Priority(Enum):
    """Enum class for incident priorities, with comparison."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

    _PRIORITY_ORDER = {  # Define explicit order for comparison
        "high": 0,
        "medium": 1,
        "low": 2,
    }

    def __lt__(self, other):
        """Define less than for priority comparison (HIGH < MEDIUM < LOW)."""
        if isinstance(other, Priority):
            return self._PRIORITY_ORDER[self.value] < self._PRIORITY_ORDER[other.value]
        return NotImplemented

    def __str__(self):
        return self.value
    
    def __repr__(self):
        return f"<{self.__class__.__name__}.{self.name}: {self.value}>"

       