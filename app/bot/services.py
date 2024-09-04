def check_valid_url(message: str) -> bool:
    return message.lower().strip().startswith("https://www.wildberries.ru/catalog/")
