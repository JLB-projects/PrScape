# Project: Scape
Project: Scape. A minimalistic take on the classic version of popular game Runescape.

Primarily intended as a learning experience, I tried to avoid using any major packages and especially game related ones that would trivialise the work needed. Since I don't plan on working with games much in the future, anything I learn about those specific packages would be wasted. Instead I decided to build my own basic systems from the ground up, even if they aren't the best possible implementations, just to get a better feel for what is possible and efficient with basic python. 

The largest package that is heavily used is Tkinter. While originally envisioned as a text/console based project, I quickly decided it would be more realistic to have at least a basic GUI in 2021. In addition, many core modules like time, random and threading were used out of necessity.

Again, due to the nature of the project, the quality of code throughout will vary depending on the time at which it was written. While I could go back and change a lot of the early design choices, it would take too much time for little gain compared to moving on to something new. In a similar vein the formatting of the code may not be perfectly in line with common standards since I just relied on Pycharm warnings and recommendations throughout most of the process, before discovering that this does not match the guidelines in their entirety.

The structure of the project allows me to easily add more in future if I want to test out something new or while learning more advanced methods. For example, I only added the account system late in development to play around with SQLite, and it wasn't too difficult to get things working again. As a result you can now use multiple password protected accounts even though they are being stored locally, due to (hopefully) proper treatment of the passwords.

As a final note before moving on to the actual gameplay: the world building was based heavily on the original Runescape to save time, but with some changes where I felt they were needed or interesting. The game's core mechanics (like how skills are trained) were intended to follow the source material where possible, but obviously being made from scratch due to the very different style of gameplay, and with some creative liberties at times. The main benefit of this approach was the existence of clear goals, since I am very goal-oriented and this gave me a large list of mini projects to work through from the beginning.


# Game Overview 
- 14 Skills to train
- 150+ Unique enemies to fight
- 100+ NPCs to interact with, including multiple quests to complete
- 250+ Items to collect 

All of which is spread over more than 150 areas ready to be explored. 

Try playing in different ways from the start by taking advantage of the multi-account support and creating many new characters. 

Jump straight into an in-depth tutorial which will get you up to speed, or brave the unknown with the option to skip it entirely (coming soon™).


# User Experience / How to play
Interaction with the game is done entirely through button presses which are presented to the user depending on their current progress and activity. Feedback is given in the form of an in-game text console primarily, but interface elements like labels, buttons or other text containers provide information and keep track of the user's data.

The behaviour of certain buttons may also change as the user progresses, switches activities or selects an option through a different button.

There is potential for more precise control of certain things via text input in future. 


# Skills
Skills can be split into 3 main categories: Combat, Gathering, and Production. The skills within each category are generally trained in a similar fashion. Combat skills require you to kill things, with the specific skill depending on weapon and style choices. Gathering skills are trained by collecting raw resources from trees, rocks or fishing. Production skills generally process the items gained from gathering, or otherwise obtained from shops or combat, and create new potentially useful items.

The underlying system is the same for each of the gathering skills, and the same is true for combat. Production skills tend to be more complex in design, differing from each other in interface style and certain training options.

At its core 'skilling' is simply the process of performing an action, gaining experience in a given skill for that action, and then eventually doing this enough to reach an experience milestone corresponding to a new level. Levelling up unlocks new things to do with a skill, and may also unlock access to further areas or quests.


# Items
TBC

