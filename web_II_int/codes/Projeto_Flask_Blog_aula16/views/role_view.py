from models import Role


class RoleView:
    @staticmethod
    def response(role):
        return {
            "id": role.id,
            "name": role.name
        }

    @staticmethod
    def list_response(roles: list[Role]):
        return [RoleView.response(role) for role in roles]
