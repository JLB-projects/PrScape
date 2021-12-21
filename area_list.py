"""Contains all the areas that are used during the game."""

from skill_obj_list import *
from enemy_list_ import *
from npc_list_ import *

# Transport = Transport(text1, text2, area_id, item_reqs={}, skill_reqs={}, quest_reqs=[])

# Areas defined here
Test_area = Area(-1, "Lum2", [Rat, Chicken], [Duke, Cook, Shopkeeper],
                 [Tree, Oak_tree, Copper_rock, Shrimp], True, False, True, True, 0,
                 transport=Transport("Boat to Lum", "(Requires 30gp)", 2, {0: 30},
                                     skill_reqs={'Attack': 69, 'Crafting': 1},
                                     quest_reqs=[0]), neighbours=[None, None, None, 2])
# Tutorial areas
tut_area_0 = Area(0, 'Tutorial island: West', [Rat], [Woman], [Tree, Shrimp, Copper_rock, Tin_rock], True, False,
                  True, False, 0, [None, 1, None, None], background='#228B22')
tut_area_1 = Area(1, 'Tutorial island: East', [Goblin], [Man_npc], [Tree, Oak_tree, Herring], True, True,
                  False, False, 0, [None, None, None, 0], background='#3b3118')
# Mainland areas
Lum = Area(2, "Lum", [Goblin, Rat], [Duke, Cook, Shopkeeper],
           [Tree, Oak_tree, Willow_tree, Yew_tree], True, False, True, True, 0, neighbours=[21, 3, 4, 50],
           background='#228B22')
Desert_gate = Area(3, "Desert Gate", [Guard], [], [Tree], False, False, False, False, 0,
                   neighbours=[22, None, 5, 2], background='#f0c44f')
East_swamp = Area(4, "East Swamp", [Frog, Big_frog, Giant_rat], [Father_eric], [Shrimp, Copper_rock, Tin_rock, Herring],
                  False, False, False, False, 0, neighbours=[2, None, None, 51], background='#174c1e')
Al_kharid = Area(5, "Al Kharid", [Al_Kharid_warrior, Man, Scorpion], [Ali, Louie, Prince], [Shrimp, Herring],
                 True, False, True, False, 0, neighbours=[3, None, 6, None], background='#f0c44f')
Desert_pass = Area(6, "Desert Pass", [Guard], [Desert_supplier], [], False, False, False, False, 0,
                   neighbours=[5, 8, None, 7], skill_reqs={'Combat': 40}, background='#f0c44f')
Kalphite_corner = Area(7, "Kalphite Corner", [Kalphite_larva], [], [], False, False, False, False, 0,
                       neighbours=[None, 6, 10, None],
                       transport=Transport("Enter Kalphite Lair", "(1 Rope)", 143, item_reqs={288: 1}),
                       background='#f0c44f')
River_crossing = Area(8, "River Crossing", [], [], [], False, False, False, False, 0,
                      neighbours=[None, 9, None, 6], background='#f0c44f')
Desert_ruins = Area(9, "Desert Ruins", [Sand_golem], [], [Teak_tree], False, False, False, False, 0,
                    neighbours=[None, None, 12, 8], background='#f0c44f')
Barren_desert = Area(10, "Barren Desert", [Desert_wolf], [], [], False, False, False, False, 0,
                     neighbours=[7, 11, 13, None], background='#f0c44f')
Mining_camp = Area(11, "Mining Camp", [Slaver, Mining_guard], [Mining_slave], [Iron_rock, Coal_rock],
                   False, False, False, False, 0, neighbours=[None, None, None, 10], background='#f0c44f')
Oasis = Area(12, "Oasis", [Desert_lizard, Desert_snake], [], [Trout], False, False, False, False, 0,
             neighbours=[9, None, 20, None], background='#f0c44f')
Bandit_camp = Area(13, "Bandit Camp", [Bandit, Bandit_leader], [Bandit_shopkeeper], [], False, False, False, False, 0,
                   neighbours=[10, None, 14, None], background='#f0c44f')
Pyramids = Area(14, "Pyramids", [Mummy], [], [], False, False, False, False, 0,
                neighbours=[13, 15, None, None], background='#f0c44f')
South_desert = Area(15, "South Desert", [Crocodile, Jackal], [Wanderer], [Mithril_rock], False, False, False, False, 0,
                    neighbours=[None, 17, 16, 14], background='#f0c44f')
Sophanem = Area(16, "Sophanem", [Locust], [High_priest, Carpenter], [Tree], True, False, False, True, 0,
                neighbours=[15, None, None, None], background='#f0c44f')
Vultures_playground = Area(17, "Vulture's Playground", [Vulture, Jackal, Giant_vulture], [], [Shrimp],
                           False, False, False, False, 0, neighbours=[19, 18, None, 15], background='#f0c44f')
Desert_outpost = Area(18, "Desert Outpost", [], [Desert_trader], [Tree], False, True, False, True, 0,
                      neighbours=[20, None, None, 17], background='#f0c44f')
