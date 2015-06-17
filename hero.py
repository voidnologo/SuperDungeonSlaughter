import random
import math
from inventory import Inventory


class Hero(object):
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.hp_max = 10
        self.hp = self.hp_max
        self.damage_min = 0
        self.damage_max = 3
        self.heal_min = 2
        self.heal_max = 4
        self.level_kills = 0
        self.total_kills = 0
        self.inventory = Inventory()

    def fight(self):
        return (random.randrange(self.damage_min, self.damage_max))

    def show_inventory(self):
        self.inventory.show_inventory()

    def add_item_to_inventory(self, item):
        self.inventory.add_item_to_inventory(item)

    # def show_inventory(self):
    #     # self.inventory = {"inventory" : "stuff"}
    #     # print(self.inventory)
    #     for i in self.inventory:
    #         print (i)

    # def add_item_to_inventory(self, item):
    #     self.inventory[item.name] = item

    # def use_item_in_inventory(self, item):
    #     if (item in self.inventory):
    #         self.inventory[item].action(self)
    #         if ("one_shot" in item.attributes):
    #             self.remove_item_from_inventory(item)
    #     else:
    #         print("Item is not in inventory. Unable to use.")

    # def remove_item_from_inventory(self, item):
    #     if (item in self.inventory):
    #         del self.inventory[item]
    #     else:
    #         print("Item is not in inventory.  Unable to remove.")

    def takeDamage(self, damage):
        self.hp -= damage

    def rest(self):
        heal = random.randrange(self.heal_min, self.heal_max)
        self.hp += heal
        if (self.hp > self.hp_max):
            self.hp = self.hp_max

        return (heal)

    def level_up(self):
        self.level += 1
        self.hp_max += self.level
        self.level_kills = 0

        if (self.damage_min == 0): #handle leveling to level 1
            self.damage_min = 1
        else:
            self.damage_min += int(math.ceil(self.damage_min * .1))

        self.damage_max += int(math.ceil(self.damage_max * .1))

        self.heal_min += int(math.ceil(self.heal_min * .1))
        self.heal_max += int(math.ceil(self.heal_max * .1))

        print("\nYou gained a level!\n")
        print("\t You are now level: " + str(self.level))
        print("\t You now have " + str(self.hp_max) + " max hp.")
        print("\t You deal " + str(self.damage_min) + " - " + str(self.damage_max) + " points of damage.")
        print("\t You heal " + str(self.heal_min) + " - " + str(self.heal_max) + " points when resting.\n")

    def details(self):
        print ("\tName: " + self.name + \
                 "\t Level: " + str(self.level) + \
                 "\t Max Hit points: " + str(self.hp_max) + \
                 "\t Damage: " + str(self.damage_min) + " - " + str(self.damage_max) +\
                 "\t Rest: " + str(self.heal_min) + " - " + str(self.heal_max))
        print ("\tName: {}\t Level: {}\t Max Hit points: {}\t Damage: {}-{}\t Rest: {}-{}")




