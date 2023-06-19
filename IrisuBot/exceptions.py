
class InvalidMinecraftUsername(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)
        
class UnexpectedDatabaseError(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)

class InvalidDatabase(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        
class PlayerAlreadyExists(Exception):
    def __init__(self, username: str) -> None:
        self.message = f"{username} has already been added to the whitelist"
        super().__init__(self.message)
        
class PlayerDoesNotExist(Exception):
    def __init__(self, username :str) -> None:
        self.message = f"{username} does not exist"
        super().__init__(self.message)