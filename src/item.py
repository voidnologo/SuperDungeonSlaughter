import simplejson as json
from utils import data_file_path


class Item:

    CATALOG = {}

    def __init__(self, **kwargs):
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

    @classmethod
    def get_item(cls, name):
        if not Item.CATALOG:
            Item._initialize_catalog()
        return Item(**Item.CATALOG[name])

    @staticmethod
    def _initialize_catalog():
        items_path = data_file_path('items.json')
        with open(items_path, 'r') as f:
            Item.CATALOG = json.load(f)