Desert_lake = Area(19, "Desert Lake", [Desert_snake], [Elderly_fisherman], [Herring], False, False, False, False, 0,
                   neighbours=[None, 20, 17, None], background='#f0c44f')
East_desert = Area(20, "East Desert", [Jackal, Desert_wolf], [], [], False, False, False, False, 0,
                   neighbours=[12, None, 18, 19], background='#f0c44f')
Farmland = Area(21, "Farmland", [Chicken, Cow, Farmer], [Farmhand], [Tree, Oak_tree, Willow_tree],
                False, False, False, False, 0, neighbours=[23, None, 2, 49], background='#228B22')
Desert_mine = Area(22, "Desert Mine", [Scorpion], [], [Iron_rock, Coal_rock, Mithril_rock, Adamant_rock],
                   False, False, False, False, 0, neighbours=[None, None, 3, None], background='#3b3118')
Wizard_circle = Area(23, "Wizard Circle", [Dark_wizard], [], [Tree, Oak_tree, Yew_tree], False, False, False, False, 0,
                     neighbours=[25, 24, 21, None], background='#228B22')
Varrock_mine = Area(24, "Varrock Mine", [Giant_rat, Bear], [], [Copper_rock, Tin_rock, Iron_rock],
                    False, False, False, False, 0, neighbours=[26, None, None, 23], background='#3b3118')
East_varrock = Area(25, "East Varrock", [Man, Rat], [Horvik, Father_lawrence, Dr_harlow], [Tree, Oak_tree],
                    True, True, False, True, 0, neighbours=[27, 26, 23, 48], background='#949494')
Dirt_road = Area(26, "Dirt Road", [City_guard], [Romeo], [Oak_tree], False, False, False, False, 0,
                 neighbours=[28, None, 24, 25], background='#3b3118')
Palace = Area(27, "Palace", [City_guard], [King_roald, Sir_prism], [Tree, Yew_tree], False, False, False, True, 0,
              neighbours=[None, None, 25, None], background='#949494')
Lumber_yard = Area(28, "Lumber Yard", [Man], [], [Tree, Oak_tree, Yew_tree], False, False, False, False, 0,
                   neighbours=[None, 29, 26, None], background='#228B22')
Strange_hut = Area(29, "Strange Hut", [Bat], [Odd_old_man], [Coal_rock], False, False, False, False, 0,
                   neighbours=[None, 30, None, 28], background='#262626')
Temple = Area(30, "Temple", [Evil_monk], [Drazel], [Tree], False, False, False, False, 0,
              neighbours=[None, 31, None, 29], background='#949494')
Canifis = Area(31, "Canifis", [Werewolf], [Strange_shopkeeper], [], True, False, False, False, 0,
               neighbours=[32, 45, 33, 30], quest_reqs=[3], background='#262626')
Old_tower = Area(32, "Old Tower", [Banshee, Spectre, Abyssal_demon], [], [], False, False, False, False, 0,
                 neighbours=[None, None, 31, None], skill_reqs={'Combat': 50}, background='#262626')
Myre_swamp_north = Area(33, "Myre Swamp North", [Swamp_snail], [Veliaf], [], False, False, False, False, 0,
                        neighbours=[31, None, 34, None], background='#174c1e')
Myre_swamp_south = Area(34, "Myre Swamp South", [Swamp_snail], [Boatmaster], [Tree], False, False, False, False, 0,
                        neighbours=[33, None, None, None],
                        transport=Transport("Boat to Mortton", "(30 gold)", 35, item_reqs={0: 30}),
                        background='#174c1e')
Mortton = Area(35, "Mortton", [Afflicted_villager, Shade], [Boatmaster, Villager], [Tree], True, False, True, True, 0,
               neighbours=[None, 42, 36, None],
               transport=Transport("Boat to Swamp", "(30 gold)", 34, item_reqs={0: 30}), background='#262626')
Abandoned_town = Area(36, "Abandoned Town", [Young_vampire, Giant_rat], [], [], False, False, False, False, 0,
                      neighbours=[35, 38, None, 37], background='#262626')
Old_mine = Area(37, "Old Mine", [Animated_pickaxe, Zombie], [], [Mithril_rock, Adamant_rock, Coal_rock],
                False, False, False, False, 0, neighbours=[None, 36, None, None], background='#262626')
Old_pier = Area(38, "Old Pier", [Young_vampire], [], [Lobster, Swordfish, Shark], False, False, False, False, 0,
                neighbours=[None, 39, None, 36], background='#262626')
Meiyer_south = Area(39, "Meiyer South", [Vampire_guard, Vampire], [Old_man_ray, Sven], [], False, False, False, False,
                    0, neighbours=[41, 40, None, 38], skill_reqs={'Combat': 75}, background='#3B1807')
Vampire_graveyard = Area(40, "Vampire Graveyard", [Young_vampire, Vampire, Elder_vampire], [], [Yew_tree],
                         False, False, False, False, 0, neighbours=[None, None, None, 39], background='#3B1807')
Meiyer_north = Area(41, "Meiyer North", [Vampire_guard, Vampire], [Veliaf_2], [], False, False, False, False, 0,
                    neighbours=[44, None, 39, None], background='#3B1807')
