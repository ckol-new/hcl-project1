# author object holds all data around an author of a post
# author object is fully serializable to and from json
class Author:
    def __init__(self, user_name: str, user_id: str, profile_link: str):
        self.user_name = user_name
        self.user_id = user_id
        self.profile_link = profile_link


    def to_dict(self):
        return {
            'user_name': self.user_name,
            'user_id': self.user_id,
            'profile_link': self.profile_link
        }
    @classmethod
    def from_dict(cls, data):
        return cls(
            user_name=data['user_name'],
            user_id=data['user_id'],
            profile_link=data['profile_link']
        )

    def __eq__(self, other):
        if not isinstance(other, Author): return False,
        return {
            self.user_name == other.user_name and
            self.user_id == other.user_id and
            self.profile_link == other.profile_link
        }