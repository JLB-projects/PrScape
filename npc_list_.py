"""Contains all the NPCS that are placed in various areas."""

from objects import *

# NPCs defined here
Cook = Npc(1, "The Cook", "Cooks things.", "Thanks again for the help.\nNow if you'll excuse me, there's lots of "
                                           "cooking to do!", [[0, 0], [0, 1]])
Duke = Npc(0, "The Duke of Lum.", "Leads the town.", "I'm much too busy to deal with you, peasant.", [[0, 1]])
Shopkeeper = ShopNpc(2, 'Shopkeeper', 'Sells things.', "Need something?",
                     Shop(Inventory([39, 1], [44, 1], [174, 1], [37, 1], [27, 1], [28, 1], [36, 1], [2, 1], [45, 1],
                                    [46, 1], [52, 1], [53, 1], [59, 1], [60, 1], [151, 1], [155, 1],
                                    [76, 1], [83, 1], [94, 1], [144, 1], [145, 1], [77, 1], [78, 1], [288, 1])))
Man_npc = Npc(3, "Man", "Lives a normal life.", "You must be new around here. Welcome! I might have some work for you "
                                                "if you come back in a while, and happen to be interested. ", [])
Tut_shop = ShopNpc(4, "Shopkeeper", "Sells things.", "Want to buy something?",
                   Shop(Inventory([1, 1], [27, 1], [28, 1], [36, 1], [37, 1], [39, 1], [44, 1], [45, 1], [52, 1],
                                  [59, 1], [66, 1], [70, 1], [174, 1], [175, 1], [201, 1])))
Woman = Npc(5, "Woman", "Lives a normal life.", "Sorry, I'm looking for my husband.", [[1, 2], [1, 3]])

Father_eric = Npc(6, "Father Eric", "A holy man.", "Praise be upon you, traveller.", flags=[[2, 0], [2, 1], [2, 2]])
Ali = ShopNpc(7, "Ali", "Loves the desert.", "Hello there! Welcome to our home.",
              Shop(Inventory([39, 1], [44, 1], [174, 1], [37, 1], [27, 1], [28, 1], [36, 1], [2, 1], [45, 1],
                             [46, 1], [52, 1], [53, 1], [59, 1], [60, 1], [151, 1], [155, 1],
                             [76, 1], [83, 1], [94, 1], [144, 1], [145, 1], [77, 1], [78, 1], [66, 1], [67, 1],
                             [68, 1], [69, 1], [70, 1], [71, 1])))
Louie = ShopNpc(8, "Louie", "Trades in leg protection.", "Need some protection for those legs? I'm your man.",
                Shop(Inventory([87, 1], [98, 1], [109, 1], [120, 1], [131, 1])))
Prince = Npc(9, "Prince", "First in line to the throne.",
             "The King isn't here right now. You're welcome to look around.")
Desert_supplier = ShopNpc(10, "Desert supplier", "Sells the essentials.",
                          "The desert can be a harsh place. I offer what you need.",
                          Shop(Inventory([39, 1], [44, 1], [174, 1], [37, 1], [27, 1], [28, 1], [36, 1], [2, 1],
                                         [45, 1], [46, 1], [52, 1], [53, 1], [59, 1], [60, 1], [151, 1], [155, 1],
                                         [76, 1], [83, 1], [94, 1], [144, 1], [145, 1], [77, 1], [78, 1], [288, 1])))
Mining_slave = Npc(11, "Mining slave", "A struggling man.", "I don't think I'll survive another day.")
Bandit_shopkeeper = ShopNpc(12, "Bandit shopkeeper", "He's watching closely.",
                            "We don't deal with strangers, unless you make it worth our time.",
                            Shop(Inventory([39, 1], [44, 1], [174, 1], [37, 1], [27, 1], [28, 1], [36, 1], [2, 1],
                                           [45, 1], [46, 1], [52, 1], [53, 1], [59, 1], [60, 1], [151, 1], [155, 1],
                                           [76, 1], [83, 1], [94, 1], [144, 1], [145, 1], [77, 1], [78, 1], [288, 1])))
