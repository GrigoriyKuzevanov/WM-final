from fastapi import HTTPException, status

RoleNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
)


RoleNotFoundForUser = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Not found role for this user"
)


NotTeamAdministrator = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Can't do this action. You're not team administrator",
)


RoleOtherStructure = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Can't do this action. Role from the other team",
)


DeleteYourselfRole = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Can't delete yourself"
)


DeleteOtherTeamRole = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Can't delete role from the other team",
)


AlreadyHaveRole = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Already have a role"
)
