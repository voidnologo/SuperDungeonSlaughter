class Inventory(object):
    def __init__(self):
        self.inventory = []

    def show_inventory(self):
        # self.inventory = {"inventory" : "stuff"}
        index = 0
        for i in self.inventory:
            print ("[" + str(index) + "] " + i.name)

    def add_item_to_inventory(self, item):
        self.inventory.append(item)

    def use_item_in_inventory(self, item):
        if (item in self.inventory):
            self.inventory[item].action(self)
            if ("one_shot" in item.attributes):
                self.remove_item_from_inventory(item)
        else:
            print("Item is not in inventory. Unable to use.")

    def remove_item_from_inventory(self, item):
        if (item in self.inventory):
            del self.inventory[item]
        else:
            print("Item is not in inventory.  Unable to remove.")
