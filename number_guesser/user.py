import random


# users Data
class User:

    """
    Класс для хранения информации об одном игроке:
    - id: Telegram user ID
    - ingame: флаг, что игра активна
    - secret_number: загаданное число
    - attempts: оставшиеся попытки
    - total_games: общее число игр
    - wins: победы
    """

    def __init__(self, user_id):
        self.ingame = False
        self.secret_number = None
        self.attempts = None
        self.total_games = 0
        self.wins = 0
        self.id = user_id

    def start_game(self):
        self.ingame = True
        self.secret_number = random.randint(1, 100)
        self.attempts = 5

    def win(self):
        self.ingame = False
        self.total_games += 1
        self.wins += 1

    def lose(self):
        self.ingame = False
        self.total_games += 1
