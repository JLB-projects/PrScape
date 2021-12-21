"""Contains all the classes that are used by the main program, along with a few useful functions and
dictionaries."""

import random


level_xp = {1: 0, 2: 83, 3: 174, 4: 276, 5: 388, 6: 512, 7: 650, 8: 801, 9: 969, 10: 1154, 11: 1358, 12: 1584,
            13: 1833, 14: 2107, 15: 2411, 16: 2746, 17: 3115, 18: 3523, 19: 3973, 20: 4470, 21: 5018, 22: 5624,
            23: 6291, 24: 7028, 25: 7842, 26: 8740, 27: 9730, 28: 10824, 29: 12031, 30: 13363, 31: 14833, 32: 16456,
            33: 18247, 34: 20224, 35: 22406, 36: 24815, 37: 27473, 38: 30408, 39: 33648, 40: 37224, 41: 41171,
            42: 45529, 43: 50339, 44: 55649, 45: 61512, 46: 67983, 47: 75127, 48: 83014, 49: 91721, 50: 101333,
            51: 111945, 52: 123660, 53: 136593, 54: 150872, 55: 166636, 56: 184040, 57: 203254, 58: 224466, 59: 247886,
            60: 273742, 61: 302288, 62: 333804, 63: 368599, 64: 407015, 65: 449429, 66: 496254, 67: 547953, 68: 605032,
            69: 668051, 70: 737627, 71: 814445, 72: 899257, 73: 992895, 74: 1096278, 75: 1210421, 76: 1336443,
            77: 1475581, 78: 1629200, 79: 1798808, 80: 1986068, 81: 2192818, 82: 2421087, 83: 2673114, 84: 2951373,
            85: 3258594, 86: 3597792, 87: 3972294, 88: 4385776, 89: 4842295, 90: 5346332, 91: 5902831, 92: 6517253,
            93: 7195629, 94: 7944614, 95: 8771558, 96: 9684577, 97: 10692629, 98: 11805606, 99: 13034431}


def get_current_lvl(current_xp):
    """Converts skill experience into the correct level."""
    if level_xp[99] < current_xp:
        return 99
    i = 99
    # Since 1-50 is <1% of the total xp for 99, most levels should be above 50 long term
    while level_xp[i] > current_xp:
        i -= 1
    else:
        return i


class Transport:
    """A way of moving between areas that aren't connected directly via neighbours.

    Allows item costs, skill and quest requirements.
    """
    def __init__(self, text1, text2, area_id, item_reqs=None, skill_reqs=None, quest_reqs=None):
        self.text1 = text1
        self.text2 = text2
        self.area_id = area_id
        self.item_reqs = item_reqs
        self.skill_reqs = skill_reqs
        self.quest_reqs = quest_reqs
        if item_reqs is None:
            self.item_reqs = {}
        if skill_reqs is None:
            self.skill_reqs = {}
        if quest_reqs is None:
            self.quest_reqs = []


class Enemy:
    """An enemy that the user can fight.

    Each has different attributes such as: skills, attack styles, attack speed, drops.
    Also allows the option to change when the enemy appears or the items that it drops based on quest progress.
    """
    def __init__(self, num, name, desc, skills, att_style, equipment, special, att_speed, drops, passive,
                 alt_drops=None, quest_lock=None):   # alt_drops = [[quest_id, obj], [drop1], ...]
        self.name = name
        self.desc = desc
        self.skills = skills
        self.att_style = att_style
        self.equipment = equipment
        self.special = special
        self.att_speed = att_speed
        self.drops = drops
        self.passive = passive
        self.id = num
        self.alt_drops = alt_drops
        if self.alt_drops is None:
            self.alt_drops = [[-1, 0]]
        self.quest_lock = quest_lock
        # alt_drops and quest_lock provide quest based variation on drop tables / availability

    def gen_loot(self, player):
        """Generates the loot from an enemy randomly based on its drop table. The alt_drops table is used if the user
        is at a relevant point in a quest for the particular enemy."""
        if self.drops != self.alt_drops and self.alt_drops[0] in player.quest_flags:
            loot_table = self.alt_drops[1::]
        else:
            loot_table = self.drops
        if (total := sum([loot_table[i][1] for i in range(len(loot_table))])) < 1:
            # Fill remaining chance with a nothing drop
            loot_table.append([-1, 1-total, 1, 1])
        item = random.choices(loot_table, weights=[loot_table[i][1] for i in range(len(loot_table))], k=1)
        item_id = item[0][0]
        quantity = random.randint(item[0][2], item[0][3])
        return [item_id, quantity]


class SkillObj:
    """A skilling object or location.

    Can specify things such as skill, requirement, experience awarded, resources given, difficulty,
    and whether a quest changes its behaviour.
    """
    def __init__(self, name, skill, req, xp, rate_1, rate_99, depletion_chance, resources, tool, quest_lock=None):
        self.name = name
        self.skill = skill
        self.req = req
        self.xp = xp
        # x / 255 = base rate of success before tool considerations, at lvl 1 and 99
        self.rate_1 = rate_1
        self.rate_99 = rate_99
        self.depletion_chance = depletion_chance
        self.resources = resources
        self.tool = tool
        self.quest_lock = quest_lock


class Npc:
    """Non-player character.

    Can be talked to, traded with and may offer the user a quest. Can also be locked behind another quest before
    appearing / disappearing.
    """
    def __init__(self, num, name, desc, dialogue=None, flags=None, quest_lock=None):
        self.id = num
        self.name = name
        self.desc = desc
        self.dialogue = dialogue
        self.flags = flags
        # NPC flags are currently only for quest tracking
        if flags is None:
            self.flags = []
        if dialogue is None:
            self.dialogue = "I can't talk right now, come back later."
        self.quest_lock = quest_lock


class ShopNpc(Npc):
    """An NPC that offers a shop for the user."""
    def __init__(self, num, name, desc, dialogue=None, shop=None, flags=None, quest_lock=None):
        super().__init__(num, name, desc, dialogue, flags, quest_lock)
        self.shop = shop
        if shop is None:
            self.shop = Shop(Inventory([1, 1]))


None_enemy = Enemy(-1, "", "", {}, 'Melee', {}, None, 2400, [[0, 1, 1, 1]], True)
# Used to patch a startup issue, should remove later


class Area:
    """Defines everything about the game areas.

    Each area can contain enemies, NPCs and skill objects.
    There is also variation in the facilities that an area has, like a bank or an anvil.
    An area can have up to 4 neighbours based on standard directions, which can be travelled to directly via a button.
    Requirements may be added before an area can be accessed. Also has the option to include a transport,
    linking to another non-neighbouring area.
    """
    def __init__(self, num, name, enemies, npcs, skill_obj, has_bank, has_anvil, has_furnace, has_range,
                 selection, neighbours=None, skill_reqs=None, quest_reqs=None, transport=None, background=None):
        self.id = num
        self.name = name
        self.enemies = enemies
        while len(self.enemies) < 4:
            self.enemies.append(None_enemy)
        self.npcs = npcs
        self.skill_obj = skill_obj
        self.has_bank = has_bank
        self.selection = selection
        self.has_anvil = has_anvil
        self.has_furnace = has_furnace
        self.has_range = has_range
        if neighbours is None:
            self.neighbours = [None, None, None, None]
            # = [North, East, South, West]
        else:
            self.neighbours = neighbours
        while len(self.neighbours) < 4:
            self.neighbours.append(None)
        self.skill_reqs = skill_reqs
        self.quest_reqs = quest_reqs
        if skill_reqs is None:
            self.skill_reqs = {}
        if quest_reqs is None:
            self.quest_reqs = []
        self.transport = transport
        self.background = background
        if background is None:
            # self.background = '#4f0781'
            self.background = '#949494'

    def __repr__(self):
        """Saves the area id number as a string to go with the rest of the save data from Player object."""
        return str(self.id)


class Quest:
    """A basic quest system for the user to progress through.

    Each quest can have any number of objectives, which consist of small tasks like gathering an item or killing some
    enemies. The quest as a whole may have skill or quest requirements along with rewards upon completion.
    Quests are completed via specific NPCs with the relevant dialogue being stored in quest and objective objects.
    """
    def __init__(self, name, number, skill_reqs, quest_reqs, start, item_rewards, xp_rewards, rewards_dialogue,
                 *objectives):
        self.name = name
        self.id = number
        self.skill_reqs = skill_reqs
        self.item_rewards = item_rewards
        self.xp_rewards = xp_rewards
        self.quest_reqs = quest_reqs
        self.start = start          # = NPC name
        self.objectives = []
        self.rewards_dialogue = rewards_dialogue
        for i in objectives:
            self.objectives.append(i)
        if skill_reqs is None:
            self.skill_reqs = {}
        if quest_reqs is None:
            self.quest_reqs = []
        if item_rewards is None:
            self.item_rewards = {}
        if xp_rewards is None:
            self.xp_rewards = {}


class Objective:
    """Objectives as mentioned in the quest class.

    Each objective stores NPC dialogue for both starting and ending the objective, along with options for user
    responses. An objective may also store items or enemies that the user needs to kill to progress, or hand out
    unique quest items for later use during the quest. The NPC where each  objective starts and ends should also be
    specified.
    """
    def __init__(self, num, obj_type, dialogue_start, dialogue_progress, response_start_1, response_start_2,
                 response_progress_1, response_progress_2, start_npc, return_npc, itemsdict=None, enemiesdict=None,
                 quest_items=None):
        self.num = num
        self.type = obj_type                # Currently not important
        self.dialogue_start = dialogue_start
        self.dialogue_progress = dialogue_progress
        self.response_start_1 = response_start_1
        self.response_start_2 = response_start_2
        self.response_progress_1 = response_progress_1
        self.response_progress_2 = response_progress_2
        self.items = itemsdict
        self.enemies = enemiesdict
        self.return_npc = return_npc
        self.start_npc = start_npc
        # Special items the user is given upon starting an objective
        self.quest_items = quest_items


class Player:
    """The class where all user data will be stored while playing.

    Default values are assigned on registration and change as the user progresses through the game.
    These values will be used in most functions to track the user's current progress and check if they are eligible
    for certain actions. The skills gain experience through skill actions and level up to provide more benefits to
    gameplay.
    """
    def __init__(self, name, skills, flags, inventory, bank, curr_area, curr_action, curr_shop, curr_spell, curr_item,
                 att_style, equipment, health=None, spawn=2, quest_flags=None):
        self.name = name
        self.skills = skills
        self.flags = flags
        self.inventory = inventory
        self.bank = bank
        self.curr_area = curr_area
        self.curr_action = curr_action
        self.curr_shop = curr_shop
        self.curr_spell = curr_spell
        self.curr_item = curr_item
        self.att_style = att_style
        self.equipment = equipment
        self.health = health
        if health is None:
            self.health = self.skills['Hitpoints'][0]
        self.spawn = spawn
        self.quest_flags = quest_flags
        if self.quest_flags is None:
            self.quest_flags = []
        self.att_speed = Items.get(self.equipment.get('Weapon', 82), Items[82]).att_speed
        self.eating = False

    def list_data(self):
        """Saves the user data to list of strings which are later stored in a database."""
        save_data = list(vars(self).values())[:-2]
        save_data = [str(i) for i in save_data]
        return save_data


class Item:
    """Standard items for the user to collect, use and buy/sell.

    Each has associated data like value, whether it stacks in the inventory or not, and the type of action it can be
    used for. Some may have requirements that functions can check before use, or a list of items that can be used to
    create it.
    """
    def __init__(self, num, name, value, stackable, examine='', resources=(), skill_reqs=None, xp=0, food=0, burn=False,
                 cook=False, quest_item=None):
        self.id = num
        self.name = name
        self.value = value
        self.stackable = stackable
        self.equippable = False
        self.food = food
        self.examine = examine
        self.burn = burn
        self.cook = cook
        self.xp = xp
        self.resources = resources
        self.quest_item = quest_item
        if skill_reqs is None:
            self.skill_reqs = {}
        else:
            self.skill_reqs = skill_reqs


class Equipment(Item):
    """Special class of items that may be equipped for use in combat.

    Each has an assortment of stats for use in combat functions, as well as the usual item properties.
    """
    def __init__(self, num, name, value, stackable, slot, examine='', resources=(), skill_reqs=None, att_style='Melee',
                 two_handed=False, att_speed=2400, acc_rating_melee=0, acc_rating_ranged=0, acc_rating_magic=0,
                 str_bonus_melee=0, str_bonus_ranged=0, str_bonus_magic=0, melee_def=0, ranged_def=0, magic_def=0,
                 equip_reqs=None, xp=0):
        super().__init__(num, name, value, stackable, examine, resources, skill_reqs, xp)
        self.equippable = True
        self.slot = slot
        self.att_speed = att_speed
        self.att_style = att_style
        self.acc_rating_melee = acc_rating_melee
        self.acc_rating_ranged = acc_rating_ranged
        self.acc_rating_magic = acc_rating_magic
        self.str_bonus_melee = str_bonus_melee
        self.str_bonus_ranged = str_bonus_ranged
        self.str_bonus_magic = str_bonus_magic
        self.melee_def = melee_def
        self.ranged_def = ranged_def
        self.magic_def = magic_def
        self.two_handed = two_handed
        self.equip_reqs = equip_reqs


