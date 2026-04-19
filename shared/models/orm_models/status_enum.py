from enum import Enum

class Status(Enum):
    """
    Enumeration of lifecycle states for ORM entities.
    
    Values
    ------
    - ACTIVE: The entity is active and operational.
    - BLOCKED: The entity is blocked and should not be used. (e.g., due to policy violations or security concerns)
    - ARCHIVED: The entity is archived and no longer active. It may be retained for historical or auditing purposes.
    - EXPIRED: The entity has expired and is no longer valid. (e.g., a quota that has reached its expiration date)
    """

    ACTIVE = "active"
    BLOCKED = "blocked"
    ARCHIVED = "archived"
    EXPIRED = "expired"