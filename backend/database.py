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


# ✅ ADD THIS: initialize hardware safely
def init_hardware(db):
    hardware = access_hardware(db)

    hardware.update_one(
        {"hardware_set": "HWSet1"},
        {
            "$setOnInsert": {
                "hardware_set": "HWSet1",
                "capacity": 100,
                "availability": 100
            }
        },
        upsert=True
    )

    hardware.update_one(
        {"hardware_set": "HWSet2"},
        {
            "$setOnInsert": {
                "hardware_set": "HWSet2",
                "capacity": 100,
                "availability": 100
            }
        },
        upsert=True
    )


# optional runner
def main():
    cluster = setup_database()
    db = access_db(cluster)
    init_hardware(db)
    print("Hardware initialized (if not already present).")


if __name__ == "__main__":
    main()