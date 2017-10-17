from os.path import abspath, join, dirname


INPUT_PROMPT = '\n{} >> '
PROJECT_ROOT = abspath(join(dirname(__file__), '..'))
DATA_DIR = join(PROJECT_ROOT, 'data')


def ask_question(verbiage):
    return input(INPUT_PROMPT.format(verbiage))


def data_file_path(target):
    return join(PROJECT_ROOT, DATA_DIR, target)
