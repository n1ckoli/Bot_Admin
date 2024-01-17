import asyncio
import pprint

from aiogram.filters import Filter
from aiogram import Bot, Dispatcher, types

BOT_TOKEN = '6893439363:AAHMWt0qa4fBqrta-430HUxvcO350Ajmk90'
# use list if there are several administrators 
ADMINS = 1053332798

dp = Dispatcher()

bot = Bot(BOT_TOKEN)

# ФИЛЬТРЫ С ПОМОЩЬЮ КЛАССОВ
class IsAdmin(Filter):
    async def __call__(self, message):
        # если несколько админов то по списку сверяем айди
        return message.from_user.id == ADMINS


@dp.message(IsAdmin())
async def handle_admin_message(message: types.Message):
    if not message.reply_to_message:
        await message.reply('Используй ответ на сообщение!')
        return

    try:
        intial_user = message.reply_to_message.forward_from.id
    except AttributeError as er:
        await message.reply('Error :(((')
        raise er
    await bot.send_message(intial_user, message.text)


@dp.message(~IsAdmin())
async def handle_user_message(message: types.Message):
    await message.forward(ADMINS)
    await message.reply('Сообщение в обработке')


if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))