Barrows = Area(42, "Barrows", [Ancient_warrior, Ancient_archer, Ancient_mage], [Strange_old_man], [Tree],
               False, False, False, False, 0, neighbours=[None, None, None, 35], background='#3b3118')
Castle_drakan = Area(43, "Castle Drakan", [Vampire_lord, Castle_guard], [Prisoner], [], False, False, False, False, 0,
                     neighbours=[None, 44, None, None], background='#3B1807')
Darkmeyer = Area(44, "Darkmeyer", [Vampire, Vampire_wizard], [Grigor_rasputin, Survivor], [Tree],
                 True, True, True, True, 0, neighbours=[None, None, 41, 43], background='#3B1807')
Haunted_woods = Area(45, "Haunted Woods", [Leech, Vampire], [], [Tree, Maple_tree], False, False, False, False, 0,
                     neighbours=[None, 46, None, 31], background='#174c1e')
Swampland = Area(46, "Swampland", [Giant_bat, Leech], [], [Tree], False, False, False, False, 0,
                 neighbours=[None, 47, None, 45], background='#174c1e')
Ghost_port = Area(47, "Ghost Port", [Tortured_soul], [Ghost_captain, Lost_soul, Ghost_shopkeeper], [],
                  True, False, True, True, 0, neighbours=[None, None, None, 46],
                  transport=Transport("Boat to Shipping Hub", "", 147), background='#262626')
West_varrock = Area(48, "West Varrock", [City_guard, Man], [Juliet, Apothecary, Swordsmith], [Tree, Oak_tree],
                    True, True, False, False, 0, neighbours=[None, 25, None, 56], background='#949494')
Flour_mill = Area(49, "Flour Mill", [Chicken, Mill_operator], [], [Tree], False, False, False, False, 0,
                  neighbours=[None, 21, 50, 54], background='#228B22')
West_lum = Area(50, "West Lum", [Giant_rat, Giant_spider], [], [Tree, Oak_tree, Willow_tree, Yew_tree],
                False, False, False, False, 0, neighbours=[49, 2, 51, 53], background='#228B22')
West_swamp = Area(51, "West Swamp", [Big_frog, Giant_rat], [Father_urney], [Coal_rock, Mithril_rock, Tree],
                  False, False, False, False, 0, neighbours=[50, 4, None, None], background='#174c1e')
Wizard_tower = Area(52, "Wizard Tower", [Wizard, Master_wizard, Lesser_demon, Skeleton], [Wizard_treyborn], [Oak_tree],
                    False, False, False, False, 0, neighbours=[53, None, None, None], background='#949494')
South_draynor = Area(53, "South Draynor", [Black_knight, Imp], [Wise_old_man], [Willow_tree, Shrimp, Herring],
                     True, False, False, False, 0, neighbours=[54, 50, 52, None], background='#228B22')
North_draynor = Area(54, "North Draynor", [Goblin, Man], [Ned], [Tree, Oak_tree], False, True, False, False, 0,
                     neighbours=[55, 49, 53, 61], background='#228B22')
Draynor_manor = Area(55, "Draynor Manor", [Ghost, Rat, Zombie], [Professor], [Tree], False, False, False, False, 0,
                     neighbours=[None, None, 54, None], background='#262626')
Barbarian_village = Area(56, "Barbarian Village", [Barbarian, Gunthor_the_brave], [Peksa],
                         [Copper_rock, Tin_rock, Trout, Salmon], False, True, False, True, 0,
                         neighbours=[57, 48, None, 59], background='#3b3118')
Edgeville = Area(57, "Edgeville", [Man, Giant_spider], [Shop_assistant, Oziach], [Willow_tree, Yew_tree],
                 True, False, True, True, 0, neighbours=[None, None, 56, 58], background='#949494')
Monastery = Area(58, "Monastery", [Black_knight, Monk], [], [Tree], False, False, False, False, 0,
                 neighbours=[None, 57, 59, None], background='#949494')
Dwarven_camp = Area(59, "Dwarven Camp", [Dwarf], [], [], False, False, False, False, 0,
                    neighbours=[58, 56, None, 67], transport=Transport("Enter Dwarven Mine", "", 141),
                    background='#3b3118')
Fally_east = Area(60, "Fally East", [City_guard, Man], [Shieldsmith], [], True, False, False, True, 0,
                  neighbours=[None, None, None, 66], background='#949494')
Family_farm = Area(61, "Family Farm", [Chicken, Cow], [], [Yew_tree], False, False, False, False, 0,
                   neighbours=[None, 54, 62, 65], background='#228B22')
Port_sarim = Area(62, "Port Sarim", [Seagull, Man], [Betty, Captain_toby], [Willow_tree], False, False, False, False, 0,
                  neighbours=[61, None, 63, 64], transport=Transport("Boat to Shipping Hub", "", 147),
                  background='#f0c44f')
Old_dock = Area(63, "Old Dock", [Seagull, Man], [Ned_2], [Willow_tree, Lobster], False, False, False, False, 0,
                neighbours=[62, None, None, None],
                transport=Transport("Boat to Crandor", "", 126), skill_reqs={'Combat': 50}, background='#f0c44f')
