from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from bookbot.lexicon.lexicon import LEXICON
from bookbot.services.file_handling import book


def create_bookmarks_keyboard(*args: int):
    kb_builder = InlineKeyboardBuilder()

    for button in sorted(args):
        kb_builder.row(InlineKeyboardButton(text=f'{button} - {book[button][:100]}', callback_data=str(button)))

    kb_builder.row(*[InlineKeyboardButton(text=LEXICON['edit_bookmarks_button'], callback_data='edit_bookmarks'),
                     InlineKeyboardButton(text=LEXICON['cancel'], callback_data='cancel')])

    return kb_builder.as_markup()


def edit_bookmarks_keyboard(*args: int):
    kb_builder = InlineKeyboardBuilder()

    for button in sorted(args):
        kb_builder.row(InlineKeyboardButton(text=f'{LEXICON["del"]}{button} - {book[button][:100]}', callback_data=f'{button}del'))

    kb_builder.row(InlineKeyboardButton(text=LEXICON['cancel'], callback_data='canceldel'))

    return kb_builder.as_markup()
