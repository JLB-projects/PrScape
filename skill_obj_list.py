"""Contains all the skill objects that are placed in various areas."""

from objects import *

# Object = SkillObj(name, skill, req, xp, rate_1, rate_99, depletion_chance, resources, tool)
Tree = SkillObj("Tree", "Woodcutting", 1, 25, 65, 200, 0.125, 3, 'Axe')
Oak_tree = SkillObj("Oak tree", "Woodcutting", 15, 40, 33, 100, 0.125, 4, 'Axe')
Willow_tree = SkillObj("Willow tree", "Woodcutting", 30, 70, 15, 51, 0.125, 5, 'Axe')
Teak_tree = SkillObj("Teak tree", "Woodcutting", 35, 90, 14, 47, 0.125, 6, 'Axe')
Maple_tree = SkillObj("Maple tree", "Woodcutting", 45, 110, 8, 26, 0.125, 7, 'Axe')
Mahogany_tree = SkillObj("Mahogany tree", "Woodcutting", 50, 140, 8, 25, 0.125, 8, 'Axe')
Yew_tree = SkillObj("Yew tree", "Woodcutting", 60, 200, 0, 15, 0.125, 9, 'Axe')
Magic_tree = SkillObj("Magic tree", "Woodcutting", 75, 300, -10, 8, 0.125, 10, 'Axe')

Copper_rock = SkillObj("Copper rock", "Mining", 1, 30, 65, 200, 0.5, 77, 'Pickaxe')
Tin_rock = SkillObj("Tin rock", "Mining", 1, 30, 65, 200, 0.5, 78, 'Pickaxe')
Iron_rock = SkillObj("Iron rock", "Mining", 15, 50, 33, 100, 0.5, 89, 'Pickaxe')
Coal_rock = SkillObj("Coal rock", "Mining", 30, 60, 15, 51, 0.5, 100, 'Pickaxe')
Mithril_rock = SkillObj("Mithril rock", "Mining", 45, 100, 8, 26, 0.5, 111, 'Pickaxe')
Adamant_rock = SkillObj("Adamant rock", "Mining", 60, 150, 0, 15, 0.5, 122, 'Pickaxe')
Runite_rock = SkillObj("Runite rock", "Mining", 75, 200, -10, 8, 0.5, 133, 'Pickaxe')

Shrimp = SkillObj("Shrimp", "Fishing", 1, 15, 50, 80, 0.1, 11, 'Fishing net/rod')
Herring = SkillObj("Herring", "Fishing", 5, 30, 30, 70, 0.1, 13, 'Fishing net/rod')
Trout = SkillObj("Trout", "Fishing", 20, 45, 30, 55, 0.1, 15, 'Fishing net/rod')
Salmon = SkillObj("Salmon", "Fishing", 30, 60, 15, 50, 0.1, 17, 'Fishing net/rod')
Lobster = SkillObj("Lobster", "Fishing", 40, 90, 5, 30, 0.1, 19, 'Fishing net/rod')
Swordfish = SkillObj("Swordfish", "Fishing", 50, 120, 5, 25, 0.1, 21, 'Fishing net/rod')
Shark = SkillObj("Shark", "Fishing", 70, 180, 0, 15, 0.1, 23, 'Fishing net/rod')
Manta_ray = SkillObj("Manta ray", "Fishing", 85, 225, -5, 10, 0.1, 25, 'Fishing net/rod')


Skill_objects = {0: Tree,
                 1: Oak_tree,
                 2: Willow_tree,
                 3: Teak_tree,
                 4: Maple_tree,
                 5: Mahogany_tree,
                 6: Yew_tree,
                 7: Magic_tree,
                 8: Copper_rock,
                 9: Tin_rock,
                 10: Iron_rock,
                 11: Coal_rock,
                 12: Mithril_rock,
                 13: Adamant_rock,
                 14: Runite_rock,
                 15: Shrimp,
                 16: Herring,
                 17: Trout,
                 18: Salmon,
                 19: Lobster,
                 20: Swordfish,
                 21: Shark,
                 22: Manta_ray}
