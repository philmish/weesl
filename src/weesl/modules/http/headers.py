from enum import Enum

class ContentType(Enum):
    JSON = "application/json"

    def __repr__(self) -> str:
        return f"{self.value}"

class UserAgent(Enum):
    CHROME_WIN = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

    def __repr__(self) -> str:
        return f"{self.value}"
