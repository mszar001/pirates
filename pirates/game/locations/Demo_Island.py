from game import location
from game.display import announce
import game.config as config
import game.items as items
from game.combat import Macaque
from game.combat import Combat
from events import *

#Demo island inherits from location(Meaning demo is a location)
class DemoIsland(location.Location):
    def __init__(self, x, y, world):
        super().__init__(x,y,world)
        #Super() refers to parent class(Location in this case)
        #So this runs the initializer of Location
        self.name = 'Island'
        self.symbol = 'I' #Symbol for map
        self.visitable = True #marks you can land on the island
        self.locations = {} #Dict of sub-locations
        self.locations['beach'] = Beach(self)
        self.locations['trees'] = Trees(self)
        #starting location?
        self.starting_location = self.locations['beach']

    def enter(self,ship):
        #What to do upon visiting this location on map
        announce('arrived at an island')
    
    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class Saber(items.Item):
    def __init__(self):
        super().__init__("cutlass", 5) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (10,60)
        self.skill = "swords"
        self.verb = "slash"
        self.verb2 = "slashes"
        
class Macaque(Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["bite"] = ["bites",random.randrange(70,101), (10,20)]
        #7 to 19 hp, bite attack, 160 to 200 speed (100 is "normal")
        super().__init__(name, random.randrange(7,20), attacks, 180 + random.randrange(-20,21))

#Sub-Locations (Beach and Trees)
class Beach(location.SubLocation):
    def __init___(self, main_location):
        super().__init__(main_location)
        self.name = "beach"
        #verbs is set up by super() initializer
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 50
        self.events.appendz

    def enter(self):
        announce ('You arrive at the Beach. Your ship is at anchor in a small bay to the South')

    #One of the Core Functions, contains handling for everything
    #More complex actions need functions to handle them
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'south'):
            announce('You return to your ship')
            #Code that stops the visit (NEED BOTH EVERY TIME!!)
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        if (verb == 'north'):
            config.the_player.next_loc = self.main_location.locations['trees']
            #Text will be printed by 'enter' of Trees.
        if (verb == 'east' or verb == 'west'):
            announce("You walk all the way around the island on the Beach, but it's not very interesting")

class Trees(location.SubLocation):
    def __init___(self, main_location):
        super().__init__(main_location)
        self.name = "trees"
        #verbs is set up by super() initializer
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        #Add some treasure
        self.verbs['take'] = self
        self.item_in_tree = items.Cutlass
        self.item_in_clothes = items.Flintlock
        
    def enter (self):
        announce('You walk into the small forest on the island.')
        if self.item_in_tree != None:
            description = description + "You see a " + self.item_in_tree
        if self.item_in_clothes != None:
            description = description + "You see a " + self.item_in_clothes
        announce (description)
    def process_verb(self, verb, cmd_list, nouns):
        if(verb in ["north", "south", "east", "west"]):
            config.the_player.next_loc = self.main_location.locations['beach']
        if (verb == 'take'):
            #The player will type something like 'take saber' or 'take all'
            if (self.item_in_tree == None and self.item_in_clothes == None):
                announce("You don't see anything to take.")
            #They just type 'take'
            elif(len(cmd_list) < 2):
                announce("Take what?")
            else:
                at_least_one = False
                i = self.item_in_tree
                if i != None and (i.name == cmd_list[1] or cmd_list[1] == 'all'):
                    announce(f'You take the {i.name} from the tree')
                    config.the_player.add_to_inventory(i)
                    self.item_in_tree = None
                    config.the_player.go = True
                    at_least_one = True
                i = self.item_in_clothes
                if i != None and (i.name == cmd_list[1] or cmd_list[1] == 'all'):
                    announce(f'You take the {i.name} out of the pile of clothes.. it looks like the person was eaten.')
                    config.the_player.add_to_inventory(i)
                    self.item_in_clothes = None
                    config.the_player.go = True
                    at_least_one = True
            if not at_least_one:
                announce("You don't see one of those around")