class Tool(Item):
    """Special class of items that are used while training gathering skills eg. Fishing.

    Tools come in a range of tiers that improve the success chance of an activity within the skill, with higher tiers
    requiring higher skill levels. Some tools may also be equipped, so standard combat stats are included here.
    """
    def __init__(self, num, name, value, stackable, skill, tier, req, acc_rating_melee=0, acc_rating_ranged=0,
                 acc_rating_magic=0, str_bonus_melee=0, str_bonus_ranged=0, str_bonus_magic=0, melee_def=0,
                 ranged_def=0, magic_def=0, equip_reqs=None, equippable=False, examine=''):
        super().__init__(num, name, value, stackable, examine)
        self.skill = skill
        self.tier = tier
        self.req = req
        self.equippable = equippable
        self.slot = 'Weapon'
        self.att_style = 'Melee'
        self.two_handed = False
        self.att_speed = 3000
        self.acc_rating_melee = acc_rating_melee
        self.acc_rating_ranged = acc_rating_ranged
        self.acc_rating_magic = acc_rating_magic
        self.str_bonus_melee = str_bonus_melee
        self.str_bonus_ranged = str_bonus_ranged
        self.str_bonus_magic = str_bonus_magic
        self.melee_def = melee_def
        self.ranged_def = ranged_def
        self.magic_def = magic_def
        self.equip_reqs = equip_reqs


class Inventory:                            # Storing item and quantity as [item_id, quantity]
    """The user's inventory for storing items.

    Has 28 slots but some items can stack with themselves in a single slot, allowing many more than 28 items.
    Automatically organised upon any change to its contents, pushing empty slots to the bottom to make certain
    functions simpler. User can interact with any item in the inventory based on the item's properties.
    """
    def __init__(self, slot0=None, slot1=None, slot2=None, slot3=None, slot4=None, slot5=None, slot6=None, slot7=None,
                 slot8=None, slot9=None, slot10=None, slot11=None, slot12=None, slot13=None, slot14=None, slot15=None,
                 slot16=None, slot17=None, slot18=None, slot19=None, slot20=None, slot21=None, slot22=None, slot23=None,
                 slot24=None, slot25=None, slot26=None, slot27=None, curr_selection=None):
        self.slot0 = slot0
        self.slot1 = slot1
        self.slot2 = slot2
        self.slot3 = slot3
        self.slot4 = slot4
        self.slot5 = slot5
        self.slot6 = slot6
        self.slot7 = slot7
        self.slot8 = slot8
        self.slot9 = slot9
        self.slot10 = slot10
        self.slot11 = slot11
        self.slot12 = slot12
        self.slot13 = slot13
        self.slot14 = slot14
        self.slot15 = slot15
        self.slot16 = slot16
        self.slot17 = slot17
        self.slot18 = slot18
        self.slot19 = slot19
        self.slot20 = slot20
        self.slot21 = slot21
        self.slot22 = slot22
        self.slot23 = slot23
        self.slot24 = slot24
        self.slot25 = slot25
        self.slot26 = slot26
        self.slot27 = slot27
        self.curr_selection = curr_selection

    def add_to_inv(self, item_id, quantity=1):
        """Adds the given item(s) and quantity to the inventory. Stacks with existing items where possible. Allows
        the use of a list in place of item_id to add multiple items at once, with an optional quantity list."""
        if item_id is None:
            return
        if type(item_id) == list:
            # Enable adding list of items at once with list of quantities
            if type(quantity) != list:
                quantity = [1]*len(item_id)
            if len(quantity) < len(item_id):
                quantity.extend([1]*(len(item_id)-len(quantity)))
            for i, j in zip(item_id, quantity):
                self.add_to_inv(i, j)
            return
        added = 0
        if Items[item_id].stackable:
            for i in range(28):
                # Check if the item already has a stack to add to
                if vars(self)['slot'+str(i)] is not None and vars(self)['slot'+str(i)][0] == item_id:
                    vars(self)['slot'+str(i)][1] += quantity
                    print(f"Added {Items[item_id].name} x {quantity} to inventory.")
                    return f"Added {Items[item_id].name} x {quantity} to inventory.", 'normal'
            for i in range(28):
                # Add to first empty slot if no existing stack
                if vars(self)['slot'+str(i)] is None:
                    vars(self)['slot' + str(i)] = [item_id, quantity]
                    print(f"Added {Items[item_id].name} x {quantity} to inventory.")
                    return f"Added {Items[item_id].name} x {quantity} to inventory.", 'normal'
            return f"Inventory is full! Item discarded: {Items[item_id].name} x {quantity}", 'warning', 0
        else:
            for j in range(quantity):
                # Add to first empty slot for each item in quantity
                for i in range(28):
                    if vars(self)['slot'+str(i)] is None:
                        vars(self)['slot' + str(i)] = [item_id, 1]
                        added += 1
                        break
                    if i == 27:
                        # If couldn't add, inv is full
                        if added > 0:
                            print(f"Added {Items[item_id].name} x {added} to inventory.")
                            return f"Added {Items[item_id].name} x {added} to inventory." + "\n" + \
                                   f"Inventory is full! Item discarded: {Items[item_id].name} x {quantity - added}", \
                                   'warning', added      # May fix this to only put the 2nd part in red
                        print(f"Inventory is full! Item discarded: {Items[item_id].name} x {quantity - added}")
                        return f"Inventory is full! Item discarded: {Items[item_id].name} x {quantity - added}", \
                               'warning', 0
            return f"Added {Items[item_id].name} x {added} to inventory.", 'normal'

    def is_in_inv(self, item_id):
        """Simply checks for an item in the user's inventory. If found, returns the quantity and the specific inventory
        slots where the item can be found, for use in other functions. Conveniently this allows it to work as a boolean
        if that is all that is required."""
        if Items[item_id].stackable:
            for i in range(28):
                if vars(self)['slot' + str(i)] is not None and vars(self)['slot' + str(i)][0] == item_id:
                    return i, vars(self)['slot' + str(i)][1]
            return False
        else:
            slots = []
            count = 0
            for i in range(28):
                if vars(self)['slot' + str(i)] is not None and vars(self)['slot' + str(i)][0] == item_id:
                    slots.append(i)
                    count += vars(self)['slot' + str(i)][1]
            if count > 1:
                return slots, count
            if count == 1:
                return slots[0], 1
            return False

    def shuffle_inv2(self):
        """Old inventory sorting function. (swaps empty with last item instead of a smoother sort)."""
        for i in range(28):
            if vars(self)['slot' + str(i)] is None:
                # Find first empty slot
                for j in range(27, i, -1):
                    # Find item closest to end and swap them
                    if vars(self)['slot' + str(j)] is not None:
                        vars(self)['slot' + str(i)], vars(self)['slot' + str(j)] = vars(self)['slot' + str(j)], \
                                                                                       vars(self)['slot' + str(i)]
                        print(f"Swapped slots {i} and {j}!")
                        break
                    if j == i+1:
                        # If cannot find a non-empty slot after slot_i then inv is sorted correctly
                        return

    def shuffle_inv(self):
        """Shuffles the items in the inventory so that the empty slots are at the bottom. This is achieved by swapping
        empty slots with the nearest item one by one so that the order of non-empty slots is unaffected."""
        for i in range(28):
            if vars(self)['slot' + str(i)] is None and i != 27:
                vars(self)['slot' + str(i)], vars(self)['slot' + str(i+1)] = vars(self)['slot' + str(i+1)], \
                                                                           vars(self)['slot' + str(i)]
        for i in range(28):
            if vars(self)['slot' + str(i)] is None:
                for j in range(27, i, -1):
                    if vars(self)['slot' + str(j)] is not None:
                        # Find out if there is an item after None. If so, run again
                        self.shuffle_inv()
                        return
                    if j == i+1:
                        # If cannot find a non-empty slot after slot_i then inv is sorted correctly
                        return

    def free_spaces(self):
        """Returns the number of empty slots in the inventory."""
        free = 0
        for i in range(27, -1, -1):
            if vars(self)['slot'+str(i)] is None:
                free += 1
            else:
                break
        return free

    def max_stack(self):
        """Returns the value of the largest stack currently in the inventory. Used for quantity buttons."""
        curr_max = 0
        for i in range(28):
            if vars(self)['slot'+str(i)] is None:
                break
            if vars(self)['slot'+str(i)][1] > curr_max:
                curr_max = vars(self)['slot'+str(i)][1]
        return curr_max

    def is_cookable(self):
        """Returns the slots which contain items ready to be processed via the cooking skill."""
        slots = []
        ids = []
        for i in range(28):
            if vars(self)['slot'+str(i)] is None:
                continue
            if Items[vars(self)['slot'+str(i)][0]].cook:
                if vars(self)['slot'+str(i)][0] not in ids:
                    slots.append(i)
                    ids.append(vars(self)['slot'+str(i)][0])
        if slots:
            return slots
        else:
            return False

    def remove_item(self, item_id, quantity=1):
        """Removes a given item and quantity from the inventory. Automatically sorts it afterwards."""
        if item_id is None or not self.is_in_inv(item_id):
            return
        if Items[item_id].stackable:
            slot = self.is_in_inv(item_id)[0]
            vars(self)['slot'+str(slot)][1] -= quantity
            if vars(self)['slot'+str(slot)][1] <= 0:
                vars(self)['slot' + str(slot)] = None
                self.shuffle_inv()
            return
        slots, count = self.is_in_inv(item_id)
        if type(slots) == int:
            loops = 1
        else:
            loops = min(quantity, len(slots))
        # Remove the given number of non-stackable items one by one
        for i in range(loops):
            # The slots variable can either be a list or an integer depending on number of items found
            if count != 1:
                vars(self)['slot'+str(slots[-1])] = None
            else:
                vars(self)['slot' + str(slots)] = None
        self.shuffle_inv()

    def remove_special_item(self, item_property, property_value):
        """Removes all items in the inventory that have a given property. Currently only quest items exist."""
        for i in range(28):
            if vars(self)['slot' + str(i)] is not None and vars(
                    Items[vars(self)['slot' + str(i)][0]])[item_property] is not None:
                if vars(Items[vars(self)['slot' + str(i)][0]])[item_property] == property_value:
                    vars(self)['slot' + str(i)] = None
        self.shuffle_inv()

    def __repr__(self):
        """Converts the inventory into string format for saving purposes."""
        final_str = 'Inventory('
        for i in range(28):
            if vars(self)['slot' + str(i)] is not None:
                final_str += str(vars(self)['slot' + str(i)])
                if i <= 26 and vars(self)['slot' + str(i+1)] is not None:
                    final_str += ', '
        return final_str + ')'


