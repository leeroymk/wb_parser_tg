import asyncio
import httpx
import random
from urllib.parse import urlparse

from fake_useragent import UserAgent


# Формируем headers
def get_headers():
    return {
        "user-agent": str(UserAgent().random),
        "content-type": "application/json",
        "x-requested-with": "XMLHttpRequest",
    }


def get_size(url: str) -> str | None:
    params = urlparse(url).query.split("&")

    size = None
    for param in params:
        param_list = param.split("=")
        if param_list[0] == "size":
            size = int(param_list[1])
    return size


# Функция для парсинга полученного словаря
def parse(response_dict, size: str | None) -> tuple[str, int]:
    product = response_dict["data"]["products"][0]
    name = product["name"]
    sizes = product["sizes"]
    for i in range(len(sizes)):
        option_id = sizes[i]["optionId"]

        for i, size_data in enumerate(sizes):
            if size is None or option_id == size:
                raw_price = size_data["price"]["total"]
                break

    price = int(raw_price / 100)

    return name, price


# Функция формирует ссылку для запроса
def get_url_for_request(url: str) -> str:
    parsed_url = urlparse(url)
    path_url = parsed_url.path
    try:
        id = path_url.split("/")[2]
    except IndexError:
        print("ошибка в get_url_for_request")
        raise
    template = "https://card.wb.ru/cards/v2/detail?curr=rub&dest=-1257786&nm="
    return template + id


# Асинхронная функция для получения данных по товару с защитой от блокировки
async def get_product_data(url: str, limit: int = 5):
    for attempt in range(limit):
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(url, headers=get_headers())
                r.raise_for_status()
                return r.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                print(f"Получили 429 Too Many Requests, ждём... Попытка {attempt + 1}")
                await asyncio.sleep(5 + random.uniform(1, 3))
            else:
                raise
        except (httpx.RequestError, httpx.TimeoutException) as e:
            print(f"Ошибка запроса: {e}. Попытка {attempt + 1}")
            await asyncio.sleep(2 + random.uniform(1, 2))
    raise Exception(f"Не удалось получить данные после {limit} попыток")
