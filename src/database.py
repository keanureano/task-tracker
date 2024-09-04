import json
import os

DATABASE = os.getenv("DATABASE", "database.json")


def __create_new_database():
    """Create a new JSON file if it doesn't exist"""
    if not os.path.exists(DATABASE):
        with open(DATABASE, "w") as file:
            json.dump([], file)


def get_all():
    if not os.path.exists(DATABASE):
        __create_new_database()
    with open(DATABASE, "r") as file:
        return json.load(file)


def add(tasks):
    with open(DATABASE, "w") as file:
        json.dump(tasks, file)