class Bank:
    """The bank for storing items that won't fit in the inventory.

    Currently allows 4 inventory sized tabs of items, and all items will stack in a bank slot regardless of their
    normal inventory behaviour. Has an associated quantity which allows the user to withdraw or deposit larger
    amounts of items at once.
    """
    def __init__(self, tab_1=Inventory(), tab_2=Inventory(), tab_3=Inventory(), tab_4=Inventory(), quantityy=1):
        self.tab_1 = tab_1
        self.tab_2 = tab_2
        self.tab_3 = tab_3
        self.tab_4 = tab_4
        self.quant = quantityy
        self.active_tab = self.tab_1

    def add_to_inv(self, item_id, quantity=1):
        """Adds the given item(s) and quantity to the bank. Allows a list of items and optional quantity list to be
        added all at once. Adds to existing stacks where possible. Adds to the currently active tab that is being
        viewed, unless the tab is full and contains no stacks of the item being added. In this case, the next tab is
        selected for deposit."""
        if item_id is None:
            return False
        if type(item_id) == list:
            if type(quantity) != list:
                quantity = [1] * len(item_id)
            if len(quantity) < len(item_id):
                quantity.extend([1] * (len(item_id) - len(quantity)))
            for i, j in zip(item_id, quantity):
                # Enable adding list of items at once with list of quantities
                self.add_to_inv(i, j)
            return
        if self.look_for_stack(item_id, self.tab_1):
            self.active_tab = self.tab_1
        elif self.look_for_stack(item_id, self.tab_2):
            self.active_tab = self.tab_2
        elif self.look_for_stack(item_id, self.tab_3):
            self.active_tab = self.tab_3
        elif self.look_for_stack(item_id, self.tab_4):
            self.active_tab = self.tab_4
        else:
            for i in range(28):
                # Add to first empty slot if no existing stack
                if vars(self.active_tab)['slot' + str(i)] is None:
                    vars(self.active_tab)['slot' + str(i)] = [item_id, quantity]
                    return f"Added {Items[item_id].name} x {quantity} to bank.", 'normal'
        for i in range(28):
            # Check if the item already has a stack to add to
            if vars(self.active_tab)['slot'+str(i)] is not None and vars(self.active_tab)['slot'+str(i)][0] == item_id:
                vars(self.active_tab)['slot'+str(i)][1] += quantity
                return f"Added {Items[item_id].name} x {quantity} to bank.", 'normal'
        j = 1
        while self.active_tab.slot27 is not None and j < 4:
            # Find next tab with space
            self.next_tab()
            j += 1
        if j == 4:
            # Bank is full
            return False
        else:
            for i in range(28):
                # Add to first empty slot if no existing stack
                if vars(self.active_tab)['slot' + str(i)] is None:
                    vars(self.active_tab)['slot' + str(i)] = [item_id, quantity]
                    print(item_id)
                    print(f"Added {Items[item_id].name} x {quantity} to bank.")
                    return f"Added {Items[item_id].name} x {quantity} to bank.", 'normal'
        return True

    @staticmethod
    def look_for_stack(item_id, tab):
        """Searches the bank in the specified tab for a given item."""
        for i in range(28):
            # Check if the item already has a stack to add to in tab
            if vars(tab)['slot'+str(i)] is not None and vars(tab)['slot'+str(i)][0] == item_id:
                return True
        return False

    def next_tab(self):
        """Switches active tab to the next one, looping back around from 4 to 1."""
        if self.active_tab == self.tab_1:
            self.active_tab = self.tab_2
        elif self.active_tab == self.tab_2:
            self.active_tab = self.tab_3
        elif self.active_tab == self.tab_3:
            self.active_tab = self.tab_4
        elif self.active_tab == self.tab_4:
            self.active_tab = self.tab_1

    def remove_from_bank(self, item_id=None, quantity=None, item_property=None, property_value=None):
        """Removes the given item and quantity from the bank. If instead a property is given, removes all items with
        that property from the bank eg. quest items."""
        if item_id is not None:
            # Remove items normally or remove special items eg. quest items from bank
            for tab in [self.tab_1, self.tab_2, self.tab_3, self.tab_4]:
                for i in range(28):
                    if vars(tab)['slot' + str(i)] is not None and vars(tab)['slot' + str(i)][0] == item_id:
                        if quantity is None or quantity >= vars(tab)['slot' + str(i)][1]:
                            vars(tab)['slot' + str(i)] = None
                        else:
                            vars(tab)['slot' + str(i)][1] -= quantity
                tab.shuffle_inv()
        elif item_property is not None and property_value is not None:
            for tab in [self.tab_1, self.tab_2, self.tab_3, self.tab_4]:
                for i in range(28):
                    if vars(tab)['slot' + str(i)] is not None and vars(
                            Items[vars(tab)['slot' + str(i)][0]])[item_property] is not None:
                        if vars(Items[vars(tab)['slot' + str(i)][0]])[item_property] == property_value:
                            vars(tab)['slot' + str(i)] = None
                tab.shuffle_inv()
        else:
            print("Bad input for remove_from_bank")

    def is_in_bank(self, item_id):
        """Checks the entire bank for the given item."""
        for tab in [self.tab_1, self.tab_2, self.tab_3, self.tab_4]:
            for i in range(28):
                if vars(tab)['slot' + str(i)] is not None and vars(tab)['slot' + str(i)][0] == item_id:
                    return True
        return False

    def __repr__(self):
        """Converts the bank to a string for save purposes."""
        final_str = 'Bank('
        for i in range(1, 5):
            final_str += str(vars(self)['tab_' + str(i)])
            if i <= 3 and vars(self)['tab_' + str(i+1)] is not None:
                final_str += ', '
        return final_str + ')'


class Shop:
    """A shop that contains various items for the user to buy and sell.

    Each shop is accessed through an NPC that owns it.
    Prices are based on the defined values of each item, with variance between buying and selling.
    """
    def __init__(self, stock=Inventory()):
        self.stock = stock

    def __repr__(self):
        """Converts shop to string for save purposes."""
        final_str = 'Shop(' + str(self.stock) + ')'
        return final_str


class Spell:
    """A magic spell that the user can cast with the required magic level and runes.

    Categorised into combat and utility spells, with combat spells having damage values while utility spells have
    experience values, along with quest/skill requirements, and a destination area.
    Currently utility spells consist purely of teleports.
    """
    def __init__(self, name, num, level, runes, damage=0, xp=0, spell_type='Combat', area=None, quest_reqs=None,
                 skill_reqs=None):
        self.name = name
        self.level = level
        self.runes = runes
        self.damage = damage
        self.type = spell_type
        self.xp = xp
        self.id = num
        self.area = area
        self.quest_reqs = quest_reqs
        self.skill_reqs = skill_reqs
        if quest_reqs is None:
            self.quest_reqs = []
        if skill_reqs is None:
            self.skill_reqs = {}

# Item dict format:
# Items = {id : {Item(id, name, value, stackable, examine, ... ), ...}