#                                                ^^   Change to require Drag slayer later
Rimmington = Area(64, "Rimmington", [Goblin, Giant_rat], [Witch], [Tin_rock, Copper_rock, Tree], False, False, False,
                  True, 0, neighbours=[65, 62, None, None], background='#3b3118')
Road = Area(65, "Road", [Highwayman], [], [Tree, Oak_tree, Yew_tree], False, False, False, False, 0,
            neighbours=[66, 61, 64, None], background='#228B22')
Fally_west = Area(66, "Fally West", [White_knight], [Shopkeeper_fally, Sir_amik], [], True, False, True, False, 0,
                  neighbours=[67, 60, 65, None], background='#949494')
Crossroads = Area(67, "Crossroads", [Highwayman, Man], [], [Tree, Oak_tree], False, False, False, False, 0,
                  neighbours=[68, 59, 66, 69], background='#228B22')
Goblin_village = Area(68, "Goblin Village", [Goblin, Goblin_chief], [Goblin_general], [Iron_rock, Tree],
                      False, False, False, False, 0, neighbours=[None, None, 67, None], background='#3b3118')
Taverley = Area(69, "Taverley", [Druid], [Sanfew], [Willow_tree], False, False, False, True, 0,
                neighbours=[70, 67, None, None], background='#949494')
Druid_circle = Area(70, "Druid Circle", [], [], [], False, False, False, False, 0,
                    neighbours=[71, None, 69, 76], background='#228B22')
Burthorpe = Area(71, "Burthorpe", [Soldier], [Duncan, Commander], [], True, True, False, True, 0,
                 neighbours=[None, None, 70, 77], background='#949494')
Mountain_pass = Area(72, "Mountain Pass", [Mountain_goat, Troll], [], [], False, False, False, False, 0,
                     neighbours=[73, None, None, 78], background='#545454')
Mountain_crossroads = Area(73, "Mountain Crossroads", [Thrower_troll, Troll], [], [], False, False, False, False, 0,
                           neighbours=[74, None, 72, 79], background='#545454')
Icy_path = Area(74, "Icy Path", [Frost_wolf, Ice_troll], [], [], False, False, False, False, 0,
                neighbours=[75, None, 73, None], background='#d1cdcd')
Ancient_ruins = Area(75, "Ancient Ruins", [Frost_wolf, Ice_troll], [Wounded_knight], [], False, False, False, False, 0,
                     neighbours=[None, None, 74, None],
                     transport=Transport("Move boulder to enter", "God Dungeon", 121), skill_reqs={'Strength': 60},
                     background='#d1cdcd')
White_mountain = Area(76, "White Mountain", [Wolf, Big_wolf, Ice_warrior], [], [Iron_rock, Tree],
                      False, False, False, False, 0, neighbours=[None, 70, None, 87], skill_reqs={'Combat': 40},
                      background='#d1cdcd')
Warrior_guild = Area(77, "Warrior Guild", [Young_cyclops, Cyclops, Large_cyclops, King_cyclops],
                     [Elite_warrior, Cyclops_herder], [], True, False, False, False, 0,
                     neighbours=[78, 71, None, None], skill_reqs={'Attack': 65, 'Strength': 65}, background='#949494')
Death_plateau = Area(78, "Death Plateau", [Troll], [Wounded_soldier], [], False, False, False, False, 0,
                     neighbours=[None, 72, 77, None], skill_reqs={'Combat': 60}, background='#545454')
Troll_stronghold = Area(79, "Troll Stronghold", [Troll, Troll_guard, Thrower_troll], [], [],
                        False, False, False, False, 0, neighbours=[None, 73, None, None],
                        transport=Transport("Enter Troll Tunnels", "", 139), background='#545454')
Mountain_camp = Area(80, "Mountain Camp", [Mountain_camper], [Chieftain], [Mithril_rock], False, False, False, False, 0,
                     neighbours=[None, None, None, 81], background='#545454')
Mountain_hills = Area(81, "Mountain Hills", [Mountain_goat, Bear], [], [Tree, Oak_tree, Maple_tree],
                      False, False, False, False, 0, neighbours=[None, 80, 82, None], background='#545454')
Windy_hills = Area(82, "Windy Hills", [Unicorn], [], [Tree, Oak_tree, Maple_tree], False, False, False, False, 0,
                   neighbours=[81, None, None, 83], background='#228B22')
Forest_trail = Area(83, "Forest Trail", [Wolf], [Worker], [Tree, Maple_tree], False, False, False, False, 0,
                    neighbours=[84, 82, 85, None], background='#228B22')
Relleka = Area(84, "Relleka", [Chicken, Relleka_warrior], [Brundt, Huntsman, Merchant], [], False, False, True, True, 0,
               neighbours=[None, None, 83, None], background='#3b3118')
Rocky_road = Area(85, "Rocky Road", [], [], [Maple_tree], False, False, False, False, 0,
                  neighbours=[83, None, 86, None], background='#545454')
Grubby_woods = Area(86, "Grubby Woods", [Guard_dog], [], [Tree, Oak_tree, Maple_tree], False, False, False, False, 0,
                    neighbours=[85, 88, 91, None], background='#228B22')
