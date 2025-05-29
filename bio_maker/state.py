
from typing import TypedDict, Optional
from model.user_profile import UserProfile

class BioGraphState(TypedDict):
    uid: str
    input: str ##  This is the instruction from the user about how to create the bio
    profile: Optional[UserProfile]
    response: Optional[str]