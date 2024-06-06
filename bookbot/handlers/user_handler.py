from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from bookbot.lexicon.lexicon import LEXICON
from bookbot.database.database import user_dict_template
from bookbot.services.file_handling import book
from bookbot.keyboards.bookmarks import create_bookmarks_keyboard, edit_bookmarks_keyboard
from bookbot.keyboards.pagination import create_pagination_keyboard
from aiogram.types import CallbackQuery
from bookbot.filters.filters import IsEditCallbackData, IsDigitCallbackData


router_1 = Router()


@router_1.message(CommandStart())
async def start_command(message: Message):
    await message.answer(LEXICON['/start'])


@router_1.message(Command(commands=['help']))
async def help_command(message: Message):
    await message.answer(LEXICON['/help'])


@router_1.message(Command(commands=['beginning']))
async def beginning_command(message: Message):
    user_dict_template['page'] = 1
    await message.answer(book[user_dict_template['page']],
                         reply_markup=create_pagination_keyboard(f'{user_dict_template["page"]}/{len(book)}',
                                                                 'forward'))


@router_1.message(Command(commands=['continue']))
async def continue_command(message: Message):
    if user_dict_template['page'] == 1:
        await message.answer(book[user_dict_template['page']],
                             reply_markup=create_pagination_keyboard(f'{user_dict_template["page"]}/{len(book)}',
                                                                     'forward'))
    elif user_dict_template['page'] == 13:
        await message.answer(book[user_dict_template['page']],
                             reply_markup=create_pagination_keyboard('backward',
                                                                     f'{user_dict_template["page"]}/{len(book)}'))
    else:
        await message.answer(book[user_dict_template['page']],
                             reply_markup=create_pagination_keyboard('backward',
                                                                     f'{user_dict_template["page"]}/{len(book)}',
                                                                     'forward'))


@router_1.message(Command(commands=['bookmarks']))
async def bookmarks_commands(message: Message):
    if len(user_dict_template['bookmarks']) == 0:
        await message.answer(LEXICON['no_bookmarks'])
    else:
        await message.answer(LEXICON['/bookmarks'], reply_markup=create_bookmarks_keyboard(*user_dict_template['bookmarks']))


@router_1.callback_query(F.data == 'forward')
async def next_page(callback: CallbackQuery):
    if user_dict_template['page'] + 1 < 381:
        user_dict_template['page'] += 1
        await callback.message.edit_text(text=book[user_dict_template['page']],
                                         reply_markup=create_pagination_keyboard('backward',
                                                                                 f'{user_dict_template["page"]}/{len(book)}',
                                                                                 'forward'))
    elif user_dict_template['page'] + 1 == len(book):
        user_dict_template['page'] += 1
        await callback.message.edit_text(text=book[user_dict_template['page']],
                                         reply_markup=create_pagination_keyboard('backward',
                                                                                 f'{user_dict_template["page"]}/{len(book)}'))


@router_1.callback_query(F.data == 'backward')
async def previous_page(callback: CallbackQuery):
    if user_dict_template['page'] - 1 > 1:
        user_dict_template['page'] -= 1
        await callback.message.edit_text(text=book[user_dict_template['page']],
                                         reply_markup=create_pagination_keyboard('backward',
                                                                                 f'{user_dict_template["page"]}/{len(book)}',
                                                                                 'forward'))
    elif user_dict_template['page'] - 1 == 1:
        user_dict_template['page'] -= 1
        await callback.message.edit_text(text=book[user_dict_template['page']],
                                         reply_markup=create_pagination_keyboard(f'{user_dict_template["page"]}/{len(book)}',
                                                                                 'forward'))


@router_1.callback_query(lambda x: len(x.data.split('/')) == 2)
async def add_to_bookmarks_command(callback: CallbackQuery):
    user_dict_template['bookmarks'].add(user_dict_template['page'])
    await callback.answer('Страница добавлена в закладки!')


@router_1.callback_query(F.data == 'edit_bookmarks')
async def edit_bookmarks_command(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['edit_bookmarks'],
                                     reply_markup=edit_bookmarks_keyboard(*user_dict_template['bookmarks']))


@router_1.callback_query(F.data == 'canceldel')
async def cancel_bookmarks_command(callback: CallbackQuery):
    await callback.answer('Отмена!')
    await callback.message.edit_text(LEXICON['/bookmarks'],
                                     reply_markup=create_bookmarks_keyboard(*user_dict_template['bookmarks']))


@router_1.callback_query(F.data == 'cancel')
async def cancel_bookmarks_command(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])


@router_1.callback_query(IsDigitCallbackData())
async def go_to_page_command(callback: CallbackQuery):
    user_dict_template['page'] = int(callback.data)
    await callback.message.edit_text(text=book[user_dict_template['page']],
                                     reply_markup=create_pagination_keyboard('backward',
                                                                             f'{user_dict_template["page"]}/{len(book)}',
                                                                             'forward'))


@router_1.callback_query(IsEditCallbackData())
async def go_to_page_command(callback: CallbackQuery):
    user_dict_template['bookmarks'].remove(int(callback.data[:-3]))
    await callback.answer('Закладка была успешна удалена!')
    if len(user_dict_template['bookmarks']) == 0:
        await callback.message.edit_text(LEXICON['no_bookmarks'])
    else:
        await callback.message.edit_text(LEXICON['/bookmarks'],
                                         reply_markup=create_bookmarks_keyboard(*user_dict_template['bookmarks']))


@router_1.message(F.text.startswith('open'))
async def open_command(message: Message):
    number = int(message.text.split()[1])
    user_dict_template['page'] = number
    if number == 381:
        reply_markup = create_pagination_keyboard('backward', f'{user_dict_template["page"]}/{len(book)}')

    elif number == 1:
        reply_markup = create_pagination_keyboard(f'{user_dict_template["page"]}/{len(book)}', 'forward')
    else:
        reply_markup = create_pagination_keyboard('backward', f'{user_dict_template["page"]}/{len(book)}', 'foraward')

    await message.answer(text=book[number],
                         reply_markup=reply_markup)

