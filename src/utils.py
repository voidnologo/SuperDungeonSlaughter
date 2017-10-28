from os.path import abspath, join, dirname


INPUT_PROMPT = '\n{} >> '
PROJECT_ROOT = abspath(join(dirname(__file__), '..'))
DATA_DIR = join(PROJECT_ROOT, 'data')


def ask_question(verbiage):
    return input(INPUT_PROMPT.format(verbiage))


def ask_yn_question(prompt):
    choice = None
    while choice not in ['y', 'n']:
        choice = input('\n{} (y/n) >>> '.format(prompt)).lower()
    return choice == 'y'


def data_file_path(target):
    return join(PROJECT_ROOT, DATA_DIR, target)
