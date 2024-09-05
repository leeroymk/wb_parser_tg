from aiogram import Router, exceptions
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.bot.services import check_valid_url, get_user_data
from app.bot.state import Form
from app.db.db_mgmt import (
    add_item,
    add_user,
    find_item_by_url,
    format_tracked_items,
    get_tracked_items_for_user,
    remove_item_for_user,
    track_item_for_user,
    update_product_data_in_db,
)
from app.bot.lexicon import LEXICON_RU
from app.parser import parser


router = Router()


# Обработка команды /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    user_data = get_user_data(message)
    await message.answer(text=LEXICON_RU["/start"])
    return add_user(user_data)


# Обработка команды /help
@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU["/help"])


# Обработка команды /list
@router.message(Command(commands="list"))
async def process_list_command(message: Message):
    user_id = message.from_user.id
    tracked_items = get_tracked_items_for_user(user_id)
    response_message = format_tracked_items(tracked_items)
    await message.answer(response_message, disable_web_page_preview=True)


# Обработка команды /add
@router.message(Command(commands="add"))
async def process_add_command(message: Message, state: FSMContext):
    await state.set_state(Form.waiting_for_add_url)
    await message.answer(text=LEXICON_RU["state_add"])


# Обработка входящих сообщений команды /add
@router.message(Form.waiting_for_add_url)
async def process_add_url(message: Message, state: FSMContext):
    url = message.text
    if not check_valid_url(url):
        await message.answer(text=LEXICON_RU["invalid_url"])
        return

    item_id = add_item(url)
    user_id = message.from_user.id
    track_item_for_user(user_id, item_id)
    await state.clear()

    await message.answer(text=LEXICON_RU["valid_url"])


# Обработка команды /remove
@router.message(Command(commands="remove"))
async def process_remove_command(message: Message, state: FSMContext):
    await state.set_state(Form.waiting_for_remove_url)
    await message.answer(text=LEXICON_RU["state_remove"])


# Обработка входящих сообщений для команды /remove
@router.message(Form.waiting_for_remove_url)
async def process_remove_url(message: Message, state: FSMContext):
    url = message.text
    if not check_valid_url(url):
        await message.answer(text=LEXICON_RU["invalid_url"])
        return

    item = find_item_by_url(url)
    if not item:
        await message.answer(text=LEXICON_RU["item_not_found"])
        return

    item_id = item["_id"]
    user_id = message.from_user.id

    remove_item_for_user(user_id, item_id)

    await state.clear()
    await message.answer(text=LEXICON_RU["item_removed"])


# Обработка ручного запуска парсинга /price
@router.message(Command(commands="price"))
async def process_price_command(message: Message):
    user_id = message.from_user.id
    try:
        if get_tracked_items_for_user(user_id):
            await message.answer(text="Парсинг запущен...")
            product_data = await parser.main(user_id)
            update_product_data_in_db(product_data)
            await message.answer(text="Парсинг завершен успешно! Данные обновлены.")
        else:
            await message.answer(text="Добавьте товары для отслеживания")
    except exceptions.TelegramNetworkError:
        await message.answer(text="Произошла ошибка сети. Пожалуйста, попробуйте еще раз позже.")
