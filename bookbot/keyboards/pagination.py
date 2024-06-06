from aiogram.utils.keyboard import (
    InlineKeyboardBuilder, InlineKeyboardButton)
from bookbot.lexicon.lexicon import LEXICON


def create_pagination_keyboard(*buttons):
    inline_kb = InlineKeyboardBuilder()
    lst_of_buttons = [InlineKeyboardButton(text=LEXICON[button] if button in LEXICON else button, callback_data=button) for button in buttons]

    inline_kb.row(*lst_of_buttons)
    return inline_kb.as_markup()