Knights_castle = Area(87, "Knight's Castle", [Knight], [King_arthur], [Tree, Oak_tree], False, False, False, False, 0,
                      neighbours=[None, 76, 90, 88], background='#949494')
Seers_village = Area(88, "Seer's Village", [Man], [Seer], [Maple_tree], True, True, False, True, 0,
                     neighbours=[None, 87, 89, 86], background='#949494')
Sorcerers_tower = Area(89, "Sorcerer's Tower", [Nightmare_conjurer, Dream_eater], [], [Magic_tree],
                       False, False, False, False, 0, neighbours=[88, 90, None, 91], skill_reqs={'Magic': 60},
                       background='#3B1807')
Catherby = Area(90, "Catherby", [Man], [Harry], [Lobster, Swordfish, Shark], True, False, False, True, 0,
                neighbours=[87, None, None, 89], background='#228B22')
Ranging_guild = Area(91, "Ranging Guild", [], [Ranging_guild_guard], [], False, False, False, False, 0,
                     neighbours=[86, 89, 92, None], background='#228B22')
Manor_farm = Area(92, "Manor Farm", [Cow, Farmer], [Master_farmer], [Tree, Oak_tree], False, False, False, False, 0,
                  neighbours=[91, None, 93, 95], background='#228B22')
East_ardy = Area(93, "East Ardy", [City_guard, Paladin], [Hideworker], [], True, False, False, True, 0,
                 neighbours=[92, None, None, 94], background='#949494')
Ardy_castle = Area(94, "Ardy Castle", [], [King_lathas], [], True, False, True, False, 0,
                   neighbours=[None, 93, 97, 104], background='#949494')
Giants_camp = Area(95, "Giants Camp", [Moss_giant, Hill_giant, Fire_giant], [], [Tree, Trout, Salmon],
                   False, False, False, False, 0, neighbours=[96, 92, None, 105], background='#228B22')
Fishing_guild = Area(96, "Fishing Guild", [], [Master_fisherman], [Lobster, Swordfish, Shark, Manta_ray],
                     False, False, False, False, 0, neighbours=[None, None, 95, None], skill_reqs={'Fishing': 60},
                     background='#228B22')
Monks_house = Area(97, "Monk's House", [Monk], [Old_monk], [Tree, Oak_tree], False, False, False, False, 0,
                   neighbours=[94, None, 98, 103], background='#228B22')
Fight_arena = Area(98, "Fight Arena", [Prison_guard, Bouncer, General_khazard], [Arena_prisoner], [],
                   False, False, False, False, 0, neighbours=[97, 99, 100, None], background='#3b3118')
Port_khazard = Area(99, "Port Khazard", [], [Dock_worker], [Manta_ray, Swordfish], True, False, False, True, 0,
                    neighbours=[None, None, None, 98], transport=Transport("Boat to Shipping Hub", "", 147),
                    background='#f0c44f')
Yanille_east = Area(100, "Yanille East", [Man], [Wizard_guild_guard], [], True, False, False, False, 0,
                    neighbours=[98, None, None, 101],
                    transport=Transport("Portal to", "Wizard's Guild", 125), skill_reqs={'Magic': 50},
                    background='#949494')
Yanille_west = Area(101, "Yanille West", [Man, Wandering_ogre], [Citizen], [Tree], False, False, False, False, 0,
                    neighbours=[None, 100, 102, None], background='#949494')
Ogre_city = Area(102, "Ogre City", [Ogre, Ogre_mage, Ogre_chief], [Friendly_ogre], [Runite_rock],
                 False, False, False, False, 0, neighbours=[101, None, None, None], skill_reqs={'Combat': 60},
                 background='#3b3118')
Gnome_battlefield = Area(103, "Gnome Battlefield", [Gnome_warrior, Khazard_trooper, Mounted_gnome], [],
                         [Tree, Oak_tree], False, False, False, False, 0, neighbours=[None, 97, None, None],
                         background='#228B22')
West_ardy = Area(104, "West Ardy", [Man, Zombie], [Underground_guard], [], False, True, False, False, 0,
                 neighbours=[None, 94, None, 109], background='#949494')
Kings_road = Area(105, "King's Road", [], [], [Tree, Oak_tree], False, False, False, False, 0,
                  neighbours=[152, 95, None, 106], background='#228B22')
Orchard = Area(106, "Orchard", [Gnome_guard, Hobgoblin], [Lumberjack], [Tree, Oak_tree, Yew_tree],
               False, False, False, False, 0, neighbours=[107, 105, None, None], background='#32CD32')
Gnome_stronghold_south = Area(107, "Gnome Stronghold South", [Gnome_guard, Gnome, Terrorbird], [],
                              [Yew_tree, Magic_tree], False, False, False, False, 0,
                              neighbours=[108, None, 106, None], background='#228B22')
Gnome_stronghold_north = Area(108, "Gnome Stronghold North", [Gnome, Gnome_guard, Terrorbird], [Gnome_king, Gulluck],
                              [Yew_tree, Magic_tree], True, False, False, True, 0,
                              neighbours=[None, None, 107, None], background='#949494')
