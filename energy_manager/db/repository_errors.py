class UnauthorizedError(Exception):
    def __init__(self, site_id: int, user_id: int) -> None:
        super().__init__(f"User {user_id} cannot operate on site {site_id}.")


class EntityNotFoundError(Exception):
    def __init__(self, name: str, id: int | None) -> None:
        super().__init__(f"Entity {name} with ID {id} not found.")
