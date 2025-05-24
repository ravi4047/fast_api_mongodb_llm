from pymongo.collection import Collection
## There are lots of stuffs I want to do to target user

"""
There will be 4 types of prompts:
- Fetch user between range 175-180cm or Foot and inches.
    - If feet/inches then we will convert it into cms.
- Fetch user of exactly 180cm height. IN that case, max height is None and range is False
- Fetch user not less than 5 ft 8 inch. In that case, range is True, but max_height in cm is None
- Fetch user less than 6 ft. In that case, min_height is None and range is True.
- Fetch list of 10 users
    - Then we will have list of 1o users name along with the distance.
- 

"""
def fetch_nearby_person_based_on_height(my_uid:str, n:int, height_in_cm: int|None = None, max_height_in_cm:int|None=None, range: bool=False):
    # n means number of person
    pass