# Project: Scape
Project: Scape. A minimalistic take on the classic version of popular game Runescape.

Primarily intended as a learning experience, I tried to avoid using major packages and especially game related ones that would trivialise the work needed. Since I don't plan on working with games much in the future, anything I learn about those specific packages would be useless. Instead I decided to build my own basic systems from the ground up, even if they aren't the best possible implementations, just to get a better feel for what is possible and efficient with basic python. 

The largest package that is heavily used is Tkinter. While originally envisioned as a text/console based project, I quickly decided it would be more realistic to have at least a basic GUI in 2021. In addition, many core modules like time, random and threading were used out of necessity.

Again, due to the nature of the project, the quality of code throughout will vary depending on the time at which it was written. While I could go back and change a lot of the early design choices, it would take too much time for little gain compared to moving on to something new. In a similar vein the formatting of the code may not be perfectly in line with common standards, since I just relied on Pycharm warnings and recommendations throughout most of the process before discovering that this does not match the guidelines in their entirety.

The structure of the project allows me to easily add more in future if I want to test out something new or while learning more advanced methods. For example, I only added the account system late in development to play around with SQLite, and it wasn't too difficult to get things working again. 

As a final note before moving on to the actual gameplay: the world building was based heavily on the original Runescape to save time, but with some changes where I felt they were needed or interesting. The game's core mechanics (like how skills are trained) were intended to follow the source material where possible, but obviously being made from scratch due to the very different style of gameplay, and with some creative liberties at times. The main benefit of this approach was the existence of clear goals, since I am very goal-oriented and this gave me a large list of mini projects to work through from the beginning.


# User Experience / How to play
Interaction with the game is done entirely through button presses which are presented to the user depending on their current progress and activity. Feedback is given in the form of an in-game text console primarily, but interface elements like labels, buttons or other text containers provide information and keep track of the user's data.

The behaviour of certain buttons may also change as the user progresses, switches activities or selects an option through a different button.

There is potential for more precise control of certain things via text input in future. 


# Game Overview 
- 14 Skills to train
- 150+ Unique enemies to fight
- 100+ NPCs to interact with, including multiple quests to complete
- 250+ Items to collect 

All of which is spread over more than 150 areas ready to be explored. 

Try playing in different ways from the start by taking advantage of the multi-account support and creating many new characters. 

Jump straight into an in-depth tutorial which will get you up to speed, or brave the unknown with the option to skip it entirely (coming soon™).


# Skills
Skills can be split into 3 main categories: Combat, Gathering, and Production. The skills within each category are generally trained in a similar fashion. Combat skills require you to kill things, with the specific skill depending on weapon and style choices. Gathering skills are trained by collecting raw resources from trees, rocks or fishing. Production skills generally process the items gained from gathering, or otherwise obtained from shops or combat, and create new potentially useful items.

