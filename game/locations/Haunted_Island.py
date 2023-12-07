from game import location
from game.display import announce
import game.config as config
from game.items import Item
from game.combat import Monster
import game.combat as combat
from game.events import *
from game import event
import numpy
import random
from game.display import menu

class Haunted_Island(location.Location):
    
    def __init__(self, x, y, w):
        super().__init__(x, y, w)
        self.name = 'island'
        self.symbol = 'I' #Symbol for map
        self.visitable = True #marks you can land on the island
        self.starting_location = Beach(self)
        self.locations = {} #Dict of sub-locations

        self.locations['beach'] = Beach(self)
        self.locations['forest'] = Forest(self)
        self.locations['strange_tree'] = StrangeTree(self)
        self.locations['tree'] = WeepingWillow(self)
        self.locations['small_clearing'] = Clearing(self)
        self.locations['cave'] = Cave(self)
        self.locations['cave_depths'] = CaveDepths(self)
        #starting location?
        self.starting_location = self.locations['beach']

    def enter(self,ship):
        #What to do upon visiting this location on map
        announce('arrived at an ominous-feeling island')
    
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

class SpiderLeg(Item):
    def __init__(self):
        super().__init__("leg", 7) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (20,70)
        self.skill = "melee"
        self.verb = "stab"
        self.verb2 = "stabs"

class BrokenBoard(Item):
    def __init__(self):
        super().__init__("board", 2) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (5,40)
        self.skill = "melee"
        self.verb = "bash"
        self.verb2 = "bashes"

class IntricateKey(Item):
    def __init__(self):
        super().__init__("key", 15)

class WillowTreasure(Item):
    def __init__(self):
        super().__init__("treasure", 50)

class Rifle(Item):
    def __init__(self):
        super().__init__("rifle", 600) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (30,110)
        self.firearm = True
        self.charges = 1
        self.skill = "guns"
        self.verb = "shoot"
        self.verb2 = "shoots"


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
            announce("You find some Wooden Boards")
            config.the_player.add_to_inventory([BrokenBoard()])

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
            announce("You enter the shockingly thick forest forest, and notice there are webs between the branches and trees.")

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
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['enter'] = self
        self.verbs['investigate'] = self
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
        if (verb == 'enter' or verb == 'investigate'):
            config.the_player.next_loc = self.main_location.locations['tree']

class WeepingWillow(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = 'tree'
        self.verbs['exit'] = self
        self.verbs['touch'] = self
    
    def enter(self):
        announce("You approach the Weeping Willow. You can see strange markings on the trunk...")
        announce("You can't tell what they mean, but they look like no writing you've ever seen.")

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == 'exit'):
            config.the_player.next_loc = self.main_location.locations['strange_tree']
        if (verb == 'touch'):
            if(IntricateKey in config.the_player):
                announce("You insert the Intricate Key into the keyhole in the base of the tree.")
                announce("With a rumble, a secret hatch at the bottom of the tree opens, revealing a treasure chest full of shiny treasure!")
                config.the_player.add_to_inventory([WillowTreasure()])
            else:
                announce("You touch the tree... nothing happens.")
                announce("But you do see what looks to be a keyhole on the tree's base.")

