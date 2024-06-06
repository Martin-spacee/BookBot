from aiogram import Router
from aiogram.types import Message

router_2 = Router()


@router_2.message()
async def any_commands(message: Message):
    await message.answer('Я тебя не понимаю! Напиши /help если нужна помощь')
