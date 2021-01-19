import enum


@enum.unique
class Role(enum.Enum):
    ACCOUNTS = 0
    EQUIPMENT = 1

    @staticmethod
    def all():
        all_roles = set()
        for role in Role:
            all_roles.add(role)

        return all_roles