Underground_pass = Area(109, "Underground Pass", [Dwarf, Lesser_demon, Disciple], [Koftik], [],
                        False, False, False, False, 0, neighbours=[None, 104, None, 110], skill_reqs={'Combat': 80},
                        background='#3b3118')
West_pass_entrance = Area(110, "West Pass Entrance", [Lost_elf, Wolf], [], [Coal_rock, Yew_tree, Adamant_rock],
                          False, False, False, False, 0, neighbours=[None, 109, 111, 112], background='#228B22')
Elven_town = Area(111, "Elven Town", [Elf_warrior, Elven_mage], [Arianwyn, Elven_supplier], [],
                  True, False, False, True, 0, neighbours=[110, None, None, 118], background='#949494')
Dense_forest = Area(112, "Dense Forest", [], [], [Trout, Salmon, Oak_tree], False, False, False, False, 0,
                    neighbours=[113, 110, 118, 115], background='#32CD32')
Elf_city_south = Area(113, "Elf City South", [], [Elf_prince], [], True, False, True, False, 0,
                      neighbours=[114, None, 112, None], background='#949494')
Elf_city_north = Area(114, "Elf City North", [], [Elf_queen], [Runite_rock, Yew_tree], False, True, False, True, 0,
                      neighbours=[None, None, 113, None], background='#949494')
High_elven_woods = Area(115, "High Elven Woods", [Elf_warrior, Grizzly_bear, Elven_archer], [],
                        [Oak_tree, Magic_tree, Salmon], False, False, False, False, 0,
                        neighbours=[None, 112, 116, None], background='#32CD32')
Port_tyras = Area(116, "Port Tyras", [], [Elven_dock_worker], [], False, False, True, False, 0,
                  neighbours=[115, 118, 117, None], transport=Transport("Boat to Shipping Hub", "", 147),
                  background='#f0c44f')
Shrine = Area(117, "Shrine", [Snake, Giant_snake], [High_priestess], [Lobster, Tree], False, False, False, False, 0,
              neighbours=[116, None, None, None],
              transport=Transport("Boat to", "Zulrah's Island", 119), background='#262626')
Hunting_grounds = Area(118, "Hunting Grounds", [Wolf, Grizzly_bear, Elven_hunter], [Wounded_elf], [Yew_tree],
                       False, False, False, False, 0, neighbours=[112, 111, None, 116], background='#32CD32')

# Dungeons / islands:

Zulrahs_island = Area(119, "Zulrah's Island", [Zulrah], [], [], False, False, False, False, 0,
                      neighbours=[None, None, None, None], skill_reqs={'Combat': 80},
                      transport=Transport("Boat to Shrine", "", 117), background='#174c1e')
God_dungeon_north = Area(120, "God Dungeon - North", [Kril_tsutaroth], [], [], False, False, False, False, 0,
                         neighbours=[None, None, 121, None], skill_reqs={'Hitpoints': 70}, background='#3B1807')
God_dungeon_entrance = Area(121, "God Dungeon - Entrance", [Spiritual_mage, Spiritual_ranger, Spiritual_warrior],
                            [], [Runite_rock], False, False, False, False, 0, neighbours=[120, 123, 124, 122],
                            transport=Transport("Climb to surface", "", 75), background='#d1cdcd')
God_dungeon_west = Area(122, "God Dungeon - West", [General_graardor], [], [], False, False, False, False, 0,
                        neighbours=[None, 121, None, None], skill_reqs={'Strength': 70}, background='#3B1807')
God_dungeon_east = Area(123, "God Dungeon - East", [Commander_zilyana], [], [], False, False, False, False, 0,
                        neighbours=[None, None, None, 121], skill_reqs={'Magic': 70}, background='#3B1807')
God_dungeon_south = Area(124, "God Dungeon - South", [Kree_arra], [], [], False, False, False, False, 0,
                         neighbours=[121, None, None, None], skill_reqs={'Ranged': 70}, background='#3B1807')
Wizards_guild = Area(125, "Wizard's Guild", [], [Elder_wizard, Wizard_shop], [], False, False, False, False, 0,
                     neighbours=[None, None, None, None],
                     transport=Transport("Portal to Yanille", "", 100), background='#949494')
Crandor_beach = Area(126, "Crandor Beach", [Moss_giant, Sand_crab], [],
                     [Oak_tree, Yew_tree, Mithril_rock, Adamant_rock], False, False, False, False, 0,
                     neighbours=[None, None, 127, None],
                     transport=Transport("Boat to Old Docks", "", 63), background='#f0c44f')
Dragons_den = Area(127, "Dragon's Den", [Elvarg, Blue_dragon, Red_dragon, Black_dragon], [], [],
                   False, False, False, False, 0, neighbours=[126, None, None, None], background='#3b3118')
Brimhaven_docks = Area(128, "Brimhaven Docks", [], [Dock_master], [], False, False, False, False, 0,
                       neighbours=[None, None, 129, None],
                       transport=Transport("Boat to Shipping Hub", "", 147), background='#f0c44f')
