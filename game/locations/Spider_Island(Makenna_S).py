from game import location
from game.display import announce
import game.config as config
import game.items as items
from game.combat import Monster
import game.combat as combat
from game.events import *
from game import event
import random

class Spider_Island(location.Location):
    def __init__(self, x, y, world):
        super().__init__(x,y,world)
        #Super() refers to parent class(Location in this case)
        #So this runs the initializer of Location
        self.name = 'Island'
        self.symbol = 'I' #Symbol for map
        self.visitable = True #marks you can land on the island
        self.locations = {} #Dict of sub-locations
        self.locations['beach'] = Beach(self)
        self.locations['forest'] = Forest(self)
        self.locations['strange_tree'] = StrangeTree(self)
        self.locations['small_clearing'] = Clearing(self)
        self.locations['cave'] = Cave(self)
        self.locations['cave_depths'] = CaveDepths(self)
        #starting location?
        self.starting_location = self.locations['beach']
        self.returning = False

    def enter(self,ship):
        #What to do upon visiting this location on map
        announce('arrived at an island')
    
    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class GiantSpider(Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["bite"] = ["bites",random.randrange(70,101), (10,20)]
        attacks["stab"] = ['stabs',random.randrange(50,101), (15,25)]
        #7 to 19 hp, bite attack, 160 to 200 speed (100 is "normal")
        super().__init__(name, random.randrange(5,15), attacks, 190 + random.randrange(-10,11))

class SpiderLeg(items):
    def __init__(self):
        super().__init__("leg", 7) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (20,70)
        self.skill = "leg"
        self.verb = "stab"
        self.verb2 = "stabs"

#sub-Locations
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
        announce("You arrive at the shore. The shore is made of many rocks rather than sand. It is difficult to traverse the beach")
        announce("The ship is docked just off of the shore, as the rocks were too sharp to dock on the shore normally.")
    
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'south'):
            announce('You return to your ship')
            #Code that stops the visit (NEED BOTH EVERY TIME!!)
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        if (verb == 'north'):
            config.the_player.next_loc = self.main_location.locations['forest']
            #Text will be printed by 'enter' of Trees.
        if (verb == 'east' or verb == 'west'):
            announce("You walk all the way around the rocky beaches. It's difficult to traverse.")
            announce("You see some webs between the rocks, and the broken remains of ships that got too close to the rocky shores.")

class Forest(location.SubLocation):
    def __init___(self, main_location):
        super().__init__(main_location)
        self.name = "forest"
        #verbs is set up by super() initializer
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 50
        self.events.appendz
    
    def enter(self):
        if(self.returning == False):
            announce("You enter the shockingly thick forest forest, and notice there are webs between the branches and trees.")
        if(self.returning == True):
            announce("You re-enter the forest, once again observing the webs that fill the thickly wooded area")
        self.returning = True

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'south'):
            config.the_player.next_loc = self.main_location.locations['beach']
        if (verb == 'north'):
            config.the_player.next_loc = self.main_location.locations['cave']
        if (verb == 'east'):
            config.the_player.next_loc = self.main_location.locations['strange_tree']
        if (verb == 'west'):
            config.the_player.next_loc = self.main_location.locations['small_clearing']

class StrangeTree(location.SubLocation):
    def __init___(self, main_location):
        super().__init__(main_location)
        self.name = "strange_tree"
        #verbs is set up by super() initializer
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 50
        self.events.appendz
    
    def enter(self):
        announce("Wandering through the woods, you come across a strange tree, bigger than the rest of the surrounding trees.")
        announce("It seems to be a yellowed and dying weeping willow tree, rustling in the wind.")
    
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'south' or verb == 'east'):
            config.the_player.next_loc = self.main_location.locations['beach']
        if (verb == 'north'):
            config.the_player.next_loc = self.main_location.locations['cave']
        if (verb == 'west'):
            config.the_player.next_loc = self.main_location.locations['forest']
        if (verb == 'enter'):
            a

class Clearing(location.SubLocation):
    def __init___(self, main_location):
        super().__init__(main_location)
        self.name = "small_clearing"
        #verbs is set up by super() initializer
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 50
        self.events.appendz
    
    def enter(self):
        announce("You enter a small clearing in the forest, and looking around, you find a couple skeletons.") 
    
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'south'):
            config.the_player.next_loc = self.main_location.locations['forest']
        if (verb == 'north'):
            config.the_player.next_loc = self.main_location.locations['cave']
        if (verb == 'east'):
            config.the_player.next_loc = self.main_location.locations['forest']
        if (verb == 'west'):
            config.the_player.next_loc = self.main_location.locations['beach']

class Cave(location.SubLocation):
    def __init___(self, main_location):
        super().__init__(main_location)
        self.name = "cave"
        #verbs is set up by super() initializer
        self.verbs['deeper'] = self
        self.verbs['exit'] = self
        self.verbs['right'] = self
        self.verbs['left'] = self
        self.event_chance = 50
        self.events.appendz
    
    def enter(self):
        announce("After traveling through the forest for a while, you come across the mouth of a dark cave.")
        announce("Lighting a lantern, you enter the cave.")
    
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'exit'):
            config.the_player.next_loc = self.main_location.locations['forest']
        if (verb == 'deeper'):
            config.the_player.next_loc = self.main_location.locations['cave_depths']
        if (verb == 'right'):
            announce("There's just the wall of the cave that direction")
        if (verb == 'left'):
            announce("There's just the wall of the cave that direction")

class CaveDepths(location.SubLocation):
    def __init___(self, main_location):
        super().__init__(main_location)
        self.name = "cave_depths"
        #verbs is set up by super() initializer
        self.verbs['deeper'] = self
        self.verbs['exit'] = self
        self.verbs['right'] = self
        self.verbs['left'] = self
        self.event_chance = 100
        self.events.append(GiantSpiderEvent())
    
    def enter(self):
        announce("Wandering deeper into the cave, it gets darker and darker, and you can see more and more cobwebs...")
    
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'exit'):
            config.the_player.next_loc = self.main_location.locations['cave']
        if (verb == 'north'):
            announce("You cannot go any deeper")
        if (verb == 'right' or verb == 'left'):
            announce("There's just the wall of the cave depths that direction")

class GiantSpiderEvent (event.Event):
    
    def __init__ (self):
        self.name = " giant spider attack."

    def process (self, world):
        result = {}
        spider = GiantSpider()
        announce("A group of giant spiders crawl out from the darkness and attack the crew!")
        combat.Combat([spider]).combat()
        announce("The giant spiders fall to the ground.")
        result["newevents"] = []
        result["message"] = ""
        announce("One of their sharp limbs break off... could be a good weapon.")
        config.the_player.add_to_inventory([SpiderLeg()])
