from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
from user import User
import os


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Bot and dispatcher objects
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


users: dict[int, User] = {}


@dp.message(CommandStart())
async def process_start_command(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = User(message.from_user.id)
    await message.answer(
        'Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
        "Чтобы получить правила игры и список доступных "
        "команд - отправьте команду /help"
    )


@dp.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(
        "Правила игры:\n\nЯ загадываю число от 1 до 100, "
        f"а вам нужно его угадать\nУ вас есть {ATTEMPTS} "
        "попыток\n\nДоступные команды:\n/help - правила "
        "игры и список команд\n/cancel - выйти из игры\n"
        "/stat - посмотреть статистику\n\nДавай сыграем?"
    )


@dp.message(Command(commands="stat"))
async def process_stat_command(message: Message):
    user = users[message.from_user.id]
    await message.answer(
        f"Всего игр сыграно: {user.total_games}\n" f"Игр выиграно: {user.wins}"
    )
    if not user.ingame:
        await message.answer("Начнем новую игру?")


@dp.message(Command(commands="cancel"))
async def process_cancel_command(message: Message):
    if users[message.from_user.id].ingame:
        users[message.from_user.id].ingame = False
        await message.answer(
            "Вы вышли из игры. Если захотите сыграть " "снова - напишите об этом"
        )
    else:
        await message.answer("А мы и так с вами не играем. " "Может, сыграем разок?")


@dp.message(
    F.text.lower().in_(
        ["да", "давай", "сыграем", "игра", "играть", "хочу играть", "хочу"]
    )
)
async def process_positive_answer(message: Message):
    user = users[message.from_user.id]
    if not user.ingame:
        user.start_game()
        await message.answer(
            "Ура!\n\nЯ загадал число от 1 до 100, " "попробуй угадать!"
        )
    else:
        await message.answer(
            "Пока мы играем в игру я могу "
            "реагировать только на числа от 1 до 100 "
            "и команды /cancel и /stat"
        )


@dp.message(F.text.lower().in_(["нет", "не", "не хочу", "не буду"]))
async def process_negative_answer(message: Message):
    if not users[message.from_user.id].ingame:
        await message.answer(
            "Жаль :(\n\nЕсли захотите поиграть - просто " "напишите об этом"
        )
    else:
        await message.answer(
            "Мы же сейчас с вами играем. Присылайте, " "пожалуйста, числа от 1 до 100"
        )


@dp.message(lambda x: x.text and x.text.isdigit() and 0 < int(x.text) < 101)
async def process_number_answer(message: Message):
    user = users[message.from_user.id]
    if user.ingame:
        if int(message.text) == user.secret_number:
            user.win()
            await message.answer("Ура!!! Вы угадали число!\n\n" "Может, сыграем еще?")
        elif int(message.text) < user.secret_number:
            user.attempts -= 1
            await message.answer("Мое число больше")
        elif int(message.text) > user.secret_number:
            user.attempts -= 1
            await message.answer("Мое число меньше")

        if user.attempts == 0:
            user.lose()
            await message.answer(
                "К сожалению, у вас больше не осталось "
                "попыток. Вы проиграли :(\n\nМое число "
                f"было {user.secret_number}\n\nДавайте "
                "сыграем еще?"
            )
    else:
        await message.answer("Мы еще не играем. Хотите сыграть?")


@dp.message()
async def process_other_messages(message: Message):
    if users[message.from_user.id].ingame:
        await message.answer(
            "Мы же сейчас с вами играем. " "Присылайте, пожалуйста, числа от 1 до 100"
        )
    else:
        await message.answer(
            "Я довольно ограниченный бот, давайте " "просто сыграем в игру?"
        )


if __name__ == "__main__":
    dp.run_polling(bot)
