from aiogram.types import Message


def check_valid_url(url: str) -> bool:
    return url.lower().strip().startswith("https://www.wildberries.ru/catalog/")


def get_user_data(message: Message) -> tuple[int, str, str]:
    user_id: int = message.from_user.id
    full_name: str = message.from_user.full_name
    username: str = message.from_user.username
    return user_id, full_name, username
