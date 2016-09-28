from utils import ask_question


def initialize_hero():
    name = ask_question("What is your hero's name?")
    return {
        'name': name,
        'level': 1,
        'hp_max': 10,
        'hp': 10,
        'damage_min': 0,
        'damage_max': 3,
        'total_kills': 0,
        'level_kills': 0,
        'heal_min': 1,
        'heal_max': 4,
    }