Items = {'None': Item(None, 'None', None, False),
         0: Item(0, 'gold coins', 1, True, examine="Lovely money!"),
         1: Item(1, 'Egg', 3, False, examine="What came first..."),
         2: Item(2, 'Bucket of milk', 5, False, examine="Great for a cake."),
         3: Item(3, 'Logs', 2, False, skill_reqs={'Firemaking': 0, 'Fletching': 0}, burn=True, xp=30,
                 examine="Good for burning or cutting. (Level 1)"),
         4: Item(4, 'Oak logs', 5, False, skill_reqs={'Firemaking': 15, 'Fletching': 15}, burn=True, xp=60,
                 examine="Good for burning or cutting. (Level 15)"),
         5: Item(5, 'Willow logs', 8, False, skill_reqs={'Firemaking': 30, 'Fletching': 30}, burn=True, xp=90,
                 examine="Good for burning or cutting. (Level 30)"),
         6: Item(6, 'Teak logs', 15, False, skill_reqs={'Firemaking': 35}, burn=True, xp=100,
                 examine="Good for burning. (Level 35)"),
         7: Item(7, 'Maple logs', 18, False, skill_reqs={'Firemaking': 45, 'Fletching': 45}, burn=True, xp=130,
                 examine="Good for burning or cutting. (Level 45)"),
         8: Item(8, 'Mahogany logs', 30, False, skill_reqs={'Firemaking': 55}, burn=True, xp=150,
                 examine="Good for burning. (Level 55)"),
         9: Item(9, 'Yew logs', 60, False, skill_reqs={'Firemaking': 60, 'Fletching': 60}, burn=True, xp=200,
                 examine="Good for burning or cutting. (Level 60)"),
         10: Item(10, 'Magic logs', 150, False, skill_reqs={'Firemaking': 75, 'Fletching': 75}, burn=True, xp=300,
                  examine="Good for burning or cutting. (Level 75)"),
         11: Item(11, 'Raw shrimp', 2, False, cook=True, skill_reqs={'Cooking': 0}, xp=30,
                  examine="Ready to be cooked. (Level 1)"),
         12: Item(12, 'Shrimp', 2, False, food=3, examine="Heals for 3 health when used as food."),
         13: Item(13, 'Raw herring', 4, False, cook=True, skill_reqs={'Cooking': 5}, xp=50,
                  examine="Ready to be cooked. (Level 5)"),
         14: Item(14, 'Herring', 4, False, food=5, examine="Heals for 5 health when used as food."),
         15: Item(15, 'Raw trout', 9, False, cook=True, skill_reqs={'Cooking': 20}, xp=70,
                  examine="Ready to be cooked. (Level 20)"),
         16: Item(16, 'Trout', 9, False, food=7, examine="Heals for 7 health when used as food."),
         17: Item(17, 'Raw salmon', 14, False, cook=True, skill_reqs={'Cooking': 30}, xp=90,
                  examine="Ready to be cooked. (Level 30)"),
         18: Item(18, 'Salmon', 14, False, food=9, examine="Heals for 9 health when used as food."),
         19: Item(19, 'Raw lobster', 30, False, cook=True, skill_reqs={'Cooking': 40}, xp=120,
                  examine="Ready to be cooked. (Level 40)"),
         20: Item(20, 'Lobster', 30, False, food=12, examine="Heals for 12 health when used as food."),
         21: Item(21, 'Raw swordfish', 50, False, cook=True, skill_reqs={'Cooking': 50}, xp=140,
                  examine="Ready to be cooked. (Level 50)"),
         22: Item(22, 'Swordfish', 50, False, food=14, examine="Heals for 14 health when used as food."),
         23: Item(23, 'Raw shark', 200, False, cook=True, skill_reqs={'Cooking': 70}, xp=200,
                  examine="Ready to be cooked. (Level 70)"),
         24: Item(24, 'Shark', 200, False, food=20, examine="Heals for 20 health when used as food."),
         25: Item(25, 'Raw manta ray', 400, False, cook=True, skill_reqs={'Cooking': 85}, xp=240,
                  examine="Ready to be cooked. (Level 85)"),
         26: Item(26, 'Manta ray', 400, False, food=22, examine="Heals for 22 health when used as food."),
         27: Item(27, 'Knife', 5, False, examine="A sharp knife."),
         28: Item(28, 'Hammer', 5, False, examine="Good for working metal."),
         29: Item(29, 'Arrow shafts', 2, True, skill_reqs={'Fletching': 0}, resources={},
                  examine="Used for making arrows. (level 1)", xp=30),
         30: Item(30, 'Headless arrow', 2, True, skill_reqs={'Fletching': 0}, resources={29: 1, 36: 1},
                  examine="I can add metal arrowheads to these. (Level 1+)", xp=45),
         31: Equipment(31, 'Leather cowl', 12, False, 'Head', acc_rating_ranged=1, melee_def=3, ranged_def=3,
                       magic_def=2, resources={175: 1}, skill_reqs={'Crafting': 1}, xp=20,
                       examine="Light protective gear for archers."),
         32: Equipment(32, 'Leather vambraces', 12, False, 'Hands', acc_rating_ranged=4, melee_def=2,
                       resources={175: 1}, skill_reqs={'Crafting': 5}, xp=20,
                       examine="Light protective gear for archers."),
         33: Equipment(33, 'Leather chaps', 24, False, 'Legs', acc_rating_ranged=4, melee_def=2,
                       resources={175: 2}, skill_reqs={'Crafting': 10}, xp=40,
                       examine="Light protective gear for archers."),
         34: Equipment(34, 'Leather body', 36, False, 'Body', acc_rating_ranged=4, acc_rating_magic=-2,
                       melee_def=9, ranged_def=9, magic_def=4, resources={175: 3}, skill_reqs={'Crafting': 15}, xp=60,
                       examine="Light protective gear for archers."),
         35: Equipment(35, 'Leather boots', 12, False, 'Feet', melee_def=1, ranged_def=1,
                       examine="Light protective gear."),
         36: Item(36, 'Feather', 5, True, examine="Some good multi purpose feathers."),
         37: Item(37, 'Bow string', 10, True, examine="I could string a bow with this. (Level 1+)"),
         38: Item(38, 'Pot of flour', 6, False, examine="A pot filled with flour from the mill."),
         39: Item(39, 'Tinderbox', 5, False, examine="Starts fires."),
         40: Equipment(40, 'Bronze gloves', 6, False, 'Hands', melee_def=2, ranged_def=2, magic_def=1,
                       acc_rating_melee=2, acc_rating_ranged=2, acc_rating_magic=1,
                       examine="A pair of gloves made from bronze. (Level 1)"),
         41: Equipment(41, 'Torn cape', 10, False, 'Cape', melee_def=2, ranged_def=2, magic_def=1,
                       examine="A long, tattered piece of fabric."),
         42: Equipment(42, 'Amulet of strength', 10, False, 'Neck', str_bonus_melee=10,
                       examine="An enchanted amulet for warriors."),
         43: Equipment(43, 'Old ring', 10, False, 'Ring', acc_rating_magic=2, acc_rating_ranged=2,
                       acc_rating_melee=2, str_bonus_melee=2, str_bonus_ranged=2, str_bonus_magic=2, melee_def=2,
                       ranged_def=2, magic_def=2, examine="Seems to hold a kind of magical power."),
         44: Item(44, 'Needle', 2, False, examine="Used to craft things."),
         45: Tool(45, 'Bronze axe', 6, False, 'Woodcutting', 1, 1, acc_rating_melee=7,
                      str_bonus_melee=8, equippable=True, examine='A tool used for Woodcutting. (Level 1)'),
         46: Tool(46, 'Iron axe', 12, False, 'Woodcutting', 2, 10, acc_rating_melee=12,
                      str_bonus_melee=12, equippable=True, examine='A tool used for Woodcutting. (Level 10)'),
         47: Tool(47, 'Steel axe', 43, False, 'Woodcutting', 3, 20, acc_rating_melee=15,
                      str_bonus_melee=16, equippable=True, examine='A tool used for Woodcutting. (Level 20)'),
         48: Tool(48, 'Mithril axe', 128, False, 'Woodcutting', 4, 30, acc_rating_melee=23,
                      str_bonus_melee=22, equippable=True, examine='A tool used for Woodcutting. (Level 30)'),
         49: Tool(49, 'Adamant axe', 556, False, 'Woodcutting', 5, 40, acc_rating_melee=32,
                      str_bonus_melee=36, equippable=True, examine='A tool used for Woodcutting. (Level 40)'),
         50: Tool(50, 'Rune axe', 7800, False, 'Woodcutting', 6, 50, acc_rating_melee=45,
                      str_bonus_melee=48, equippable=True, examine='A tool used for Woodcutting. (Level 50)'),
         51: Tool(51, 'Dragon axe', 75000, False, 'Woodcutting', 7, 60, acc_rating_melee=60,
                      str_bonus_melee=61, equippable=True, examine='A tool used for Woodcutting. (Level 60)'),
         52: Tool(52, 'Bronze pickaxe', 6, False, 'Mining', 1, 1, acc_rating_melee=7,
                      str_bonus_melee=8, equippable=True, examine='A tool used for Mining. (Level 1)'),
         53: Tool(53, 'Iron pickaxe', 12, False, 'Mining', 2, 10, acc_rating_melee=12,
                      str_bonus_melee=12, equippable=True, examine='A tool used for Mining. (Level 10)'),
         54: Tool(54, 'Steel pickaxe', 43, False, 'Mining', 3, 20, acc_rating_melee=15,
                      str_bonus_melee=16, equippable=True, examine='A tool used for Mining. (Level 20)'),
         55: Tool(55, 'Mithril pickaxe', 128, False, 'Mining', 4, 30, acc_rating_melee=23,
                      str_bonus_melee=22, equippable=True, examine='A tool used for Mining. (Level 30)'),
         56: Tool(56, 'Adamant pickaxe', 556, False, 'Mining', 5, 40, acc_rating_melee=32,
                      str_bonus_melee=36, equippable=True, examine='A tool used for Mining. (Level 40)'),
         57: Tool(57, 'Rune pickaxe', 7800, False, 'Mining', 6, 50, acc_rating_melee=45,
                      str_bonus_melee=48, equippable=True, examine='A tool used for Mining. (Level 50)'),
         58: Tool(58, 'Dragon pickaxe', 75000, False, 'Mining', 7, 60, acc_rating_melee=60,
                      str_bonus_melee=61, equippable=True, examine='A tool used for Mining. (Level 60)'),
         59: Tool(59, 'Tattered net', 5, False, 'Fishing', 1, 1, examine='A tool used for Fishing. (Level 1)'),
         60: Tool(60, 'Rusty rod', 20, False, 'Fishing', 2, 10, examine='A tool used for Fishing. (Level 10)'),
         61: Tool(61, 'Basic net', 200, False, 'Fishing', 3, 20, examine='A tool used for Fishing. (Level 20)'),
         62: Tool(62, 'Old rod', 500, False, 'Fishing', 4, 30, examine='A tool used for Fishing. (Level 30)'),
         63: Tool(63, 'High quality net', 1000, False, 'Fishing', 5, 40, examine='A tool used for Fishing. (Level 40)'),
         64: Tool(64, 'Good rod', 25000, False, 'Fishing', 6, 50, examine='A tool used for Fishing. (Level 50)'),
         65: Tool(65, 'Full fishing gear', 100000, False, 'Fishing', 7, 60,
                  examine='A tool used for Fishing. (Level 60)'),
         66: Item(66, 'Air rune', 4, True, examine='A basic elemental rune used for air spells.'),
         67: Item(67, 'Water rune', 4, True, examine='A basic elemental rune used for water spells.'),
         68: Item(68, 'Earth rune', 4, True, examine='A basic elemental rune used for earth spells.'),
         69: Item(69, 'Fire rune', 4, True, examine='A basic elemental rune used for fire spells.'),
         70: Item(70, 'Mind rune', 4, True, examine='A basic rune used for weak combat spells.'),
         71: Item(71, 'Chaos rune', 30, True, examine='A rune used for combat spells.'),
         72: Item(72, 'Death rune', 120, True, examine='A rune used for strong combat spells.'),
         73: Item(73, 'Blood rune', 250, True, examine='A rune used for the strongest combat spells.'),
         74: Item(74, 'Law rune', 180, True, examine='A rune used primarily for teleport spells.'),
         75: Item(75, 'Soul rune', 300, True, examine='Placeholder rune'),
         76: Equipment(76, 'Fractured staff', 5, False, 'Weapon', att_style='Magic', att_speed=2400, acc_rating_magic=8,
                       equip_reqs={'Magic': 1}, magic_def=10, examine="A basic magical staff."),
         77: Item(77, 'Copper ore', 3, False, skill_reqs={'Smithing': 0}, examine="Goes great with Tin."),
         78: Item(78, 'Tin ore', 3, False, skill_reqs={'Smithing': 0}, examine="Goes great with Copper."),
         79: Item(79, 'Bronze bar', 5, False, skill_reqs={'Smithing': 0}, xp=30, resources={77: 1, 78: 1},
                  examine="Used to smith bronze items. (Level 1)"),
         80: Item(80, 'Bronze arrowheads', 2, True, skill_reqs={'Fletching': 0, 'Smithing': 0}, xp=1, resources={79: 1},
                  examine="Would look better as arrows. (Level 1)"),
         81: Equipment(81, 'Bronze boots', 6, False, 'Feet', acc_rating_ranged=-1, acc_rating_magic=-3,
                       melee_def=2, ranged_def=1, resources={79: 1}, skill_reqs={'Smithing': 1},
                       examine="Foot protection. (Level 1)"),
         82: Equipment(82, 'Bronze dagger', 6, False, 'Weapon', att_speed=2400, acc_rating_melee=4,
                       str_bonus_melee=3, resources={79: 1}, skill_reqs={'Smithing': 2},
                       examine="Good for stabbing. (Level 1)"),
         83: Equipment(83, 'Bronze sword', 13, False, 'Weapon', att_speed=2400, acc_rating_melee=7,
                       str_bonus_melee=6, resources={79: 2}, skill_reqs={'Smithing': 4},
                       examine="A razor sharp sword. (Level 1)"),
         84: Equipment(84, 'Bronze helmet', 13, False, 'Head', acc_rating_magic=-6, acc_rating_ranged=-3,
                       melee_def=4, ranged_def=4, magic_def=-1, resources={79: 2}, skill_reqs={'Smithing': 6},
                       examine="Head protection. (Level 1)"),
         85: Equipment(85, 'Bronze shield', 19, False, 'Shield', acc_rating_ranged=-3, acc_rating_magic=-8,
                       melee_def=6, ranged_def=6, magic_def=-1, resources={79: 3}, skill_reqs={'Smithing': 8},
                       examine="Extra protection for combat. (Level 1)"),
         86: Equipment(86, 'Bronze 2h sword', 19, False, 'Weapon', two_handed=True, acc_rating_melee=9,
                       str_bonus_melee=10, att_speed=3600, resources={79: 3}, skill_reqs={'Smithing': 10},
                       examine="A large, heavy sword. (Level 1)"),
         87: Equipment(87, 'Bronze platelegs', 19, False, 'Legs', acc_rating_ranged=-11, acc_rating_magic=-21,
                       melee_def=7, ranged_def=7, magic_def=-4, resources={79: 3}, skill_reqs={'Smithing': 12},
                       examine="Leg protection. (Level 1)"),
         88: Equipment(88, 'Bronze platebody', 26, False, 'Body', acc_rating_ranged=-15, acc_rating_magic=-30,
                       melee_def=14, ranged_def=14, magic_def=-6, resources={79: 5}, skill_reqs={'Smithing': 13},
                       examine="Chest protection. (Level 1)"),
         89: Item(89, 'Iron ore', 12, False, skill_reqs={'Smithing': 15},
                  examine="Ready to be smithed into bars. (Level 15)"),
         90: Item(90, 'Iron bar', 15, False, skill_reqs={'Smithing': 15}, xp=60, resources={89: 1},
                  examine="Used to smith iron items. (Level 15)"),
         91: Item(91, 'Iron arrowheads', 3, True, skill_reqs={'Fletching': 15, 'Smithing': 15}, xp=3, resources={90: 1},
                  examine="Would look better as arrows. (Level 15)"),
         92: Equipment(92, 'Iron boots', 16, False, 'Feet', acc_rating_ranged=-1, acc_rating_magic=-3,
                       melee_def=6, equip_reqs={'Defence': 10}, resources={90: 1},
                       skill_reqs={'Smithing': 16}, examine="Foot protection. (Level 10)"),
         93: Equipment(93, 'Iron dagger', 16, False, 'Weapon', att_speed=2400, acc_rating_melee=8,
                       str_bonus_melee=7, equip_reqs={'Attack': 10}, resources={90: 1}, skill_reqs={'Smithing': 17},
                       examine="Good for stabbing. (Level 10)"),
         94: Equipment(94, 'Iron sword', 31, False, 'Weapon', att_speed=2400, acc_rating_melee=15,
                       str_bonus_melee=14, equip_reqs={'Attack': 10}, resources={90: 2}, skill_reqs={'Smithing': 19},
                       examine="A razor sharp sword. (Level 10)"),
         95: Equipment(95, 'Iron helmet', 31, False, 'Head', acc_rating_magic=-6, acc_rating_ranged=-3,
                       melee_def=9, ranged_def=9, magic_def=-1, equip_reqs={'Defence': 10}, resources={90: 2},
                       skill_reqs={'Smithing': 21}, examine="Head protection. (Level 10)"),
         96: Equipment(96, 'Iron shield', 46, False, 'Shield', acc_rating_ranged=-3, acc_rating_magic=-8,
                       melee_def=14, ranged_def=14, magic_def=-1, equip_reqs={'Defence': 10}, resources={90: 3},
                       skill_reqs={'Smithing': 23}, examine="Extra protection for combat. (Level 10)"),
         97: Equipment(97, 'Iron 2h sword', 46, False, 'Weapon', two_handed=True, acc_rating_melee=21,
                       str_bonus_melee=22, att_speed=3600, equip_reqs={'Attack': 10}, resources={90: 3},
                       skill_reqs={'Smithing': 25}, examine="A large, heavy sword. (Level 10)"),
         98: Equipment(98, 'Iron platelegs', 46, False, 'Legs', acc_rating_ranged=-11, acc_rating_magic=-21,
                       melee_def=16, ranged_def=16, magic_def=-4, equip_reqs={'Defence': 10}, resources={90: 3},
                       skill_reqs={'Smithing': 27}, examine="Leg protection. (Level 10)"),
         99: Equipment(99, 'Iron platebody', 76, False, 'Body', acc_rating_ranged=-15, acc_rating_magic=-30,
                       melee_def=30, ranged_def=31, magic_def=-6, equip_reqs={'Defence': 10}, resources={90: 5},
                       skill_reqs={'Smithing': 28}, examine="Chest protection. (Level 10)"),
         100: Item(100, 'Coal', 18, False, skill_reqs={'Smithing': 30}, examine="Used with various ore to make bars."),
         101: Item(101, 'Steel bar', 30, False, skill_reqs={'Smithing': 30}, xp=100, resources={89: 1, 100: 1},
                   examine="Used to smith steel items. (Level 30)"),
         102: Item(102, 'Steel arrowheads', 5, True, skill_reqs={'Fletching': 30, 'Smithing': 30}, xp=5,
                        resources={101: 1}, examine="Would look better as arrows. (Level 30)"),
         103: Equipment(103, 'Steel boots', 31, False, 'Feet', acc_rating_ranged=-1, acc_rating_magic=-3,
                        melee_def=8, equip_reqs={'Defence': 20}, resources={101: 1},
                        skill_reqs={'Smithing': 31}, examine="Foot protection. (Level 20)"),
         104: Equipment(104, 'Steel dagger', 31, False, 'Weapon', att_speed=2400, acc_rating_melee=10,
                        str_bonus_melee=7, equip_reqs={'Attack': 20}, resources={101: 1}, skill_reqs={'Smithing': 32},
                        examine="Good for stabbing. (Level 20)"),
         105: Equipment(105, 'Steel sword', 31, False, 'Weapon', att_speed=2400, acc_rating_melee=19,
                        str_bonus_melee=14, equip_reqs={'Attack': 20}, resources={101: 2}, skill_reqs={'Smithing': 34},
                        examine="A razor sharp sword. (Level 20)"),
         106: Equipment(106, 'Steel helmet', 61, False, 'Head', acc_rating_magic=-6, acc_rating_ranged=-3,
                        melee_def=12, ranged_def=12, magic_def=-1, equip_reqs={'Defence': 20}, resources={101: 2},
                        skill_reqs={'Smithing': 36}, examine="Head protection. (Level 20)"),
         107: Equipment(107, 'Steel shield', 91, False, 'Shield', acc_rating_ranged=-3, acc_rating_magic=-8,
                        melee_def=18, ranged_def=18, magic_def=-1, equip_reqs={'Defence': 20}, resources={101: 3},
                        skill_reqs={'Smithing': 38}, examine="Extra protection for combat. (Level 20)"),
         108: Equipment(108, 'Steel 2h sword', 91, False, 'Weapon', two_handed=True, acc_rating_melee=27,
                        str_bonus_melee=26, att_speed=3600, equip_reqs={'Attack': 20}, resources={101: 3},
                        skill_reqs={'Smithing': 40}, examine="A large, heavy sword. (Level 20)"),
         109: Equipment(109, 'Steel platelegs', 91, False, 'Legs', acc_rating_ranged=-11, acc_rating_magic=-21,
                        melee_def=20, ranged_def=20, magic_def=-4, equip_reqs={'Defence': 20}, resources={101: 3},
                        skill_reqs={'Smithing': 42}, examine="Leg protection. (Level 20)"),
         110: Equipment(110, 'Steel platebody', 151, False, 'Body', acc_rating_ranged=-15, acc_rating_magic=-30,
                        melee_def=38, ranged_def=40, magic_def=-6, equip_reqs={'Defence': 20}, resources={101: 5},
                        skill_reqs={'Smithing': 43}, examine="Chest protection. (Level 20)"),
         111: Item(111, 'Mithril ore', 50, False, skill_reqs={'Smithing': 45},
                   examine="Ready to be smithed into bars. (Level 45)"),
         112: Item(112, 'Mithril bar', 75, False, skill_reqs={'Smithing': 45}, xp=135, resources={111: 1, 100: 2},
                   examine="Used to smith mithril items. (Level 45)"),
         113: Item(113, 'Mithril arrowheads', 9, True, skill_reqs={'Fletching': 45, 'Smithing': 45}, xp=8,
                        resources={112: 1}, examine="Would look better as arrows. (Level 45)"),
         114: Equipment(114, 'Mithril boots', 76, False, 'Feet', acc_rating_ranged=-1, acc_rating_magic=-3,
                        melee_def=9, equip_reqs={'Defence': 30}, resources={112: 1},
                        skill_reqs={'Smithing': 46}, examine="Foot protection. (Level 30)"),
         115: Equipment(115, 'Mithril dagger', 76, False, 'Weapon', att_speed=2400, acc_rating_melee=11,
                        str_bonus_melee=10, equip_reqs={'Attack': 30}, resources={112: 1}, skill_reqs={'Smithing': 47},
                        examine="Good for stabbing. (Level 30)"),
         116: Equipment(116, 'Mithril sword', 151, False, 'Weapon', att_speed=2400, acc_rating_melee=21,
                        str_bonus_melee=20, equip_reqs={'Attack': 30}, resources={112: 2}, skill_reqs={'Smithing': 49},
                        examine="A razor sharp sword. (Level 30)"),
         117: Equipment(117, 'Mithril helmet', 151, False, 'Head', acc_rating_magic=-6, acc_rating_ranged=-3,
                        melee_def=13, ranged_def=13, magic_def=-1, equip_reqs={'Defence': 30}, resources={112: 2},
                        skill_reqs={'Smithing': 51}, examine="Head protection. (Level 30)"),
         118: Equipment(118, 'Mithril shield', 226, False, 'Shield', acc_rating_ranged=-3, acc_rating_magic=-8,
                        melee_def=21, ranged_def=20, magic_def=-1, equip_reqs={'Defence': 30}, resources={112: 3},
                        skill_reqs={'Smithing': 53}, examine="Extra protection for combat. (Level 30)"),
         119: Equipment(119, 'Mithril 2h sword', 226, False, 'Weapon', two_handed=True, acc_rating_melee=30,
                        str_bonus_melee=31, att_speed=3600, equip_reqs={'Attack': 30}, resources={112: 3},
                        skill_reqs={'Smithing': 55}, examine="A large, heavy sword. (Level 30)"),
         120: Equipment(120, 'Mithril platelegs', 226, False, 'Legs', acc_rating_ranged=-11, acc_rating_magic=-21,
                        melee_def=22, ranged_def=22, magic_def=-4, equip_reqs={'Defence': 30}, resources={112: 3},
                        skill_reqs={'Smithing': 57}, examine="Leg protection. (Level 30)"),
         121: Equipment(121, 'Mithril platebody', 376, False, 'Body', acc_rating_ranged=-15, acc_rating_magic=-30,
                        melee_def=44, ranged_def=44, magic_def=-6, equip_reqs={'Defence': 30}, resources={112: 5},
                        skill_reqs={'Smithing': 58}, examine="Chest protection. (Level 30)"),
         122: Item(122, 'Adamantite ore', 120, False, skill_reqs={'Smithing': 60},
                   examine="Ready to be smithed into bars. (Level 60)"),
         123: Item(123, 'Adamant bar', 150, False, skill_reqs={'Smithing': 60}, xp=175, resources={122: 1, 100: 3},
                   examine="Used to smith adamant items. (Level 60)"),
         124: Item(124, 'Adamant arrowheads', 17, True, skill_reqs={'Fletching': 60, 'Smithing': 60}, xp=12,
                        resources={123: 1}, examine="Would look better as arrows. (Level 60)"),
         125: Equipment(125, 'Adamant boots', 151, False, 'Feet', acc_rating_ranged=-1, acc_rating_magic=-3,
                        melee_def=11, str_bonus_melee=1, equip_reqs={'Defence': 40}, resources={123: 1},
                        skill_reqs={'Smithing': 61}, examine="Foot protection. (Level 40)"),
         126: Equipment(126, 'Adamant dagger', 151, False, 'Weapon', att_speed=2400, acc_rating_melee=15,
                        str_bonus_melee=14, equip_reqs={'Attack': 40}, resources={123: 1}, skill_reqs={'Smithing': 62},
                        examine="Good for stabbing. (Level 40)"),
         127: Equipment(127, 'Adamant sword', 301, False, 'Weapon', att_speed=2400, acc_rating_melee=29,
                        str_bonus_melee=28, equip_reqs={'Attack': 40}, resources={123: 2}, skill_reqs={'Smithing': 64},
                        examine="A razor sharp sword. (Level 40)"),
         128: Equipment(128, 'Adamant helmet', 301, False, 'Head', acc_rating_magic=-6, acc_rating_ranged=-3,
                        melee_def=19, ranged_def=19, magic_def=-1, equip_reqs={'Defence': 40}, resources={123: 2},
                        skill_reqs={'Smithing': 66}, examine="Head protection. (Level 40)"),
         129: Equipment(129, 'Adamant shield', 451, False, 'Shield', acc_rating_ranged=-3, acc_rating_magic=-8,
                        melee_def=29, ranged_def=29, magic_def=-1, equip_reqs={'Defence': 40}, resources={123: 3},
                        skill_reqs={'Smithing': 68}, examine="Extra protection for combat. (Level 40)"),
         130: Equipment(130, 'Adamant 2h sword', 451, False, 'Weapon', two_handed=True, acc_rating_melee=43,
                        str_bonus_melee=44, att_speed=3600, equip_reqs={'Attack': 40}, resources={123: 3},
                        skill_reqs={'Smithing': 70}, examine="A large, heavy sword. (Level 40)"),
         131: Equipment(131, 'Adamant platelegs', 451, False, 'Legs', acc_rating_ranged=-11, acc_rating_magic=-21,
                        melee_def=31, ranged_def=31, magic_def=-4, equip_reqs={'Defence': 40}, resources={123: 3},
                        skill_reqs={'Smithing': 72}, examine="Leg protection. (Level 40)"),
         132: Equipment(132, 'Adamant platebody', 751, False, 'Body', acc_rating_ranged=-15, acc_rating_magic=-30,
                        melee_def=60, ranged_def=63, magic_def=-6, equip_reqs={'Defence': 40}, resources={123: 5},
                        skill_reqs={'Smithing': 73}, examine="Chest protection. (Level 40)"),
         133: Item(133, 'Runite ore', 500, False, skill_reqs={'Smithing': 75},
                   examine="Ready to be smithed into bars. (Level 75)"),
         134: Item(134, 'Runite bar', 750, False, skill_reqs={'Smithing': 75}, xp=250, resources={133: 1, 100: 4},
                   examine="Used to smith rune items. (Level 75)"),
         135: Item(135, 'Rune arrowheads', 66, True, skill_reqs={'Fletching': 75, 'Smithing': 75}, xp=15,
                        resources={134: 1}, examine="Would look better as arrows. (Level 75)"),
         136: Equipment(136, 'Rune boots', 501, False, 'Feet', acc_rating_ranged=-1, acc_rating_magic=-3,
                        melee_def=13, str_bonus_melee=2, equip_reqs={'Defence': 50}, resources={134: 1},
                        skill_reqs={'Smithing': 76}, examine="Foot protection. (Level 50)"),
         137: Equipment(137, 'Rune dagger', 501, False, 'Weapon', att_speed=2400, acc_rating_melee=25,
                        str_bonus_melee=24, equip_reqs={'Attack': 50}, resources={134: 1}, skill_reqs={'Smithing': 77},
                        examine="Good for stabbing. (Level 50)"),
         138: Equipment(138, 'Rune sword', 1001, False, 'Weapon', att_speed=2400, acc_rating_melee=45,
                        str_bonus_melee=44, equip_reqs={'Attack': 50}, resources={134: 2}, skill_reqs={'Smithing': 79},
                        examine="A razor sharp sword. (Level 50)"),
         139: Equipment(139, 'Rune helmet', 1001, False, 'Head', acc_rating_magic=-3, acc_rating_ranged=-6,
                        melee_def=30, ranged_def=30, magic_def=-1, equip_reqs={'Defence': 50}, resources={134: 2},
                        skill_reqs={'Smithing': 81}, examine="Head protection. (Level 50)"),
         140: Equipment(140, 'Rune shield', 1501, False, 'Shield', acc_rating_ranged=-3, acc_rating_magic=-8,
                        melee_def=46, ranged_def=46, magic_def=-1, equip_reqs={'Defence': 50}, resources={134: 3},
                        skill_reqs={'Smithing': 83}, examine="Extra protection for combat. (Level 50)"),
         141: Equipment(141, 'Rune 2h sword', 1501, False, 'Weapon', two_handed=True, acc_rating_melee=69,
                        str_bonus_melee=70, att_speed=3600, equip_reqs={'Attack': 50}, resources={134: 3},
                        skill_reqs={'Smithing': 85}, examine="A large, heavy sword. (Level 50)"),
         142: Equipment(142, 'Rune platelegs', 1501, False, 'Legs', acc_rating_ranged=-11, acc_rating_magic=-21,
                        melee_def=49, ranged_def=49, magic_def=-4, equip_reqs={'Defence': 50}, resources={134: 3},
                        skill_reqs={'Smithing': 87}, examine="Leg protection. (Level 50)"),
         143: Equipment(143, 'Rune platebody', 2501, False, 'Body', acc_rating_ranged=-15, acc_rating_magic=-30,
                        melee_def=78, ranged_def=80, magic_def=-6, equip_reqs={'Defence': 50}, resources={134: 5},
                        skill_reqs={'Smithing': 88}, examine="Chest protection. (Level 50)"),
         144: Equipment(144, 'Bronze arrows', 2, True, 'Ammo', equip_reqs={'Ranged': 1}, str_bonus_ranged=7,
                        resources={30: 1, 80: 1}, xp=15, examine="Arrows with bronze heads. (Level 1)"),
         145: Equipment(145, 'Iron arrows', 4, True, 'Ammo', equip_reqs={'Ranged': 10}, str_bonus_ranged=10,
                        resources={30: 1, 91: 1}, xp=45, examine="Arrows with iron heads. (Level 10)"),
         146: Equipment(146, 'Steel arrows', 8, True, 'Ammo', equip_reqs={'Ranged': 20}, str_bonus_ranged=16,
                        resources={30: 1, 102: 1}, xp=75, examine="Arrows with steel heads. (Level 20)"),
         147: Equipment(147, 'Mithril arrows', 12, True, 'Ammo', equip_reqs={'Ranged': 30}, str_bonus_ranged=22,
                        resources={30: 1, 113: 1}, xp=105, examine="Arrows with mithril heads. (Level 30)"),
         148: Equipment(148, 'Adamant arrows', 20, True, 'Ammo', equip_reqs={'Ranged': 40}, str_bonus_ranged=31,
                        resources={30: 1, 124: 1}, xp=150, examine="Arrows with adamant heads. (Level 40)"),
         149: Equipment(149, 'Rune arrows', 50, True, 'Ammo', equip_reqs={'Ranged': 50}, str_bonus_ranged=49,
                        resources={30: 1, 135: 1}, xp=210, examine="Arrows with rune heads. (Level 50)"),
         150: Item(150, 'Shortbow (u)', 2, False, skill_reqs={'Fletching': 5}, resources={3: 1},
                        examine="I need a string for this. (Level 1)", xp=40),
         151: Equipment(151, 'Shortbow', 4, False, 'Weapon', att_style='Ranged', two_handed=True,
                        equip_reqs={'Ranged': 1}, resources={150: 1, 37: 1}, acc_rating_ranged=8, xp=40,
                        examine="Short but effective. (Level 1)"),
         152: Item(152, 'Longbow (u)', 4, False, skill_reqs={'Fletching': 10}, resources={3: 1},
                        examine="I need a string for this. (Level 1)", xp=55),
         153: Equipment(153, 'Longbow', 6, False, 'Weapon', att_style='Ranged', two_handed=True, att_speed=3000,
                        equip_reqs={'Ranged': 1}, resources={152: 1, 37: 1}, acc_rating_ranged=8, xp=55,
                        examine="A large sturdy bow. (Level 1)"),
         154: Item(154, 'Oak shortbow (u)', 8, False, skill_reqs={'Fletching': 20}, resources={4: 1},
                        examine="I need a string for this. (Level 15)", xp=85),
         155: Equipment(155, 'Oak shortbow', 12, False, 'Weapon', att_style='Ranged', two_handed=True,
                        equip_reqs={'Ranged': 10}, resources={154: 1, 37: 1}, acc_rating_ranged=14, xp=85,
                        examine="Short but effective. (Level 10)"),
         156: Item(154, 'Oak longbow (u)', 12, False, skill_reqs={'Fletching': 25}, resources={4: 1},
                        examine="I need a string for this. (Level 15)", xp=100),
         157: Equipment(155, 'Oak longbow', 18, False, 'Weapon', two_handed=True, att_style='Ranged', att_speed=3000,
                        equip_reqs={'Ranged': 10}, resources={156: 1, 37: 1}, acc_rating_ranged=14, xp=100,
                        examine="A large sturdy bow. (Level 10)"),
         158: Item(154, 'Willow shortbow (u)', 24, False, skill_reqs={'Fletching': 35}, resources={5: 1},
                        examine="I need a string for this. (Level 30)", xp=130),
         159: Equipment(155, 'Willow shortbow', 32, False, 'Weapon', two_handed=True, att_style='Ranged',
                        equip_reqs={'Ranged': 20}, resources={158: 1, 37: 1}, acc_rating_ranged=20, xp=130,
                        examine="Short but effective. (Level 20)"),
         160: Item(154, 'Willow longbow (u)', 30, False, skill_reqs={'Fletching': 40}, resources={5: 1},
                        examine="I need a string for this. (Level 30)", xp=145),
         161: Equipment(155, 'Willow longbow', 40, False, 'Weapon', two_handed=True, att_style='Ranged', att_speed=3000,
                        equip_reqs={'Ranged': 20}, resources={160: 1, 37: 1}, acc_rating_ranged=20, xp=145,
                        examine="A large sturdy bow. (Level 20)"),
         162: Item(162, 'Maple shortbow (u)', 45, False, skill_reqs={'Fletching': 50}, resources={7: 1},
                        examine="I need a string for this. (Level 45)", xp=175),
         163: Equipment(163, 'Maple shortbow', 60, False, 'Weapon', two_handed=True, att_style='Ranged',
                        equip_reqs={'Ranged': 30}, resources={162: 1, 37: 1}, acc_rating_ranged=29, xp=175,
                        examine="Short but effective. (Level 30)"),
         164: Item(164, 'Maple longbow (u)', 50, False, skill_reqs={'Fletching': 55}, resources={7: 1},
                        examine="I need a string for this. (Level 45)", xp=190),
         165: Equipment(165, 'Maple longbow', 68, False, 'Weapon', two_handed=True, att_style='Ranged', att_speed=3000,
                        equip_reqs={'Ranged': 30}, resources={164: 1, 37: 1}, acc_rating_ranged=29, xp=190,
                        examine="A large sturdy bow. (Level 30)"),
         166: Item(166, 'Yew shortbow (u)', 90, False, skill_reqs={'Fletching': 65}, resources={9: 1},
                        examine="I need a string for this. (Level 60)", xp=220),
         167: Equipment(167, 'Yew shortbow', 110, False, 'Weapon', two_handed=True, att_style='Ranged',
                        equip_reqs={'Ranged': 40}, resources={166: 1, 37: 1}, acc_rating_ranged=47, xp=220,
                        examine="Short but effective. (Level 40)"),
         168: Item(168, 'Yew longbow (u)', 110, False, skill_reqs={'Fletching': 70}, resources={9: 1},
                        examine="I need a string for this. (Level 60)", xp=235),
         169: Equipment(169, 'Yew longbow', 135, False, 'Weapon', two_handed=True, att_style='Ranged', att_speed=3000,
                        equip_reqs={'Ranged': 40}, resources={168: 1, 37: 1}, acc_rating_ranged=47, xp=235,
                        examine="A large sturdy bow. (Level 40)"),
         170: Item(170, 'Magic shortbow (u)', 215, False, skill_reqs={'Fletching': 80}, resources={10: 1},
                        examine="I need a string for this. (Level 75)", xp=265),
         171: Equipment(171, 'Magic shortbow', 250, False, 'Weapon', two_handed=True, att_style='Ranged',
                        equip_reqs={'Ranged': 50}, resources={170: 1, 37: 1}, acc_rating_ranged=69, xp=265,
                        examine="Short but effective. (Level 50)"),
         172: Item(172, 'Magic longbow (u)', 240, False, skill_reqs={'Fletching': 85}, resources={10: 1},
                        examine="I need a string for this. (Level 75)", xp=280),
         173: Equipment(173, 'Magic longbow', 280, False, 'Weapon', two_handed=True, att_style='Ranged', att_speed=3000,
                        equip_reqs={'Ranged': 50}, resources={172: 1, 37: 1}, acc_rating_ranged=69, xp=280,
                        examine="A large sturdy bow. (Level 50)"),
         174: Item(174, 'Thread', 2, True, examine="Used to craft things."),
         175: Item(175, 'Cow leather', 10, False, examine="Used to craft Ranged armour. (Level 1+)"),
         176: Item(176, 'Frog leather', 45, False, examine="Used to craft Ranged armour. (Level 20+)"),
         177: Item(177, 'Green dragon leather', 100, False, examine="Used to craft Ranged armour. (Level 40+)"),
         178: Item(178, 'Blue dragon leather', 250, False, examine="Used to craft Ranged armour. (Level 50+)"),
         179: Item(179, 'Red dragon leather', 500, False, examine="Used to craft Ranged armour. (Level 60+)"),
         180: Item(180, 'Black dragon leather', 1500, False, examine="Used to craft Ranged armour. (Level 70+)"),
         181: Equipment(181, 'Frog leather coif', 60, False, 'Head', resources={176: 1}, equip_reqs={'Ranged': 20},
                        skill_reqs={'Crafting': 20}, xp=40, acc_rating_magic=-3, acc_rating_ranged=2, melee_def=4,
                        magic_def=2, ranged_def=3, examine="Ranged armour made from frog hide. (Level 20)"),
         182: Equipment(182, 'Frog leather vambraces', 60, False, 'Hands', resources={176: 1},
                        equip_reqs={'Ranged': 20}, skill_reqs={'Crafting': 25}, xp=40, acc_rating_magic=-5,
                        acc_rating_ranged=2, melee_def=2, magic_def=1, ranged_def=1,
                        examine="Ranged armour made from frog hide. (Level 20)"),
         183: Equipment(183, 'Frog leather chaps', 120, False, 'Legs', resources={176: 2}, equip_reqs={'Ranged': 20},
                        skill_reqs={'Crafting': 30}, xp=80, acc_rating_magic=-5, acc_rating_ranged=2, melee_def=8,
                        magic_def=4, ranged_def=9, examine="Ranged armour made from frog hide. (Level 20)"),
         184: Equipment(184, 'Frog leather body', 180, False, 'Body', resources={176: 3}, equip_reqs={'Ranged': 20},
                        skill_reqs={'Crafting': 35}, xp=120, acc_rating_magic=-5, acc_rating_ranged=10, melee_def=26,
                        magic_def=15, ranged_def=32, examine="Ranged armour made from frog hide. (Level 20)"),
         185: Equipment(185, "Green d'hide coif", 240, False, 'Head', resources={177: 1}, equip_reqs={
                        'Ranged': 40, 'Defence': 40}, skill_reqs={'Crafting': 40}, xp=80, acc_rating_magic=-10,
                        acc_rating_ranged=6, melee_def=5, magic_def=4, ranged_def=8,
                        examine="Ranged armour made from green dragonhide. (Level 40)"),
         186: Equipment(186, "Green d'hide vambraces", 240, False, 'Hands', resources={177: 1},
                        equip_reqs={'Ranged': 40, 'Defence': 40}, skill_reqs={'Crafting': 45}, xp=80,
                        acc_rating_magic=-10, acc_rating_ranged=8, melee_def=3, magic_def=2, ranged_def=2,
                        examine="Ranged armour made from green dragonhide. (Level 40)"),
         187: Equipment(187, "Green d'hide chaps", 480, False, 'Legs', resources={177: 2}, equip_reqs={
                        'Ranged': 40, 'Defence': 40}, skill_reqs={'Crafting': 50}, xp=160, acc_rating_magic=-10,
                        acc_rating_ranged=8, melee_def=15, magic_def=8, ranged_def=17,
                        examine="Ranged armour made from green dragonhide. (Level 40)"),
         188: Equipment(188, "Green d'hide body", 720, False, 'Body', resources={177: 3}, equip_reqs={
                        'Ranged': 40, 'Defence': 40},  skill_reqs={'Crafting': 55}, xp=240, acc_rating_magic=-15,
                        acc_rating_ranged=15, melee_def=30, magic_def=20, ranged_def=35,
                        examine="Ranged armour made from green dragonhide. (Level 40)"),
         189: Equipment(189, "Blue d'hide coif", 600, False, 'Head', resources={178: 1}, equip_reqs={
                        'Ranged': 50, 'Defence': 40}, skill_reqs={'Crafting': 50}, xp=100, acc_rating_magic=-10,
                        acc_rating_ranged=8, melee_def=6, magic_def=5, ranged_def=10,
                        examine="Ranged armour made from blue dragonhide. (Level 50)"),
         190: Equipment(190, "Blue d'hide vambraces", 600, False, 'Hands', resources={178: 1},
                        equip_reqs={'Ranged': 50, 'Defence': 40}, skill_reqs={'Crafting': 55}, xp=100,
                        acc_rating_magic=-10, acc_rating_ranged=9, melee_def=4, magic_def=4, ranged_def=3,
                        examine="Ranged armour made from blue dragonhide. (Level 50)"),
         191: Equipment(191, "Blue d'hide chaps", 1200, False, 'Legs', resources={178: 2}, equip_reqs={
                        'Ranged': 50, 'Defence': 40}, skill_reqs={'Crafting': 60}, xp=200, acc_rating_magic=-10,
                        acc_rating_ranged=11, melee_def=18, magic_def=14, ranged_def=20,
                        examine="Ranged armour made from blue dragonhide. (Level 50)"),
         192: Equipment(192, "Blue d'hide body", 1800, False, 'Body', resources={178: 3}, equip_reqs={
                       'Ranged': 50, 'Defence': 40}, skill_reqs={'Crafting': 65}, xp=300, acc_rating_magic=-15,
                        acc_rating_ranged=20, melee_def=36, magic_def=26, ranged_def=40,
                        examine="Ranged armour made from blue dragonhide. (Level 50)"),
         193: Equipment(193, "Red d'hide coif", 1200, False, 'Head', resources={179: 1}, equip_reqs={
                        'Ranged': 60, 'Defence': 40}, skill_reqs={'Crafting': 60}, xp=120, acc_rating_magic=-10,
                        acc_rating_ranged=10, melee_def=8, magic_def=7, ranged_def=12,
                        examine="Ranged armour made from red dragonhide. (Level 60)"),
         194: Equipment(194, "Red d'hide vambraces", 1200, False, 'Hands', resources={179: 1},
                        equip_reqs={'Ranged': 60, 'Defence': 40}, skill_reqs={'Crafting': 65}, xp=120,
                        acc_rating_magic=-10, acc_rating_ranged=10, melee_def=5, magic_def=6, ranged_def=4,
                        examine="Ranged armour made from red dragonhide. (Level 60)"),
         195: Equipment(195, "Red d'hide chaps", 2400, False, 'Legs', resources={179: 2}, equip_reqs={
                        'Ranged': 60, 'Defence': 40}, skill_reqs={'Crafting': 70}, xp=240, acc_rating_magic=-10,
                        acc_rating_ranged=14, melee_def=22, magic_def=18, ranged_def=20,
                        examine="Ranged armour made from red dragonhide. (Level 60)"),
         196: Equipment(196, "Red d'hide body", 3600, False, 'Body', resources={179: 3}, equip_reqs={
                       'Ranged': 60, 'Defence': 40}, skill_reqs={'Crafting': 75}, xp=360, acc_rating_magic=-15,
                        acc_rating_ranged=25, melee_def=42, magic_def=36, ranged_def=45,
                        examine="Ranged armour made from red dragonhide. (Level 60)"),
         197: Equipment(197, "Black d'hide coif", 3200, False, 'Head', resources={180: 1}, equip_reqs={
                        'Ranged': 70, 'Defence': 40}, skill_reqs={'Crafting': 70}, xp=150, acc_rating_magic=-10,
                        acc_rating_ranged=12, melee_def=10, magic_def=8, ranged_def=14,
                        examine="Ranged armour made from red dragonhide. (Level 70)"),
         198: Equipment(198, "Black d'hide vambraces", 3200, False, 'Hands', resources={180: 1},
                        equip_reqs={'Ranged': 70, 'Defence': 40}, skill_reqs={'Crafting': 75}, xp=150,
                        acc_rating_magic=-10, acc_rating_ranged=11, melee_def=6, magic_def=8, ranged_def=5,
                        examine="Ranged armour made from red dragonhide. (Level 70)"),
         199: Equipment(199, "Black d'hide chaps", 6400, False, 'Legs', resources={180: 2}, equip_reqs={
                        'Ranged': 70, 'Defence': 40}, skill_reqs={'Crafting': 80}, xp=300, acc_rating_magic=-10,
                        acc_rating_ranged=17, melee_def=26, magic_def=23, ranged_def=26,
                        examine="Ranged armour made from red dragonhide. (Level 70)"),
         200: Equipment(200, "Black d'hide body", 9600, False, 'Body', resources={180: 3}, equip_reqs={
                        'Ranged': 70, 'Defence': 40}, skill_reqs={'Crafting': 85}, xp=450, acc_rating_magic=-15,
                        acc_rating_ranged=30, melee_def=48, magic_def=45, ranged_def=50,
                        examine="Ranged armour made from red dragonhide. (Level 70)"),
         201: Item(201, "Flowers", 10, False, examine="They smell lovely."),
         202: Equipment(202, 'Old staff', 20, False, 'Weapon', att_style='Magic', att_speed=2400,
                        acc_rating_magic=10, str_bonus_magic=4, magic_def=10, equip_reqs={'Magic': 10},
                        examine="A magical piece of wood. (Level 10)"),
         203: Equipment(203, 'Sturdy staff', 75, False, 'Weapon', att_style='Magic', att_speed=2400,
                        acc_rating_magic=12, str_bonus_magic=6, magic_def=10, equip_reqs={'Magic': 20},
                        examine="A strong magical stick. (Level 20)"),
         204: Equipment(204, 'Magical staff', 150, False, 'Weapon', att_style='Magic', att_speed=2400,
                        acc_rating_magic=14, str_bonus_magic=8, magic_def=11, equip_reqs={'Magic': 30},
                        examine="A staff with a magical aura. (Level 30)"),
         205: Equipment(205, 'Mystic staff', 750, False, 'Weapon', att_style='Magic', att_speed=2400,
                        acc_rating_magic=16, str_bonus_magic=10, magic_def=12, equip_reqs={'Magic': 40},
                        examine="It shines in the light. (Level 40)"),
         206: Equipment(206, 'Enchanted staff', 2500, False, 'Weapon', att_style='Magic', att_speed=2400,
                        acc_rating_magic=18, str_bonus_magic=12, magic_def=15, equip_reqs={'Magic': 50},
                        examine="A staff that was enchanted by a powerful mage. (Level 50)"),
         207: Equipment(207, 'Staff of Nightmares', 10000, False, 'Weapon', att_style='Magic', att_speed=2400,
                        acc_rating_magic=25, str_bonus_magic=20, magic_def=15, equip_reqs={'Magic': 60},
                        examine="An ancient staff corrupted by darkness. (Level 60)"),
         208: Equipment(208, 'Staff of the Gods', 100000, False, 'Weapon', att_style='Magic', att_speed=2400,
                        acc_rating_magic=30, str_bonus_magic=32, magic_def=20, equip_reqs={'Magic': 75},
                        examine="A staff imbued with a God's power. (Level 75)"),
         209: Equipment(209, 'Bow of the Gods', 100000, False, 'Weapon', att_style='Ranged', att_speed=2400,
                        acc_rating_ranged=99, str_bonus_ranged=40, equip_reqs={'Ranged': 75}, two_handed=True,
                        examine="A bow imbued with a God's power. (Level 75)"),
         210: Equipment(210, 'Blade of the Gods', 100000, False, 'Weapon', att_style='Melee',
                        att_speed=2400, acc_rating_melee=94, str_bonus_melee=100, equip_reqs={'Attack': 75},
                        examine="A sword imbued with a God's power. (Level 75)"),
         211: Equipment(211, 'Wizard hat', 12, False, 'Head', equip_reqs={'Magic': 1}, acc_rating_magic=2, magic_def=2,
                        examine="A slightly magical hat. (Level 1)"),
         212: Equipment(212, 'Wizard robe top', 24, False, 'Body', equip_reqs={'Magic': 1}, acc_rating_magic=4,
                        magic_def=3, examine="A slightly magical robe top. (Level 1)"),
         213: Equipment(213, 'Wizard robe bottoms', 18, False, 'Legs', equip_reqs={'Magic': 1}, acc_rating_magic=2,
                        magic_def=2, examine="Some slightly magical robe bottoms. (Level 1)"),
         214: Equipment(214, 'Wizard boots', 12, False, 'Feet', equip_reqs={'Magic': 1}, acc_rating_magic=2,
                        magic_def=1, examine="A slightly magical pair of boots. (Level 1)"),
         215: Equipment(215, 'Enchanted hat', 75, False, 'Head', equip_reqs={'Magic': 20}, acc_rating_magic=3,
                        magic_def=3, examine="A magical hat. (Level 20)"),
         216: Equipment(216, 'Enchanted robe top', 150, False, 'Body', equip_reqs={'Magic': 20}, acc_rating_magic=10,
                        magic_def=10, examine="A magical robe top. (Level 20)"),
         217: Equipment(217, 'Enchanted robe bottoms', 125, False, 'Legs', equip_reqs={'Magic': 20}, acc_rating_magic=7,
                        magic_def=7, examine="Some magical robe bottoms. (Level 20)"),
         218: Equipment(218, 'Enchanted boots', 75, False, 'Feet', equip_reqs={'Magic': 20}, acc_rating_magic=4,
                        magic_def=3, examine="A magical pair of boots. (Level 20)"),
         219: Equipment(219, 'Mystic hat', 200, False, 'Head', equip_reqs={'Magic': 40, 'Defence': 20},
                        acc_rating_magic=4, magic_def=4, examine="A very magical hat. (Level 40)"),
         220: Equipment(220, 'Mystic robe top', 600, False, 'Body', equip_reqs={'Magic': 40, 'Defence': 20},
                        acc_rating_magic=20, magic_def=20, examine="A very magical robe top. (Level 40)"),
         221: Equipment(221, 'Mystic robe bottoms', 400, False, 'Legs', equip_reqs={'Magic': 40, 'Defence': 20},
                        acc_rating_magic=15, magic_def=15, examine="Some very magical robe bottoms. (Level 40)"),
         222: Equipment(222, 'Mystic boots', 200, False, 'Feet', equip_reqs={'Magic': 40, 'Defence': 20},
                        acc_rating_magic=6, magic_def=5, examine="A very magical pair of boots. (Level 40)"),
         223: Equipment(223, 'Nightmare hat', 2000, False, 'Head', equip_reqs={'Magic': 60, 'Defence': 40},
                        acc_rating_magic=6, magic_def=6, melee_def=15,
                        examine="An ancient hat corrupted by darkness. (Level 60)"),
         224: Equipment(224, 'Nightmare robe top', 6000, False, 'Body', equip_reqs={'Magic': 60, 'Defence': 40},
                        acc_rating_magic=30, magic_def=30, melee_def=52,
                        examine="An ancient robe top corrupted by darkness. (Level 60)"),
         225: Equipment(225, 'Nightmare robe bottom', 4000, False, 'Legs', equip_reqs={'Magic': 60, 'Defence': 40},
                        acc_rating_magic=22, magic_def=22, melee_def=33,
                        examine="Some ancient robe bottoms corrupted by darkness. (Level 60)"),
         226: Equipment(226, 'Nightmare boots', 2000, False, 'Feet', equip_reqs={'Magic': 60, 'Defence': 40},
                        acc_rating_magic=10, magic_def=9, melee_def=10,
                        examine="An ancient pair of boots corrupted by darkness. (Level 60)"),
         227: Equipment(227, "Dragon helm", 10000, False, 'Head', equip_reqs={'Defence': 60}, acc_rating_magic=-6,
                        acc_rating_ranged=-3, melee_def=45, ranged_def=46, magic_def=-1,
                        examine="Head protection. (Level 60)"),
         228: Equipment(228, "Dragon platebody", 25000, False, 'Body', equip_reqs={'Defence': 60}, acc_rating_magic=-30,
                        acc_rating_ranged=-15, melee_def=106, ranged_def=106, magic_def=-6,
                        examine="Chest protection. (Level 60)"),
         229: Equipment(229, "Dragon platelegs", 15000, False, 'Legs', equip_reqs={'Defence': 60}, acc_rating_magic=-21,
                        acc_rating_ranged=-11, melee_def=65, ranged_def=65, magic_def=-4,
                        examine="Leg protection. (Level 60)"),
         230: Equipment(230, "Dragon shield", 15000, False, 'Shield', equip_reqs={'Defence': 60}, acc_rating_magic=-8,
                        acc_rating_ranged=-3, melee_def=58, ranged_def=58, magic_def=-1,
                        examine="Extra protection for combat. (Level 60)"),
         231: Equipment(231, "Dragon boots", 5000, False, 'Feet', equip_reqs={'Defence': 60}, acc_rating_magic=-3,
                        acc_rating_ranged=-1, melee_def=17, str_bonus_melee=4, examine="Foot protection. (Level 60)"),
         232: Equipment(232, "Warrior ring", 5000, False, 'Ring', str_bonus_melee=8, acc_rating_melee=10,
                        examine="A legendary ring worn by long forgotten warriors."),
         233: Equipment(233, "Archer ring", 5000, False, 'Ring', str_bonus_ranged=8, acc_rating_ranged=10,
                        examine="A legendary ring worn by long forgotten archers."),
         234: Equipment(234, "Seer's ring", 5000, False, 'Ring', str_bonus_magic=8, acc_rating_magic=10,
                        examine="A legendary ring worn by long forgotten wizards."),
         235: Equipment(235, "Cape of close combat", 4000, False, 'Cape', str_bonus_melee=4, acc_rating_melee=4,
                        melee_def=11, ranged_def=11, magic_def=11,
                        examine="A cape that improves skill with melee weapons."),
         236: Equipment(236, "Cape of arrows", 4000, False, 'Cape', str_bonus_ranged=4, acc_rating_ranged=8,
                        melee_def=4, ranged_def=6, magic_def=8, examine="A cape that has a magical effect on arrows."),
         237: Equipment(237, "Cape of spells", 4000, False, 'Cape', str_bonus_magic=4, acc_rating_magic=4,
                        melee_def=4, ranged_def=2, magic_def=8, examine="A cape that enhances magical power."),
         238: Equipment(238, "Amulet of glory", 2000, False, 'Neck', str_bonus_melee=6, acc_rating_melee=10,
                        acc_rating_ranged=10, acc_rating_magic=10, melee_def=5, ranged_def=5, magic_def=5,
                        examine="A powerful amulet."),
         239: Equipment(239, "Amulet of torture", 20000, False, 'Neck', str_bonus_melee=12, acc_rating_melee=15,
                        examine="A very powerful amulet, enhancing melee power."),
         240: Equipment(240, "Amulet of anguish", 20000, False, 'Neck', str_bonus_ranged=8, acc_rating_ranged=15,
                        examine="A very powerful amulet, enhancing ranged power."),
         241: Equipment(241, "Amulet of the occult", 20000, False, 'Neck', str_bonus_magic=10, acc_rating_magic=15,
                        examine="A very powerful amulet, enhancing magic power."),
         242: Equipment(242, "Enchanted orb", 150, False, 'Shield', equip_reqs={'Magic': 20}, acc_rating_magic=4,
                        magic_def=4, examine="A magical orb. (Level 20)"),
         243: Equipment(243, "Mage's book", 800, False, 'Shield', equip_reqs={'Magic': 40}, acc_rating_magic=8,
                        magic_def=8, examine="A book that belonged to a powerful mage. (Level 40)"),
         244: Equipment(244, "Nightmare orb", 3500, False, 'Shield', equip_reqs={'Magic': 60}, acc_rating_magic=12,
                        magic_def=12, examine="An ancient magical orb, corrupted by darkness. (Level 60)"),
         245: Equipment(245, "Arcane shield", 55000, False, 'Shield', equip_reqs={'Magic': 75, 'Defence': 60},
                        acc_rating_magic=20, magic_def=20, melee_def=50, ranged_def=40,
                        examine="A very powerful shield, imbued with strong magic. (Level 75)"),
         246: Equipment(246, "Dragon arrows", 150, True, 'Ammo', equip_reqs={'Ranged': 60}, str_bonus_ranged=69,
                        examine="Arrows with dragon metal heads. (Level 60)"),
         247: Equipment(247, "Dragon sword", 10000, False, 'Weapon', equip_reqs={'Attack': 60}, acc_rating_melee=67,
                        str_bonus_melee=66, att_style='Melee', examine="A razor sharp sword. (Level 60)"),
         248: Equipment(248, "Dragon 2h sword", 15000, False, 'Weapon', two_handed=True, equip_reqs={'Attack': 60},
                        acc_rating_melee=92, str_bonus_melee=93, att_style='Melee', att_speed=3600,
                        examine="A large, heavy sword. (Level 60)"),
         249: Equipment(249, "Crystal bow", 10000, False, 'Weapon', two_handed=True, equip_reqs={'Ranged': 60},
                        acc_rating_ranged=80, att_style='Ranged',
                        examine="A magical bow, crafted by elves. (Level 60)"),
         250: Equipment(250, "Bronze defender", 50, False, 'Shield', equip_reqs={'Attack': 1, 'Defence': 1},
                        acc_rating_melee=2, acc_rating_magic=-3, acc_rating_ranged=-2, melee_def=2, magic_def=-3,
                        examine="A defensive weapon made from bronze. (Level 1)"),
         251: Equipment(251, "Iron defender", 100, False, 'Shield', equip_reqs={'Attack': 10, 'Defence': 10},
                        acc_rating_melee=6, acc_rating_magic=-3, acc_rating_ranged=-2, melee_def=6, magic_def=-3,
                        str_bonus_melee=1,
                        examine="A defensive weapon made from iron. (Level 10)"),
         252: Equipment(252, "Steel defender", 200, False, 'Shield', equip_reqs={'Attack': 20, 'Defence': 20},
                        acc_rating_melee=8, acc_rating_magic=-3, acc_rating_ranged=-2, melee_def=8, magic_def=-3,
                        str_bonus_melee=2,
                        examine="A defensive weapon made from steel. (Level 20)"),
         253: Equipment(253, "Mithril defender", 400, False, 'Shield', equip_reqs={'Attack': 30, 'Defence': 30},
                        acc_rating_melee=9, acc_rating_magic=-3, acc_rating_ranged=-2, melee_def=9, magic_def=-3,
                        str_bonus_melee=3,
                        examine="A defensive weapon made from mithril. (Level 30)"),
         254: Equipment(254, "Adamant defender", 800, False, 'Shield', equip_reqs={'Attack': 40, 'Defence': 40},
                        acc_rating_melee=12, acc_rating_magic=-3, acc_rating_ranged=-2, melee_def=12, magic_def=-3,
                        str_bonus_melee=4,
                        examine="A defensive weapon made from bronze. (Level 40)"),
         255: Equipment(255, "Rune defender", 1600, False, 'Shield', equip_reqs={'Attack': 50, 'Defence': 50},
                        acc_rating_melee=19, acc_rating_magic=-3, acc_rating_ranged=-2, melee_def=19, magic_def=-3,
                        str_bonus_melee=5,
                        examine="A defensive weapon made from rune. (Level 50)"),
         256: Equipment(256, "Dragon defender", 3200, False, 'Shield', equip_reqs={'Attack': 60, 'Defence': 60},
                        acc_rating_melee=24, acc_rating_magic=-3, acc_rating_ranged=-2, melee_def=24, magic_def=-3,
                        str_bonus_melee=6,
                        examine="A defensive weapon made from dragon metal. (Level 60)"),
         257: Equipment(257, "Iron gloves", 100, False, 'Hands', equip_reqs={'Defence': 10}, acc_rating_melee=4,
                        acc_rating_magic=2, acc_rating_ranged=4, melee_def=4, magic_def=2, ranged_def=4,
                        str_bonus_melee=4, examine="A pair of gloves made from iron. (Level 10)"),
         258: Equipment(258, "Steel gloves", 200, False, 'Hands', equip_reqs={'Defence': 20}, acc_rating_melee=5,
                        acc_rating_magic=3, acc_rating_ranged=5, melee_def=5, magic_def=3, ranged_def=5,
                        str_bonus_melee=5, examine="A pair of gloves made from steel. (Level 20)"),
         259: Equipment(259, "Mithril gloves", 400, False, 'Hands', equip_reqs={'Defence': 30}, acc_rating_melee=6,
                        acc_rating_magic=3, acc_rating_ranged=6, melee_def=6, magic_def=3, ranged_def=6,
                        str_bonus_melee=6, examine="A pair of gloves made from mithril. (Level 30)"),
         260: Equipment(260, "Adamant gloves", 800, False, 'Hands', equip_reqs={'Defence': 40}, acc_rating_melee=7,
                        acc_rating_magic=4, acc_rating_ranged=7, melee_def=7, magic_def=4, ranged_def=7,
                        str_bonus_melee=7, examine="A pair of gloves made from adamant. (Level 40)"),
         261: Equipment(261, "Rune gloves", 1600, False, 'Hands', equip_reqs={'Defence': 50}, acc_rating_melee=8,
                        acc_rating_magic=4, acc_rating_ranged=8, melee_def=8, magic_def=4, ranged_def=8,
                        str_bonus_melee=8, examine="A pair of gloves made from rune. (Level 50)"),
         262: Equipment(262, "Dragon gloves", 3200, False, 'Hands', equip_reqs={'Defence': 60}, acc_rating_melee=9,
                        acc_rating_magic=5, acc_rating_ranged=9, melee_def=9, magic_def=5, ranged_def=9,
                        str_bonus_melee=9, examine="A pair of gloves made from dragon metal. (Level 60)"),
         263: Equipment(263, "Bracelet of torment", 3500, False, 'Hands', acc_rating_magic=8, str_bonus_magic=8,
                        magic_def=8, equip_reqs={'Magic': 60},
                        examine="An old bracelet bursting with magical power. (Level 60)"),
         264: Equipment(264, "Karil's coif", 16000, False, 'Head', equip_reqs={'Ranged': 70, 'Defence': 70},
                        acc_rating_magic=-10, acc_rating_ranged=14, melee_def=12, magic_def=10, ranged_def=16,
                        examine="A piece of an ancient archer's equipment. (Level 70)"),
         265: Equipment(265, "Karil's skirt", 32000, False, 'Legs', equip_reqs={'Ranged': 70, 'Defence': 70},
                        acc_rating_magic=-10, acc_rating_ranged=20, melee_def=36, magic_def=35, ranged_def=36,
                        examine="A piece of an ancient archer's equipment. (Level 70)"),
         266: Equipment(266, "Karil's top", 48000, False, 'Body', equip_reqs={'Ranged': 70, 'Defence': 70},
                        acc_rating_magic=-15, acc_rating_ranged=35, melee_def=58, magic_def=65, ranged_def=60,
                        examine="A piece of an ancient archer's equipment. (Level 70)"),
         267: Equipment(267, "Dharok's helmet", 16000, False, 'Head', equip_reqs={'Defence': 70},
                        acc_rating_magic=-3, acc_rating_ranged=-1, melee_def=52, magic_def=-1, ranged_def=56,
                        examine="A piece of an ancient warrior's equipment. (Level 70)"),
         268: Equipment(268, "Dharok's legs", 32000, False, 'Legs', equip_reqs={'Defence': 70},
                        acc_rating_magic=-21, acc_rating_ranged=-11, melee_def=85, magic_def=-4, ranged_def=92,
                        examine="A piece of an ancient warrior's equipment. (Level 70)"),
         269: Equipment(269, "Dharok's platebody", 48000, False, 'Body', equip_reqs={'Defence': 70},
                        acc_rating_magic=-30, acc_rating_ranged=-10, melee_def=120, magic_def=-6, ranged_def=132,
                        examine="A piece of an ancient warrior's equipment. (Level 70)"),
         270: Equipment(270, "Ahrim's hood", 16000, False, 'Head', equip_reqs={'Magic': 70, 'Defence': 70},
                        acc_rating_magic=8, melee_def=15, magic_def=8,
                        examine="A piece of an ancient mage's equipment. (Level 70)"),
         271: Equipment(271, "Ahrim's skirt", 32000, False, 'Legs', equip_reqs={'Magic': 70, 'Defence': 70},
                        acc_rating_magic=26, melee_def=33, magic_def=26,
                        examine="A piece of an ancient mage's equipment. (Level 70)"),
         272: Equipment(272, "Ahrim's robe top", 48000, False, 'Body', equip_reqs={'Magic': 70, 'Defence': 70},
                        acc_rating_magic=36, melee_def=55, magic_def=36,
                        examine="A piece of an ancient mage's equipment. (Level 70)"),
         273: Item(273, "Banana", 5, False, examine="Monkeys love them."),
         274: Item(274, "Quest_item", 1, True, quest_item=0),
         275: Item(275, "Fake_quest_item", 2, True, quest_item=0),
         276: Item(276, "Giant egg", 5, True, quest_item=0, examine="How did that fit in there..."),
         277: Item(277, "Black bead", 25, True, quest_item=3, examine="One of the wizard's magical beads."),
         278: Item(278, "White bead", 25, True, quest_item=3, examine="One of the wizard's magical beads."),
         279: Item(279, "Red bead", 25, True, quest_item=3, examine="One of the wizard's magical beads."),
         280: Item(280, "Yellow bead", 25, True, quest_item=3, examine="One of the wizard's magical beads."),
         281: Item(281, "Ghostspeak amulet", 1, True, quest_item=2, examine="Allows a holy man to speak to the dead."),
         282: Item(282, "Skeleton's head", 1, True, quest_item=2, examine="Spooky."),
         283: Item(283, "Jail key", 1, True, quest_item=3, examine="Opens the Temple jail cell."),
         284: Item(284, "Un-focused rune stones", 1, True, quest_item=3,
                   examine="One of the wizards' worst kept secrets."),
         285: Item(285, "Juliet's letter", 1, True, quest_item=4, examine="A letter, sealed with a kiss."),
         286: Item(286, "Cadava berries", 2, True, quest_item=4, examine="A berry that seems inedible."),
         287: Item(287, "Cadava potion", 1, True, quest_item=4, examine="One sip will knock the strongest man out."),
         288: Item(288, "Rope", 20, False, examine="A long piece of rope.")
         }

