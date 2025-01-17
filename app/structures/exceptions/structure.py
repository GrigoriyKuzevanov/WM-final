from fastapi import HTTPException, status

StructureNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Structure not found"
)
