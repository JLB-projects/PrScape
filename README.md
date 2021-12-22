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

> Skill list image while cutting a tree
 ![Skill_list](https://user-images.githubusercontent.com/96324587/147042795-df45c086-91c6-46fc-a399-a1785dd97b24.PNG)


The underlying system is the same for each of the gathering skills, and the same is true for combat. Production skills tend to be more complex in design, differing from each other in interface style and certain training options.

At its core 'skilling' is simply the process of performing an action, gaining experience in a given skill for that action, and then eventually doing this enough to reach an experience milestone corresponding to a new level. Levelling up unlocks new things to do with a skill, and may also unlock access to further areas or quests.


# Items
There are lots of different kinds of items to find. Some can be equipped for use in combat while others may be used as tools to improve gathering skills. Regardless, all items have a set of actions that can be performed related to them via options in the inventory, and can be transferred to and from the bank if desired. 

> Inventory image with options 

Items may be uniquely obtained through skills, enemies, or even bought from shops with gold in some cases. Collecting them is important to progress, like training production skills, completing quests and preparing for harder combat encounters.


# Areas
The game world is split into areas, each containing a unique combination of enemies, skill objects and NPCs. They are also themed with basic background colours to add to the experience. Each area offers a selection of facilities like a bank to store items or an anvil to smith metal.

> Example of area with bank, anvil, a few neighbours, transport option 

Navigating between areas is simple: there are up to four directionally labeled buttons placed on appropriate sides of the window when a neighbouring area exists. In some areas there is an alternative way to travel, and an extra button will appear offering access to a non-neighbouring area. This form of transport may require certain items or payment to use.


# Combat
Each area may contain a few types of enemy to fight. Combat allows you to level combat skills and often find valuable items as a reward. The world provides a wide range of enemy difficulties to give a sense of progression, with areas generally increasing in difficulty as you move further from the starting location. It is key to note that most high end combat equipment is uniquely obtained through difficult enemy encounters.

> Combat in progress showing enemy information 


# NPCs + Quests
NPCs = Non-player characters. These exist for you to talk to, trade with and complete quests. NPC owned shops allow you to access important items easily and obtain early upgrades much faster than production skills would allow, in exchange for gold. 

> Image of NPC conversation talking about a quest 

Quests, while limited in scope, provide something to do as a break from training skills. For example, an NPC might ask you to kill a certain enemy or obtain a special item for them. After completing a series of these tasks, a reward is given which may include items, skill experience or access to a new area.


# Tutorial

> Register / Login screen 

Upon starting the game, a choice is given to register or login. If registration is chosen, then after entering a name and password the tutorial will begin. 

> Tutorial video 

The tutorial explains every major aspect of the game, walking through an example of each activity. Interface elements are introduced slowly to avoid overburdening a new user. The tutorial builds up to a point where the user is given a basic quest to complete by themselves, encompassing most of the content, which unlocks the main game upon completion.


# Changelog
Rough list of major changes in chronological order, but no timestamps saved:

