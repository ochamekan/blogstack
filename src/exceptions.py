class AppBaseException(Exception):
    def __init__(self, message: str, error_code: str, status_code: int = 400) -> None:
        self.message: str = message
        self.error_code: str = error_code
        self.status_code: int = status_code
        super().__init__(self.message)
