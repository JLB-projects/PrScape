# Changelog
The following is a rough list of updates in chronological order. Some things might be missed since I didn't update it too often. They start around the time the core combat system was added.

------

Swapped experience generation to after each attack to fit better with weapon and attack style switching while in combat, instead of only calculating xp on kill.\
Also reworked the combat process to account for changed attack speed and damage via weapon switching. Now checks weapon data after each attack, and can benefit from a quick to slow weapon switch for a single attack for example.

Added a bunch of new items for equipment testing.\
Added a 1hand / 2hand flag for weapons to prevent equipping shields with 2h weapons etc.\
Tested equip/inventory stuff eg. 2h weapons forces shield to be removed and prevents unequipping if full inventory.\
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
