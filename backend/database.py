import os
from pymongo import MongoClient
from dotenv import load_dotenv


# SETUP CONNECTION
def setup_database():
    load_dotenv()
    cluster = MongoClient(os.getenv("MONGO_URI"))
    return cluster


# MAIN DATABASE (single DB for everything)
def access_db(cluster):
    return cluster["main_database"]


# COLLECTIONS
def access_users(db):
    return db["users"]


def access_projects(db):
    return db["projects"]


def access_hardware(db):
    return db["hardware"]


def access_allocations(db):
    return db["allocations"]


# OPTIONAL: INITIALIZE HARDWARE (run once)
def init_hardware(db):
    hardware = access_hardware(db)

    hardware.update_one(
        {"name": "HWSet1"},
        {"$setOnInsert": {"capacity": 100, "available": 100, "checked_out": 0}},
        upsert=True
    )

    hardware.update_one(
        {"name": "HWSet2"},
        {"$setOnInsert": {"capacity": 100, "available": 100, "checked_out": 0}},
        upsert=True
    )


# RUN THIS FILE TO INITIALIZE DATA
def main():
    cluster = setup_database()
    db = access_db(cluster)
    init_hardware(db)
    print("Database initialized.")


if __name__ == "__main__":
    main()