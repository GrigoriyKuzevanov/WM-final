from fastapi import HTTPException, status

TaskBeforeNow = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Your task datetime is before now"
)


TaskForThisUser = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Can't create task for this user"
)


TasksNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Tasks not found"
)


NotTaskCreator = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Can't do this action. You're not creator of the task",
)


NotTaskAssignee = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Can't do this action. You're not assignee of the task",
)
