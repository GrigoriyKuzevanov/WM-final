__all__ = (
    "Role",
    "roles_users_association",
    "Structure",
    "roles_structures_association",
    "Relation",
)

from .relation import Relation
from .role import Role
from .role import association_table as roles_users_association
from .structure import Structure
from .structure import association_table as roles_structures_association
