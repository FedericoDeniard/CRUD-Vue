from models.user_model import User
from schemas.user_schema import UserSchema
from config import users
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError
import bcrypt

def create_user(user_data: dict):
    user_schema = UserSchema()
    try:
        validated_user = user_schema.load(user_data.__dict__)

        password = validated_user['password'].encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        validated_user['password'] = hashed_password.decode('utf-8')
        
        result = users.insert_one(validated_user)
        validated_user['_id'] = str(result.inserted_id)
        return {"message": "User created successfully", "user": validated_user}, 201
    except DuplicateKeyError:
        return {
            "error": f"Username: '{validated_user['username']}' already exists."
        }, 400
    except Exception as err:
        return {"error": str(err) }, 400

def delete_users():
    users.delete_many({})

def delete_user(user_id):
    try:
        user_id = ObjectId(user_id)
        user = users.find_one({"_id": user_id})
        if user:
            user_schema = UserSchema()
            users.delete_one({"_id": ObjectId(user_id)})
            return {"deleted_juser": user_schema.dump(user)}, 200
        else:
            return {"error": "User not found"}, 404
    except Exception as err:
        return {"message": str(err)}, 400
    
def get_user(user_id):
    try:
        user_id = ObjectId(user_id)
        user = users.find_one({"_id": user_id})
        if user:
            user_schema = UserSchema()
            return user_schema.dump(user), 200
        else:
            return {"error": "User not found"}, 404
    except Exception as err:
        return {"message": str(err)}, 400

def modify_user(user_id, user_data):
    try:
        user_id = ObjectId(user_id)
        user = users.find_one({"_id": user_id})
        if user:
            if user_data["username"] != user["username"]:
                existing_user = users.find_one({"username": user_data["username"]})
                if existing_user:
                    return {"error": "Username already exists"}, 400
            user_schema = UserSchema()
            validated_user = user_schema.load(user_data)
            users.update_one({"_id": user_id}, {"$set": validated_user})
            return {"message": "User updated successfully", "user": validated_user}, 200
        else:
            return {"error": "User not found"}, 404
    except Exception as err:
        return {"message": str(err)}, 400