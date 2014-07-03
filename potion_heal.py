from item import Item
from hero import Hero

class Potion_heal(Item):
   def __init__(self):
      super().__init__("Healing Potion", "potion", (Hero))
      self.attributes = ["one_shot"]

   def details (self):
      super().details()
      print ("Action: Heals the hero for 50% hp")

   def action(self, target):
      # if type(target) in self.actor:
      if isinstance(target, self.actor):
         heal_amount = int(target.hp_max / 2)
         target.hp += heal_amount
         if (target.hp > target.hp_max):
            target.hp = target.hp_max
      else:
         print("Unable to use item on target.")
