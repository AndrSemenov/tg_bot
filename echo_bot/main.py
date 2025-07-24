from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ContentType
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Bot and dispatcher objects
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Start handler
@dp.message(Command(commands="start"))
async def process_start_command(message: Message):
    await message.answer("Hello!\nI'm an Echo\nPlease, write something to me")


# Help handler
@dp.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer("Send me a message and I will answer you the same message")


# Message handler
@dp.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(
            text="This type of update isn't supprted by send_copy method "
        )


if __name__ == "__main__":
    dp.run_polling(bot)