Wanderer = Npc(13, "Wanderer", "A mysterious woman.", "I see great things for you. We will talk again soon.")
High_priest = Npc(14, "High priest", "A very priestly man.",
                  "The plague is upon us, traveller. I bless thee with protection.")
Carpenter = ShopNpc(15, "Carpenter", "A block of a man.", "My wares are limited, but you may find them useful.",
                    Shop(Inventory([39, 1], [44, 1], [174, 1], [37, 1], [27, 1], [28, 1], [36, 1], [2, 1], [45, 1],
                                   [46, 1], [52, 1], [53, 1], [59, 1], [60, 1], [151, 1], [155, 1],
                                   [76, 1], [83, 1], [94, 1], [144, 1], [145, 1], [77, 1], [78, 1], [66, 1], [67, 1],
                                   [68, 1], [69, 1], [70, 1], [71, 1])))
Desert_trader = ShopNpc(16, "Desert trader", "A market stall trader.",
                        "Food is scarce here, but I have many other things to trade.",
                        Shop(Inventory([39, 1], [44, 1], [174, 1], [37, 1], [27, 1], [28, 1], [36, 1], [2, 1], [45, 1],
                                       [46, 1], [52, 1], [53, 1], [59, 1], [60, 1], [151, 1], [155, 1],
                                       [76, 1], [83, 1], [94, 1], [144, 1], [145, 1], [77, 1], [78, 1], [66, 1],
                                       [67, 1], [68, 1], [69, 1], [70, 1], [71, 1])))
Elderly_fisherman = Npc(17, "Elderly fisherman", "He's caught everything once.",
                        "You are welcome to fish here, but please be mindful of our needs.")
Farmhand = Npc(18, "Farmhand", "Tends to his crops.", "I'm starting to think we have too many animals here! ")
Horvik = ShopNpc(19, "Horvik", "Sells the best plate bodies.", "Rock hard. Durable. You in need of protection?",
                 Shop(Inventory([88, 1], [99, 1], [110, 1], [121, 1], [132, 1])))
Swordsmith = ShopNpc(20, "Swordsmith", "Makes a living from swords.", "Need a blade? I can help you out.",
                     Shop(Inventory([83, 1], [94, 1], [105, 1], [116, 1], [127, 1])))
Dr_harlow = Npc(21, "Dr Harlow", "A retired vampire hunter.", "*Hic* I could use another beer *Hic*")
Romeo = Npc(22, "Romeo", "Rather dense.", "Oh Juliet, how I miss your loving touch…", [[4, 0], [4, 1], [4, 2], [4, 6]])
King_roald = Npc(23, "King Roald", "Varrock's resident monarch.", "Sorry, I'm much too busy to talk right now.",
                 [[3, 0], [3, 5]])
Sir_prism = Npc(24, "Sir prism", "The king's best knight.", "I serve the king.")
Odd_old_man = Npc(25, "Odd old man", "Carries a lot of bones.",
                  "Sticks and stones may break their bones, but I prefer them intact and shiny.")
Drazel = Npc(26, "Drazel", "A holier man.", "The danger from the east grows stronger each day, adventurer.",
             [[3, 0], [3, 1], [3, 2], [3, 4], [3, 5]])
Strange_shopkeeper = ShopNpc(27, "Strange shopkeeper", "Smells like dog food.", "Woof.",
                             Shop(Inventory([39, 1], [44, 1], [174, 1], [37, 1], [27, 1], [28, 1], [36, 1], [2, 1],
                                            [45, 1], [46, 1], [52, 1], [53, 1], [59, 1], [60, 1], [151, 1], [155, 1],
                                            [76, 1], [83, 1], [94, 1], [144, 1], [145, 1], [77, 1], [78, 1], [66, 1],
                                            [67, 1], [68, 1], [69, 1], [70, 1], [71, 1])))
