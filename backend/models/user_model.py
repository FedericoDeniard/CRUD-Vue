from dataclasses import dataclass

@dataclass
class UserPreferences:
    timezone: str

    def to_dict(self):
        return {
            "timezone": self.timezone
        }

@dataclass
class User:
    username: str
    password: str
    roles: list[str]
    preferences: UserPreferences
    active: bool
    created_ts: float

