"""Contains all the quests and their objectives that are used in the game."""

from objects import *

# The quests are built from a series of objectives
obj0 = Objective(0, 'item', "Oh dear, I really am in a bit of trouble. Would you be interested in a short quest?\nI "
                            "just need a few ingredients:\n1 Giant egg, 1 Bucket of milk, 1 Pot of flour",
                 "How goes it?\nI'm really pushing the deadlines here.", "I'll do it.", "No thanks.",
                 "I have them here!", "Still working on it.", 1, 1, itemsdict={276: 1, 2: 1, 38: 1})
obj1 = Objective(1, 'kill', "You're a hero!\nIf it isn't too much trouble, there's also a bit of a rat problem in the "
                            "kitchen.\nIf you kill 5 of them before people notice, the Duke will reward you for sure!",
                 "You've been helping the cook?\nI suppose there might be a reward here for you when you're done.",
                 "Alright.", "Ew! No way.", "All done sir!", "I'll be back.", 1, 0, enemiesdict={2: 5})
Cooks_assistant = Quest("Cooks Assistant", 0, None, None, "Cook", {0: 50}, {'Cooking': 500},
                        "Thank you so much for the help!\n I can teach you a small bit about cooking, "
                        "and please take some coins for your trouble.", obj0, obj1)

obj0 = Objective(0, 'kill', "Hey there! I'm interested in becoming an adventurer, like you. Could I watch you kill a "
                 "few goblins? 5 should be enough.", "Is that 5 goblins yet? I haven't been counting...",
                 "I'll do it.", "Not right now.",
                 "That's 5 of them.", "Still working on it.", 3, 3, enemiesdict={0: 5})
obj1 = Objective(1, 'item', "I think I'm ready to try some fighting, but I don't have any equipment. Could you grab a "
                 "few things for me?\nA Shortbow, 60 Bronze arrows and 5 cooked Shrimp should suffice.", "Do you have "
                 "the items? You can check your quest log if you forgot.", "I'll be right back.", "Maybe later.",
                 "I have them all here.", "Not quite yet.", 3, 3, itemsdict={151: 1, 144: 60, 12: 5})
obj2 = Objective(2, 'item', "Before I head off on adventures, could you buy some flowers and take them to my wife? She "
                 "lives on the western part of the island, and isn't too supportive of my choice.", "Hello there, is "
                 "there something you need?", "Alright.", "I'll consider it.", "I have a\ngift for you.", "No, sorry.",
                 3, 5, itemsdict={201: 1})
obj3 = Objective(3, 'kill', "I can't believe him. If you beat him in a fight, he might reconsider. Would you do that "
                 "for me?", "Has he changed his mind?", "I'll try.", "Sounds dangerous.", "Yep!", "Not just yet.",
                 5, 5, enemiesdict={4: 1})
Tut_quest = Quest("Tutorial", 1, None, None, "Man", None, {'Attack': 100, 'Defence': 100, 'Strength': 100,
                                                           'Ranged': 100, 'Magic': 100, 'Hitpoints': 100},
                  "Thank you kind stranger. Hopefully he will come home again soon. I'm sure you learned a small bit "
                  "about combat in the process, and I believe the boat to the mainland has arrived."
                  "\nGood luck on your travels.", obj0, obj1, obj2, obj3)

obj0 = Objective(0, '', "Hello there! I'm having a problem with a particular ghost in the church, and would be very "
                        "grateful if you could lend a hand.\nI need someone to get an amulet from my friend in the "
                        "swamps, Father Urney. Interested?", "What do you want then?", "I'll go find him.",
                 "Sorry, I'm busy.", "Father Eric sent me.", "Nothing.", 6, 43)
obj1 = Objective(1, 'item', "He wants the amulet doesn't he? I have it here. It allows a spiritual man to speak to "
                            "ghosts. You should get going, before I change my mind.", "Do you have it? This thing is "
                            "driving me insane!", "I'm on it.", "Maybe.", "Got it right here.", "Sorry, not yet.",
                 43, 6, itemsdict={281: 1}, quest_items=[281])
obj2 = Objective(2, 'item', "Okay, the ghost seems to be angry that his body's skull is missing. He saw a wizard take "
                            "it, presumably for some illegal necromancy. Try searching the wizard's tower to the west, "
                            "there may be a re-animated skeleton making use of the head. Get it back.",
                 "Got the head? I'll put it back in the coffin for you, and this ghost can rest at last.",
                 "I'll take a look.", "Sounds a bit too scary.", "Here, catch!", "I'm still looking.", 6, 6,
                 itemsdict={282: 1})
Restless_ghost = Quest("Restless ghost", 2, None, None, "Father Eric", {0: 250}, {'Hitpoints': 250},
                       "Thanks! Hopefully that's the end of the noise. Take this gold for your troubles.", obj0, obj1,
                       obj2)
obj0 = Objective(0, '', "Welcome, adventurer. You look like someone who enjoys a quest now and again. Would you do me "
                        "a favour and check on our man in the temple, to the east? He is tasked with guarding us from "
                        "the evils of the far east, but I haven't heard from Drazel for a week now.", "Pssst, I'm over "
                        "here, in the jail cell! Did the king send you?", "I do love a good quest!", "No thanks.",
                        "Yes, I'm here to help.", "No, just watching.", 23, 26)
obj1 = Objective(1, '', "These evil monks have broken into the temple and locked me up. I'm sure one of them has the "
                        "key, see if you can get it for me.", "Did you find it?", "One key coming right up...",
                        "Not my problem.", "Yep!", "Not yet.", 26, 26, itemsdict={283: 1})
