from utils import ask_question


def initialize_hero():
    name = ask_question("What is your hero's name?")
    return {
        'name': name,
        'level': 1,
        'hp': 10,
        'damage': 2
    }
