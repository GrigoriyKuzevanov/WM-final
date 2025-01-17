from fastapi import HTTPException, status

RelationAlreadyExists = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Relation already exists"
)


RelationNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Relation not found"
)


RelationForNotYourStructure = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Can't do this action. Not your structure's relation",
)
