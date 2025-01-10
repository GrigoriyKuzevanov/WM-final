from typing import TypeVar

from structures.adapters.relation_adapter import RelationAdapter
from structures.adapters.role_adapter import RoleAdapter
from structures.exceptions.relation import (
    RelationAlreadyExists,
    RelationForNotYourStructure,
    RelationNotFound,
)
from structures.exceptions.role import RoleNotFound
from structures.models import Relation
from structures.schemas.realtion import RelationCreate

RNM = TypeVar("RNM", bound=Relation)


class RelationService:
    """Relations managing service."""

    def __init__(self, relations_adapter: RelationAdapter) -> None:
        """Inits RelationService.

        Args:
            relations_adapter (RelationAdapter): Adapter to interacting with database
        """

        self.relations_adapter = relations_adapter

    async def create_relation(
        self,
        roles_adapter: RoleAdapter,
        relation_create_schema: RelationCreate,
        structure_id: int,
    ) -> RNM:
        """Creates a new relation.

        Args:
            roles_adapter (RoleAdapter): Adapter for interactive with database
            relation_create_schema (RelationCreate): Schema to create new relation
            structure_id (int): Structure id

        Raises:
            RoleNotFound: If roles not found
            RelationAlreadyExists: If relation with these id's already exists

        Returns:
            Relation: Created relation model
        """
        superior_role = await roles_adapter.read_item_by_id(
            relation_create_schema.superior_id
        )
        subordinate_role = await roles_adapter.read_item_by_id(
            relation_create_schema.subordinate_id
        )

        if not superior_role or not subordinate_role:
            raise RoleNotFound

        if (
            superior_role.structure_id != structure_id
            or subordinate_role.structure_id != structure_id
        ):
            raise RelationForNotYourStructure

        if await self.relations_adapter.get_relation_by_superior_id_and_suboridinate_id(
            superior_id=relation_create_schema.superior_id,
            subordinate_id=relation_create_schema.subordinate_id,
        ):
            raise RelationAlreadyExists

        return await self.relations_adapter.create_realtion_with_users_structure_id(
            relation_create_schema, structure_id
        )

    async def delete_relation(self, relation_id: int, structure_id: int) -> None:
        """Deletes relation by provided id.

        Args:
            relation_id (int): Relation id
            structure_id (int): Structure id
        """

        relation_to_delete = await self.relations_adapter.read_item_by_id(relation_id)

        if not relation_to_delete:
            raise RelationNotFound

        if not relation_to_delete.structure_id == structure_id:
            raise RelationForNotYourStructure

        await self.relations_adapter.delete_item(relation_to_delete)