#   Format of spell: Name, id, level_req, runes_req, damage, xp(for non-combat only), spell_type, area, quest/skill_reqs
Spellbook = {0: Spell('Air strike', 0, 1, [[66, 1], [70, 1]], 2),
             1: Spell('Water strike', 1, 5, [[66, 1], [67, 1], [70, 1]], 4),
             2: Spell('Earth strike', 2, 9, [[66, 1], [68, 1], [70, 1]], 6),
             3: Spell('Fire strike', 3, 13, [[66, 1], [69, 1], [70, 1]], 8),
             4: Spell('Air bolt', 4, 17, [[66, 5], [71, 1]], 9),
             5: Spell('Water bolt', 5, 23, [[66, 3], [67, 3], [71, 1]], 10),
             6: Spell('Earth bolt', 6, 29, [[66, 3], [68, 3], [71, 1]], 11),
             7: Spell('Fire bolt', 7, 35, [[66, 3], [69, 3], [71, 1]], 12),
             8: Spell('Air blast', 8, 41, [[66, 9], [72, 1]], 13),
             9: Spell('Water blast', 9, 47, [[66, 7], [67, 7], [72, 1]], 14),
             10: Spell('Earth blast', 10, 53, [[66, 7], [68, 7], [72, 1]], 15),
             11: Spell('Fire blast', 11, 59, [[66, 7], [69, 7], [72, 1]], 16),
             12: Spell('Air wave', 12, 65, [[66, 13], [73, 1]], 18),
             13: Spell('Water wave', 13, 71, [[66, 11], [67, 11], [73, 1]], 20),
             14: Spell('Earth wave', 14, 77, [[66, 11], [68, 11], [73, 1]], 22),
             15: Spell('Fire wave', 15, 83, [[66, 11], [69, 11], [73, 1]], 24),
             16: Spell('Teleport to Varrock', 16, 25, [[66, 3], [69, 1], [74, 1]], xp=50, spell_type='Teleport',
                       area=25),
             17: Spell('Teleport to Lum', 17, 35, [[66, 3], [68, 1], [74, 1]], xp=75,
                       spell_type='Teleport', area=2),
             18: Spell('Teleport to Ardy', 18, 50, [[74, 2], [67, 2]], xp=110,
                       spell_type='Teleport', area=93, skill_reqs={'Combat': 40}),
             19: Spell('Teleport to Canifis', 19, 66, [[67, 2], [68, 2], [74, 2]], xp=140,
                       spell_type='Teleport', area=31, quest_reqs=[3]),
             }
