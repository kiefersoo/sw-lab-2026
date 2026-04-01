import pymongo 
from pymongo import MongoClient
import os
from dotenv import load_dotenv


def setup_database():
    load_dotenv(r"backend\.gitignore\.env")    
    cluster = MongoClient(os.getenv("MONGO_URI"))
    return cluster

def access_db(cluster):
   db = cluster["user_database"]
   return db

def access_projects_db(cluster):
    db = cluster["project_database"]
    return db

def access_users(db):
    users = db["users"]
    return users

def access_projects(db):
    projects = db["projects"]
    return projects

def access_hardware_db(cluster):
    db = cluster["hardware_database"]
    return db

def access_hardware(db):
    hardware = db["hardware_collection"]
    return hardware

def main():
    cluster = setup_database()
    hardware_db = access_hardware_db(cluster)
    hardware = access_hardware(hardware_db)
    hardware.insert_one({"name": "HWSet1", "capacity": 100, "available": 100, "checked_out": 0})
    hardware.insert_one({"name": "HWSet2", "capacity": 100, "available": 100, "checked_out": 0})

    













if __name__ == "__main__":
    main()


