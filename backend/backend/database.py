import pymongo 
from pymongo import MongoClient
import os
from dotenv import load_dotenv


def setup_database():
    load_dotenv(r"backend\.env")    
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

def main():
    cluster = setup_database()
    db = access_db(cluster)
    users = access_users(db)
    users.insert_one({
    "username": "alskdjlkajsd",
    "password": "WiiSports"
    })    













if __name__ == "__main__":
    main()