Brimhaven_town = Area(129, "Brimhaven Town", [Pirate], [Pirate_npc, Exotic_fisherman], [], True, True, False, True, 0,
                      neighbours=[128, 130, 132, None], background='#3b3118')
Volcano = Area(130, "Volcano", [Volcanic_creature, Jad, Zuk], [], [Iron_rock, Coal_rock, Tree],
               False, False, False, False, 0, neighbours=[None, 131, None, 129], background='#3b3118')
Banana_plantation = Area(131, "Banana Plantation", [Monkey], [], [Tree], False, False, False, False, 0,
                         neighbours=[None, None, None, 130], background='#228B22')
Beach_storefront = Area(132, "Beach Storefront", [Sand_crab], [Jimmy], [], False, True, False, False, 0,
                        neighbours=[129, None, 133, None], background='#f0c44f')
Taibo_village = Area(133, "Taibo Village", [Tribesman, Jungle_spider], [Tribe_leader], [Teak_tree, Coal_rock],
                     False, False, False, False, 0, neighbours=[132, 134, None, None], background='#3b3118')
Central_jungle = Area(134, "Central Jungle", [Tribesman, Jungle_spider], [], [Teak_tree, Mahogany_tree],
                      False, False, False, False, 0, neighbours=[None, None, 135, 133], background='#32CD32')
River_village = Area(135, "River Village", [], [Forester, River_fisher], [Trout, Salmon], True, False, True, True, 0,
                     neighbours=[134, None, 136, None], background='#f0c44f')
Southern_jungle = Area(136, "Southern Jungle", [Jungle_spider, Jungle_savage], [], [Teak_tree, Mahogany_tree],
                       False, False, False, False, 0, neighbours=[135, 138, None, 137],
                       skill_reqs={'Combat': 70, 'Woodcutting': 60}, background='#32CD32')
Western_jungle = Area(137, "Western Jungle", [Jungle_wolf, Jungle_bird], [], [Teak_tree, Mahogany_tree],
                      False, False, False, False, 0, neighbours=[None, 136, None, None], background='#32CD32')
Eastern_jungle = Area(138, "Eastern Jungle", [Bush_snake, Jungle_fisherman], [], [Teak_tree, Mahogany_tree],
                      False, False, False, False, 0, neighbours=[None, None, None, 136], background='#32CD32')
Troll_tunnels = Area(139, "Troll Tunnels", [Troll, Thrower_troll], [], [], False, False, False, False, 0,
                     neighbours=[140, None, None, None],
                     transport=Transport("Climb to surface", "", 79), background='#3b3118')
Troll_base_camp = Area(140, "Troll Base Camp", [Troll_general], [], [], False, False, False, False, 0,
                       neighbours=[None, None, 139, None], background='#3b3118')
Dwarven_mine_entrance = Area(141, "Dwarven Mine Entrance", [Dwarf], [Dwarf_trader], [Copper_rock, Tin_rock, Coal_rock],
                             False, False, False, False, 0, neighbours=[None, None, 142, None],
                             skill_reqs={'Mining': 30},
                             transport=Transport("Climb to surface", "", 59), background='#3b3118')
Dwarven_mine_south = Area(142, "Dwarven Mine South", [Dwarf], [Dwarven_overseer], [Iron_rock, Mithril_rock],
                          False, False, False, False, 0, neighbours=[141, None, None, None], background='#3b3118')
Kalphite_lair_entrance = Area(143, "Kalphite Lair Entrance", [Kalphite_worker], [], [], False, False, False, False, 0,
                              neighbours=[None, None, None, 144],
                              transport=Transport("Climb rope to surface", "", 7), background='#3b3118')
Kalphite_lair_tunnels = Area(144, "Kalphite Lair Tunnels", [Kalphite_worker, Kalphite_soldier], [], [],
                             False, False, False, False, 0, neighbours=[None, 143, 145, None], background='#3b3118')
Kalphite_nest = Area(145, "Kalphite Nest", [Kalphite_guardian], [], [], False, False, False, False, 0,
                     neighbours=[144, None, None, 146], background='#3b3118')
Queens_chamber = Area(146, "Queen's Chamber", [Kalphite_queen], [], [], False, False, False, False, 0,
                      neighbours=[None, 145, None, None], background='#3b3118')
# Boats
Shipping_hub = Area(147, "Shipping Hub", [], [Shipmaster], [], False, False, False, False, 0,
                    neighbours=[148, 149, 150, 151],
                    transport=Transport("Boat to Brimhaven", "(100 gold)", 128), background='#949494')
North_docks = Area(148, "North Docks", [], [], [], False, False, False, False, 0,
                   neighbours=[None, None, 147, None],
                   transport=Transport("Boat to Port Sarim", "(FREE)", 62), background='#f0c44f')
East_docks = Area(149, "East Docks", [], [], [], False, False, False, False, 0,
                  neighbours=[None, None, None, 147],
                  transport=Transport("Boat to Ghost Port", "(200 gold)", 47), quest_reqs=[3], background='#f0c44f')
