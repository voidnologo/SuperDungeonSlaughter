import random

class Monster(object):
   def __init__(self, name, hpmin, hpmax, damagemin, damagemax, minlvl, maxlvl):
      self.name = name
      self.hp_min = int(hpmin)
      self.hp_max = int(hpmax)
      self.damage_min = int(damagemin)
      self.damage_max = int(damagemax)
      self.min_level = int(minlvl)
      self.max_level = int(maxlvl)
      # self.hp_min = 2
      # self.hp_max = 7
      # self.damage_min = 0
      # self.damage_max = 3

      # input("MONSTER Creation " + name + " " +  hpmin + " " +  hpmax + " " +  damagemin + " " +  damagemax)

      self.hp = random.randrange(self.hp_min, self.hp_max)

   def fight(self):
      # print("MONSTER: fight")

      return (random.randrange(self.damage_min, self.damage_max))

   def inventory(self):
      self.inventory = {"inventory" : "stuff"}
      print(self.inventory)

   def takeDamage(self, damage):
      self.hp -= damage

   def details(self):
      print ("\tType: " + self.name + \
         "\t Hit points: " + str(self.hp_min) + " - " + str(self.hp_max) + \
         "\t Damage: " + str(self.damage_min) + " - " + str(self.damage_max) +\
         "\t Min Level: " + str(self.min_level) +\
         "\t Max Level: " + str(self.max_level))