| ![Skill_list](https://user-images.githubusercontent.com/96324587/147042795-df45c086-91c6-46fc-a399-a1785dd97b24.PNG) | 
|:--:| 
| *Cutting a tree while viewing the skills tab.* |

The underlying system is the same for each of the gathering skills, and the same is true for combat. Production skills tend to be more complex in design, differing from each other in interface style and certain training options.

At its core 'skilling' is simply the process of performing an action, gaining experience in a given skill for that action, and then eventually doing this enough to reach an experience milestone corresponding to a new level. Levelling up unlocks new things to do with a skill, and may also unlock access to further areas or quests.


# Items
There are lots of different kinds of items to find. Some can be equipped for use in combat while others may be used as tools to improve gathering skills. Regardless, all items have a set of actions that can be performed related to them via options in the inventory, and can be transferred to and from the bank if desired. 

| ![Inv_example](https://user-images.githubusercontent.com/96324587/147043322-c72f4b8b-505e-4b9f-a3e9-b92aeb24c08f.PNG) | 
|:--:| 
| *Looking at the inventory with logs selected.* |

Items may be uniquely obtained through skills, enemies, or even bought from shops with gold in some cases. Collecting them is important to progress, like training production skills, completing quests and preparing for harder combat encounters.


# Areas
The game world is split into areas, each containing a unique combination of enemies, skilling locations and NPCs. They are also themed with basic background colours to add to the experience. Each area offers a selection of facilities like a bank to store items or an anvil to smith metal.

| ![Area_example](https://user-images.githubusercontent.com/96324587/147043601-585fe28f-d7e5-4b11-bc28-ea1c35f84553.PNG) | 
|:--:| 
| *Trying to smith inside a city with an anvil, bank, and cooking range.* |

Navigating between areas is simple: there are up to four directionally labeled buttons placed on appropriate sides of the window when a neighbouring area exists. In some areas there is an alternative way to travel, and an extra button will appear offering access to a non-neighbouring area. This form of transport may require certain items or payment to use.


# Combat
Each area may contain a few types of enemy to fight. Combat allows you to level combat skills and often find valuable items as a reward. The world provides a wide range of enemy difficulties to give a sense of progression, with areas generally increasing in difficulty as you move further from the starting location. It is key to note that most high end combat equipment is uniquely obtained through difficult enemy encounters.


| ![Combat_example](https://user-images.githubusercontent.com/96324587/147045032-1656c3c3-2a87-494c-b178-7399f6478ed7.PNG) | 
|:--:| 
| *Fighting a Scorpion with a melee weapon.* |

# NPCs + Quests
NPCs = Non-player characters. These exist for you to talk to, trade with and complete quests. NPC owned shops allow you to access important items easily and obtain early upgrades much faster than production skills would allow, in exchange for gold. 

| ![NPC_quest](https://user-images.githubusercontent.com/96324587/147043909-77c7b290-375d-4abc-8357-9b9d92f8b46d.PNG) | 
|:--:| 
| *Talking to an NPC about a quest.* |

Quests, while limited in scope, provide something to do as a break from training skills. For example, an NPC might ask you to kill a certain enemy or obtain a special item for them. After completing a series of these tasks, a reward is given which may include items, skill experience or access to a new area.


# Tutorial
Upon starting the game, a choice is given to register or login. If registration is chosen, then after entering a name and password the tutorial will begin. 

| [<img src="https://user-images.githubusercontent.com/96324587/147043985-11039c54-05df-4a4a-bab8-090c05da05f7.PNG" width="100%">](https://youtu.be/le1BLLInPfU) | 
|:--:| 
| *A sample play-through video of the tutorial. (Click to play)* |

The tutorial explains every major aspect of the game, walking through an example of each activity. Interface elements are introduced slowly to avoid overburdening a new user. The tutorial builds up to a point where the user is given a basic quest to complete by themselves, encompassing most of the content, which unlocks the main game upon completion.


# Changelog
The following is a rough list of updates in chronological order, but unfortunately timestamps were not saved. They start around the time the core combat system was added.

------

Swapped experience generation to after each attack to fit better with weapon and attack style switching while in combat, instead of only calculating xp on kill. 
Also reworked the combat process to account for changed attack speed and damage via weapon switching. Checks after each attack, can benefit from a quick to slow weapon switch for a single attack for example.

Added a bunch of new items for equipment testing. 
Added a 1hand / 2hand flag for weapons to prevent equipping shields with 2h weapons etc.
Tested equip/inventory stuff eg. 2h weapons forces shield to be removed and prevents unequipping if full inventory.
Added total equipment stats to equipment interface.

Completely changed inventory algorithm: now moves each item over by one slot after removing an item to fill the space.
Added functionality to keep inventory visible while restarting combat or skills multiple times for convenience.

Reworked combat formulas.
Added skilling success formulas, skilling tools that improve these chances and added inventory checks before skilling to find highest tier tool.
Added Progress bar for skilling.

Added bank, using inventory objects as tabs to create 4 total bank tabs.
Bank replaces most of the top console with the bank interface and adds quantity buttons for 1, 5, 10, 50, ALL.

Added skills interface, which displays current skill levels and updates whenever they gain experience.
Added trade button to npc interface when selecting a shop NPC, which allows user to open the shop interface.

In bank interface: inventory item behaviour changed to deposit on left click without showing the usual options. 
Blocked bank opening while doing something since it changes the interface drastically. Inventory is now forced open during banking. 
Added bank specific add_to_inv functions and similar, allowing stacking of all items automatically.
Added shop, similar to bank: shows an inventory style ui, but without all 28 slots if not in use. Uses same quantity selectors as bank and shows prices on the item buttons. 
Added deposit/sell all button, and last selected quantity is now saved until logout for bank and shop.

Designed magic combat using runes and requiring a staff to cast spells. User's weapon now easily determines combat style.
Updated attack function with correct rune usage and such.
Added Spellbook tab to the interface, showing available combat and non-combat spells with level requirements and rune costs.
Added runes to the current test shop so they can now be purchased.

Added way to cook food, either by lighting a fire first or visiting an area containing a cooking range.
Added way to select food in inventory as primary. Eat button will consume the selected food when pressed.

Swapped some manual item removals for the new user.inventory.remove_item() method.
Top left part of interface now has furnace/anvil/range buttons etc in preparation for production skills. 

Made furnace/anvil area specific rather than always available.
Area buttons now only show up if there is a neighbouring area in the relevant direction.
Created setup_area: sets up the interface to show only buttons that are relevant to current area.
Added command to direction buttons to call swap_area when one exists.
Changed direction button commands so they can now only be used when idle.

Reworked eating to work directly from inventory rather than selecting food and then pressing a separate eat button.

Added smithing, consisting of separate smelting and smithing processes with unique interfaces. 
Added hammer requirement to smithing (not the smelting portion).

Added fletching with various bows, arrows etc. Requires a knife for certain actions.
Changed bowstrings to be stackable for ease of use.
Added knife/hammer/bowstring etc to basic shop so skills can be trained properly without relying on monster drops immediately.
Now shows selected inventory item above the item's options. 
Now auto-selects next copy of same item after drop/burn to allow smooth multi-drop/burn without repeatedly selecting the item.

Added system for basic quests: simple dialogue with npcs, checks for items in inventory on completion, tracks monster kills, requires certain skill levels to start/finish a quest, provides rewards.

Added natural HP-regen over time for QOL.
Split up npcs, enemies etc into their own files to import for cleaner main file, before mass producing more of each type of object.

Finished area_setup, can now be used with direction buttons, after logging in / tutorial, and more. 

Added a tutorial which slowly introduces basic features, runs through an example of each skill and combat style, and then guides the user through a basic quest.

Fixed a lot of shop bugs such as the selected item not being cleared after a sale in certain situations. This led to infinite gold.
Added daemon flag to ALL threads so there are never any errors of this type on closing. Checked each thread to make sure this doesn't break anything. 

Fully tested tutorial and the new checkpoint system. Rebalanced goblins since they were too challenging for a tutorial enemy. Possibly need to nerf final boss "Man".
Fixed console having an inconsistent scroll position on bank/shop opening.

Added minor death mechanic: teleports user to spawnpoint on death, may change later to something more meaningful.

Added primitive save/load features with text file reading/writing.
Changed save/load methods for custom objects so that they export as a string that can be used to reconstruct them, eg. the inventory saves as Inventory([0, 1], ... ).
Set up register / login interfaces, with fully functional account creation/login leading into the tutorial / current area.

Added skilling nodes corresponding to each resource that is used in current skills.
Added equipment stats for smithed items, bows, arrows, weapons/armour.
Added new tier-60 weapons/armour for each style, and 4 total tiers of magic armour since it didn't have any before.
Added rune preservation effect to magic staves, scaling with 50% of weapon tier.
Added 80% arrow preservation to Cape of arrows, the best-in-slot ranged cape.
Added rings, amulets, gloves, capes, and shields for each style.

Created a "World map" externally to plan areas and their connectivity to each other.
Added to map: Dungeons/islands: God wars, Dwarven mine, Zulrah island, Wizard guild, Karamja, Crandor, Troll stronghold. These are only accessible via a new transport option that allows travel to specific non-neighbouring areas.

Added lots of new enemies and NPCS.
Added relevant shops to NPC list.

Added clarity to areas that do not contain any enemies, NPCs or skill locations via a message.
Added combat style, combat level and more info to enemy details interface.
Changed enemy specific damage formulas since they don't have weapons/spells/armour like the player.
Added ability for NPCS to give quest items mid-quest, that may be required for later objectives in the same quest. Deletes them on quest completion. Prevents dropping them if they are a non-standard item that would be irretrievable. 

Added "alt_drop_table" to some monsters to drop different items only during quests. Dropped item will usually be a quest_item as above.
Added functionality to add/remove NPCs and enemies from a certain area dependent on user's quest progress. For example, completing "Romeo and juliet" will "kill" juliet, removing her from her area and hence the game. A certain quest may also unlock a new enemy.

Added 3 basic quests.
Added all areas with their standard contents.
Added neighbours to each area, finally allowing navigation through the game world.
Added transport options with requirements to all relevant areas, like dungeons and islands.

Added some console messages on quest completion, detailing the rewards.
Fixed some bad combat formulas, may still need some perfecting in future.
Fixed bug where having no quests started allowed user to bypass all quest requirements.

Changed the magic teleport spells to work with the new areas, adjusted level requirements, added non-magic skill and quest requirements.
Added a way to check quest requirements: Upon talking to quest giver of an unavailable quest, gives current dialogue but also details the missing requirements in console. 
Made some minor changes to text sizes to fit buttons better in extreme situations.

Added a list of colours for backgrounds dependent on current area type: sandy for desert areas, dark green for swamps, blood red for vampire area, brown underground, grey mountains, and green for normal outdoor areas.
Fixed some interface size / text problems with quests. 
Standardised the font size for some commonly used interfaces.

Added aforementioned area based background colours to every single area.
Added examine texts for all items.