South_docks = Area(150, "South Docks", [], [], [], False, False, False, False, 0,
                   neighbours=[147, None, None, None],
                   transport=Transport("Boat to Port Khazard", "(200 gold)", 99), skill_reqs={'Combat': 40},
                   background='#f0c44f')
West_docks = Area(151, "West Docks", [], [], [], False, False, False, False, 0,
                  neighbours=[None, 147, None, None],
                  transport=Transport("Boat to Port Tyras", "(500 gold)", 116), skill_reqs={'Combat': 80},
                  background='#f0c44f')

Kings_training_grounds = Area(152, "King's Training Grounds", [Caged_ogre], [Kings_guard], [],
                              False, False, False, False, 0, neighbours=[None, None, 105, None],
                              skill_reqs={'Combat': 80}, background='#3b3118')

Areas = {-1: Test_area,
         0: tut_area_0,
         1: tut_area_1,
         2: Lum,
         3: Desert_gate,
         4: East_swamp,
         5: Al_kharid,
         6: Desert_pass,
         7: Kalphite_corner,
         8: River_crossing,
         9: Desert_ruins,
         10: Barren_desert,
         11: Mining_camp,
         12: Oasis,
         13: Bandit_camp,
         14: Pyramids,
         15: South_desert,
         16: Sophanem,
         17: Vultures_playground,
         18: Desert_outpost,
         19: Desert_lake,
         20: East_desert,
         21: Farmland,
         22: Desert_mine,
         23: Wizard_circle,
         24: Varrock_mine,
         25: East_varrock,
         26: Dirt_road,
         27: Palace,
         28: Lumber_yard,
         29: Strange_hut,
         30: Temple,
         31: Canifis,
         32: Old_tower,
         33: Myre_swamp_north,
         34: Myre_swamp_south,
         35: Mortton,
         36: Abandoned_town,
         37: Old_mine,
         38: Old_pier,
         39: Meiyer_south,
         40: Vampire_graveyard,
         41: Meiyer_north,
         42: Barrows,
         43: Castle_drakan,
         44: Darkmeyer,
         45: Haunted_woods,
         46: Swampland,
         47: Ghost_port,
         48: West_varrock,
         49: Flour_mill,
         50: West_lum,
         51: West_swamp,
         52: Wizard_tower,
         53: South_draynor,
         54: North_draynor,
         55: Draynor_manor,
         56: Barbarian_village,
         57: Edgeville,
         58: Monastery,
         59: Dwarven_camp,
         60: Fally_east,
         61: Family_farm,
         62: Port_sarim,
         63: Old_dock,
         64: Rimmington,
         65: Road,
         66: Fally_west,
         67: Crossroads,
         68: Goblin_village,
         69: Taverley,
         70: Druid_circle,
         71: Burthorpe,
         72: Mountain_pass,
         73: Mountain_crossroads,
         74: Icy_path,
         75: Ancient_ruins,
         76: White_mountain,
         77: Warrior_guild,
         78: Death_plateau,
         79: Troll_stronghold,
         80: Mountain_camp,
         81: Mountain_hills,
         82: Windy_hills,
         83: Forest_trail,
         84: Relleka,
         85: Rocky_road,
         86: Grubby_woods,
         87: Knights_castle,
         88: Seers_village,
         89: Sorcerers_tower,
         90: Catherby,
         91: Ranging_guild,
         92: Manor_farm,
         93: East_ardy,
         94: Ardy_castle,
         95: Giants_camp,
         96: Fishing_guild,
         97: Monks_house,
         98: Fight_arena,
         99: Port_khazard,
         100: Yanille_east,
         101: Yanille_west,
         102: Ogre_city,
         103: Gnome_battlefield,
         104: West_ardy,
         105: Kings_road,
         106: Orchard,
         107: Gnome_stronghold_south,
         108: Gnome_stronghold_north,
         109: Underground_pass,
         110: West_pass_entrance,
         111: Elven_town,
         112: Dense_forest,
         113: Elf_city_south,
         114: Elf_city_north,
         115: High_elven_woods,
         116: Port_tyras,
         117: Shrine,
         118: Hunting_grounds,
         119: Zulrahs_island,
         120: God_dungeon_north,
         121: God_dungeon_entrance,
         122: God_dungeon_west,
         123: God_dungeon_east,
         124: God_dungeon_south,
         125: Wizards_guild,
         126: Crandor_beach,
         127: Dragons_den,
         128: Brimhaven_docks,
         129: Brimhaven_town,
         130: Volcano,
         131: Banana_plantation,
         132: Beach_storefront,
         133: Taibo_village,
         134: Central_jungle,
         135: River_village,
         136: Southern_jungle,
         137: Western_jungle,
         138: Eastern_jungle,
         139: Troll_tunnels,
         140: Troll_base_camp,
         141: Dwarven_mine_entrance,
         142: Dwarven_mine_south,
         143: Kalphite_lair_entrance,
         144: Kalphite_lair_tunnels,
         145: Kalphite_nest,
         146: Queens_chamber,
         147: Shipping_hub,
         148: North_docks,
         149: East_docks,
         150: South_docks,
         151: West_docks,
         152: Kings_training_grounds}
