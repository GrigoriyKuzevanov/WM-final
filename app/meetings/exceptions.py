from fastapi import HTTPException, status

MeetingBeforeNow = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Your meeting datetime is before now"
)


MeetingsNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Meetings not found"
)


NotMeetingCreator = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Can't do this action. You're not creator of the meeting",
)


UserAlreadyAdded = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="User already added to meeting"
)


UserNotFoundInMeeting = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="User not found in meeting users"
)
