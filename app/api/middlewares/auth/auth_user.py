from starlette.authentication import BaseUser
class SimpleUser(BaseUser):
    def __init__(self, user_id):
        self.user_id = user_id

    @property
    def is_authenticated(self) -> bool:
        return True  # pragma: no cover

    @property
    def identity(self) -> int:
        return self.user_id