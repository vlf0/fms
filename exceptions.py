class TagNotFindError(Exception):

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message: str = message

    def __str__(self) -> str:
        return f'Was caught {self.__class__.__name__}! {self.message}'
