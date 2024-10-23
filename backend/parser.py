from config import users, test_connection
from services.users.user_utils import convert_user
from schemas.user_schema import  UserSchema
from models.user_model import User
from services.users.user_service import create_user
import json

def load_users_from_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)
    
def parse_data(data):
    data = load_users_from_file('data.json')
    results = []
    errors = []
    for user in data.get("users", []):
        try:
            transformed_data = convert_user(user)
            user_schema = UserSchema()
            schema_errors = user_schema.validate(transformed_data)
            if schema_errors:
                    errors.append({"user": user.get("user", "unknown"), "errors": schema_errors})
                    continue
            
            user_instance = User(**transformed_data)
            result = create_user(user_instance)
            results.append(result)
        except Exception as err:
            errors.append({"user": user.get("user", "unknown"), "error": str(err)})
        
    if errors:
        print("Errors", errors)
    else:
        print("Users created successfully:", results)

if __name__ == "__main__":
    parse_data('./data.json')
    