Veliaf = Npc(28, "Veliaf", "Leader of the resistance.", "The fight is not yet won.")
Boatmaster = Npc(29, "Boatmaster", "Master of boats.", "Need a ride? I know these swamps better than anyone.")
Villager = Npc(30, "Villager", "Something seems off about him.", "I don't feel so good…")
Old_man_ray = Npc(31, "Old man Ray", "He remembers life before it all.", "Be quiet, the vampires are always listening.")
Sven = Npc(32, "Sven", "He keeps to himself.", "Do I know you?")
Veliaf_2 = Npc(33, "Veliaf", "Leader of the resistance.", "I worry we will never be rid of the vampires for good.")
Strange_old_man = Npc(34, "Strange old man", "Seems confused.", "I was there, you know. When it all began.")
Prisoner = Npc(35, "Prisoner", "Seems desperate.", "Please help me.")
Grigor_rasputin = Npc(36, "Grigor Rasputin", "Shame how he carried on.", "If they find you here, I can't protect you.")
Survivor = Npc(37, "Survivor", "Does his best.", "Why would you come here? By choice of all things…")
Ghost_captain = Npc(38, "Ghost captain", "Believes he's alive.",
                    "Care to board my ship? She's unsinkable. Bet my life on it.")
Lost_soul = Npc(39, "Lost soul", "Can't find the light.", "So alone. So cold. So empty.")
Ghost_shopkeeper = ShopNpc(40, "Ghost shopkeeper", "He may be a ghost but the products are real.",
                           "I can offer you some things to keep you alive. Or not, I need some company.",
                           Shop(Inventory([39, 1], [44, 1], [174, 1], [37, 1], [27, 1], [28, 1], [36, 1], [2, 1],
                                          [45, 1], [46, 1], [52, 1], [53, 1], [59, 1], [60, 1], [151, 1], [155, 1],
                                          [76, 1], [83, 1], [94, 1], [144, 1], [145, 1], [77, 1], [78, 1], [66, 1],
                                          [67, 1], [68, 1], [69, 1], [70, 1], [71, 1])))
Juliet = Npc(41, "Juliet", "A tearful damsel. ", "What are you looking at?", [[4, 0], [4, 1], [4, 5], [4, 6]],
             quest_lock=[[4, 7], 'kill'])
Apothecary = Npc(42, "Apothecary", "His potions are too strong for you.",
                 "Sorry but I can't make you a potion right now.", [[4, 3], [4, 4], [4, 5]])
Father_urney = Npc(43, "Father Urney", "Very holy.", "Go away! ", [[2, 0], [2, 1]])
Wizard_treyborn = Npc(44, "Wizard Treyborn", "Magical and potentially insane.",
                      "These darn imps are always stealing my beads…", [[3, 2], [3, 3], [3, 4]])
Wise_old_man = Npc(45, "Wise old man", "A venerable and rich sage. ",
                   "I hear the manor to the north is haunted. But who believes in that nonsense!")
Ned = Npc(46, "Ned", "An ageing man with a dream.", "I still dream that I can sail the seas once more…")
Professor = Npc(47, "Professor", "Fits the stereotype perfectly.",
                "I'm going mad in here! Get out before it's too late…")
Peksa = ShopNpc(48, "Peksa", "Headstrong.", "Are you interested in a helmet?",
                Shop(Inventory([84, 1], [95, 1], [106, 1], [117, 1], [128, 1])))
Shop_assistant = ShopNpc(49, "Shop assistant", "Sells the essentials.", "Can I help you at all?",
                         Shop(Inventory([39, 1], [44, 1], [174, 1], [37, 1], [27, 1], [28, 1], [36, 1], [2, 1], [45, 1],
                                        [46, 1], [52, 1], [53, 1], [59, 1], [60, 1], [151, 1], [155, 1],
                                        [76, 1], [83, 1], [94, 1], [144, 1], [145, 1], [77, 1], [78, 1], [288, 1])))
