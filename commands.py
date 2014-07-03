class Commands(object):

   def __init__(self):
      self.commands = {
         "fight" : "Attack!",
         "f"     : "Attack!",
         "flee"  : "Run away (exits game)",
         "help"  : "Display a list of commands",
         "h"     : "Display a list of commands",
         "inv"   : "Display inventory",
         "i"     : "Display inventory",
         "rest"  : "Don't attack in order to gain back HP. Careful, the monster still attacks!",
         "r"     : "Don't attack in order to gain back HP. Careful, the monster still attacks!",
         "kills" : "Number of kills you have",
         "view"  : "View details about the monster or hero. \"view:<target>\". Target can = \"h\"\\\"hero\" or \"m\"\\\"mon\"\\\"monster\".",
         "v"     : "View details about the monster or hero. \"v:<target>\". Target can = \"h\"\\\"hero\" or \"m\"\\\"mon\"\\\"monster\".",
         "use"   : "Use an item in your inventory. \"use:<item>:<target>\". Target can = \"h\"\\\"hero\" or \"m\"\\\"mon\"\\\"monster\".",
         "u"     : "Use an item in your inventory. \"u:<item>:<target>\". Target can = \"h\"\\\"hero\" or \"m\"\\\"mon\"\\\"monster\"."
      }

   def listCommands(self):
      return(self.commands)

   def showCommands(self):
      for key in sorted(self.commands):
         print ("\t" + key + "\t" + self.commands[key])

   def validateCommand(self, inp):
      cmd = inp.strip().split(":")
      command = cmd.pop(0)

      if (command in self.commands):
         return(True)
      else:
         return(False)

   def performCommand(self, inp, game_obj):
      cmd = inp.strip().split(":")
      # if len(cmd) > 1:
      #    command = cmd.pop(0)
      #    t1 = cmd.pop(0)
      #    if len(cmd) > 1:
      #       t2 = cmd.pop(0)

      # else:
      #    command = cmd.pop(0)
      #    t1 = ""
      #    t2 = ""

      command = cmd.pop(0)


      # print("COMMAND: " + command)
      # print("TARGET: " + target)

      if (command == "help" or command == "h"):
         print(self.showCommands())

      elif (command == "rest" or command == "r"):
         monster_attack = game_obj.MONSTER.fight()
         hero_heal = game_obj.HERO.rest()
         game_obj.HERO.takeDamage(monster_attack)
         print("\t" + game_obj.HERO.name + " healed " + str(hero_heal) + " points of damage.")
         print("\t" + game_obj.MONSTER.name + " dealt " + str(monster_attack) + " points of damage.")  

      elif (command == "fight" or command == "f"):
         hero_attack = game_obj.HERO.fight()
         monster_attack = game_obj.MONSTER.fight()
         game_obj.HERO.takeDamage(monster_attack)
         game_obj.MONSTER.takeDamage(hero_attack)
         print("\t" + game_obj.HERO.name + " dealt " + str(hero_attack) + " points of damage.")
         print("\t" + game_obj.MONSTER.name + " dealt " + str(monster_attack) + " points of damage.")

      elif (command == "kills"):
         print("\tYou have " + str(game_obj.HERO.total_kills) + " kills.")

      elif (command == "view" or command == "v"):
         if len(cmd) == 1:
            target = cmd[0]

            if target != "":
               if (target == "m" or target == "mon" or target == "monster"):
                  game_obj.MONSTER.details()
               elif (target == "h" or target == "hero"):
                  game_obj.HERO.details()
               else:
                  print ("Unable to view details.")
            else:
               print ("Specify target to view.")
         else:
            print ("Invalid number of parameters specified.")
      
      elif (command == "flee"):
         print ("You run away.")

      elif (command == "inv" or command == "i"):
         game_obj.HERO.show_inventory()

      elif (command == "u" or command == "use"):
         if len(cmd) == 2:
            item = cmd[0]
            target = cmd[1]

            if item != "":
               if item in game_obj.HERO.inventory:               
                  if target != "":
                     if target in ("h", "hero"):
                        game_obj.HERO.inventory[item].action(game_obj.HERO)
                     elif target in ("m", "mon", "monster"):
                        pass
                     else:
                        print("Invalid target.")
                  else:
                     print("Specify target to use item on.")
               else:
                  print("Item does not exist in inventory.")
            else:
               print ("Specify item to use.")
         else:
            print ("Invalid number of parameters specified.")
      

