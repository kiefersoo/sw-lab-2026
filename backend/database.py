import os
from pymongo import MongoClient
from dotenv import load_dotenv


def setup_database():
    load_dotenv()
    return MongoClient(os.getenv("MONGO_URI"))


def access_db(cluster):
    return cluster["hardware_database"]


def access_users(db):
    return db["users"]


def access_projects(db):
    return db["projects"]


def access_hardware(db):
    return db["hardware_collection"]


def access_allocations(db):
    return db["allocations"]