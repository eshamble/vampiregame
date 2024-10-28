
from collections import namedtuple
from idlelib.pathbrowser import PathBrowserTreeItem

#DECLARE variable current_room to be ‘hall’
current_room = 'hall'

# room has fields room_text_output,
#  item, and rooms_in_directions
#
# rooms_in_directions is a dictionary with the keys being direction names,
#  and the values being room #names
Room = namedtuple('Room', ['room_text_output', 'item', 'rooms_in_directions'])
# Fills rooms_dictionary with Rooms
rooms_dictionary = {'kitchen': Room('You are in the kitchen.', 'garlic',
                                    {'west': 'smoke room'}),
                    'bedroom': Room('You are in the bedroom.', 'necklace',
                                    {'north': 'hall', 'east': 'bathroom'}),
                    'armory': Room('You are in the armory.', 'sword',
                                   {'east': 'hall'}),
                    'garden': Room('You are in the garden.', 'stake',
                                   {'south': 'garage'}),
                    'smoke room': Room('You are in the smoke room.', 'lighter',
                                       {'south': 'hall', 'east' : 'kitchen'}),
                    'garage': Room('You are in the garage.', 'gasoline',
                                   {'west': 'hall', 'north': 'garden'}),
                    'hall': Room('You are in the hall.', False,
                                 {'north': 'smoke room', 'west': 'armory', 'south': 'bedroom', 'east': 'garage'}),
                    'bathroom': Room('You are in the bathroom.\n'
                                     'The vampire stares at its empty '
                                     'reflection in the mirror.', False,
                                     {'west': 'bedroom'})}

#Create Item named tuple with fields obtained, successful_text, and failure_text
Item = namedtuple('Item', ['obtained', 'successful_text', 'failed_text', 'room_text'])
#CReate dictionary of Items in a specific order to make later iteration easier
item_dictionary = {'garlic': Item(False, 'You repel the vampire with garlic.',
                                  'You cannot repel the vampire without garlic.',
                                  'There is GARLIC on the counter.'),
                   'necklace': Item(False, 'You scare the vampire with the silver necklace.',
                                    'The vampire is not afraid without the necklace.',
                                    'There is a silver NECKLACE on the vanity.'),
                   'sword': Item(False, "You slash the vampire's head off with a sword.",
                                    'Without a sword, the vampire keeps its head.',
                                    'There is a SWORD leaned against the wall.'),
                   'stake': Item(False, 'You plunge a stake deep in its chest.',
                                    'Without a stake, you cannot pierce its heart.',
                                    'There is a STAKE in the dirt.'),
                   'gasoline': Item(False, 'You douse the vampire in gasoline.',
                                    'Without gasoline, you cannot light a fire.',
                                    'There is GASOLINE on a shelf.'),
                   'lighter': Item(False, 'You use the lighter to create a bonfire out of its carcass.',
                                   'Without the lighter, you cannot set the vampire on fire.',
                                   'There is a LIGHTER on the coffee table.')}
#DECLARE list inventory
inventory = []

#Prints game instructions
def print_instructions():
    print("\nTo move, type 'go north', 'go south', 'go east' or 'go west'."
          " \nTo pick up an item, type 'get [item]' (for example: get necklace).")
# Prints information about the room a player is in, including
# the rooms in every direction, and the text associated with an item
def display_room_text():
    print(rooms_dictionary.get(current_room).room_text_output)
    if current_room != 'bathroom':
        for entry in rooms_dictionary.get(current_room).rooms_in_directions:
            print('The {} is to the {}.'.format(rooms_dictionary.get(current_room).rooms_in_directions.get(entry),
                                                entry))
    if item_dictionary.get(rooms_dictionary.get(current_room).item) and not item_dictionary.get(rooms_dictionary.get(current_room).item).obtained:
        print(item_dictionary.get(rooms_dictionary.get(current_room).item).room_text)


# Moves the user to a different room if that room is in that direction

def move_user(direction):
    global current_room
    if direction in rooms_dictionary.get(current_room).rooms_in_directions:
        current_room = rooms_dictionary.get(current_room).rooms_in_directions.get(direction)
    else:
        print('There is no room to the {}. Try something else?'.format(direction))

#Get item: checks if item is the room's assigned item and
#if the user has already obtained it. If the item is correct
#and not yet obtained, it adds the item to the inventory
#and flags the item as obtained. Prints out messages
#for the user upon success and failure.
def get_item(item):
    global item_dictionary
    if item == rooms_dictionary.get(current_room).item:
        if item_dictionary.get(item).obtained:
            print("You have already obtained this item!")
        else:
            #sets item's obtained value to true
            item_dictionary[item] = Item(True,
                                         item_dictionary.get(item).successful_text,
                                         item_dictionary.get(item).failed_text,
                                         item_dictionary.get(item).room_text)
            inventory.append(item)
            print("You have taken the {}!".format(item))
    else:
        print("There is no {} in this room.".format(item))
#Splits the user input, and calls a handler function as many times as necessary
#to get the user to give proper input
def handle_input(user_input):
    user_input = user_input.split()
    user_input = handle_input_innards(user_input)
    while len(user_input) != 2 and user_input[0].lower() != 'go' and user_input[0].lower() == 'get':
        user_input = handle_input_innards(user_input)

#Calls different functions depending on if the user wants to go somewhere or
#get an item. Prints messages if input is invalid. Returns the user input
#so handle_input() can call it again if necessary
def handle_input_innards(user_input):
    if len(user_input) == 2:
        if user_input[0].lower() == 'go':
            move_user(user_input[1].lower())
        elif user_input[0].lower() == 'get':
            get_item(user_input[1].lower())
        else:
            print("Invalid command. Try again?")
    else:
        print("Invalid input length. Try again?")
    return user_input
"""
DEFINE FUNCTION vampire_encounter():
CALL display_room_text()
DECLARE VARIABLE player_alive to be true
FOR each entry i in item_dictionary:
	IF player_alive is true:
IF i.obtained is true:
	OUTPUT i.successful_text
	#successful_text for the last room contains a winning message
	
ELSE:
#player loses
OUTPUT i.failed_text
OUTPUT losing message
BREAK
"""
def vampire_encounter():
    display_room_text()
    for i in item_dictionary:
        if item_dictionary.get(i).obtained:
            print(item_dictionary.get(i).successful_text)
        else:
            print(item_dictionary.get(i).failed_text)
            print('The vampire catches you in a vice grip, and sinks\n'
                  'its teeth into your neck. You can feel yourself getting\n'
                  'drained. It kills you. You lose.')
            exit()
    print('You have killed the vampire. You win!')
    exit()

#calls functions to print the room's text, display inventory,
#print the instructions, and handle input.
def user_turn():
    print('\n ~~~~~~~~~~')
    display_room_text()
    print('Inventory: {}'.format(inventory))
    print_instructions()
    print('What would you like to do?')
    handle_input(input())

#main part: displays instructions, then has the user turns in a loop
#until the user enters the bathroom, triggering the vampire encounter
print("Welcome to the vampire game! \n")
print("You’ve been called to a mansion to exterminate "
      "\na vampire that’s taking up residence. Unfortunately, "
      "\nyou left your supplies at home, so you need to "
      "\nsearch the mansion for them. You will need garlic"
      "\nfrom the kitchen and a silver necklace from the "
      "\nbedroom to repel the vampire, a sword from the "
      "\narmory to fight it, a stake from the garden to kill "
      "\nit, and a lighter from the smoke room and some "
      "\ngasoline from the garage to burn the body afterwards.")

while current_room != 'bathroom':
    user_turn()
vampire_encounter()