Oziach = Npc(50, "Oziach", "A strange little man.",
             "Come back when yer a bit stronger, adventurer. I could use the help.")
Shieldsmith = ShopNpc(51, "Shieldsmith", "A fine armourer.", "A shield is as important as a sword, I say.",
                      Shop(Inventory([85, 1], [96, 1], [107, 1], [118, 1], [129, 1])))
Betty = ShopNpc(52, "Betty", "Looks nice.", "Don't tell the Wizard Guild, but I have some basic runes you can buy.",
                Shop(Inventory([66, 1], [67, 1], [68, 1], [69, 1], [70, 1], [71, 1], [72, 1], [74, 1])))
Captain_toby = Npc(53, "Captain Toby", "An old sea dog.", "Need a ride?")
Ned_2 = Npc(54, "Ned", "An ageing man with a dream.", "Ready to go? There are dragons to kill.")
Witch = Npc(55, "Witch", "The hat's a dead giveaway. ", "Don’t believe what they say, I'm not a witch!")
Shopkeeper_fally = ShopNpc(56, "Shopkeeper", "Sells the essentials.", "Need something?",
                           Shop(Inventory([39, 1], [44, 1], [174, 1], [37, 1], [27, 1], [28, 1], [36, 1], [2, 1],
                                          [45, 1], [46, 1], [52, 1], [53, 1], [59, 1], [60, 1], [151, 1], [155, 1],
                                          [76, 1], [83, 1], [94, 1], [144, 1], [145, 1], [77, 1], [78, 1], [288, 1])))
Sir_amik = Npc(57, "Sir Amik", "Leader of the white knights.", "Welcome to our great city.")
Goblin_general = Npc(58, "Goblin general", "Leader of the goblins.", "Oi! Get out of our village!")
Sanfew = Npc(59, "Sanfew", "An old druid.", "I mix potions and concoctions, but I seem to be missing some ingredients.")
Kaquamix = Npc(60, "Kaquamix", "The most respected druid around.", "Anyone is welcome to stay with the druids, friend.")
Duncan = Npc(61, "Duncan", "A hard working man.", "Be careful to the north, traveller. The trolls won't be friendly.")
Commander = Npc(62, "Commander", "Can't wait to go to war.",
                "Attention recruit! Be on alert, the trolls are preparing an invasion any minute.")
Wounded_knight = Npc(63, "Wounded knight", "Clearly traumatised.",
                     "Please… don't go in there. There's nothing but death to await you.")
Elite_warrior = Npc(64, "Elite warrior", "Knows his way around a blade.",
                    "Come see me when you are a master of attack. I might have a gift for you.")
Cyclops_herder = Npc(65, "Cyclops herder", "Used to herd cows.",
                     "Feel free to try your luck on these Cyclops, and you could get your hands on a "
                     "nice piece of kit!")
Wounded_soldier = Npc(66, "Wounded soldier", "Can't wait to go home.",
                      "These trolls damn near killed me! Be on guard, adventurer.")
Chieftain = Npc(67, "Chieftain", "Leader of the mountain camp.", "We welcome travellers, but don't stay too long.")
Worker = Npc(68, "Worker", "Fixes things.", "Somebody's gotta fix these bridges! Sucks to be me…")
Brundt = Npc(69, "Brundt", "The tribe's chieftain.", "Greetings, traveller. Care to join us?")
Huntsman = Npc(70, "Huntsman", "A local hunter.", "The hunt is on.")
Merchant = ShopNpc(71, "Merchant", "Sells the essentials.", "I have wares, if you have coin.",
                   Shop(Inventory([39, 1], [44, 1], [174, 1], [37, 1], [27, 1], [28, 1], [36, 1], [2, 1], [45, 1],
                                  [46, 1], [52, 1], [53, 1], [59, 1], [60, 1], [151, 1], [155, 1],
                                  [76, 1], [83, 1], [94, 1], [144, 1], [145, 1], [77, 1], [78, 1], [66, 1], [67, 1],
                                  [68, 1], [69, 1], [70, 1], [71, 1])))
