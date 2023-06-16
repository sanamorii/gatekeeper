
class InvalidMinecraftUsername(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)
        
class UnexpectedDatabaseError(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)