from models.user_model import User, UserPreferences
from datetime import datetime

def get_roles(user_data: User):
    roles = []
    if user_data["is_user_admin"]:
            roles.append("admin")
    if user_data["is_user_manager"]:
        roles.append("manager")
    if user_data["is_user_tester"]:
        roles.append("tester")
    return roles

def convert_to_timestamp(iso_string: str):
     timestamped = datetime.fromisoformat(iso_string.replace('Z', '+00:00')).timestamp()
     return timestamped

def convert_user(user_data: dict):
    try:
        user_preferences = UserPreferences(timezone=user_data["user_timezone"])
        transformed_data = {
            "username": user_data["user"],
            "password": user_data["password"],
            "roles": get_roles(user_data),
            "preferences": user_preferences.to_dict(),
            "active": user_data["is_user_active"],
            "created_ts": convert_to_timestamp(user_data["created_at"])
        }
        return transformed_data
    except KeyError as err:
        raise KeyError(f"Missing required field: {str(err)}")
    except ValueError as err:
        raise ValueError(f"Invalid value for field: {str(err)}")
    except Exception as err:
        raise Exception(f"Unexpected error during user conversion: {str(err)}")