King_arthur = Npc(72, "King Arthur", "A legendary king.", "The knights of the square table welcome you.")
Seer = Npc(73, "Seer", "Could use a shave.", "I see your future. I see death.")
Harry = ShopNpc(74, "Harry", "Something fishy about him.",
                "Fishing is my life, I've got a few things to spare if you're interested.",
                Shop(Inventory([59, 1], [60, 1], [61, 1], [62, 1], [63, 1])))
Master_farmer = Npc(75, "Master farmer", "A master of farming",
                    "I think someone has been killing my cattle! If you see anything, let me know.")
Hideworker = ShopNpc(76, "Hideworker", "Works well with hides.", "I swear my hides are ethically obtained!",
                     Shop(Inventory([185, 1], [186, 1], [187, 1], [188, 1], [144, 1], [145, 1], [146, 1], [147, 1],
                                    [148, 1], [151, 1], [153, 1], [155, 1], [157, 1], [159, 1], [161, 1], [163, 1],
                                    [165, 1], [167, 1], [169, 1])))
King_lathas = Npc(77, "King Lathas", "A shady looking king.", "Begone peasant.")
Master_fisherman = ShopNpc(78, "Master fisherman", "The man in charge of the guild.",
                           "Welcome to the guild, stranger. Take a look around, or come see me if you need equipment.",
                           Shop(Inventory([59, 1], [60, 1], [61, 1], [62, 1], [63, 1], [64, 1])))
Old_monk = Npc(79, "Old monk", "An old holy man.",
               "If you need some peace from the constant fighting to the south, you're welcome to stay.")
Arena_prisoner = Npc(80, "Arena prisoner", "A man of misfortune.", "I'll be out of here any day now…")
Dock_worker = Npc(81, "Dock worker", "Keeps it ship shape.",
                  "The ships might be old, but they sail the seas all the same!")
Wizard_guild_guard = Npc(82, "Wizard's Guild guard", "Magical.",
                         "Only the best users of magic can find their way to the guild.")
Citizen = Npc(83, "Citizen", "Just a regular guy.",
              "Hello, stranger. Have you visited the Wizard's Guild? I hear it's all the rage these days.")
Friendly_ogre = Npc(84, "Friendly ogre", "Seems friendly.",
                    "The ogres have turned on you, human. I don't support the violence, but maybe I can be of help.")
Underground_guard = Npc(85, "Underground guard", "Keeps people out.",
                        "Halt! Beyond this entrance lies danger. Only the king's best men may enter.")
Kings_guard = Npc(86, "King's guard", "Keeps the ogres coming.",
                  "A friend of the king is always welcome. Please, feel free to train your skills on these ogres. "
                  "They won't fight back, but they also aren't carrying any loot for you.")
Gnome_king = Npc(87, "Gnome king", "Small but respected.",
                 "Our kingdom may be in need of your talents, soon enough. For now, enjoy your stay.")
Gulluck = ShopNpc(88, "Gulluck", "Sells weapons bigger than he is.", "Gnomes need gold too, you know. Got some?",
                  Shop(Inventory([86, 1], [97, 1], [108, 1], [119, 1], [130, 1], [144, 1], [145, 1], [146, 1], [147, 1],
                                 [148, 1], [151, 1], [153, 1], [155, 1], [157, 1], [159, 1], [161, 1], [163, 1],
                                 [165, 1], [167, 1], [169, 1])))
