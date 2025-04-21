from enum import Enum

class Priority(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
   
    def __lt__(self, other):
        """ Define less than for priority comparison (CAT_1 > CAT_2 > ...) """

        if self.__class__ is other.__class__:
            return list(self.__class__).index(self) < list(other.__class__).index(other)
        return NotImplemented 

    def __gt__(self, other):
        """ Define greater than for priority comparison """

        if self.__class__ is other.__class__:
            return list(self.__class__).index(self) > list(other.__class__).index(other)
        return NotImplemented
       