class Clearing (location.SubLocation):
    def __init___(self, m):
        super().__init__(m)
        self.name = "small_clearing"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['investigate'] = self
    

    def enter (self):
        announce("You enter a small clearing in the forest, and looking around, you find a couple skeletons.") 
    

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == 'south' or verb == 'east'):
            config.the_player.next_loc = self.main_location.locations['forest']
        if (verb == 'north'):
            config.the_player.next_loc = self.main_location.locations['cave']
        if (verb == 'west'):
            config.the_player.next_loc = self.main_location.locations['beach']
        if (verb == "investigate"):
            announce("You investigate the clearing.")
            self.clearingGame()
    
    def clearingGame(self):
        self.playingGame = True
        announce("The four skeletons are completely bare, not a single item on them.")
        announce("Two are right next to each other, one is near the other two, and the last is on the other end of the clearing from the three.")
        announce("However you find a pile of hats and broken or unusable weapons in a pile to the side.")
        announce("There is a pirate hat, a mask, a bandana, and an eyepatch, and then a two pistols, a rusted sword, and an unusable rifle.")
        announce("Near the items, there are rocks with words carved into them.")
        self.skeleton1 = []
        self.skeleton1correct = ['bandana', 'pistol']
        self.skeleton2 = []
        self.skeleton2correct = ['eyepatch', 'pistol']
        self.skeleton3 = []
        self.skeleton3correct = ['pirate hat', 'sword']
        self.skeleton4 = []
        self.skeleton4correct = ['mask', 'rifle']
        self.itemslist = ["pirate hat", "mask", "bandana", "eyepatch", "pistol", "pistol", "sword", "rifle"]
        
        while(self.playingGame == True):
            if(self.checkCorrect() == True):
                announce("After a moment of nothing, a rumbling echoes from the ground, revealing a pristine rifle and pistol, complete with ammo.")
                config.the_player.add_to_inventory([Item.Flintlock()])
                config.the_player.add_to_inventory([Rifle()])
                announce("The ghosts of these two sailors and this aspiring pirate smile upon you.")
                for i in config.the_player.get_pirates():
                    i.lucky = True
                self.gamePlayed == True
            else:
                if(self.itemslist == [] and self.checkCorrect() == False):
                    announce("This must not be the right solution...")
                announce("What will you do?")
                if(self.skeleton1 == [] and self.skeleton2 == [] and
                self.skeleton3 == [] and self.skeleton4 == []):
                    choice = input("a- read the notes\nb- pick up one of the items\nor cancel to do something else")
                else:
                    choice = input("a- read the notes\nb- pick up one of the items\nc- take an item from a skeleton\nor cancel to choose something else")
                if (choice == 'a' or choice == 'read'):
                    announce("There are four carved notes.")
                    announce("The first reads: I am a sailor. I sail the seas with my best pal, Stanley. I lost an eye a long time ago.")
                    announce("The second reads: I've never once left Fredrick's side. I depend on him a lot, and we shared everything, even weaopns.")
                    announce("The third reads: I am the enemy of those who sail the seas. I watch from afar, and my rifle will find each of their hearts.")
                    announce("The last reads: I am a girl who loves the sea, and practices the sword diligently in hopes to one day be a pirate myself")
                elif (choice == 'b' or choice == 'pick up'):
                    self.pickupItem()
                elif(choice == 'c' or choice == 'take'):
                    self.takeFromSkeleton()
                elif(choice == 'cancel'):
                    return
                else:
                    print("Invalid input")

    def pickupItem(self):
        '''A method that picks up an item from the pile and gives it to one of the skeletons'''
        if(self.itemslist != []):
            announce("Which item do you pick up?")
            item = input(self.itemslist)
            if(item in self.itemslist):
                self.itemslist.remove(item)
            elif(item == 'cancel'):
                return
            else:
                while(item not in self.itemslist):
                    print("Invalid item")
                    item = input(self.itemslist)
                self.itemslist.remove(item)

            announce(f"Skeleton 1 is leaning against Skeleton 2. Skeleton 3 is nearby, and Skeleton 4 is on the other side of the clearing.\nWhich skeleton do you give the {item} to?")
            self.placingItem(item)
        else:
            announce("There's nothing to pick up!")
    
    def checkCorrect(self):
        '''checks if the skeleton orientation is correct'''
        self.skeleton1.sort()
        self.skeleton2.sort()
        self.skeleton3.sort()
        self.skeleton4.sort()
        if(self.skeleton1 == self.skeleton1correct and
           self.skeleton2 == self.skeleton2correct and
           self.skeleton3 == self.skeleton3correct and
           self.skeleton4 == self.skeleton4correct):
            return(True)
        else:
            return(False)
    
    def takeFromSkeleton(self):
        '''takes an item from a skeleton to move elsewhere'''
        announce("Skeleton 1 is leaning against Skeleton 2. Skeleton 3 is nearby, and Skeleton 4 is on the other side of the clearing.")
        take = input("Which would you like to take from? 1, 2, 3, or 4? Or cancel?")
        if(take == '1'):
            if(self.skeleton1 != []):
                announce(f"Skeleton 1 has {self.skeleton1}")
                item = input("Which item would you like to take?")
                self.placingItem(item)
                self.skeleton1.remove(item)
            else:
                announce("This skeleton doesn't have anything you can take!")
        elif(take == '2'):
            if(self.skeleton2 != []):
                announce(f"Skeleton 2 has {self.skeleton2}")
                item = input("Which item would you like to take?")
                self.placingItem(item)
                self.skeleton2.remove(item)
            else:
                announce("This skeleton doesn't have anything you can take!")
        elif(take == '3'):
            if(self.skeleton3 != []):
                announce(f"Skeleton 3 has {self.skeleton3}")
                item = input("Which item would you like to take?")
                self.placingItem(item)
                self.skeleton3.remove(item)
            else:
                announce("This skeleton doesn't have anything you can take!")
        elif(take == '4'):
            if(self.skeleton4 != []):
                announce(f"Skeleton 4 has {self.skeleton4}")
                item = input("Which item would you like to take?")
                self.placingItem(item)
                self.skeleton4.remove(item)
            else:
                announce("This skeleton doesn't have anything you can take!")
        elif(take == 'cancel'):
            return
        else:
            announce("Invalid command")
            return

    def placingItem(self, item):
        '''Method for placing an item that'd been picked up.'''
        choice = input("1, 2, 3, 4, or put it back in the pile?")
        if (choice == '1'):
            self.skeleton1.append(item)
            announce(f"You give the {item} to the skeleton")
        if (choice == '2'):
            self.skeleton2.append(item)
            announce(f"You give the {item} to the skeleton")
        elif (choice == '3'):
            self.skeleton3.append(item)
            announce(f"You give the {item} to the skeleton")
        elif (choice == '4'):
            self.skeleton4.append(item)
            announce(f"You give the {item} to the skeleton")
        elif (choice == 'back' or choice == 'put it back'):
            self.itemslist.append(item)
            announce(f"You put the {item} back into the pile")
        else:
            announce("Invalid response")
            return


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
            announce("But against the wall of the cave, you spot a chest.")
            announce("Open it?")
            if (verb == 'open'):
                announce("The chest is empty, except for a single, intricate key.")
                config.the_player.add_to_inventory([IntricateKey()])
            if (verb == 'exit'):
                announce("You continue without opening the chest.")

class GiantSpiderEvent (event.Event):
    
    def __init__ (self):
        self.name = " giant spider attack."

    def process (self, world):
        result = {}
        spider = GiantSpider()
        announce("A group of giant spiders crawl out from the darkness and attack the crew!")
        combat.Combat([spider]).combat()
        announce("The giant spiders crumple to the ground, curling up.")
        result["newevents"] = []
        result["message"] = ""
        announce("One of their sharp limbs break off. It could be a good weapon.")
        config.the_player.add_to_inventory([SpiderLeg()])
