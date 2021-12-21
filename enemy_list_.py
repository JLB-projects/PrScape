"""Contains all the enemies that are placed in various areas."""

from objects import *

# Enemies defined here
Goblin = Enemy(0, 'Goblin', 'A short smelly creature.', {'Attack': [1, ], 'Defence': [1, ], 'Hitpoints': [5, ],
               'Magic': [1, ], 'Strength': [1, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
               [[0, 0.4, 1, 15], [28, 0.3, 1, 1], [82, 0.3, 1, 1]], True)
Cow = Enemy(1, 'Cow', 'Milky.', {'Attack': [1, ], 'Defence': [1, ], 'Hitpoints': [8, ],
            'Magic': [1, ], 'Strength': [1, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400, [[175, 1, 1, 1]], True)
Rat = Enemy(2, 'Rat', 'A diseased rodent.', {'Attack': [1, ], 'Defence': [1, ], 'Hitpoints': [2, ],
            'Magic': [1, ], 'Strength': [1, ], 'Ranged': [1, ]}, 'Melee', {}, None, 3000,
            [[0, 1, 1, 5]], True)
Chicken = Enemy(3, 'Chicken', 'Lays eggs.', {'Attack': [1, ], 'Defence': [1, ], 'Hitpoints': [3, ],
                'Magic': [1, ], 'Strength': [1, ], 'Ranged': [1, ]}, 'Melee', {}, None, 1800, [[1, 0.5, 1, 1],
                                                                                               [36, 0.5, 1, 7]], True,
                alt_drops=[[0, 0], [276, 1, 1, 1]])
Man_enemy = Enemy(4, 'Man', 'A hopeful adventurer.', {'Attack': [10, ], 'Defence': [10, ], 'Hitpoints': [10, ],
                  'Magic': [1, ], 'Strength': [10, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400, [[0, 1, 100, 100]],
                  True)
Frog = Enemy(5, 'Frog', 'Jumps around a little.', {'Attack': [5, ], 'Defence': [3, ], 'Hitpoints': [8, ],
             'Magic': [1, ], 'Strength': [4, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
             [[176, 0.5, 1, 2], [66, 0.2, 1, 10], [67, 0.2, 1, 10], [70, 0.1, 1, 10]], True)
Man = Enemy(6, 'Man', 'A regular man.', {'Attack': [1, ], 'Defence': [1, ], 'Hitpoints': [7, ],
            'Magic': [1, ], 'Strength': [1, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
            [[0, 0.5, 1, 20], [66, 0.2, 1, 10], [67, 0.2, 1, 10], [70, 0.1, 1, 10]], True)
Mill_operator = Enemy(7, 'Mill Operator', 'Operates the mill.', {'Attack': [10, ], 'Defence': [5, ],
                      'Hitpoints': [10, ], 'Magic': [1, ], 'Strength': [10, ], 'Ranged': [1, ]}, 'Melee', {}, None,
                      3000, [[0, 0.4, 1, 20], [38, 0.6, 1, 1]], True)
Seagull = Enemy(8, 'Seagull', 'An annoying sea bird.', {'Attack': [10, ], 'Defence': [1, ], 'Hitpoints': [8, ],
                'Magic': [1, ], 'Strength': [10, ], 'Ranged': [1, ]}, 'Melee', {}, None, 3000,
                [[-1, 1, 1, 1]], True)
Kalphite_larva = Enemy(9, 'Kalphite larva', 'A very young kalphite.', {'Attack': [1, ], 'Defence': [1, ],
                       'Hitpoints': [5, ], 'Magic': [1, ], 'Strength': [1, ], 'Ranged': [1, ]}, 'Melee', {}, None, 4800,
                       [[0, 0.8, 1, 10], [81, 0.1, 1, 1], [-1, 0.1, 1, 1]], True)
Guard = Enemy(10, 'Guard', 'Keeps the people safe.', {'Attack': [20, ], 'Defence': [14, ],
              'Hitpoints': [22, ], 'Magic': [1, ], 'Strength': [18, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
              [[0, 0.3, 1, 50], [145, 0.2, 1, 25], [146, 0.2, 1, 25], [104, 0.3, 1, 1]], True)
Big_frog = Enemy(11, 'Big frog', 'Jumps around a lot.', {'Attack': [25, ], 'Defence': [15, ],
                 'Hitpoints': [25, ], 'Magic': [1, ], 'Strength': [20, ], 'Ranged': [1, ]}, 'Melee', {}, None, 3000,
                 [[176, 0.5, 1, 3], [66, 0.2, 1, 20], [67, 0.2, 1, 20], [71, 0.1, 1, 10]], True)
Giant_rat = Enemy(12, 'Giant rat', 'A large diseased rodent.', {'Attack': [20, ], 'Defence': [20, ],
                  'Hitpoints': [18, ], 'Magic': [1, ], 'Strength': [20, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                  [[39, 0.3, 1, 1], [84, 0.2, 1, 1], [0, 0.3, 1, 30], [-1, 0.2, 1, 1]], True)
Al_Kharid_warrior = Enemy(13, 'Al-Kharid warrior', 'Loyal to the prince.', {'Attack': [17, ], 'Defence': [14, ],
                          'Hitpoints': [19, ], 'Magic': [1, ], 'Strength': [15, ], 'Ranged': [1, ]}, 'Melee', {}, None,
                          2400, [[40, 0.2, 1, 1], [99, 0.2, 1, 1], [0, 0.4, 1, 30], [98, 0.2, 1, 1]], True)
Scorpion = Enemy(14, 'Scorpion', 'Has a scary set of pincers.', {'Attack': [21, ], 'Defence': [21, ],
                 'Hitpoints': [17, ], 'Magic': [1, ], 'Strength': [22, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                 [[34, 0.4, 1, 1], [35, 0.4, 1, 1], [-1, 0.2, 1, 1]], True)
Locust = Enemy(15, 'Locust', 'A sign of the plague?', {'Attack': [15, ], 'Defence': [1, ],
               'Hitpoints': [27, ], 'Magic': [1, ], 'Strength': [18, ], 'Ranged': [1, ]}, 'Melee', {}, None, 1800,
               [[-1, 1, 1, 1]], True)
Farmer = Enemy(16, 'Farmer', 'Tends to his crops.', {'Attack': [3, ], 'Defence': [8, ],
               'Hitpoints': [12, ], 'Magic': [1, ], 'Strength': [8, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
               [[0, 0.5, 1, 25], [144, 0.3, 1, 20], [145, 0.2, 1, 20]], True)
Bat = Enemy(17, 'Bat', 'An annoying flappy thing.', {'Attack': [5, ], 'Defence': [5, ],
            'Hitpoints': [8, ], 'Magic': [1, ], 'Strength': [8, ], 'Ranged': [1, ]}, 'Melee', {}, None, 1800,
            [[175, 0.5, 1, 1], [0, 0.5, 1, 15]], True)
Banshee = Enemy(18, 'Banshee', 'A wailing ghost.', {'Attack': [15, ], 'Defence': [1, ],
                'Hitpoints': [22, ], 'Magic': [20, ], 'Strength': [18, ], 'Ranged': [1, ]}, 'Magic', {}, None, 2400,
                [[-1, 0.2, 1, 1], [222, 0.05, 1, 1], [219, 0.05, 1, 1], [47, 0.2, 1, 1], [0, 0.5, 1, 45]], True)
Swamp_snail = Enemy(19, 'Swamp snail', 'Slimy.', {'Attack': [5, ], 'Defence': [22, ],
                    'Hitpoints': [8, ], 'Magic': [50, ], 'Strength': [5, ], 'Ranged': [10, ]}, 'Ranged', {}, None, 1800,
                    [[-1, 0.3, 1, 1], [93, 0.2, 1, 1], [96, 0.2, 1, 1], [99, 0.3, 1, 1]], True)
Young_vampire = Enemy(20, 'Young vampire', 'Paler than most.', {'Attack': [25, ], 'Defence': [20, ],
                      'Hitpoints': [25, ], 'Magic': [1, ], 'Strength': [20, ], 'Ranged': [1, ]}, 'Melee', {}, None,
                      2400, [[-1, 0.2, 1, 1], [47, 0.2, 1, 1], [105, 0.3, 1, 1], [110, 0.3, 1, 1]], True)
Leech = Enemy(21, 'Leech', 'Sucks.', {'Attack': [80, ], 'Defence': [35, ],
              'Hitpoints': [30, ], 'Magic': [1, ], 'Strength': [20, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
              [[-1, 1, 1, 1]], True)
Giant_spider = Enemy(22, 'Giant spider', 'Still 8 legs, but much bigger.', {'Attack': [20, ], 'Defence': [21, ],
                     'Hitpoints': [32, ], 'Magic': [1, ], 'Strength': [24, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                     [[0, 0.3, 1, 50], [82, 0.2, 1, 1], [83, 0.3, 1, 1], [-1, 0.2, 1, 1]], True)
Wizard = Enemy(23, 'Wizard', 'Slightly magical.', {'Attack': [1, ], 'Defence': [1, ],
               'Hitpoints': [14, ], 'Magic': [15, ], 'Strength': [18, ], 'Ranged': [1, ]}, 'Magic', {}, None, 2400,
               [[211, 0.1, 1, 1], [212, 0.1, 1, 1], [213, 0.1, 1, 1], [214, 0.1, 1, 1], [66, 0.1, 10, 25],
               [67, 0.1, 10, 20], [68, 0.1, 10, 20], [69, 0.1, 10, 20], [76, 0.1, 1, 1], [202, 0.1, 1, 1]], True)
Skeleton = Enemy(24, 'Skeleton', 'Spooky, scary.', {'Attack': [24, ], 'Defence': [24, ],
                 'Hitpoints': [17, ], 'Magic': [1, ], 'Strength': [24, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                 [[89, 0.3, 1, 2], [144, 0.2, 1, 30], [145, 0.3, 1, 40], [-1, 0.2, 1, 1]], True,
                 alt_drops=[[2, 2], [282, 1, 1, 1]])
Ghost = Enemy(25, 'Ghost', 'Boo!', {'Attack': [1, ], 'Defence': [25, ],
              'Hitpoints': [27, ], 'Magic': [28, ], 'Strength': [1, ], 'Ranged': [1, ]}, 'Magic', {}, None, 2400,
              [[-1, 1, 1, 1]], True)
Barbarian = Enemy(26, 'Barbarian', 'Angry and dangerous.', {'Attack': [15, ], 'Defence': [10, ],
                  'Hitpoints': [24, ], 'Magic': [1, ], 'Strength': [14, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                  [[0, 0.4, 1, 25], [40, 0.1, 1, 1], [84, 0.3, 1, 1], [93, 0.2, 1, 1]], True)
Monk = Enemy(27, 'Monk', "He's halfway there.", {'Attack': [15, ], 'Defence': [15, ],
             'Hitpoints': [15, ], 'Magic': [20, ], 'Strength': [10, ], 'Ranged': [1, ]}, 'Magic', {}, None, 2400,
             [[0, 0.3, 10, 30], [242, 0.1, 1, 1]], True)
Dwarf = Enemy(28, 'Dwarf', 'Short, but angry.', {'Attack': [20, ], 'Defence': [21, ],
              'Hitpoints': [26, ], 'Magic': [1, ], 'Strength': [22, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
              [[0, 0.3, 20, 50], [53, 0.15, 1, 1], [52, 0.3, 1, 1], [-1, 0.25, 1, 1]], True)
Highwayman = Enemy(29, 'Highwayman', 'Steals from the less fortunate.', {'Attack': [10, ], 'Defence': [1, ],
                   'Hitpoints': [13, ], 'Magic': [1, ], 'Strength': [12, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                   [[0, 0.45, 1, 20], [41, 0.15, 1, 1], [-1, 0.4, 1, 1]], True)
Mountain_goat = Enemy(30, 'Mountain goat', 'Eats anything.', {'Attack': [20, ], 'Defence': [21, ],
                      'Hitpoints': [21, ], 'Magic': [1, ], 'Strength': [25, ], 'Ranged': [1, ]}, 'Melee', {}, None,
                      2400, [[100, 0.3, 1, 1], [89, 0.2, 1, 1], [-1, 0.5, 1, 1]], True)
Young_cyclops = Enemy(31, 'Young cyclops', "One eye. Don't think he'll grow another.", {'Attack': [20, ],
                      'Defence': [25, ], 'Hitpoints': [30, ], 'Magic': [1, ], 'Strength': [25, ], 'Ranged': [1, ]},
                      'Melee', {}, None, 3000, [[0, 0.3, 20, 50], [250, 0.1, 1, 1], [251, 0.1, 1, 1]], True)
Mountain_camper = Enemy(32, 'Mountain camper', 'Camps in the mountains.', {'Attack': [15, ], 'Defence': [5, ],
                        'Hitpoints': [20, ], 'Magic': [50, ], 'Strength': [20, ], 'Ranged': [25, ]}, 'Ranged', {}, None,
                        2400, [[0, 0.6, 10, 40]], True)
Unicorn = Enemy(33, 'Unicorn', "One horn. Mythical.", {'Attack': [11, ], 'Defence': [13, ],
                'Hitpoints': [19, ], 'Magic': [1, ], 'Strength': [13, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                [[12, 0.2, 1, 3], [15, 0.2, 1, 1], [0, 0.1, 1, 15]], True)
Hill_giant = Enemy(34, 'Hill giant', "Very large.", {'Attack': [18, ], 'Defence': [26, ],
                   'Hitpoints': [35, ], 'Magic': [1, ], 'Strength': [25, ], 'Ranged': [1, ]}, 'Melee', {}, None, 3000,
                   [[0, 0.3, 20, 50], [108, 0.1, 1, 1], [110, 0.1, 1, 1], [103, 0.1, 1, 1]], True)
Snake = Enemy(35, 'Snake', "Slithering serpent.", {'Attack': [25, ], 'Defence': [40, ],
              'Hitpoints': [25, ], 'Magic': [1, ], 'Strength': [25, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
              [[-1, 1, 1, 1]], True)
Sand_crab = Enemy(36, 'Sand crab', "Sandy.", {'Attack': [1, ], 'Defence': [1, ],
                  'Hitpoints': [60, ], 'Magic': [1, ], 'Strength': [1, ], 'Ranged': [1, ]}, 'Melee', {}, None, 1800,
                  [[-1, 1, 1, 1]], True)
Monkey = Enemy(37, 'Monkey', "Our long lost relative?", {'Attack': [10, ], 'Defence': [5, ],
               'Hitpoints': [12, ], 'Magic': [1, ], 'Strength': [5, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
               [[273, 0.5, 1, 2]], True)
Kalphite_worker = Enemy(38, 'Kalphite worker', "Insect repellent might not be enough.", {'Attack': [20, ],
                        'Defence': [20, ], 'Hitpoints': [40, ], 'Magic': [1, ], 'Strength': [20, ], 'Ranged': [1, ]},
                        'Melee', {}, None, 2400, [[0, 0.3, 20, 60], [106, 0.15, 1, 1], [103, 0.15, 1, 1],
                        [47, 0.1, 1, 1]], True)
Sand_golem = Enemy(39, 'Sand golem', "Rock solid.", {'Attack': [20, ], 'Defence': [40, ],
                   'Hitpoints': [40, ], 'Magic': [50, ], 'Strength': [20, ], 'Ranged': [45, ]}, 'Ranged', {}, None,
                   2400, [[0, 0.3, 50, 100], [163, 0.15, 1, 1], [165, 0.15, 1, 1], [102, 0.3, 5, 25]], True)
Desert_wolf = Enemy(40, 'Desert wolf', "A scavenger of the sands.", {'Attack': [50, ],
                    'Defence': [52, ], 'Hitpoints': [69, ], 'Magic': [1, ], 'Strength': [55, ], 'Ranged': [1, ]},
                    'Melee', {}, None, 2400, [[120, 0.3, 20, 60], [115, 0.2, 1, 1], [105, 0.3, 1, 1]], True)
Slaver = Enemy(41, 'Slaver', "Keeps slaves in line.", {'Attack': [40, ], 'Defence': [30, ],
               'Hitpoints': [45, ], 'Magic': [1, ], 'Strength': [40, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
               [[35, 0.3, 1, 1], [31, 0.3, 1, 1], [104, 0.2, 1, 1]], True)
Mining_guard = Enemy(42, 'Mining guard', "Guards the mine.", {'Attack': [45, ], 'Defence': [40, ],
                     'Hitpoints': [52, ], 'Magic': [1, ], 'Strength': [45, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                     [[55, 0.1, 20, 60], [54, 0.15, 1, 1], [53, 0.2, 1, 1], [52, 0.3, 1, 1]], True)
Desert_lizard = Enemy(43, 'Desert lizard', "Reptile of the sands.", {'Attack': [30, ], 'Defence': [20, ],
                      'Hitpoints': [25, ], 'Magic': [1, ], 'Strength': [32, ], 'Ranged': [1, ]}, 'Melee', {}, None,
                      2400, [[219, 0.1, 1, 1], [222, 0.1, 1, 1], [100, 0.5, 1, 1]], True)
Desert_snake = Enemy(44, 'Desert snake', "Slithers through the sand.", {'Attack': [20, ], 'Defence': [20, ],
                     'Hitpoints': [10, ], 'Magic': [1, ], 'Strength': [20, ], 'Ranged': [1, ]}, 'Melee', {}, None, 1800,
                     [[77, 0.3, 1, 1], [78, 0.2, 1, 1], [79, 0.2, 1, 1]], True)
Bandit = Enemy(45, 'Bandit', "Wants to take your money.", {'Attack': [50, ], 'Defence': [50, ],
               'Hitpoints': [50, ], 'Magic': [1, ], 'Strength': [50, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
               [[0, 0.3, 100, 200], [103, 0.15, 1, 1], [104, 0.15, 1, 1]], True)
Crocodile = Enemy(46, 'Crocodile', "In a while...", {'Attack': [53, ], 'Defence': [54, ],
                  'Hitpoints': [62, ], 'Magic': [1, ], 'Strength': [54, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                  [[0, 0.3, 80, 120], [13, 0.3, 1, 1], [15, 0.3, 1, 1]], True)
Jackal = Enemy(47, 'Jackal', "He has had his day.", {'Attack': [17, ], 'Defence': [30, ],
               'Hitpoints': [32, ], 'Magic': [1, ], 'Strength': [28, ], 'Ranged': [1, ]}, 'Melee', {}, None, 1800,
               [[0, 0.2, 20, 60], [175, 0.4, 1, 2], [116, 0.15, 1, 1], [115, 0.15, 1, 1]], True)
Vulture = Enemy(48, 'Vulture', "Run if they circle you...", {'Attack': [40, ], 'Defence': [10, ],
                'Hitpoints': [45, ], 'Magic': [1, ], 'Strength': [40, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                [[0, 0.2, 50, 160], [114, 0.15, 1, 1], [36, 0.3, 10, 50], [115, 0.2, 1, 1]], True)
Dark_wizard = Enemy(49, 'Dark wizard', "Went to the dark side.", {'Attack': [1, ], 'Defence': [10, ],
                    'Hitpoints': [35, ], 'Magic': [40, ], 'Strength': [1, ], 'Ranged': [1, ]}, 'Magic', {}, None, 2400,
                    [[203, 0.1, 1, 1], [214, 0.1, 1, 1], [213, 0.15, 1, 1], [212, 0.1, 1, 1], [211, 0.1, 1, 1],
                    [66, 0.2, 10, 50], [68, 0.15, 10, 50], [71, 0.1, 1, 15]], True)
Bear = Enemy(50, 'Bear', "Is that black or brown?", {'Attack': [30, ], 'Defence': [25, ],
             'Hitpoints': [35, ], 'Magic': [1, ], 'Strength': [29, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
             [[0, 0.3, 40, 120], [175, 0.4, 1, 1]], True, alt_drops=[[4, 4], [286, 0.5, 1, 1]])
City_guard = Enemy(51, 'City guard', "Keeps the city safe.", {'Attack': [40, ], 'Defence': [40, ],
                   'Hitpoints': [50, ], 'Magic': [1, ], 'Strength': [40, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                   [[0, 0.4, 50, 200], [258, 0.15, 1, 1]], True)
Evil_monk = Enemy(52, 'Evil monk', "Practices the dark arts.", {'Attack': [1, ], 'Defence': [40, ],
                  'Hitpoints': [40, ], 'Magic': [50, ], 'Strength': [1, ], 'Ranged': [1, ]}, 'Magic', {}, None, 2400,
                  [[203, 0.2, 1, 1], [66, 0.15, 10, 50], [67, 0.15, 10, 50], [68, 0.15, 10, 50], [69, 0.15, 10, 50],
                  [71, 0.15, 10, 50]], True, alt_drops=[[3, 1], [283, 0.25, 1, 1]])
Werewolf = Enemy(53, 'Werewolf', "Woof.", {'Attack': [60, ], 'Defence': [60, ],
                 'Hitpoints': [70, ], 'Magic': [1, ], 'Strength': [60, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                 [[0, 0.4, 140, 350], [116, 0.2, 1, 1], [119, 0.2, 1, 1], [259, 0.1, 1, 1]], True)
Spectre = Enemy(54, 'Spectre', "A smelly ghost.", {'Attack': [1, ], 'Defence': [80, ],
                'Hitpoints': [70, ], 'Magic': [80, ], 'Strength': [1, ], 'Ranged': [1, ]}, 'Magic', {}, None, 2400,
                [[0, 0.4, 200, 350], [220, 0.2, 1, 1], [221, 0.2, 1, 1], [139, 0.1, 1, 1]], True)
Afflicted_villager = Enemy(55, 'Afflicted villager', "Seems to be unwell.", {'Attack': [45, ], 'Defence': [40, ],
                           'Hitpoints': [30, ], 'Magic': [1, ], 'Strength': [30, ], 'Ranged': [1, ]}, 'Melee', {}, None,
                           2400, [[0, 0.8, 50, 200]], True)
Shade = Enemy(56, 'Shade', "Shadowy remains.", {'Attack': [1, ], 'Defence': [40, ],
              'Hitpoints': [50, ], 'Magic': [60, ], 'Strength': [40, ], 'Ranged': [1, ]}, 'Magic', {}, None, 2400,
              [[215, 0.15, 50, 200], [216, 0.15, 1, 1], [217, 0.15, 1, 1], [218, 0.15, 1, 1]], True)
Vampire = Enemy(57, 'Vampire', "A scary blood sucking monster.", {'Attack': [70, ], 'Defence': [30, ],
                'Hitpoints': [80, ], 'Magic': [1, ], 'Strength': [50, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                [[0, 0.4, 50, 400], [48, 0.2, 1, 1], [121, 0.2, 1, 1]], True)
Animated_pickaxe = Enemy(58, 'Animated pickaxe', "How does it move?", {'Attack': [40, ], 'Defence': [40, ],
                         'Hitpoints': [40, ], 'Magic': [1, ], 'Strength': [55, ], 'Ranged': [1, ]}, 'Melee', {}, None,
                         2400, [[55, 0.1, 50, 200], [54, 0.2, 1, 1], [53, 0.2, 1, 1], [52, 0.3, 1, 1]], True)
Zombie = Enemy(59, 'Zombie', "Walking rotten flesh.", {'Attack': [41, ], 'Defence': [40, ],
               'Hitpoints': [38, ], 'Magic': [1, ], 'Strength': [33, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
               [[106, 0.1, 1, 1], [47, 0.2, 1, 1], [145, 0.2, 25, 50]], True)
Tortured_soul = Enemy(60, 'Tortured soul', "A tortured soul.", {'Attack': [52, ], 'Defence': [38, ],
                      'Hitpoints': [51, ], 'Magic': [65, ], 'Strength': [1, ], 'Ranged': [1, ]}, 'Magic', {}, None,
                      2400, [[0, 0.4, 50, 200], [66, 0.2, 10, 50], [69, 0.15, 10, 50], [71, 0.1, 10, 40],
                      [70, 0.15, 50, 250]], True)
Master_wizard = Enemy(61, 'Master wizard', "A master of magic.", {'Attack': [40, ], 'Defence': [50, ],
                      'Hitpoints': [80, ], 'Magic': [70, ], 'Strength': [55, ], 'Ranged': [1, ]}, 'Magic', {}, None,
                      2400, [[206, 0.1, 1, 1], [242, 0.1, 1, 1], [215, 0.1, 1, 1], [216, 0.1, 1, 1], [217, 0.1, 1, 1],
                      [218, 0.1, 1, 1], [66, 0.2, 25, 100], [71, 0.1, 25, 50], [67, 0.1, 50, 200]], True)
Black_knight = Enemy(62, 'Black knight', "Dark-hearted.", {'Attack': [35, ], 'Defence': [35, ],
                     'Hitpoints': [42, ], 'Magic': [1, ], 'Strength': [35, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                     [[55, 0.2, 1, 1], [107, 0.2, 1, 1], [110, 0.2, 1, 1], [52, 0.2, 1, 1]], True)
Gunthor_the_brave = Enemy(63, 'Gunthor the brave', "Barbarian leader.", {'Attack': [40, ], 'Defence': [40, ],
                          'Hitpoints': [35, ], 'Magic': [1, ], 'Strength': [35, ], 'Ranged': [1, ]}, 'Melee', {}, None,
                          2400, [[257, 0.2, 1, 1], [98, 0.2, 1, 1], [92, 0.2, 1, 1], [53, 0.2, 1, 1]], True)
White_knight = Enemy(64, 'White knight', "Light-hearted.", {'Attack': [32, ], 'Defence': [30, ],
                     'Hitpoints': [55, ], 'Magic': [1, ], 'Strength': [35, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                     [[105, 0.2, 1, 1], [104, 0.2, 1, 1], [110, 0.2, 1, 1], [0, 0.3, 60, 150]], True)
Goblin_chief = Enemy(65, 'Goblin chief', "Leader of the goblins.", {'Attack': [55, ], 'Defence': [40, ],
                     'Hitpoints': [60, ], 'Magic': [50, ], 'Strength': [50, ], 'Ranged': [60, ]}, 'Ranged', {}, None,
                     2400, [[43, 0.2, 1, 1], [159, 0.3, 1, 1], [146, 0.3, 10, 100], [0, 0.2, 50, 250]], True)
Druid = Enemy(66, 'Druid', "In touch with nature.", {'Attack': [1, ], 'Defence': [32, ],
              'Hitpoints': [40, ], 'Magic': [60, ], 'Strength': [55, ], 'Ranged': [1, ]}, 'Magic', {}, None, 2400,
              [[242, 0.1, 1, 1], [66, 0.2, 25, 75], [67, 0.2, 25, 75], [68, 0.2, 25, 75], [69, 0.2, 25, 75],
              [71, 0.1, 10, 30]], True)
Soldier = Enemy(67, 'Soldier', "Loyal and brave.", {'Attack': [55, ], 'Defence': [38, ],
                'Hitpoints': [39, ], 'Magic': [1, ], 'Strength': [30, ], 'Ranged': [1, ]}, 'Melee', {}, None, 3000,
                [[258, 0.15, 1, 1], [106, 0.2, 1, 1], [109, 0.2, 1, 1], [0, 0.3, 30, 120]], True)
Troll = Enemy(68, 'Troll', "Mean and ugly.", {'Attack': [40, ], 'Defence': [40, ],
              'Hitpoints': [85, ], 'Magic': [1, ], 'Strength': [75, ], 'Ranged': [1, ]}, 'Melee', {}, None, 3600,
              [[126, 0.15, 1, 1], [125, 0.15, 1, 1], [128, 0.2, 1, 1], [0, 0.3, 50, 220]], True)
Thrower_troll = Enemy(69, 'Thrower troll', "Loves throwing rocks.", {'Attack': [55, ], 'Defence': [30, ],
                      'Hitpoints': [80, ], 'Magic': [1, ], 'Strength': [30, ], 'Ranged': [60, ]}, 'Ranged', {}, None,
                      2400, [[181, 0.15, 1, 1], [182, 0.15, 1, 1], [183, 0.15, 1, 1], [184, 0.15, 1, 1],
                      [146, 0.3, 10, 50]], True)
Frost_wolf = Enemy(70, 'Frost wolf', "Frost bites.", {'Attack': [100, ], 'Defence': [70, ],
                   'Hitpoints': [70, ], 'Magic': [1, ], 'Strength': [90, ], 'Ranged': [1, ]}, 'Melee', {}, None, 3000,
                   [[20, 0.25, 1, 3], [186, 0.2, 1, 1], [22, 0.2, 1, 2], [259, 0.15, 1, 1]], True)
Wolf = Enemy(71, 'Wolf', "The dog's scarier cousin.", {'Attack': [50, ], 'Defence': [52, ],
             'Hitpoints': [69, ], 'Magic': [1, ], 'Strength': [55, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
             [[16, 0.25, 1, 5], [18, 0.2, 1, 3], [0, 0.35, 30, 120]], True)
Ice_warrior = Enemy(72, 'Ice warrior', "Cold inside and out.", {'Attack': [47, ], 'Defence': [47, ],
                    'Hitpoints': [59, ], 'Magic': [1, ], 'Strength': [47, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                    [[116, 0.2, 1, 1], [114, 0.2, 1, 1], [115, 0.2, 1, 1], [0, 0.3, 50, 150]], True)
Cyclops = Enemy(73, 'Cyclops', "One eye, waiting to die.", {'Attack': [47, ], 'Defence': [46, ],
                'Hitpoints': [55, ], 'Magic': [1, ], 'Strength': [50, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                [[253, 0.15, 1, 1], [252, 0.25, 1, 1], [0, 0.4, 50, 120]], True)
Guard_dog = Enemy(74, 'Guard dog', "Definitely not your best friend.", {'Attack': [35, ], 'Defence': [37, ],
                  'Hitpoints': [49, ], 'Magic': [1, ], 'Strength': [36, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                  [[20, 0.25, 1, 2], [111, 0.25, 1, 1], [100, 0.2, 1, 4], [0, 0.2, 25, 100]], True)
Knight = Enemy(75, 'Knight', "Member of the militia.", {'Attack': [38, ], 'Defence': [31, ],
               'Hitpoints': [52, ], 'Magic': [1, ], 'Strength': [40, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
               [[259, 0.15, 1, 1], [117, 0.25, 1, 1], [114, 0.25, 1, 1], [0, 0.3, 60, 150]], True)
Moss_giant = Enemy(76, 'Moss giant', "I don't think he showers.", {'Attack': [30, ], 'Defence': [30, ],
                   'Hitpoints': [60, ], 'Magic': [1, ], 'Strength': [30, ], 'Ranged': [1, ]}, 'Melee', {}, None, 3000,
                   [[119, 0.2, 1, 1], [114, 0.2, 1, 1], [259, 0.2, 1, 1], [0, 0.3, 10, 190]], True)
Prison_guard = Enemy(77, 'Prison guard', "Tries to keep order.", {'Attack': [40, ], 'Defence': [45, ],
                     'Hitpoints': [40, ], 'Magic': [1, ], 'Strength': [45, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                     [[0, 0.8, 32, 125]], True)
Bouncer = Enemy(78, 'Bouncer', "Hello, nice doggy...", {'Attack': [60, ], 'Defence': [60, ],
                'Hitpoints': [90, ], 'Magic': [1, ], 'Strength': [75, ], 'Ranged': [1, ]}, 'Melee', {}, None, 3000,
                [[0, 0.9, 300, 480]], True)
Wandering_ogre = Enemy(79, 'Wandering ogre', "Looks confused.", {'Attack': [43, ], 'Defence': [43, ],
                       'Hitpoints': [60, ], 'Magic': [1, ], 'Strength': [43, ], 'Ranged': [1, ]}, 'Melee', {}, None,
                       2400, [[119, 0.2, 1, 1], [117, 0.2, 1, 1], [66, 0.1, 10, 75], [66, 0.1, 10, 75],
                              [67, 0.1, 10, 75], [68, 0.1, 10, 75], [69, 0.1, 10, 75], [71, 0.1, 10, 25]], True)
Ogre = Enemy(80, 'Ogre', "Large, dim looking humanoid.", {'Attack': [54, ], 'Defence': [54, ],
             'Hitpoints': [60, ], 'Magic': [1, ], 'Strength': [54, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
             [[122, 0.2, 1, 1], [89, 0.2, 1, 1], [100, 0.2, 1, 4], [0, 0.3, 50, 175]], True)
Gnome_warrior = Enemy(81, 'Gnome warrior', "Hero of the gnomes.", {'Attack': [35, ], 'Defence': [30, ],
                      'Hitpoints': [40, ], 'Magic': [1, ], 'Strength': [30, ], 'Ranged': [1, ]}, 'Melee', {}, None,
                      2400, [[101, 0.2, 1, 1], [105, 0.2, 1, 1], [104, 0.2, 1, 1]], True)
Khazard_trooper = Enemy(82, 'Khazard trooper', "Hates gnomes.", {'Attack': [50, ], 'Defence': [50, ],
                        'Hitpoints': [32, ], 'Magic': [1, ], 'Strength': [45, ], 'Ranged': [1, ]}, 'Melee', {}, None,
                        2400, [[108, 0.25, 1, 1], [110, 0.25, 1, 1], [0, 0.3, 10, 120]], True)
Mounted_gnome = Enemy(83, 'Mounted gnome', "Rides that thing for miles.", {'Attack': [40, ], 'Defence': [40, ],
                      'Hitpoints': [55, ], 'Magic': [1, ], 'Strength': [40, ], 'Ranged': [1, ]}, 'Ranged', {}, None,
                      2400, [[163, 0.25, 1, 1], [165, 0.2, 1, 1], [146, 0.3, 1, 50], [147, 0.3, 1, 25]], True)
Caged_ogre = Enemy(84, 'Caged ogre', "Can't touch this.", {'Attack': [46, ], 'Defence': [30, ],
                   'Hitpoints': [70, ], 'Magic': [1, ], 'Strength': [30, ], 'Ranged': [40, ]}, 'Ranged', {}, None, 2400,
                   [[-1, 1, 1, 1]], True)
Gnome_guard = Enemy(85, 'Gnome guard', "A gnome guard.", {'Attack': [30, ], 'Defence': [60, ],
                    'Hitpoints': [70, ], 'Magic': [40, ], 'Strength': [50, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                    [[0, 0.75, 100, 250]], True)
Hobgoblin = Enemy(86, 'Hobgoblin', "Ugly, smelly creature.", {'Attack': [39, ], 'Defence': [35, ],
                  'Hitpoints': [52, ], 'Magic': [1, ], 'Strength': [39, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                  [[105, 0.1, 1, 1], [94, 0.2, 1, 1], [0, 0.1, 100, 120], [66, 0.1, 10, 50],
                   [67, 0.1, 10, 50], [68, 0.1, 10, 50], [69, 0.1, 10, 50], [70, 0.1, 10, 50], [71, 0.1, 1, 25]], True)
Gnome = Enemy(87, 'Gnome', "A mini man.", {'Attack': [10, ], 'Defence': [10, ],
              'Hitpoints': [20, ], 'Magic': [1, ], 'Strength': [20, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
              [[7, 0.2, 1, 2], [27, 0.2, 1, 1], [37, 0.2, 1, 25], [0, 0.3, 10, 40]], True)
Terrorbird = Enemy(88, 'Terrorbird', "Practically jurassic.", {'Attack': [33, ], 'Defence': [28, ],
                   'Hitpoints': [37, ], 'Magic': [1, ], 'Strength': [33, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                   [[17, 0.2, 1, 2], [36, 0.2, 10, 50], [19, 0.2, 1, 2], [0, 0.3, 10, 100]], True)
Disciple = Enemy(89, 'Disciple', "Has faith in bigger things.", {'Attack': [30, ], 'Defence': [40, ],
                 'Hitpoints': [76, ], 'Magic': [80, ], 'Strength': [30, ], 'Ranged': [1, ]}, 'Magic', {}, None, 2400,
                 [[219, 0.1, 1, 1], [222, 0.1, 1, 1], [66, 0.2, 10, 75], [67, 0.1, 10, 75],
                  [68, 0.1, 10, 75], [69, 0.15, 10, 75], [70, 0.15, 10, 50], [71, 0.1, 10, 25]], True)
Lost_elf = Enemy(90, 'Lost elf', "An elf in bad health.", {'Attack': [50, ], 'Defence': [20, ],
                 'Hitpoints': [57, ], 'Magic': [1, ], 'Strength': [50, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                 [[0, 0.9, 100, 250]], True)
Grizzly_bear = Enemy(91, 'Grizzly bear', "A very big bear.", {'Attack': [40, ], 'Defence': [35, ],
                     'Hitpoints': [55, ], 'Magic': [1, ], 'Strength': [36, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                     [[175, 0.4, 1, 5], [118, 0.2, 1, 1], [0, 0.3, 10, 190]], True)
Giant_snake = Enemy(92, 'Giant snake', "Snaaaaaaaake.", {'Attack': [60, ], 'Defence': [60, ],
                    'Hitpoints': [80, ], 'Magic': [1, ], 'Strength': [60, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                    [[22, 0.2, 1, 3], [108, 0.2, 1, 1], [175, 0.3, 1, 3]], True)
Pirate = Enemy(93, 'Pirate', "Drank a bit too much.", {'Attack': [30, ], 'Defence': [30, ],
               'Hitpoints': [30, ], 'Magic': [1, ], 'Strength': [30, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
               [[0, 0.75, 40, 160]], True)
Tribesman = Enemy(94, 'Tribesman', "A primitive warrior.", {'Attack': [23, ], 'Defence': [26, ],
                  'Hitpoints': [39, ], 'Magic': [1, ], 'Strength': [33, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                  [[115, 0.2, 1, 1], [116, 0.3, 1, 1], [0, 0.4, 10, 120]], True)
Jungle_spider = Enemy(95, 'Jungle spider', "Barely visible, very deadly.", {'Attack': [35, ], 'Defence': [35, ],
                      'Hitpoints': [50, ], 'Magic': [1, ], 'Strength': [37, ], 'Ranged': [1, ]}, 'Melee', {}, None,
                      2400, [[218, 0.2, 1, 1], [215, 0.2, 1, 1], [0, 0.3, 50, 225]], True)
Jungle_wolf = Enemy(96, 'Jungle wolf', "A species thought extinct.", {'Attack': [50, ], 'Defence': [52, ],
                    'Hitpoints': [69, ], 'Magic': [1, ], 'Strength': [55, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                    [[16, 0.3, 1, 3], [20, 0.3, 1, 3], [90, 0.3, 1, 1]], True)
Jungle_bird = Enemy(97, 'Jungle bird', "Like a jungle chicken.", {'Attack': [40, ], 'Defence': [40, ],
                    'Hitpoints': [40, ], 'Magic': [1, ], 'Strength': [40, ], 'Ranged': [1, ]}, 'Melee', {}, None, 1800,
                    [[21, 0.2, 1, 4], [36, 0.4, 10, 100], [0, 0.3, 10, 190]], True)
Bush_snake = Enemy(98, 'Bush snake', "Hides in bushes.", {'Attack': [35, ], 'Defence': [50, ],
                   'Hitpoints': [44, ], 'Magic': [1, ], 'Strength': [38, ], 'Ranged': [1, ]}, 'Melee', {}, None, 1800,
                   [[47, 0.2, 1, 1], [46, 0.35, 1, 1], [0, 0.35, 25, 175]], True)
Kalphite_soldier = Enemy(99, 'Kalphite soldier', "Need a bigger shoe.", {'Attack': [70, ], 'Defence': [60, ],
                         'Hitpoints': [90, ], 'Magic': [1, ], 'Strength': [70, ], 'Ranged': [1, ]}, 'Melee', {}, None,
                         2400, [[121, 0.2, 1, 1], [115, 0.2, 1, 1], [147, 0.2, 10, 25], [66, 0.2, 25, 50],
                         [71, 0.1, 10, 40], [72, 0.1, 1, 15]], True)
Bandit_leader = Enemy(100, 'Bandit leader', "Very tough looking.", {'Attack': [35, ], 'Defence': [75, ],
                      'Hitpoints': [99, ], 'Magic': [80, ], 'Strength': [38, ], 'Ranged': [80, ]}, 'Ranged', {}, None,
                      1800, [[233, 0.1, 1, 1], [147, 0.35, 10, 50], [0, 0.3, 125, 575], [148, 0.25, 1, 40]], True)
Mummy = Enemy(101, 'Mummy', "Tightly wrapped.", {'Attack': [35, ], 'Defence': [90, ],
              'Hitpoints': [120, ], 'Magic': [99, ], 'Strength': [38, ], 'Ranged': [1, ]}, 'Magic', {}, None, 2400,
              [[263, 0.05, 1, 1], [215, 0.2, 1, 1], [216, 0.2, 1, 1], [217, 0.2, 1, 1], [218, 0.2, 1, 1],
              [206, 0.1, 1, 1], [242, 0.05, 1, 1]], True)
Giant_vulture = Enemy(102, 'Giant vulture', "A very, very large bird.", {'Attack': [75, ], 'Defence': [70, ],
                      'Hitpoints': [95, ], 'Magic': [50, ], 'Strength': [75, ], 'Ranged': [1, ]}, 'Melee', {}, None,
                      2400, [[125, 0.1, 1, 1], [126, 0.3, 1, 1], [36, 0.3, 25, 150], [0, 0.3, 125, 375]], True)
Abyssal_demon = Enemy(103, 'Abyssal demon', "Demon from the abyss.", {'Attack': [97, ], 'Defence': [90, ],
                      'Hitpoints': [120, ], 'Magic': [69, ], 'Strength': [67, ], 'Ranged': [1, ]}, 'Melee', {}, None,
                      2400, [[261, 0.1, 1, 1], [142, 0.2, 1, 1], [136, 0.2, 1, 1], [0, 0.3, 125, 475]], True)
Vampire_guard = Enemy(104, 'Vampire guard', "Protects the vampires.", {'Attack': [95, ], 'Defence': [50, ],
                      'Hitpoints': [130, ], 'Magic': [99, ], 'Strength': [7, ], 'Ranged': [95, ]}, 'Ranged', {}, None,
                      2400, [[185, 0.2, 1, 1], [186, 0.2, 1, 1], [187, 0.2, 1, 1], [188, 0.2, 1, 1],
                      [148, 0.2, 5, 50]], True)
Elder_vampire = Enemy(105, 'Elder vampire', "Bigger than the rest.", {'Attack': [120, ], 'Defence': [60, ],
                      'Hitpoints': [150, ], 'Magic': [40, ], 'Strength': [80, ], 'Ranged': [1, ]}, 'Melee', {}, None,
                      2400, [[51, 0.05, 1, 1], [140, 0.15, 1, 1], [141, 0.15, 1, 1], [142, 0.1, 1, 1],
                      [0, 0.5, 225, 775]], True)
Castle_guard = Enemy(106, 'Castle guard', "A vampire with purpose.", {'Attack': [100, ], 'Defence': [85, ],
                     'Hitpoints': [105, ], 'Magic': [1, ], 'Strength': [80, ], 'Ranged': [1, ]}, 'Melee', {}, None,
                     2400, [[229, 0.05, 1, 1], [143, 0.1, 1, 1], [140, 0.25, 1, 1], [0, 0.45, 150, 575]], True)
Vampire_wizard = Enemy(107, 'Vampire wizard', "Loves blood magic.", {'Attack': [35, ], 'Defence': [80, ],
                       'Hitpoints': [120, ], 'Magic': [120, ], 'Strength': [8, ], 'Ranged': [1, ]}, 'Magic', {}, None,
                       2400, [[234, 0.05, 1, 1], [219, 0.1, 1, 1], [221, 0.1, 1, 1], [220, 0.1, 1, 1],
                       [66, 0.2, 75, 150], [67, 0.1, 75, 150], [68, 0.1, 75, 150], [69, 0.1, 75, 150],
                       [72, 0.1, 25, 50], [222, 0.05, 1, 1]], True)
Lesser_demon = Enemy(108, 'Lesser demon', "Lesser is relative.", {'Attack': [73, ], 'Defence': [71, ],
                     'Hitpoints': [83, ], 'Magic': [1, ], 'Strength': [70, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                     [[227, 0.05, 1, 1], [128, 0.2, 1, 1], [139, 0.1, 1, 1], [0, 0.35, 125, 475]], True)
Ice_troll = Enemy(109, 'Ice troll', "Mean, cold and ugly.", {'Attack': [75, ], 'Defence': [75, ],
                  'Hitpoints': [100, ], 'Magic': [1, ], 'Strength': [90, ], 'Ranged': [1, ]}, 'Melee', {}, None,
                  3000, [[132, 0.15, 1, 1], [49, 0.15, 1, 1], [66, 0.2, 50, 100], [69, 0.2, 50, 100], [72, 0.1, 1, 50]],
                  True)
Big_wolf = Enemy(110, 'Big wolf', "Leads the pack.", {'Attack': [60, ], 'Defence': [62, ],
                 'Hitpoints': [74, ], 'Magic': [1, ], 'Strength': [61, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                 [[189, 0.15, 1, 1], [190, 0.15, 1, 1], [191, 0.15, 1, 1], [192, 0.15, 125, 475], [18, 0.25, 1, 1]],
                 True)
Large_cyclops = Enemy(111, 'Large cyclops', "A one-eyed man eater.", {'Attack': [60, ], 'Defence': [55, ],
                      'Hitpoints': [110, ], 'Magic': [1, ], 'Strength': [70, ], 'Ranged': [1, ]}, 'Melee', {}, None,
                      2400, [[255, 0.1, 1, 1], [254, 0.2, 1, 1], [0, 0.65, 125, 675]], True)
Troll_guard = Enemy(112, 'Troll guard', "Got to go through him.", {'Attack': [70, ], 'Defence': [40, ],
                    'Hitpoints': [90, ], 'Magic': [80, ], 'Strength': [75, ], 'Ranged': [80, ]}, 'Ranged', {}, None,
                    3000, [[167, 0.15, 1, 1], [169, 0.15, 1, 1], [147, 0.25, 25, 75], [148, 0.15, 1, 45],
                    [0, 0.2, 150, 550]], True)
Relleka_warrior = Enemy(113, 'Relleka warrior', "One of the town's finest.", {'Attack': [100, ], 'Defence': [60, ],
                        'Hitpoints': [100, ], 'Magic': [1, ], 'Strength': [100, ], 'Ranged': [1, ]}, 'Melee', {}, None,
                        3000, [[232, 0.1, 1, 1], [138, 0.2, 1, 1], [0, 0.55, 225, 975]], True)
Nightmare_conjurer = Enemy(114, 'Nightmare conjurer', "What nightmares are made of.", {'Attack': [73, ],
                           'Defence': [80, ], 'Hitpoints': [140, ], 'Magic': [120, ], 'Strength': [70, ],
                           'Ranged': [1, ]}, 'Magic', {}, None, 2400, [[207, 0.1, 1, 1], [244, 0.1, 1, 1],
                           [243, 0.15, 1, 1], [66, 0.1, 25, 175], [67, 0.1, 25, 175], [68, 0.1, 25, 175],
                           [69, 0.1, 25, 175], [71, 0.1, 25, 75], [72, 0.1, 25, 50], [73, 0.05, 1, 15]], True)
Dream_eater = Enemy(115, 'Dream eater', "Eater of dreams.", {'Attack': [73, ], 'Defence': [70, ],
                    'Hitpoints': [110, ], 'Magic': [99, ], 'Strength': [70, ], 'Ranged': [1, ]}, 'Magic', {}, None,
                    2400, [[223, 0.1, 1, 1], [224, 0.1, 1, 1], [225, 0.1, 1, 1], [226, 0.1, 1, 1],
                    [66, 0.1, 25, 175], [67, 0.1, 25, 175], [68, 0.1, 25, 175],
                    [69, 0.1, 25, 175], [71, 0.1, 25, 75], [72, 0.05, 25, 50], [73, 0.05, 1, 15]], True)
Paladin = Enemy(116, 'Paladin', "A holy warrior.", {'Attack': [54, ], 'Defence': [64, ],
                'Hitpoints': [82, ], 'Magic': [1, ], 'Strength': [120, ], 'Ranged': [1, ]}, 'Melee', {}, None, 3000,
                [[238, 0.1, 1, 1], [136, 0.2, 1, 1], [142, 0.2, 1, 1], [0, 0.45, 125, 875]], True)
Fire_giant = Enemy(117, 'Fire giant', "A fiery giant.", {'Attack': [65, ], 'Defence': [65, ],
                   'Hitpoints': [111, ], 'Magic': [1, ], 'Strength': [65, ], 'Ranged': [1, ]}, 'Melee', {}, None, 2400,
                   [[138, 0.1, 1, 1], [131, 0.25, 1, 1], [128, 0.15, 1, 1], [0, 0.35, 150, 475]], True)
General_khazard = Enemy(118, 'General khazard', "Looks real nasty.", {'Attack': [75, ], 'Defence': [80, ],
                        'Hitpoints': [150, ], 'Magic': [1, ], 'Strength': [78, ], 'Ranged': [1, ]}, 'Melee', {}, None,
                        2400, [[130, 0.15, 1, 1], [132, 0.25, 1, 1], [125, 0.25, 1, 1], [260, 0.25, 1, 1]], True)
Ogre_mage = Enemy(119, 'Ogre mage', "Smarter than the others.", {'Attack': [73, ], 'Defence': [70, ],
                  'Hitpoints': [75, ], 'Magic': [80, ], 'Strength': [70, ], 'Ranged': [1, ]}, 'Magic', {}, None, 3000,
                  [[206, 0.2, 1, 1], [219, 0.2, 1, 1], [220, 0.2, 1, 1], [221, 0.2, 1, 1], [222, 0.2, 1, 1]], True)
Elf_warrior = Enemy(120, 'Elf warrior', "Knows his way around a spear.", {'Attack': [95, ], 'Defence': [80, ],
                    'Hitpoints': [100, ], 'Magic': [1, ], 'Strength': [95, ], 'Ranged': [1, ]}, 'Melee', {}, None,
                    2400, [[235, 0.1, 1, 1], [137, 0.25, 1, 1], [136, 0.25, 1, 1], [261, 0.1, 1, 1], [227, 0.1, 1, 1]],
                    True)
Elven_mage = Enemy(121, 'Elven mage', "Uses long forgotten magic.", {'Attack': [73, ], 'Defence': [70, ],
                   'Hitpoints': [100, ], 'Magic': [99, ], 'Strength': [70, ], 'Ranged': [1, ]}, 'Magic', {}, None,
                   2400, [[237, 0.1, 1, 1], [220, 0.15, 1, 1], [221, 0.15, 1, 1], [66, 0.1, 25, 175],
                   [67, 0.1, 25, 175],  [68, 0.1, 25, 175], [69, 0.1, 25, 175], [71, 0.1, 25, 75], [72, 0.1, 25, 50]],
                   True)
Elven_archer = Enemy(122, 'Elven archer', "He's basically Legolas.", {'Attack': [73, ], 'Defence': [70, ],
                     'Hitpoints': [100, ], 'Magic': [70, ], 'Strength': [70, ], 'Ranged': [90, ]}, 'Ranged', {}, None,
                     2400, [[236, 0.1, 1, 1], [185, 0.2, 1, 1], [186, 0.2, 1, 1], [187, 0.2, 1, 1], [188, 0.2, 1, 1],
                     [148, 0.1, 25, 75]], True)
Elven_hunter = Enemy(123, 'Elven hunter', "Hunts bigger game than you.", {'Attack': [73, ], 'Defence': [60, ],
                     'Hitpoints': [88, ], 'Magic': [80, ], 'Strength': [70, ], 'Ranged': [70, ]}, 'Ranged', {}, None,
                     2400, [[171, 0.15, 1, 1], [173, 0.25, 1, 1], [167, 0.25, 1, 1], [148, 0.25, 25, 75]], True)
Spiritual_warrior = Enemy(124, 'Spiritual warrior', "Warrior of the gods.", {'Attack': [100, ], 'Defence': [100, ],
                          'Hitpoints': [100, ], 'Magic': [1, ], 'Strength': [100, ], 'Ranged': [70, ]}, 'Melee', {},
                          None, 2400, [[231, 0.05, 1, 1], [136, 0.25, 1, 1], [142, 0.2, 1, 1], [139, 0.35, 1, 1]], True)
Spiritual_ranger = Enemy(125, 'Spiritual ranger', "Defender of the gods.", {'Attack': [73, ], 'Defence': [80, ],
                         'Hitpoints': [100, ], 'Magic': [80, ], 'Strength': [7, ], 'Ranged': [120, ]}, 'Ranged', {},
                         None, 2400, [[249, 0.05, 1, 1], [193, 0.2, 1, 1], [194, 0.2, 1, 1], [195, 0.2, 1, 1],
                         [196, 0.2, 1, 1], [149, 0.15, 10, 50]], True)
Spiritual_mage = Enemy(126, 'Spiritual mage', "Servant of the gods.", {'Attack': [73, ], 'Defence': [60, ],
                       'Hitpoints': [75, ], 'Magic': [100, ], 'Strength': [70, ], 'Ranged': [70, ]}, 'Magic', {}, None,
                       2400, [[243, 0.1, 1, 1], [223, 0.1, 1, 1], [224, 0.1, 1, 1], [225, 0.1, 1, 1],
                       [226, 0.1, 1, 1], [66, 0.15, 50, 200], [68, 0.15, 50, 200], [72, 0.1, 20, 80],
                       [73, 0.1, 1, 20]], True)
Elvarg = Enemy(127, 'Elvarg', "A scary dragon.", {'Attack': [70, ], 'Defence': [70, ],
               'Hitpoints': [80, ], 'Magic': [1, ], 'Strength': [70, ], 'Ranged': [70, ]}, 'Melee', {}, None,
               2400, [[177, 0.35, 1, 3], [130, 0.2, 1, 1], [131, 0.2, 1, 1], [0, 0.25, 125, 475]], True)
Volcanic_creature = Enemy(128, 'Volcanic creature', "Hot and rock hard.", {'Attack': [80, ], 'Defence': [60, ],
                          'Hitpoints': [75, ], 'Magic': [80, ], 'Strength': [70, ], 'Ranged': [70, ]}, 'Melee', {},
                          None, 2400, [[260, 0.25, 1, 1], [229, 0.1, 1, 1], [143, 0.15, 1, 1], [0, 0.45, 125, 375]],
                          True)
Jungle_fisherman = Enemy(129, 'Jungle fisherman', "Loves the local fauna.", {'Attack': [70, ], 'Defence': [50, ],
                         'Hitpoints': [80, ], 'Magic': [1, ], 'Strength': [70, ], 'Ranged': [70, ]}, 'Melee', {}, None,
                         2400, [[65, 0.1, 1, 1], [64, 0.15, 1, 1], [63, 0.2, 1, 1], [62, 0.25, 1, 1], [61, 0.3, 1, 1]],
                         True)
Jungle_savage = Enemy(130, 'Jungle savage', "A not so friendly local.", {'Attack': [76, ], 'Defence': [76, ],
                      'Hitpoints': [90, ], 'Magic': [1, ], 'Strength': [76, ], 'Ranged': [70, ]}, 'Melee', {}, None,
                      2400, [[138, 0.15, 1, 1], [127, 0.25, 1, 1], [126, 0.25, 1, 1], [125, 0.25, 1, 1]], True)
Kalphite_guardian = Enemy(131, 'Kalphite guardian', "Protects the queen.", {'Attack': [90, ], 'Defence': [80, ],
                          'Hitpoints': [115, ], 'Magic': [1, ], 'Strength': [80, ], 'Ranged': [70, ]}, 'Melee', {},
                          None, 3000, [[141, 0.15, 1, 1], [130, 0.25, 1, 1], [127, 0.25, 1, 1], [0, 0.35, 225, 775]],
                          True)
Red_dragon = Enemy(132, 'Red dragon', "A very powerful dragon.", {'Attack': [90, ], 'Defence': [80, ],
                   'Hitpoints': [110, ], 'Magic': [1, ], 'Strength': [90, ], 'Ranged': [70, ]}, 'Melee', {}, None,
                   2400, [[179, 0.35, 1, 3], [142, 0.15, 1, 1], [143, 0.2, 1, 1], [0, 0.3, 225, 775]], True)
Blue_dragon = Enemy(133, 'Blue dragon', "A powerful dragon.", {'Attack': [83, ], 'Defence': [75, ],
                    'Hitpoints': [90, ], 'Magic': [1, ], 'Strength': [78, ], 'Ranged': [70, ]}, 'Melee', {}, None,
                    2400, [[178, 0.35, 1, 3], [132, 0.15, 1, 1], [131, 0.2, 1, 1], [148, 0.3, 125, 475]], True)
Vampire_lord = Enemy(134, 'Vampire lord', "Lord of the vampires.", {'Attack': [110, ], 'Defence': [110, ],
                     'Hitpoints': [180, ], 'Magic': [40, ], 'Strength': [110, ], 'Ranged': [70, ]}, 'Melee', {}, None,
                     3000, [[241, 0.05, 1, 1], [223, 0.1, 1, 1], [224, 0.1, 1, 1], [225, 0.1, 1, 1],
                     [226, 0.1, 1, 1], [66, 0.2, 100, 250], [69, 0.15, 100, 250], [72, 0.1, 100, 200],
                     [73, 0.1, 10, 100]], True)
Ancient_warrior = Enemy(135, 'Ancient warrior', "A vengeful warrior spirit.", {'Attack': [100, ], 'Defence': [100, ],
                        'Hitpoints': [100, ], 'Magic': [1, ], 'Strength': [120, ], 'Ranged': [70, ]}, 'Melee', {}, None,
                        3000, [[267, 0.05, 1, 1], [268, 0.05, 1, 1], [269, 0.05, 1, 1], [142, 0.2, 1, 1],
                        [136, 0.2, 1, 1], [261, 0.2, 1, 1], [0, 0.25, 300, 900]], True)
Ancient_mage = Enemy(136, 'Ancient mage', "A vengeful mage spirit.", {'Attack': [83, ], 'Defence': [100, ],
                     'Hitpoints': [100, ], 'Magic': [150, ], 'Strength': [78, ], 'Ranged': [70, ]}, 'Magic', {}, None,
                     3600, [[270, 0.05, 1, 1], [271, 0.05, 1, 1], [272, 0.05, 1, 1], [207, 0.1, 1, 1], [244, 0.1, 1, 1],
                     [66, 0.2, 100, 250], [69, 0.2, 100, 250], [72, 0.15, 100, 200], [73, 0.1, 10, 100]], True)
Ancient_archer = Enemy(137, 'Ancient archer', "A vengeful archer spirit.", {'Attack': [83, ], 'Defence': [100, ],
                       'Hitpoints': [100, ], 'Magic': [1, ], 'Strength': [78, ], 'Ranged': [120, ]}, 'Ranged', {}, None,
                       2400, [[264, 0.05, 1, 1], [265, 0.05, 1, 1], [266, 0.05, 1, 1], [150, 0.35, 45, 110],
                       [246, 0.15, 15, 60], [149, 0.35, 50, 150]], True)
Troll_general = Enemy(138, 'Troll general', "Leader of the trolls.", {'Attack': [70, ], 'Defence': [80, ],
                      'Hitpoints': [140, ], 'Magic': [1, ], 'Strength': [145, ], 'Ranged': [70, ]}, 'Melee', {}, None,
                      3000, [[239, 0.05, 1, 1], [142, 0.2, 1, 1], [140, 0.2, 1, 1], [141, 0.2, 1, 1],
                      [0, 0.35, 500, 1250]], True)
King_cyclops = Enemy(139, 'King cyclops', "King of the one-eyed warriors.", {'Attack': [95, ], 'Defence': [85, ],
                     'Hitpoints': [150, ], 'Magic': [1, ], 'Strength': [95, ], 'Ranged': [70, ]}, 'Melee', {}, None,
                     2400, [[256, 0.05, 1, 1], [0, 0.85, 400, 1000]], True)
Ogre_chief = Enemy(140, 'Ogre chief', "Leader of the ogres.", {'Attack': [83, ], 'Defence': [110, ],
                   'Hitpoints': [99, ], 'Magic': [1, ], 'Strength': [78, ], 'Ranged': [101, ]}, 'Ranged', {}, None,
                   2400, [[58, 0.1, 1, 1], [193, 0.15, 1, 1], [194, 0.15, 1, 1], [195, 0.15, 1, 1],
                   [196, 0.15, 1, 1], [149, 0.2, 25, 100], [150, 0.1, 10, 50]], True)
Zulrah = Enemy(141, 'Zulrah', "A giant swamp snake.", {'Attack': [83, ], 'Defence': [120, ],
               'Hitpoints': [200, ], 'Magic': [150, ], 'Strength': [78, ], 'Ranged': [150, ]}, 'Ranged', {}, None,
               2400, [[240, 0.05, 1, 1], [247, 0.1, 1, 1], [143, 0.2, 1, 1], [142, 0.2, 1, 1], [0, 0.45, 750, 3500]],
               True)
Kril_tsutaroth = Enemy(142, 'Kril Tsutaroth', "A monstrous demon.", {'Attack': [120, ], 'Defence': [150, ],
                       'Hitpoints': [200, ], 'Magic': [60, ], 'Strength': [150, ], 'Ranged': [70, ]}, 'Melee', {}, None,
                       2400, [[208, 0.05, 1, 1], [229, 0.1, 1, 1], [227, 0.2, 1, 1], [0, 0.65, 1125, 3475]], True)
General_graardor = Enemy(143, 'General Graardor', "A giant war chief.", {'Attack': [120, ], 'Defence': [150, ],
                         'Hitpoints': [200, ], 'Magic': [1, ], 'Strength': [180, ], 'Ranged': [70, ]}, 'Melee', {},
                         None, 3000, [[210, 0.05, 1, 1], [230, 0.1, 1, 1], [227, 0.2, 1, 1], [0, 0.65, 1125, 3475]],
                         True)
Commander_zilyana = Enemy(144, 'Commander Zilyana', "A magical winged beast.", {'Attack': [83, ], 'Defence': [110, ],
                          'Hitpoints': [200, ], 'Magic': [180, ], 'Strength': [78, ], 'Ranged': [70, ]}, 'Magic', {},
                          None, 2400, [[245, 0.05, 1, 1], [244, 0.1, 1, 1], [224, 0.1, 1, 1], [225, 0.1, 1, 1],
                          [226, 0.1, 1, 1], [227, 0.1, 1, 1], [66, 0.1, 250, 500], [67, 0.05, 250, 500],
                          [68, 0.05, 250, 500], [69, 0.05, 250, 500], [72, 0.1, 50, 200], [73, 0.1, 50, 100]], True)
Kree_arra = Enemy(145, "Kree'arra", "A huge bird-like creature.", {'Attack': [83, ], 'Defence': [120, ],
                  'Hitpoints': [200, ], 'Magic': [150, ], 'Strength': [78, ], 'Ranged': [180, ]}, 'Ranged', {}, None,
                  3000, [[209, 0.05, 1, 1], [197, 0.1, 1, 1], [198, 0.1, 1, 1], [199, 0.1, 1, 1], [200, 0.1, 1, 1],
                  [246, 0.2, 35, 100], [150, 0.35, 50, 200]], True)
Jad = Enemy(146, 'Jad', "Wouldn't want to get stepped on.", {'Attack': [83, ], 'Defence': [120, ],
            'Hitpoints': [180, ], 'Magic': [120, ], 'Strength': [78, ], 'Ranged': [150, ]}, 'Ranged', {}, None,
            3000, [[248, 0.15, 1, 1], [227, 0.15, 1, 1], [231, 0.15, 1, 1], [134, 0.2, 1, 4], [0, 0.35, 1500, 3000]],
            True)
Zuk = Enemy(147, 'Zuk', "An elite volcanic warrior.", {'Attack': [125, ], 'Defence': [140, ],
            'Hitpoints': [180, ], 'Magic': [1, ], 'Strength': [145, ], 'Ranged': [70, ]}, 'Melee', {}, None,
            3000, [[262, 0.1, 1, 1], [197, 0.15, 1, 1], [198, 0.15, 1, 1], [199, 0.15, 1, 1], [200, 0.15, 1, 1],
            [247, 0.1, 1, 1], [0, 0.2, 2000, 4000]], True)
Kalphite_queen = Enemy(148, 'Kalphite queen', "Largest bug you can find.", {'Attack': [100, ], 'Defence': [105, ],
                       'Hitpoints': [210, ], 'Magic': [10, ], 'Strength': [160, ], 'Ranged': [70, ]}, 'Melee', {}, None,
                       2400, [[228, 0.1, 1, 1], [136, 0.25, 1, 1], [140, 0.25, 1, 1], [142, 0.25, 1, 1],
                       [230, 0.15, 1, 1]], True)
Black_dragon = Enemy(149, 'Black dragon', "A very, very powerful dragon.", {'Attack': [110, ], 'Defence': [90, ],
                     'Hitpoints': [110, ], 'Magic': [1, ], 'Strength': [120, ], 'Ranged': [70, ]}, 'Melee', {}, None,
                     2400, [[180, 0.35, 1, 3], [229, 0.1, 1, 1], [142, 0.2, 1, 1], [200, 0.15, 1, 1],
                     [0, 0.2, 1000, 2200]], True)
Imp = Enemy(150, 'Imp', 'A mischievous little thing.', {'Attack': [5, ], 'Defence': [5, ],
            'Hitpoints': [10, ], 'Magic': [1, ], 'Strength': [10, ], 'Ranged': [1, ]}, 'Melee', {}, None,
            2400, [[0, 0.5, 10, 30]], True, alt_drops=[[3, 3], [277, 0.2, 1, 1], [278, 0.2, 1, 1], [279, 0.2, 1, 1],
                                                       [280, 0.2, 1, 1]])
Giant_bat = Enemy(151, "Giant bat", "A big flappy thing.", {'Attack': [35, ], 'Defence': [35, ],
                  'Hitpoints': [38, ], 'Magic': [1, ], 'Strength': [32, ], 'Ranged': [1, ]}, 'Melee', {}, None,
                  2400, [[0, 0.6, 25, 90]], True)

Enemies = {0: Goblin,
           1: Cow,
           2: Rat,
           3: Chicken,
           4: Man_enemy,
           5: Frog,
           6: Man,
           7: Mill_operator,
           8: Seagull,
           9: Kalphite_larva,
           10: Guard,
           11: Big_frog,
           12: Giant_rat,
           13: Al_Kharid_warrior,
           14: Scorpion,
           15: Locust,
           16: Farmer,
           17: Bat,
           18: Banshee,
           19: Swamp_snail,
           20: Young_vampire,
           21: Leech,
           22: Giant_spider,
           23: Wizard,
           24: Skeleton,
           25: Ghost,
           26: Barbarian,
           27: Monk,
           28: Dwarf,
           29: Highwayman,
           30: Mountain_goat,
           31: Young_cyclops,
           32: Mountain_camper,
           33: Unicorn,
           34: Hill_giant,
           35: Snake,
           36: Sand_crab,
           37: Monkey,
           38: Kalphite_worker,
           39: Sand_golem,
           40: Desert_wolf,
           41: Slaver,
           42: Mining_guard,
           43: Desert_lizard,
           44: Desert_snake,
           45: Bandit,
           46: Crocodile,
           47: Jackal,
           48: Vulture,
           49: Dark_wizard,
           50: Bear,
           51: City_guard,
           52: Evil_monk,
           53: Werewolf,
           54: Spectre,
           55: Afflicted_villager,
           56: Shade,
           57: Vampire,
           58: Animated_pickaxe,
           59: Zombie,
           60: Tortured_soul,
           61: Master_wizard,
           62: Black_knight,
           63: Gunthor_the_brave,
           64: White_knight,
           65: Goblin_chief,
           66: Druid,
           67: Soldier,
           68: Troll,
           69: Thrower_troll,
           70: Frost_wolf,
           71: Wolf,
           72: Ice_warrior,
           73: Cyclops,
           74: Guard_dog,
           75: Knight,
           76: Moss_giant,
           77: Prison_guard,
           78: Bouncer,
           79: Wandering_ogre,
           80: Ogre,
           81: Gnome_warrior,
           82: Khazard_trooper,
           83: Mounted_gnome,
           84: Caged_ogre,
           85: Gnome_guard,
           86: Hobgoblin,
           87: Gnome,
           88: Terrorbird,
           89: Disciple,
           90: Lost_elf,
           91: Grizzly_bear,
           92: Giant_snake,
           93: Pirate,
           94: Tribesman,
           95: Jungle_spider,
           96: Jungle_wolf,
           97: Jungle_bird,
           98: Bush_snake,
           99: Kalphite_soldier,
           100: Bandit_leader,
           101: Mummy,
           102: Giant_vulture,
           103: Abyssal_demon,
           104: Vampire_guard,
           105: Elder_vampire,
           106: Castle_guard,
           107: Vampire_wizard,
           108: Lesser_demon,
           109: Ice_troll,
           110: Big_wolf,
           111: Large_cyclops,
           112: Troll_guard,
           113: Relleka_warrior,
           114: Nightmare_conjurer,
           115: Dream_eater,
           116: Paladin,
           117: Fire_giant,
           118: General_khazard,
           119: Ogre_mage,
           120: Elf_warrior,
           121: Elven_mage,
           122: Elven_archer,
           123: Elven_hunter,
           124: Spiritual_warrior,
           125: Spiritual_ranger,
           126: Spiritual_mage,
           127: Elvarg,
           128: Volcanic_creature,
           129: Jungle_fisherman,
           130: Jungle_savage,
           131: Kalphite_guardian,
           132: Red_dragon,
           133: Blue_dragon,
           134: Vampire_lord,
           135: Ancient_warrior,
           136: Ancient_mage,
           137: Ancient_archer,
           138: Troll_general,
           139: King_cyclops,
           140: Ogre_chief,
           141: Zulrah,
           142: Kril_tsutaroth,
           143: General_graardor,
           144: Commander_zilyana,
           145: Kree_arra,
           146: Jad,
           147: Zuk,
           148: Kalphite_queen,
           149: Black_dragon,
           150: Imp,
           151: Giant_bat}
