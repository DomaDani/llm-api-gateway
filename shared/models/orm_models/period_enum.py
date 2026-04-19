from enum import Enum

class Period(Enum):
    """
    Enumeration of supported quota reset periods.
    
    Values
    ------
    - MINUTE
    - HOUR
    - DAY
    - WEEK
    - MONTH
    """

    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"