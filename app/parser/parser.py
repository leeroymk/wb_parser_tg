import asyncio
import random
from app.db.db_mgmt import get_url_list
from app.parser.services import get_product_data, get_size, get_url_for_request, parse


# Основная асинхронная функция
async def main(user_id: int):
    raw_url_list = get_url_list(user_id)

    tasks = []

    for raw_url in raw_url_list:
        await asyncio.sleep(random.uniform(1, 3))
        url = get_url_for_request(raw_url)
        task = get_product_data(url)
        tasks.append((task, raw_url))

    results = await asyncio.gather(*(task for task, _ in tasks))

    product_data = {}

    for result, raw_url in zip(results, (raw_url for _, raw_url in tasks)):
        size = get_size(raw_url)
        name, price = parse(result, size)
        product_data[name] = {"price": price, "url": raw_url}
        print(f"Товар: {name}, Цена: {price} руб.")

    return product_data


if __name__ == "__main__":
    asyncio.run(main())
