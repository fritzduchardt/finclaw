import atexit
import json
import logging
import os
from typing import Any

from pymongo import MongoClient

client = MongoClient(
    f"mongodb://{os.environ.get('MONGO_HOST', 'localhost')}:{os.environ.get('MONGO_PORT', 27017)}"
)
db = client["finclaw"]


@atexit.register
def close_mongo_client():
    client.close()


def insert(collection: str, payload: str) -> bool:
    logging.info(f"Inserts into collection: {collection}, payload: {payload}")

    try:
        collection = db[collection]
        collection.insert_many(json.loads(payload))
        return True

    except Exception as e:
        logging.error(f"Mongo failure: {e}")
        return False

def update(collection: str, filter_json: str, update_json: str) -> bool:
    logging.info(f"Updates into collection: {collection}, filter: {filter_json}, update:  {update_json}")

    try:
        collection = db[collection]
        collection.update_many(json.loads(filter_json), json.loads(update_json))
        return True

    except Exception as e:
        logging.error(f"Mongo failure: {e}")
        return False


def read(collection: str, filters: str) -> list[dict[str, Any]] | None:
    logging.info(f"Reading stats for: {collection} with: {filters}")
    try:
        collection = db[collection]
        results = collection.find(json.loads(filters))
        result_list = []
        for result in results:
            result.pop("_id", None)
            result_list.append(result)
        return result_list

    except Exception as e:
        logging.error(f"Mongo failure: {e}")
        return None


def delete(collection: str, filters: str) -> int:
    logging.info(f"Deleting stats for: {collection} with: {filters}")
    try:
        collection = db[collection]
        result = collection.delete_many(json.loads(filters))
        return int(result.deleted_count)

    except Exception as e:
        logging.error(f"Mongo failure: {e}")
        return 0
