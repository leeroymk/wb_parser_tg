from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon import LEXICON_RU


button_list = KeyboardButton(text=LEXICON_RU["/list"])
button_add = KeyboardButton(text=LEXICON_RU["/add"])
button_remove = KeyboardButton(text=LEXICON_RU["/remove"])
button_price = KeyboardButton(text=LEXICON_RU["/price"])

kb_builder = ReplyKeyboardBuilder()

kb_builder.row(button_list, button_add, button_remove, button_price, width=2)
