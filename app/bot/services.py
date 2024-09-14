from aiogram.types import Message
import re


def check_valid_url(url: str) -> bool:
    valid_beginnings = ("https://www.wildberries.ru/catalog/", "https://wildberries.ru/catalog/")
    return url.startswith(valid_beginnings)


def get_user_data(message: Message) -> tuple[int, str, str]:
    user_id: int = message.from_user.id
    full_name: str = message.from_user.full_name
    username: str = message.from_user.username
    return user_id, full_name, username


def get_url(text_message: str) -> str:
    url_pattern = r"https?://[^\s]+"
    url = re.search(url_pattern, text_message).group()
    return url