Koftik = Npc(89, "Koftik", "Loyal to the king.", "I'll watch your back down here, if you watch mine.")
Arianwyn = Npc(90, "Arianwyn", "A seemingly friendly elf.",
               "We don’t get humans around here very often. Be careful, not all of us are so accommodating.")
Elven_supplier = ShopNpc(91, "Elven supplier", "Sells the essentials.",
                         "I don’t know, I guess I can sell you some things. You better not steal anything!",
                         Shop(Inventory([39, 1], [44, 1], [174, 1], [37, 1], [27, 1], [28, 1], [36, 1], [2, 1], [45, 1],
                                        [46, 1], [52, 1], [53, 1], [59, 1], [60, 1], [151, 1], [155, 1],
                                        [76, 1], [83, 1], [94, 1], [144, 1], [145, 1], [77, 1], [78, 1], [66, 1],
                                        [67, 1], [68, 1], [69, 1], [70, 1], [71, 1])))
Elf_prince = Npc(92, "Elf prince", "Looks concerned.",
                 "Welcome to the city, human. I hope you can be of use to us somehow.")
Elf_queen = Npc(93, "Elf queen", "A pretentious, fancy looking elf.", "Look, but don't touch.")
Elven_dock_worker = Npc(94, "Elven dock worker", "Manages the docks.",
                        "All races are welcome on the boat, but the prices aren’t cheap.")
High_priestess = Npc(95, "High priestess", "Seems mentally unwell.",
                     "She speaks to me, still. Sleepless nights… The voices…")
Wounded_elf = Npc(96, "Wounded elf", "In need of help.",
                  "The wildlife can be vicious around these parts. Feel free to help out with the culling.")
Elder_wizard = Npc(97, "Elder wizard", "The best wizard around.",
                   "The guild welcomes you. It's nice to see another aspiring mage.")
Wizard_shop = ShopNpc(98, "Wizard shop", "A supplier of magical items.",
                      "Runes, robes and magical staves, all available for purchase!",
                      Shop(Inventory([66, 1], [67, 1], [68, 1], [69, 1], [70, 1], [71, 1], [72, 1], [73, 1], [74, 1],
                                     [205, 1], [219, 1], [220, 1], [221, 1], [222, 1])))
Dock_master = Npc(99, "Dock master", "Master of docks.",
                  "Island life is lonely, so I take to the seas now and then. I can take you too, if you’d like.")
Pirate_npc = Npc(100, "Pirate", "Isn't your matey.", "Arrrrrrr! ")
Exotic_fisherman = Npc(101, "Exotic fisherman", "Fisher of exotic fish.",
                       "There isn’t a fish I haven't caught, I tell you!")
Jimmy = ShopNpc(102, "Jimmy", "Has goods for sale.", "The tribe brings me things. I sell them.",
                Shop(Inventory([39, 1], [44, 1], [174, 1], [37, 1], [27, 1], [28, 1], [36, 1], [2, 1], [45, 1],
                               [46, 1], [52, 1], [53, 1], [59, 1], [60, 1], [151, 1], [155, 1],
                               [76, 1], [83, 1], [94, 1], [144, 1], [145, 1], [77, 1], [78, 1], [66, 1], [67, 1],
                               [68, 1], [69, 1], [70, 1], [71, 1])))
Tribe_leader = Npc(103, "Tribe leader", "Slightly confrontational.",
                   "I would step carefully around these parts, traveller. ")
Forester = Npc(104, "Forester", "Chops fancy wood.",
               "The jungle to the south has been unexplored for decades. Man, I’d love to see it someday.")
River_fisher = Npc(105, "River fisher", "Born and raised on these fish.", "These fish just taste better.")
Dwarf_trader = ShopNpc(106, "Dwarf trader", "Mines his own business.",
                       "Tools of the trade are my speciality, and the only trade I know is mining.",
                       Shop(Inventory([52, 1], [53, 1], [54, 1], [55, 1], [56, 1], [57, 1])))
