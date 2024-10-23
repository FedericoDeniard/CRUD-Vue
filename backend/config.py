from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("DATABASE_URI") 



client = MongoClient(uri, server_api=ServerApi('1'))

db = client["deepersystem"]
users = db.users

def create_users_table():
    users.create_index([("username", 1)], unique=True)


def test_connection():
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(f"Connection failed: {e}")

create_users_table()
test_connection()