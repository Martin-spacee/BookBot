from config.config import Config
from aiogram import Bot, Dispatcher
from keyboards.main_menu import set_main_menu
from handlers import user_handler, other_handler
import asyncio


async def main():
    config = Config(r'C:\Users\marti\PycharmProjects\BookBot\bookbot\.env')
    bot = Bot(config.bot_token, parse_mode='HTML')
    dp = Dispatcher()

    await set_main_menu(bot)

    dp.include_router(user_handler.router_1)
    dp.include_router(other_handler.router_2)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