Dwarven_overseer = Npc(107, "Dwarven Overseer", "A little oppressive.", "Get to work!")
Shipmaster = Npc(108, "Shipmaster", "Master of ships.",
                 "Different destinations await you from each dock, but we don't take just anyone.")
Ranging_guild_guard = Npc(109, "Ranging Guild guard", "Currently unemployed.",
                          "The guild isn't quite ready yet, traveller. Come back later.")
Lumberjack = ShopNpc(110, "Lumberjack", "He's okay.", "Need some help cutting those trees?",
                     Shop(Inventory([45, 1], [46, 1], [47, 1], [48, 1], [49, 1], [50, 1])))
Father_lawrence = Npc(111, "Father Lawrence", "A holy man.", "Praise be upon you, traveller.", flags=[[4, 2], [4, 3]])

Npcs = {0: Duke,
        1: Cook,
        2: Shopkeeper,
        3: Man_npc,
        4: Tut_shop,
        5: Woman,
        6: Father_eric,
        7: Ali,
        8: Louie,
        9: Prince,
        10: Desert_supplier,
        11: Mining_slave,
        12: Bandit_shopkeeper,
        13: Wanderer,
        14: High_priest,
        15: Carpenter,
        16: Desert_trader,
        17: Elderly_fisherman,
        18: Farmhand,
        19: Horvik,
        20: Swordsmith,
        21: Dr_harlow,
        22: Romeo,
        23: King_roald,
        24: Sir_prism,
        25: Odd_old_man,
        26: Drazel,
        27: Strange_shopkeeper,
        28: Veliaf,
        29: Boatmaster,
        30: Villager,
        31: Old_man_ray,
        32: Sven,
        33: Veliaf_2,
        34: Strange_old_man,
        35: Prisoner,
        36: Grigor_rasputin,
        37: Survivor,
        38: Ghost_captain,
        39: Lost_soul,
        40: Ghost_shopkeeper,
        41: Juliet,
        42: Apothecary,
        43: Father_urney,
        44: Wizard_treyborn,
        45: Wise_old_man,
        46: Ned,
        47: Professor,
        48: Peksa,
        49: Shop_assistant,
        50: Oziach,
        51: Shieldsmith,
        52: Betty,
        53: Captain_toby,
        54: Ned_2,
        55: Witch,
        56: Shopkeeper_fally,
        57: Sir_amik,
        58: Goblin_general,
        59: Sanfew,
        60: Kaquamix,
        61: Duncan,
        62: Commander,
        63: Wounded_knight,
        64: Elite_warrior,
        65: Cyclops_herder,
        66: Wounded_soldier,
        67: Chieftain,
        68: Worker,
        69: Brundt,
        70: Huntsman,
        71: Merchant,
        72: King_arthur,
        73: Seer,
        74: Harry,
        75: Master_farmer,
        76: Hideworker,
        77: King_lathas,
        78: Master_fisherman,
        79: Old_monk,
        80: Arena_prisoner,
        81: Dock_worker,
        82: Wizard_guild_guard,
        83: Citizen,
        84: Friendly_ogre,
        85: Underground_guard,
        86: Kings_guard,
        87: Gnome_king,
        88: Gulluck,
        89: Koftik,
        90: Arianwyn,
        91: Elven_supplier,
        92: Elf_prince,
        93: Elf_queen,
        94: Elven_dock_worker,
        95: High_priestess,
        96: Wounded_elf,
        97: Elder_wizard,
        98: Wizard_shop,
        99: Dock_master,
        100: Pirate_npc,
        101: Exotic_fisherman,
        102: Jimmy,
        103: Tribe_leader,
        104: Forester,
        105: River_fisher,
        106: Dwarf_trader,
        107: Dwarven_overseer,
        108: Shipmaster,
        109: Ranging_guild_guard,
        110: Lumberjack,
        111: Father_lawrence}
