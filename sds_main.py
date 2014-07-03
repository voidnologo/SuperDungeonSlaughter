# import random

from hero import Hero
# from monster import Monster
from commands import Commands
from game_object import GameObject
from bestiary import Bestiary
from colors import bcolors
# import sys
# from item import Item
from potion_heal import Potion_heal

###initialize game
command_obj = Commands()
bestiary = Bestiary("monsters.txt")

def getInput ():
  if (game_obj.HERO.hp / game_obj.HERO.hp_max) > 0.66:
    hp_color = bcolors.FG_BOLD_GREEN
  elif (game_obj.HERO.hp / game_obj.HERO.hp_max) > 0.33:
    hp_color = bcolors.FG_BOLD_YELLOW
  else:
    hp_color = bcolors.FG_BOLD_RED

  prompt = bcolors.BOLD + game_obj.HERO.name + bcolors.ENDC +\
            " - lvl: [" + str(game_obj.HERO.level) + "]" +\
            " - hp: " + hp_color + "[" + str(game_obj.HERO.hp) + "/" + str(game_obj.HERO.hp_max) + "]" + bcolors.ENDC +\
            " .... " + \
            bcolors.FG_MAGENTA + game_obj.MONSTER.name + bcolors.ENDC +\
            " - hp: [" + str(game_obj.MONSTER.hp) +"]" +\
            bcolors.FG_CYAN + "   #action >" + bcolors.ENDC
  command = input(prompt).lower()
  if (not command_obj.validateCommand(command)):
      print("Invalid input")
      command = getInput()

  return (command)


###intro
print(bcolors.BOLD + bcolors.UNDERLINE + bcolors.BG_RED + "Welcome to Super Dungeon Slaughter!" + bcolors.ENDC)
# game_on = input('\n\nDo you want to fight? [y/n]:')

# ### start game
# if (game_on.lower() == "y"):
#    print("playing the game!")
# else:
#    print("Too bad!  Playing the game anyways! \n\n")

### set up battle
hero_name = input("\n\nWhat is your hero's name? ")
# monster_name = "Goblin" + str(random.randint(324, 17319))

new_hero = Hero(hero_name)
new_hero.add_item_to_inventory(Potion_heal())
new_monster = bestiary.get_monster_from_bestiary_by_level(new_hero.level)


#while (new_monster.min_level > new_hero.level):   #get a new new_monster if too high level
#   new_monster = bestiary.get_monster_from_bestiary() 


### check variables, introduce battle
# print("Your Hero's name is: " + HERO.name + " and you are fighting a: " + MONSTER.name)


### battle loop
print("Start the battle!")
print("Enter \"help\" or \"h\" for a list of commands.")

game_obj = GameObject(new_hero, new_monster)
fight = True

while (fight):
   command = getInput()

   if (command == "flee"):
      break
   else:
      command_obj.performCommand(command, game_obj)

   if (game_obj.HERO.hp <= 0):
      fight = False

   if (game_obj.MONSTER.hp <= 0):
      # ++number_of_kills
      game_obj.HERO.total_kills += 1
      game_obj.HERO.level_kills += 1
      print("\nCongratulations!  You killed the " + game_obj.MONSTER.name + "!")
      print("\tYou have killed " + str(game_obj.HERO.total_kills) + " monsters.")
      print("\tPrepare for your next fight!\n")
      # monster_name = "Goblin" + str(random.randint(324, 17319))
      game_obj.MONSTER = bestiary.get_monster_from_bestiary()

      # print("\nNEW MONSTER: ")
      # game_obj.MONSTER.details()
      # print("Hero level " + str(type(game_obj.HERO.level)))

      # while ((game_obj.MONSTER.min_level > game_obj.HERO.level) and (game_obj.MONSTER.max_level < game_obj.HERO.level)):   #get a new monster if too high level
      # while (game_obj.MONSTER.min_level > game_obj.HERO.level):   #get a new monster if too high level
      game_obj.MONSTER = bestiary.get_monster_from_bestiary_by_level(game_obj.HERO.level) 

      if (not game_obj.HERO.level_kills % game_obj.HERO.level):
         game_obj.HERO.level_up()

if (game_obj.HERO.hp > 0):
   print("\n\tYou have killed " + str(game_obj.HERO.total_kills) + " monsters before running away!")
else:
   print("\n\tYou died!  And you only managed to kill " + str(game_obj.HERO.total_kills) + " monsters.")
   print("\tBetter luck next time.\n\n")