obj2 = Objective(2, '', "Ahh, that's better. Unfortunately, they destroyed the holy statue protecting us from the east."
                        " I'll need some un-focused rune stones to repair it, but that kind of stuff isn't easy to "
                        "find. Could you talk to Treyborn at the wizard's tower? He's an old friend.",
                 "What brings you to the tower, stranger? I'm having a terrible day.", "I'll talk to him.",
                 "Sounds like work.", "I need some \nun-focused rune stones.", "Just browsing.", 26, 44)
obj3 = Objective(3, '', "Rune stones? I shouldn't be sharing those with a non-wizard. However, I owe Drazel a favour, "
                        "so maybe I can help you out. Some imps have stolen my magic beads, and ran off to the north. "
                        "If you can find all 4, I'll give you what you want.", "Have you found my beads?",
                 "Sounds like a deal.", "Screw your beads, old man.", "Got them right here.", "Nope.", 44, 44,
                 itemsdict={277: 1, 278: 1, 279: 1, 280: 1})
obj4 = Objective(4, '', "Alright, a deal's a deal. Take these stones, but don't give them to anyone except Drazel. "
                        "They are very powerful.", "Did he give you the stones? I'm not sure how long we have until the"
                                                   " evil starts creeping in.",
                 "Thanks!", "About time.", "He did, but it wasn't easy.", "No, still trying.", 44, 26,
                 itemsdict={284: 1}, quest_items=[284])
obj5 = Objective(5, '', "Oh good! Thank you, traveller. I'll have the statue rebuilt shortly. You can run along and "
                        "tell the king the news.", "Do you have news from the east?", "Bye!", "Later.",
                 "Drazel was in trouble,\nbut everything is alright now.", "Nothing new.", 26, 23)
Priest_in_peril = Quest('Priest in peril', 3, None, [2], "King Roald", {0: 2500},
                        {'Attack': 1000, 'Strength': 1000, 'Defence': 1000, 'Hitpoints': 1000, 'Ranged': 1000,
                         'Magic': 1000},
                        "Good work. Take some gold from my treasury. I'll also tell Drazel to allow you passage "
                        "through the temple, if you ever want to help our fight in the east.",
                        obj0, obj1, obj2, obj3, obj4, obj5)
obj0 = Objective(0, '', "Will you help me? I'm in love with a girl, Juliet, but our families forbid us from seeing "
                        "each other. I'm desperate to see her, but I'm out of ideas. Could you talk to her for me? "
                        "Maybe she has a plan.", "What are you looking at?", "Anything for love.", "Not interested.",
                 "Romeo sent me.", "You, stupid.", 22, 41)
obj1 = Objective(1, '', "Oh, Romeo. I was working on something that could get us together once and for all, "
                        "but I can't do it alone. The details are in this letter. If you show it to Romeo, he can "
                        "work out the rest. Are you up for it?", "So, did she have any ideas?",
                 "I guess I'm already helping.", "I'll consider it.", "She gave me this letter.", "I'll ask again.",
                 41, 22, itemsdict={285: 1}, quest_items=[285])
obj2 = Objective(2, '', "Oh, this is brilliant! Looks like she wants to fake her death, then I can meet her in the "
                        "crypts and we can escape together. We need some sort of way to make it believable though. "
                        "Father Lawrence is a trusted friend, could you try talking to him for me?",
                 "Welcome to the church. Do you need something in particular?", "I'll go find him.",
                 "This is getting complicated.", "Romeo needs help.", "Just praying.", 22, 111)
obj3 = Objective(3, '', "Faking her death? I heard of a special potion that could work for that purpose. The apothecary"
                        " would know more, though. Give him a visit.",
                 "I make all sorts of potions, but nobody seems to use them. Do you want one?",
                 "I'll see what he knows.", "I'm done helping.", "Yes, a very special one.", "Keep your potions.",
                 111, 42)
obj4 = Objective(4, '', "Ah, a customer! I do know how to make such a potion, but I don't keep ingredients on hand. I "
                        "need special berries, Cadava, that usually grow outside the city to the southeast. Bears tend "
                        "to steal them though, so you might need to kill a few.",
                 "Do you have them? I hope it wasn't much trouble.", "I'll be back.", "I'm not your errand boy.",
                 "Got them here.", "Working on it.", 42, 42, itemsdict={286: 1})
obj5 = Objective(5, '', "Just a mix here, a quick shake there, and... Done! One sip of this baby and she'll be out like"
                        " a light. Any local doctor will think she's dead, at least for a while. Take this to her.",
                 "Did you think of something? I can't wait much longer.", "I'll get right on it.", "About time.",
                 "Yep! This potion should work.", "No clue.", 42, 41, quest_items=[287], itemsdict={287: 1})
obj6 = Objective(6, '', "A potion? Are you sure it's safe? Whatever, I'd rather die than never see Romeo again. Tell "
                        "him to meet me in the crypts, tonight. Hopefully I'll still be breathing.",
                 "Is everything set up? I can't wait longer.", "On my way!", "Good luck.",
                 "Yes, in the crypts tonight.", "Not yet.", 41, 22)
Romeo_and_juliet = Quest('Romeo and Juliet', 4, None, None, 'Romeo', {0: 500}, None,
                         "Oh good! Here, take some gold for your troubles. I won't make you wait around for tonight. "
                         "From here on out it's just me and Juliet. Thanks so much!",
                         obj0, obj1, obj2, obj3, obj4, obj5, obj6)

Quests = {0: Cooks_assistant,
          1: Tut_quest,
          2: Restless_ghost,
          3: Priest_in_peril,
          4: Romeo_and_juliet}
