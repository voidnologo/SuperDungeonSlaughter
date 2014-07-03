class GameObject(object):
   def __init__(self, hero_obj, monster_obj):
      # self.level_kills = 0
      # self.number_of_kills = 0
      self.HERO = hero_obj
      self.MONSTER = monster_obj