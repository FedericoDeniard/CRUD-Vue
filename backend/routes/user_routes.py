from flask import Blueprint, request, jsonify
from models.user_model import User
from services.users.user_utils import convert_user
from services.users.user_service import create_user, delete_user, get_user, modify_user
from config import users
from schemas.response import Response


user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/new_user', methods=['POST'])
def add_user():
    user_data = request.get_json()
    try:
        transformed_data = convert_user(user_data)
        user = User(**transformed_data)
    except Exception as err:
        response = Response("error", 400, error={"error": str(err)})
        return response.to_dict(), 400
    result, status = create_user(user)  
    response = Response("success" if status == 201 else "error", status, data=result)
    return response.to_dict(), status

@user_blueprint.route('/user/<user_id>', methods=['GET'])
def get_user_route(user_id):
    user, status = get_user(user_id)
    response = Response("success" if status == 200 else "error", status, data=user)
    return response.to_dict(), status

@user_blueprint.route("/delete_user/<user_id>", methods=["DELETE"])
def delete_user_route(user_id):
    result, status = delete_user(user_id)
    response = Response("success" if status == 200 else "error", status, data=result)
    return response.to_dict(), status

@user_blueprint.route("/users/<user_id>/edit", methods=["PUT"])
def edit_user_route(user_id):
    user_data = request.get_json()
    try:
        transformed_data = convert_user(user_data)
    except Exception as err:
        response = Response("error", 400, error={"error": str(err)})
        return response.to_dict(), 400
    result, status = modify_user(user_id, transformed_data)
    response = Response("success" if status == 200 else "error", status, data=result)
    return response.to_dict(), status

@user_blueprint.route("/users", methods=["GET"])
def get_users():
    user_list =  users.find({}, {"password": 0}).to_list(length=None)
    for user in user_list:
        user["_id"] = str(user["_id"])
    response = Response("success", 200, data=user_list)
    return response.to_dict(), 200