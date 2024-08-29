from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from lexicon import LEXICON_RU
from services import get_cart


router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU["/start"])


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands="/help"))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU["/help"])
    await message.reply(text="ПАМАГИТИ")


# Этот хэндлер срабатывает на команду /list
@router.message(Command(commands="/list"))
async def process_list_command(message: Message):
    list_answer: str = get_cart()
    await message.answer(text=f"Тут будет список отслеживаемых товаров {list_answer}")


# Этот хэндлер срабатывает на команду /add
@router.message(Command(commands="/add"))
async def process_add_command(message: Message):
    # handle_message
    await message.answer(text="Тут будет сообщение о том что товар добавлен")


# Этот хэндлер срабатывает на команду /remove
@router.message(Command(commands="/remove"))
async def process_remove_command(message: Message):
    # handle_message()
    await message.answer(text="Тут будет сообщение о том что товар удален")


# Этот хэндлер срабатывает на команду /price
@router.message(Command(commands="/price"))
async def process_price_command(message: Message):
    # parse()
    await message.answer(text="Подождите, идет парсинг товаров...")


@router.message()
async def send_answer(message: Message):
    await message.answer(text=str(type(message)))
