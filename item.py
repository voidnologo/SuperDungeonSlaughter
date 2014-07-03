class Item(object):
   def __init__(self, name, category, actor):
      self.name = name
      self.category = category
      self.actor = actor
      self.attributes = []

   def details(self):
      print ("Name: " + self.name)
      print ("Category: " + self.category)
      # print ("Actor: ", end='')
      # for i in self.actor:
      #    print ("\t" + i, end='')
      # print("\n")
      

   def effect(self):
      pass