import random
from monster import Monster

class Bestiary():

     def __init__(self, filename):
          self.bestiary = []
          # get_monster_data_from_file("bestiary.txt")

     # def get_monster_data_from_file(self, filename):

          try:
                with open(filename) as f:
                     for each_line in f:
                          # line = f.readline()
                          monster_data = each_line.strip().split(';')
                          #name, hp min, hp max, damage min, damage max, min lvl to fight, max lvl to fight
                          self.bestiary.append(Monster(monster_data[0], monster_data[1], monster_data[2],\
                                                        monster_data[3], monster_data[4], monster_data[5], monster_data[6]))

          except IOError as ioerr:
                print('File error: ' + str(ioerr))
                return(None)


     def get_monster_from_bestiary(self):
          nm = self.bestiary[random.randrange(0, len(self.bestiary))]
          return(Monster(nm.name, nm.hp_min, nm.hp_max, nm.damage_min, nm.damage_max, nm.min_level, nm.max_level))
     
     def get_monster_from_bestiary_by_level(self, level):
          monster_level_min = 9999
          monster_level_max = 0
          while not (monster_level_min <= level and monster_level_max >= level):
                nm = self.bestiary[random.randrange(0, len(self.bestiary))]
                monster_level_min = nm.min_level
                monster_level_max = nm.max_level

          return(Monster(nm.name, nm.hp_min, nm.hp_max, nm.damage_min, nm.damage_max, nm.min_level, nm.max_level))
