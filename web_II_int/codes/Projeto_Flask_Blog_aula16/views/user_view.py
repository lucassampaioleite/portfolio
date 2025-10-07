from models import User


class UserView:
    @staticmethod
    def response(user: User):
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": {
                "id": user.role_id,
                "name": user.role.name if user.role else None
            }
        }

    @staticmethod
    def list_response(users: list[User]):
        return [UserView.response(user) for user in users]
