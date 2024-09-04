import httpx
import asyncio
import random
from urllib.parse import urlparse
from services import get_headers


Product = tuple[str, str]


# Функция для получения ID из URL
def parse_id(url: str) -> str:
    parsed_url = urlparse(url)
    path_url = parsed_url.path
    id = path_url.split("/")[2]
    template = "https://card.wb.ru/cards/v2/detail?curr=rub&dest=-1257786&nm="
    return template + id


# Асинхронная функция для получения данных по товару с защитой от блокировки
async def get_product_data(url: str):
    limit = 5
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


# Функция для парсинга полученного словаря
def parse(response_dict) -> Product:
    product = response_dict["data"]["products"][0]
    name = product["name"]
    raw_price = product["sizes"][0]["price"]["total"]
    price = str(int(int(raw_price) / 100))
    return name, price


# Основная асинхронная функция
async def main():
    url_list: list[str] = [
        "https://www.wildberries.ru/catalog/230521217/detail.aspx",
        "https://www.wildberries.ru/catalog/241788121/detail.aspx",
        "https://www.wildberries.ru/catalog/171630341/detail.aspx",
    ]

    tasks = []
    for url in url_list:
        # Добавляем случайную задержку между запросами
        await asyncio.sleep(random.uniform(1, 3))
        tasks.append(get_product_data(parse_id(url)))

    results = await asyncio.gather(*tasks)

    for result in results:
        name, price = parse(result)
        print(f"Product: {name}, Price: {price} RUB")


if __name__ == "__main__":
    asyncio.run(main())
