from datetime import datetime
from typing import Dict, List
from pymongo import MongoClient, UpdateOne
from bson import ObjectId
from pymongo.errors import BulkWriteError


client = MongoClient("mongodb://root:example@localhost:27017/")

db = client["parser_db"]

users_collection = db["users"]
items_collection = db["items"]


def add_item(url: str) -> ObjectId:
    existing_item = items_collection.find_one({"url": url})
    if existing_item:
        return existing_item["_id"]

    item = {"url": url, "name": "Unnamed Product", "current_price": 0.0, "price_history": []}
    result = items_collection.insert_one(item)
    return result.inserted_id


def add_user(user_data: tuple[int, str, str]) -> ObjectId:
    user_id, full_name, username = user_data
    existing_user = users_collection.find_one({"user_id": user_id})

    if existing_user:
        print(f"Пользователь с id {user_id} уже существует")
        return existing_user["_id"]

    user = {
        "user_id": user_id,
        "tracked_item_ids": [],
        "full_name": full_name,
        "username": username,
    }

    result = users_collection.insert_one(user)
    print(f"Пользователь с id {user_id} успешно добавлен")
    return result.inserted_id


def track_item_for_user(user_id: int, item_id: ObjectId) -> None:
    user = users_collection.find_one({"user_id": user_id})
    if not user:
        print(f"Пользователь с user_id {user_id} не найден.")
        return

    item = items_collection.find_one({"_id": item_id})
    if not item:
        print(f"Товар с item_id {item_id} не найден.")
        return

    result = users_collection.update_one(
        {"user_id": user_id}, {"$addToSet": {"tracked_item_ids": item_id}}
    )

    if result.modified_count == 0:
        print("Ничего не обновлено. Возможно, товар уже отслеживается.")
    else:
        print(f"Товар с id {item_id} успешно добавлен в список отслеживаемых товаров")


def update_item_data(item_id: ObjectId, parsed_data: dict) -> None:
    items_collection.update_one(
        {"_id": item_id},
        {
            "$set": {
                "product_id": parsed_data["product_id"],
                "name": parsed_data["name"],
                "current_price": parsed_data["price"],
            },
            "$push": {"price_history": parsed_data["price"]},
        },
    )


def get_tracked_items_for_user(user_id: int) -> List[Dict[str, any]]:
    user = users_collection.find_one({"user_id": user_id})

    if not user or "tracked_item_ids" not in user or not user["tracked_item_ids"]:
        return []

    tracked_items = items_collection.find({"_id": {"$in": user["tracked_item_ids"]}})
    return list(tracked_items)


def format_tracked_items(items: List[Dict[str, any]]) -> str:
    if not items:
        return "Список отслеживания товаров пуст"

    response_message = "Список товаров для отслеживания:\n\n"
    for item in items:
        name = item.get("name", "Unnamed Product")
        price = item.get("current_price", "Price not available")
        url = item.get("url", "Wrong URL")
        response_message += f"{name}: {price} руб.\n{url}\n\n"

    return response_message


def find_item_by_url(url: str):
    item = items_collection.find_one({"url": url})
    return item


def remove_item_for_user(user_id: int, item_id: ObjectId) -> None:
    users_collection.update_one({"user_id": user_id}, {"$pull": {"tracked_item_ids": item_id}})


def get_url_list(user_id: int) -> List[str]:
    user = users_collection.find_one({"user_id": user_id})
    tracked_items = items_collection.find({"_id": {"$in": user["tracked_item_ids"]}})
    tracked_urls = [item["url"] for item in tracked_items]
    return tracked_urls


def update_product_data_in_db(product_data: dict[str, dict[str, str]]):
    operations = []
    for name, data in product_data.items():
        url = data.get("url", "unknown_url")

        operations.append(
            UpdateOne(
                {"url": url},
                {
                    "$set": {"current_price": int(data["price"]), "name": name, "url": url},
                    "$push": {
                        "price_history": {"price": int(data["price"]), "date": datetime.now()}
                    },
                },
                upsert=True,
            )
        )

    if operations:
        try:
            result = items_collection.bulk_write(operations)
            print(f"Обновлено: {result.modified_count}. Вставлено новых: {result.upserted_count}.")
        except BulkWriteError as bwe:
            print(f"Ошибка массового обновления: {bwe.details}")
    else:
        print("Нет данных для обновления.")
