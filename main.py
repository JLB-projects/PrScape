"""The main file. Contains the tkinter window class and all of the core functions that are used during runtime.
Starts the game when it is run."""

from tkinter import *
import _tkinter
from tkinter.ttk import Progressbar
import time
import sqlite3 as sql
from hashlib import pbkdf2_hmac
from os import urandom
from threading import Thread, Lock
# from threading import enumerate as thread_enumerate       # (for debugging threads)

from quest_list import *
from area_list import *


# Easy way to globally change base xp rates
global_xp_multiplier = 1

# Initial values to make things work before loading a profile
inv = Inventory([31, 1], [32, 1], [33, 1], [34, 1], [35, 1], [36, 100], [37, 100], [38, 1], [39, 1], [40, 1], [41, 1],
                [42, 1], [43, 1], [44, 1], [1, 1], [29, 1], [30, 100], [1, 1], [45, 1], [52, 1], [59, 1], [0, 10000],
                [67, 10], [70, 10], [76, 1], [80, 100], [27, 1], [102, 100])
banktest1 = Inventory([0, 1], [1, 1], [2, 1], [3, 10], [4, 10], [5, 10], [6, 10], [7, 10], [8, 10], [9, 10], [10, 10],
                      [11, 1], [12, 1], [13, 1], [14, 1], [15, 1], [16, 1], [17, 1], [18, 1], [19, 1], [20, 1],
                      [21, 1], [22, 1], [23, 1], [77, 3], [78, 2], [79, 10], [39, 1])
banktest2 = Inventory([175, 10], [176, 10], [177, 10], [174, 100], [45, 1], [52, 1], [59, 1])
bank_tut = Inventory([0, 100], [42, 1], [45, 1], [52, 1], [59, 1], [27, 1], [28, 1], [39, 1])

user = Player('', {'Attack': [1, 0], 'Cooking': [1, 0], 'Crafting': [1, 0], 'Defence':  [1, 0],
                   'Firemaking': [1, 0], 'Fishing': [1, 0], 'Fletching': [1, 0], 'Hitpoints': [10, 1154],
                   'Magic': [1, 0], 'Mining': [1, 0], 'Ranged': [1, 0], 'Smithing': [1, 0], 'Strength': [1, 0],
                   'Woodcutting': [1, 0]}, {'DEFAULT': 0}, inv, Bank(tab_1=banktest1, tab_2=banktest2),
              Lum, 'idle', [], 0, 0, "Accurate", {})

tut_inv = Inventory([0, 25], [66, 10], [37, 5], [12, 1], [12, 1])

text_lock = Lock()
fletch_list = [0] * 6
smith_list = [0] * 9
cook_list = [0] * 10
craft_list = [0] * 4
running = True
flashing = False
fire_timer = 0


# The class containing every UI element
class MyWindow:
    """The main window that contains all the interfaces used during the game."""
    def __init__(self, win):
        tabvar = IntVar(win, value=100)
        quantvar = IntVar(win, value=200)
        spellvar = IntVar(win, value=300)
        spellvar2 = IntVar(win, value=400)
        cookvar = IntVar(win, value=500)
        smeltvar = IntVar(win, value=600)
        smith_tabvar = IntVar(win, value=700)
        smithvar = IntVar(win, value=800)
        fletchvar = IntVar(win, value=900)
        craftvar = IntVar(win, value=1000)
        self.north_btn = Button(win, text="North", command=lambda: swap_area(0), font=('Helvetica bold', 16), bg="grey")
        self.east_btn = Button(win, text="East", command=lambda: swap_area(1), font=('Helvetica bold', 16), bg="grey")
        self.south_btn = Button(win, text="South", command=lambda: swap_area(2), font=('Helvetica bold', 16), bg="grey")
        self.west_btn = Button(win, text="West", command=lambda: swap_area(3), font=('Helvetica bold', 16), bg="grey")
        self.register_btn = Button(win, text="Create new account", command=register, font=('Helvetica bold', 16), 
                                   bg="grey")
        self.login_btn = Button(win, text="Login", command=login, font=('Helvetica bold', 16), bg="grey")
        self.reg_user = Entry(bd=5, font=('Helvetica bold', 16), fg='black')
        self.reg_pass = Entry(bd=5, font=('Helvetica bold', 16), show='*', fg='black')
        self.reg_pass2 = Entry(bd=5, font=('Helvetica bold', 16), show='*', fg='black')
        self.reg_user_lbl = Label(win, text="Choose a username:", bg='#4f0781', fg='white',
                                  font=('Helvetica bold', 20))
        self.reg_pass_lbl = Label(win, text="Choose a password:", bg='#4f0781', fg='white',
                                  font=('Helvetica bold', 20))
        self.reg_pass2_lbl = Label(win, text="Confirm your password:", bg='#4f0781', fg='white',
                                   font=('Helvetica bold', 20))
        self.reg_warning_lbl = Label(win, text="Passwords don't match!", bg='#4f0781', fg='red',
                                     font=('Helvetica bold', 20))
        self.submit_btn = Button(win, text="Submit", command=submit, font=('Helvetica bold', 16), bg="grey")
        self.pass_toggle = Button(win, text="Show password", command=self.toggle_pass, font=('Helvetica bold', 16),
                                  bg="grey")
        self.log_user_lbl = Label(win, text="Enter username:", bg='#4f0781', fg='white', font=('Helvetica bold', 20))
        self.log_pass_lbl = Label(win, text="Enter password:", bg='#4f0781', fg='white', font=('Helvetica bold', 20))
        self.log_user = Entry(bd=5, font=('Helvetica bold', 16), fg='black')
        self.log_pass = Entry(bd=5, font=('Helvetica bold', 16), show='*', fg='black')
        self.back_btn = Button(win, text="Back", command=startup, font=('Helvetica bold', 16), bg="grey")
        self.main_console = Text(win, bd=5, font=('Helvetica bold', 16), fg='white', bg='black', state=DISABLED,
                                 selectbackground='black', wrap='word')
        self.main_input = Entry(bd=5, font=('Helvetica bold', 16), fg='white', bg='black', selectbackground='black')
        self.list_enemies = Button(win, text="Enemies", command=list_enemies,
                                   font=('Helvetica bold', 16), bg="grey")
        self.list_skill_obj = Button(win, text="Skilling locations", command=list_skill_obj,
                                     font=('Helvetica bold', 16), bg="grey")
        self.list_npcs = Button(win, text="Npcs", command=list_npcs,
                                font=('Helvetica bold', 16), bg="grey")
        self.list_skills = Button(win, text="Skills", command=list_skills, font=('Helvetica bold', 16), bg="grey")
        self.list_backpack = Button(win, text="Inventory", command=list_inv, font=('Helvetica bold', 16), bg="grey")
        self.equipment = Button(win, text="Equipment", command=list_equipment, font=('Helvetica bold', 16), bg="grey")
        self.list_bank = Button(win, text="Bank", command=open_bank,
                                font=('Helvetica bold', 16), bg="grey")
        self.enemy_list1 = Radiobutton(win, text=user.curr_area.enemies[0].name, indicatoron=0, command=lambda:
                                       select(0, "enemy"), font=('Helvetica bold', 12), bg='grey', value=1)
        self.enemy_list2 = Radiobutton(win, text=user.curr_area.enemies[1].name, indicatoron=0, command=lambda:
                                       select(1, "enemy"), bg='grey', font=('Helvetica bold', 12), value=2)
        self.enemy_list3 = Radiobutton(win, text=user.curr_area.enemies[2].name, indicatoron=0, command=lambda:
                                       select(2, "enemy"), bg='grey', font=('Helvetica bold', 12), value=3)
        self.enemy_list4 = Radiobutton(win, text=user.curr_area.enemies[3].name, indicatoron=0, command=lambda:
                                       select(3, "enemy"), bg='grey', font=('Helvetica bold', 12), value=4)
        self.enemy1_lbl = Label(win, text=f"Hp:{user.curr_area.enemies[0].skills.get('Hitpoints', [1])[0]},   Max hit: "
                                          f"{max_hit(user.curr_area.enemies[0])}",
                                bg='grey', font=('Helvetica bold', 12))
        self.enemy2_lbl = Label(win, text=f"Hp:{user.curr_area.enemies[1].skills.get('Hitpoints', [1])[0]},   Max hit: "
                                          f"{max_hit(user.curr_area.enemies[1])}", bg='grey',
                                font=('Helvetica bold', 12))
        self.enemy3_lbl = Label(win, text=f"Hp:{user.curr_area.enemies[2].skills.get('Hitpoints', [1])[0]},   Max hit: "
                                          f"{max_hit(user.curr_area.enemies[2])}", bg='grey',
                                font=('Helvetica bold', 12))
        self.enemy4_lbl = Label(win, text=f"Hp:{user.curr_area.enemies[3].skills.get('Hitpoints', [1])[0]},   Max hit: "
                                          f"{max_hit(user.curr_area.enemies[3])}", bg='grey',
                                font=('Helvetica bold', 12))
        self.enemy_fight = Button(win, text="Fight!", command=lambda:
                                            combat_thread(user.curr_area.enemies[user.curr_area.selection]),
                                  font=('Helvetica bold', 16), bg="grey")
        self.eat = Button(win, text="Eat", command=lambda: eat(user.inventory.curr_selection),
                          font=('Helvetica bold', 16), bg="grey")
        self.flee = Button(win, text="Flee", command=flee, font=('Helvetica bold', 16), bg="grey")
        self.hp_bar = Label(win, text="HP: "+str(user.health), bg='grey', font=('Helvetica bold', 16))
        self.enemy_bar = Label(win, text="Enemy HP: ", bg='grey', font=('Helvetica bold', 16))
        self.skill_list1 = Radiobutton(win, text=user.curr_area.skill_obj[0].name, indicatoron=0,
                                       command=lambda: select(0, "skills"),
                                       font=('Helvetica bold', 12), bg='grey', value=1)
        self.skill_list2 = Radiobutton(win, text=user.curr_area.skill_obj[1].name, indicatoron=0,
                                       command=lambda: select(1, "skills"),
                                       bg='grey', font=('Helvetica bold', 12), value=2)
        self.skill_list3 = Radiobutton(win, text=user.curr_area.skill_obj[2].name, indicatoron=0,
                                       command=lambda: select(2, "skills"),
                                       bg='grey', font=('Helvetica bold', 12), value=3)
        self.skill_list4 = Radiobutton(win, text=user.curr_area.skill_obj[3].name, indicatoron=0,
                                       command=lambda: select(3, "skills"),
                                       bg='grey', font=('Helvetica bold', 12), value=4)
        self.skill1_lbl = Label(win, text=f"Lvl req: {user.curr_area.skill_obj[0].req},  Resource: "
                                          f"{Items[user.curr_area.skill_obj[0].resources].name}", bg='grey',
                                font=('Helvetica bold', 12))
        self.skill2_lbl = Label(win, text=f"Lvl req: {user.curr_area.skill_obj[1].req},  Resource: "
                                          f"{Items[user.curr_area.skill_obj[1].resources].name}", bg='grey',
                                font=('Helvetica bold', 12))
        self.skill3_lbl = Label(win, text=f"Lvl req: {user.curr_area.skill_obj[2].req},  Resource: "
                                          f"{Items[user.curr_area.skill_obj[2].resources].name}", bg='grey',
                                font=('Helvetica bold', 12))
        self.skill4_lbl = Label(win, text=f"Lvl req: {user.curr_area.skill_obj[3].req},  Resource: "
                                          f"{Items[user.curr_area.skill_obj[3].resources].name}", bg='grey',
                                font=('Helvetica bold', 12))
        self.skill_start = Button(win, text="Start \n"+user.curr_area.skill_obj[user.curr_area.selection].skill,
                                  command=lambda: skill_thread(user.curr_area.skill_obj[user.curr_area.selection]),
                                  font=('Helvetica bold', 14), bg="grey")
        self.skill_stop = Button(win, text="Stop \n"+user.curr_area.skill_obj[user.curr_area.selection].skill,
                                 command=stop_skill, font=('Helvetica bold', 14), bg="grey")
        self.area_title = Label(win, text=user.curr_area.name, bg='grey', font=('Helvetica bold', 20))
        self.npc_list1 = Radiobutton(win, text=user.curr_area.npcs[0].name, indicatoron=0,
                                     command=lambda: select(0, "npcs"), font=('Helvetica bold', 12), bg='grey', value=1)
        self.npc_list2 = Radiobutton(win, text=user.curr_area.npcs[1].name, indicatoron=0,
                                     command=lambda: select(1, "npcs"), bg='grey', font=('Helvetica bold', 12), value=2)
        self.npc_list3 = Radiobutton(win, text=user.curr_area.npcs[2].name, indicatoron=0,
                                     command=lambda: select(2, "npcs"), bg='grey', font=('Helvetica bold', 12), value=3)
        self.interact_npc = Button(win, text="Talk to \n"+user.curr_area.npcs[user.curr_area.selection].name,
                                   command=lambda: talk_npc(user.curr_area.npcs[user.curr_area.selection]),
                                   font=('Helvetica bold', 11), bg="grey")
        self.npc1_lbl = Label(win, text=f"{user.curr_area.npcs[0].desc}", bg='grey', font=('Helvetica bold', 12))
        self.npc2_lbl = Label(win, text=f"{user.curr_area.npcs[1].desc}", bg='grey', font=('Helvetica bold', 12))
        self.npc3_lbl = Label(win, text=f"{user.curr_area.npcs[2].desc}", bg='grey', font=('Helvetica bold', 12))
        self.inv_0 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                            command=lambda: interact_item(user.inventory.slot0, 0))
        self.inv_1 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                            command=lambda: interact_item(user.inventory.slot1, 1))
        self.inv_2 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                            command=lambda: interact_item(user.inventory.slot2, 2))
        self.inv_3 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                            command=lambda: interact_item(user.inventory.slot3, 3))
        self.inv_4 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                            command=lambda: interact_item(user.inventory.slot4, 4))
        self.inv_5 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                            command=lambda: interact_item(user.inventory.slot5, 5))
        self.inv_6 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                            command=lambda: interact_item(user.inventory.slot6, 6))
        self.inv_7 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                            command=lambda: interact_item(user.inventory.slot7, 7))
        self.inv_8 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                            command=lambda: interact_item(user.inventory.slot8, 8))
        self.inv_9 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                            command=lambda: interact_item(user.inventory.slot9, 9))
        self.inv_10 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: interact_item(user.inventory.slot10, 10))
        self.inv_11 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: interact_item(user.inventory.slot11, 11))
        self.inv_12 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: interact_item(user.inventory.slot12, 12))
        self.inv_13 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: interact_item(user.inventory.slot13, 13))
        self.inv_14 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: interact_item(user.inventory.slot14, 14))
        self.inv_15 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: interact_item(user.inventory.slot15, 15))
        self.inv_16 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: interact_item(user.inventory.slot16, 16))
        self.inv_17 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: interact_item(user.inventory.slot17, 17))
        self.inv_18 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: interact_item(user.inventory.slot18, 18))
        self.inv_19 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: interact_item(user.inventory.slot19, 19))
        self.inv_20 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: interact_item(user.inventory.slot20, 20))
        self.inv_21 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: interact_item(user.inventory.slot21, 21))
        self.inv_22 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: interact_item(user.inventory.slot22, 22))
        self.inv_23 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: interact_item(user.inventory.slot23, 23))
        self.inv_24 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: interact_item(user.inventory.slot24, 24))
        self.inv_25 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: interact_item(user.inventory.slot25, 25))
        self.inv_26 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: interact_item(user.inventory.slot26, 26))
        self.inv_27 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: interact_item(user.inventory.slot27, 27))
        self.bank_0 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: bank_withdraw(user.bank.active_tab.slot0, 0))
        self.bank_1 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: bank_withdraw(user.bank.active_tab.slot1, 1))
        self.bank_2 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: bank_withdraw(user.bank.active_tab.slot2, 2))
        self.bank_3 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: bank_withdraw(user.bank.active_tab.slot3, 3))
        self.bank_4 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: bank_withdraw(user.bank.active_tab.slot4, 4))
        self.bank_5 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: bank_withdraw(user.bank.active_tab.slot5, 5))
        self.bank_6 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: bank_withdraw(user.bank.active_tab.slot6, 6))
        self.bank_7 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: bank_withdraw(user.bank.active_tab.slot7, 7))
        self.bank_8 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: bank_withdraw(user.bank.active_tab.slot8, 8))
        self.bank_9 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                             command=lambda: bank_withdraw(user.bank.active_tab.slot9, 9))
        self.bank_10 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                              command=lambda: bank_withdraw(user.bank.active_tab.slot10, 10))
        self.bank_11 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                              command=lambda: bank_withdraw(user.bank.active_tab.slot11, 11))
        self.bank_12 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                              command=lambda: bank_withdraw(user.bank.active_tab.slot12, 12))
        self.bank_13 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                              command=lambda: bank_withdraw(user.bank.active_tab.slot13, 13))
        self.bank_14 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                              command=lambda: bank_withdraw(user.bank.active_tab.slot14, 14))
        self.bank_15 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                              command=lambda: bank_withdraw(user.bank.active_tab.slot15, 15))
        self.bank_16 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                              command=lambda: bank_withdraw(user.bank.active_tab.slot16, 16))
        self.bank_17 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                              command=lambda: bank_withdraw(user.bank.active_tab.slot17, 17))
        self.bank_18 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                              command=lambda: bank_withdraw(user.bank.active_tab.slot18, 18))
        self.bank_19 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                              command=lambda: bank_withdraw(user.bank.active_tab.slot19, 19))
        self.bank_20 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                              command=lambda: bank_withdraw(user.bank.active_tab.slot20, 20))
        self.bank_21 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                              command=lambda: bank_withdraw(user.bank.active_tab.slot21, 21))
        self.bank_22 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                              command=lambda: bank_withdraw(user.bank.active_tab.slot22, 22))
        self.bank_23 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                              command=lambda: bank_withdraw(user.bank.active_tab.slot23, 23))
        self.bank_24 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                              command=lambda: bank_withdraw(user.bank.active_tab.slot24, 24))
        self.bank_25 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                              command=lambda: bank_withdraw(user.bank.active_tab.slot25, 25))
        self.bank_26 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                              command=lambda: bank_withdraw(user.bank.active_tab.slot26, 26))
        self.bank_27 = Button(win, text='', font=('Helvetica bold', 8), bg="grey",
                              command=lambda: bank_withdraw(user.bank.active_tab.slot27, 27))
        self.bank_deposit_all = Button(win, text='Deposit \nAll', font=('Helvetica bold', 16), bg="grey",
                                       command=bank_deposit_all)
        self.shop_0 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(0))
        self.shop_1 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(1))
        self.shop_2 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(2))
        self.shop_3 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(3))
        self.shop_4 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(4))
        self.shop_5 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(5))
        self.shop_6 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(6))
        self.shop_7 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(7))
        self.shop_8 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(8))
        self.shop_9 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(9))
        self.shop_10 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(10))
        self.shop_11 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(11))
        self.shop_12 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(12))
        self.shop_13 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(13))
        self.shop_14 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(14))
        self.shop_15 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(15))
        self.shop_16 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(16))
        self.shop_17 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(17))
        self.shop_18 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(18))
        self.shop_19 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(19))
        self.shop_20 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(20))
        self.shop_21 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(21))
        self.shop_22 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(22))
        self.shop_23 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(23))
        self.shop_24 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(24))
        self.shop_25 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(25))
        self.shop_26 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(26))
        self.shop_27 = Button(win, text='', font=('Helvetica bold', 8), bg="grey", command=lambda: shop_buy(27))
        self.shop_sell_all = Button(win, text='Sell \nAll', font=('Helvetica bold', 16), bg="grey",
                                    command=sell_all)
        self.skill_0 = Button(win, text=str(list(user.skills.keys())[0]) + "\nLevel: " +
                              str(list(user.skills.values())[0][0]) +
                              "\nExp: " + str(round(list(user.skills.values())[0][1])),
                              font=('Helvetica bold', 10), bg="grey", command=lambda: xp_to_next(0))
        self.skill_1 = Button(win, text=str(list(user.skills.keys())[1]) + "\nLevel: " +
                              str(list(user.skills.values())[1][0]) +
                              "\nExp: " + str(round(list(user.skills.values())[1][1], 2)),
                              font=('Helvetica bold', 10), bg="grey", command=lambda: xp_to_next(1))
        self.skill_2 = Button(win, text=str(list(user.skills.keys())[2]) + "\nLevel: " +
                              str(list(user.skills.values())[2][0]) +
                              "\nExp: " + str(round(list(user.skills.values())[2][1])),
                              font=('Helvetica bold', 10), bg="grey", command=lambda: xp_to_next(2))
        self.skill_3 = Button(win, text=str(list(user.skills.keys())[3]) + "\nLevel: " +
                              str(list(user.skills.values())[3][0]) +
                              "\nExp: " + str(round(list(user.skills.values())[3][1])),
                              font=('Helvetica bold', 10), bg="grey", command=lambda: xp_to_next(3))
        self.skill_4 = Button(win, text=str(list(user.skills.keys())[4]) + "\nLevel: " +
                              str(list(user.skills.values())[4][0]) +
                              "\nExp: " + str(round(list(user.skills.values())[4][1])),
                              font=('Helvetica bold', 10), bg="grey", command=lambda: xp_to_next(4))
        self.skill_5 = Button(win, text=str(list(user.skills.keys())[5]) + "\nLevel: " +
                              str(list(user.skills.values())[5][0]) +
                              "\nExp: " + str(round(list(user.skills.values())[5][1])),
                              font=('Helvetica bold', 10), bg="grey", command=lambda: xp_to_next(5))
        self.skill_6 = Button(win, text=str(list(user.skills.keys())[6]) + "\nLevel: " +
                              str(list(user.skills.values())[6][0]) +
                              "\nExp: " + str(round(list(user.skills.values())[6][1])),
                              font=('Helvetica bold', 10), bg="grey", command=lambda: xp_to_next(6))
        self.skill_7 = Button(win, text=str(list(user.skills.keys())[7]) + "\nLevel: " +
                              str(list(user.skills.values())[7][0]) +
                              "\nExp: " + str(round(list(user.skills.values())[7][1])),
                              font=('Helvetica bold', 10), bg="grey", command=lambda: xp_to_next(7))
        self.skill_8 = Button(win, text=str(list(user.skills.keys())[8]) + "\nLevel: " +
                              str(list(user.skills.values())[8][0]) +
                              "\nExp: " + str(round(list(user.skills.values())[8][1])),
                              font=('Helvetica bold', 10), bg="grey", command=lambda: xp_to_next(8))
        self.skill_9 = Button(win, text=str(list(user.skills.keys())[9]) + "\nLevel: " +
                              str(list(user.skills.values())[9][0]) +
                              "\nExp: " + str(round(list(user.skills.values())[9][1])),
                              font=('Helvetica bold', 10), bg="grey", command=lambda: xp_to_next(9))
        self.skill_10 = Button(win, text=str(list(user.skills.keys())[10]) + "\nLevel: " + str(
                               list(user.skills.values())[10][0]) +
                               "\nExp: " + str(round(list(user.skills.values())[10][1])),
                               font=('Helvetica bold', 10), bg="grey", command=lambda: xp_to_next(10))
        self.skill_11 = Button(win, text=str(list(user.skills.keys())[11]) + "\nLevel: " + str(
                               list(user.skills.values())[11][0]) +
                               "\nExp: " + str(round(list(user.skills.values())[11][1])),
                               font=('Helvetica bold', 10), bg="grey", command=lambda: xp_to_next(11))
        self.skill_12 = Button(win, text=str(list(user.skills.keys())[12]) + "\nLevel: " + str(
                               list(user.skills.values())[12][0]) +
                               "\nExp: " + str(round(list(user.skills.values())[12][1])),
                               font=('Helvetica bold', 10), bg="grey", command=lambda: xp_to_next(12))
        self.skill_13 = Button(win, text=str(list(user.skills.keys())[13]) + "\nLevel: " + str(
                               list(user.skills.values())[13][0]) +
                               "\nExp: " + str(round(list(user.skills.values())[13][1])),
                               font=('Helvetica bold', 10), bg="grey", command=lambda: xp_to_next(13))
        self.combat_lvl = Button(win, text=f"Combat level:\n{combat_level(user)}", font=('Helvetica bold', 10),
                                 bg="grey", command=lambda: xp_to_next(-1))
        self.style1 = Button(win, text='', font=('Helvetica bold', 16), bg="grey",
                             command=print)
        self.style2 = Button(win, text='', font=('Helvetica bold', 16), bg="grey",
                             command=print)
        self.style3 = Button(win, text='', font=('Helvetica bold', 16), bg="grey",
                             command=print)
        self.curr_style = Label(win, text="Current style:\n"+user.att_style, bg='grey', font=('Helvetica bold', 16))
        self.equip_item = Button(win, text="Equip", command=lambda: equip_item(user.inventory.curr_selection),
                                 bg='grey', font=('Helvetica bold', 16))
        self.drop_item = Button(win, text="Drop", command=lambda: drop_item(user.inventory.curr_selection),
                                bg='grey', font=('Helvetica bold', 16))
        self.equipment_head = Button(win, text="Head:\n"+Items[user.equipment.get('Head', 'None')].name, bg='grey',
                                     font=('Helvetica bold', 10), command=lambda: unequip_item('Head'))
        self.equipment_neck = Button(win, text="Neck:\n"+Items[user.equipment.get('Neck', 'None')].name, bg='grey',
                                     font=('Helvetica bold', 10), command=lambda: unequip_item('Neck'))
        self.equipment_body = Button(win, text="Body:\n"+Items[user.equipment.get('Body', 'None')].name, bg='grey',
                                     font=('Helvetica bold', 10), command=lambda: unequip_item('Body'))
        self.equipment_legs = Button(win, text="Legs\n"+Items[user.equipment.get('Legs', 'None')].name, bg='grey',
                                     font=('Helvetica bold', 10), command=lambda: unequip_item('Legs'))
        self.equipment_feet = Button(win, text="Feet\n"+Items[user.equipment.get('Feet', 'None')].name, bg='grey',
                                     font=('Helvetica bold', 10), command=lambda: unequip_item('Feet'))
        self.equipment_cape = Button(win, text="Cape:\n"+Items[user.equipment.get('Cape', 'None')].name, bg='grey',
                                     font=('Helvetica bold', 10), command=lambda: unequip_item('Cape'))
        self.equipment_weapon = Button(win, text="Weapon:\n"+Items[user.equipment.get('Weapon', 'None')].name,
                                       bg='grey', font=('Helvetica bold', 10), command=lambda: unequip_item('Weapon'))
        self.equipment_hands = Button(win, text="Hands:\n"+Items[user.equipment.get('Hands', 'None')].name, bg='grey',
                                      font=('Helvetica bold', 10), command=lambda: unequip_item('Hands'))
        self.equipment_ammo = Button(win, text="Ammo:\n"+Items[user.equipment.get('Ammo', ['None', ''])[0]].name+"\n" +
                                               str(user.equipment.get('Ammo', ['None', ''])[1]), bg='grey',
                                     font=('Helvetica bold', 10), command=lambda: unequip_item('Ammo'))
        self.equipment_shield = Button(win, text="Shield:\n"+Items[user.equipment.get('Shield', 'None')].name,
                                       bg='grey', font=('Helvetica bold', 10), command=lambda: unequip_item('Shield'))
        self.equipment_ring = Button(win, text="Ring:\n"+Items[user.equipment.get('Ring', 'None')].name, bg='grey',
                                     font=('Helvetica bold', 10), command=lambda: unequip_item('Ring'))
        self.main_console.tag_config('warning', background="black", foreground="red")
        self.main_console.tag_config('normal', background="black", foreground="white")
        self.main_console.tag_config('good', background="black", foreground="#00e600")
        self.att_speed = Label(win, text="Attack Speed(ms): ", bg='grey', font=('Helvetica bold', 12))
        self.acc_melee = Label(win, text="Melee accuracy: ", bg='grey', font=('Helvetica bold', 12))
        self.acc_ranged = Label(win, text="Ranged accuracy: ", bg='grey', font=('Helvetica bold', 12))
        self.acc_magic = Label(win, text="Magic accuracy: ", bg='grey', font=('Helvetica bold', 12))
        self.str_melee = Label(win, text="Melee strength: ", bg='grey', font=('Helvetica bold', 12))
        self.str_ranged = Label(win, text="Ranged strength: ", bg='grey', font=('Helvetica bold', 12))
        self.str_magic = Label(win, text="Magic strength: ", bg='grey', font=('Helvetica bold', 12))
        self.melee_def = Label(win, text="Melee defence: ", bg='grey', font=('Helvetica bold', 12))
        self.ranged_def = Label(win, text="Ranged defence: ", bg='grey', font=('Helvetica bold', 12))
        self.magic_def = Label(win, text="Magic defence: ", bg='grey', font=('Helvetica bold', 12))
        self.testinv = Button(win, text="Is in inv?", bg='grey', font=('Helvetica bold', 12),
                              command=lambda: checkinv(1))
        # self.testinv.place(relx=0.1, rely=0.1, relwidth=0.05, relheight=0.05)
        self.examine_item = Button(win, text="Examine", bg='grey', font=('Helvetica bold', 16),
                                   command=lambda: self.insert_text_thread(user.inventory.curr_selection[0].examine))
        self.progress = Progressbar(win, orient=HORIZONTAL, length=100, mode='determinate')
        self.tab_1 = Radiobutton(win, text="Tab 1", indicatoron=0, value=10, variable=tabvar, bg='grey', font=(
            'Helvetica bold', 14), command=lambda: bank_tab_swap(1))
        self.tab_2 = Radiobutton(win, text="Tab 2", indicatoron=0, value=11, variable=tabvar, bg='grey', font=(
            'Helvetica bold', 14), command=lambda: bank_tab_swap(2))
        self.tab_3 = Radiobutton(win, text="Tab 3", indicatoron=0, value=12, variable=tabvar, bg='grey', font=(
            'Helvetica bold', 14), command=lambda: bank_tab_swap(3))
        self.tab_4 = Radiobutton(win, text="Tab 4", indicatoron=0, value=13, variable=tabvar, bg='grey', font=(
            'Helvetica bold', 14), command=lambda: bank_tab_swap(4))
        self.quantity_1 = Radiobutton(win, text="1", indicatoron=0, value=20, variable=quantvar, bg='grey', font=(
            'Helvetica bold', 16), command=lambda: setattr(user.bank, 'quant', 1))
        self.quantity_2 = Radiobutton(win, text="5", indicatoron=0, value=21, variable=quantvar, bg='grey', font=(
            'Helvetica bold', 16), command=lambda: setattr(user.bank, 'quant', 5))
        self.quantity_3 = Radiobutton(win, text="10", indicatoron=0, value=22, variable=quantvar, bg='grey', font=(
            'Helvetica bold', 16), command=lambda: setattr(user.bank, 'quant', 10))
        self.quantity_4 = Radiobutton(win, text="50", indicatoron=0, value=23, variable=quantvar, bg='grey', font=(
            'Helvetica bold', 16), command=lambda: setattr(user.bank, 'quant', 50))
        self.quantity_5 = Radiobutton(win, text="ALL", indicatoron=0, value=24, variable=quantvar, bg='grey', font=(
            'Helvetica bold', 16), command=lambda: setattr(user.bank, 'quant', 9999999))
        self.quantity_label = Label(text="Quantity:", bg='grey', font=('Helvetica bold', 14))
        self.sell_item = Button(win, text="Sell", command=lambda: sell_item(user.inventory.curr_selection),
                                bg='grey', font=('Helvetica bold', 16))
        self.value_item = Button(win, text="Value", command=lambda: value_item(user.inventory.curr_selection),
                                 bg='grey', font=('Helvetica bold', 16))
        self.close_shop = Button(win, text="Close shop", command=open_shop, bg='grey', font=('Helvetica bold', 16))
        self.open_shop = Button(win, text="Open shop", command=open_shop, bg='grey', font=('Helvetica bold', 16))
        self.spellbook = Button(win, text="Spells", command=list_spells, bg='grey', font=('Helvetica bold', 16))
        self.spell_0 = Radiobutton(win, text="Air strike\nLevel 1\n1 Air, 1 Mind", command=lambda: set_spell(
                       0), bg='grey', font=('Helvetica bold', 9), indicatoron=0, value=30, variable=spellvar)
        self.spell_1 = Radiobutton(win, text="Water strike\nLevel 5\n1 Air, 1 Mind, 1 Water", command=lambda: set_spell(
            1), bg='grey', font=('Helvetica bold', 9), indicatoron=0, value=31, variable=spellvar)
        self.spell_2 = Radiobutton(win, text="Earth strike\nLevel 9\n1 Air, 1 Mind, 1 Earth", command=lambda: set_spell(
            2), bg='grey', font=('Helvetica bold', 9), indicatoron=0, value=32, variable=spellvar)
        self.spell_3 = Radiobutton(win, text="Fire strike\nLevel 13\n1 Air, 1 Mind, 1 Fire", command=lambda: set_spell(
            3), bg='grey', font=('Helvetica bold', 9), indicatoron=0, value=33, variable=spellvar)
        self.spell_4 = Radiobutton(win, text="Air bolt\nLevel 17\n5 Air, 1 Chaos", command=lambda: set_spell(
            4), bg='grey', font=('Helvetica bold', 9), indicatoron=0, value=34, variable=spellvar)
        self.spell_5 = Radiobutton(win, text="Water bolt\nLevel 23\n3 Air, 1 Chaos, 3 Water", command=lambda: set_spell(
            5), bg='grey', font=('Helvetica bold', 9), indicatoron=0, value=35, variable=spellvar)
        self.spell_6 = Radiobutton(win, text="Earth bolt\nLevel 29\n3 Air, 1 Chaos, 3 Earth", command=lambda: set_spell(
            6), bg='grey', font=('Helvetica bold', 9), indicatoron=0, value=36, variable=spellvar)
        self.spell_7 = Radiobutton(win, text="Fire bolt\nLevel 35\n3 Air, 1 Chaos, 3 Fire", command=lambda: set_spell(
            7), bg='grey', font=('Helvetica bold', 9), indicatoron=0, value=37, variable=spellvar)
        self.spell_8 = Radiobutton(win, text="Air blast\nLevel 41\n9 Air, 1 Death", command=lambda: set_spell(
            8), bg='grey', font=('Helvetica bold', 9), indicatoron=0, value=38, variable=spellvar)
        self.spell_9 = Radiobutton(win, text="Water blast\nLevel 47\n7 Air, 1 Death, 7 Water",
                                   command=lambda: set_spell(9), bg='grey',
                                   font=('Helvetica bold', 9), indicatoron=0, value=39, variable=spellvar)
        self.spell_10 = Radiobutton(win, text="Earth blast\nLevel 53\n7 Air, 1 Death, 7 Earth",
                                    command=lambda: set_spell(10),
                                    bg='grey', font=('Helvetica bold', 9), indicatoron=0, value=40, variable=spellvar)
        self.spell_11 = Radiobutton(win, text="Fire blast\nLevel 59\n7 Air, 1 Death, 7 Fire",
                                    command=lambda: set_spell(11), bg='grey',
                                    font=('Helvetica bold', 9), indicatoron=0, value=41, variable=spellvar)
        self.spell_12 = Radiobutton(win, text="Air wave\nLevel 65\n13 Air, 1 Blood",
                                    command=lambda: set_spell(12), bg='grey', font=('Helvetica bold', 9),
                                    indicatoron=0, value=42, variable=spellvar)
        self.spell_13 = Radiobutton(win, text="Water wave\nLevel 71\n11 Air, 1 Blood, 11 Water",
                                    command=lambda: set_spell(13), bg='grey',
                                    font=('Helvetica bold', 9), indicatoron=0, value=43, variable=spellvar)
        self.spell_14 = Radiobutton(win, text="Earth wave\nLevel 77\n11 Air, 1 Blood, 11 Earth",
                                    command=lambda: set_spell(14), bg='grey',
                                    font=('Helvetica bold', 9), indicatoron=0, value=44, variable=spellvar)
        self.spell_15 = Radiobutton(win, text="Fire wave\nLevel 83\n11 Air, 1 Blood, 11 Fire",
                                    command=lambda: set_spell(15), bg='grey',
                                    font=('Helvetica bold', 9), indicatoron=0, value=45, variable=spellvar)
        self.spell_16 = Button(win, text="Teleport to\nVarrock\nLevel 25\n1 Law, 3 Air, 1 Fire", command=lambda:
                               cast_spell(Spellbook[16]), bg='grey', font=('Helvetica bold', 9))
        self.spell_17 = Button(win, text="Teleport to\nLum\nLevel 35\n1 Law, 3 Air, 1 Earth", command=lambda:
                               cast_spell(Spellbook[17]), bg='grey', font=('Helvetica bold', 9))
        self.spell_18 = Button(win, text="Teleport to\nArdy\nLevel 50\n2 Law, 2 Water", command=lambda:
                               cast_spell(Spellbook[18]), bg='grey', font=('Helvetica bold', 9),)
        self.spell_19 = Button(win, text="Teleport to\nCanifis\nLevel 66\n2 Law, 2 Water, 2 Earth", command=lambda:
                               cast_spell(Spellbook[19]), bg='grey', font=('Helvetica bold', 9))
        self.combat_spells = Radiobutton(win, text="Combat Spells", command=lambda: spell_tab(
            0), bg='grey', font=('Helvetica bold', 12), indicatoron=0, value=50, variable=spellvar2)
        self.utility_spells = Radiobutton(win, text="Utility Spells", command=lambda: spell_tab(
            1), bg='grey', font=('Helvetica bold', 12), indicatoron=0, value=51, variable=spellvar2)
        self.burn = Button(win, text="Burn", command=lambda: burn_log(user.inventory.curr_selection),
                           bg='grey', font=('Helvetica bold', 16))
        self.cooking = Button(win, text="Cook", command=list_cooking, bg='grey', font=('Helvetica bold', 16))
        self.start_cook = Button(win, text="Start\nCooking", command=cook_thread, bg='grey', font=(
                                 'Helvetica bold', 16))
        self.stop_cook = Button(win, text="Stop\nCooking", command=lambda: setattr(user, 'curr_action', 'flee'),
                                bg='grey', font=('Helvetica bold', 16))
        self.cooks_left = Label(win, text="", bg='grey', font=('Helvetica bold', 14))
        self.cook_0 = Radiobutton(win, text="", command=lambda: setattr(user, 'curr_item', Items[vars(user.inventory)[
                                                        'slot' + str(cook_list[0])][0]]), bg='grey',
                                  font=('Helvetica bold', 12), variable=cookvar, value=60, indicatoron=0)
        self.cook_1 = Radiobutton(win, text="", command=lambda: setattr(user, 'curr_item', Items[vars(user.inventory)[
                                                        'slot' + str(cook_list[1])][0]]), bg='grey',
                                  font=('Helvetica bold', 12), variable=cookvar, value=61, indicatoron=0)
        self.cook_2 = Radiobutton(win, text="", command=lambda: setattr(user, 'curr_item', Items[vars(user.inventory)[
                                                        'slot' + str(cook_list[2])][0]]), bg='grey',
                                  font=('Helvetica bold', 12), variable=cookvar, value=62, indicatoron=0)
        self.cook_3 = Radiobutton(win, text="", command=lambda: setattr(user, 'curr_item', Items[vars(user.inventory)[
                                                        'slot' + str(cook_list[3])][0]]), bg='grey',
                                  font=('Helvetica bold', 12), variable=cookvar, value=63, indicatoron=0)
        self.cook_4 = Radiobutton(win, text="", command=lambda: setattr(user, 'curr_item', Items[vars(user.inventory)[
                                                        'slot' + str(cook_list[4])][0]]), bg='grey',
                                  font=('Helvetica bold', 12), variable=cookvar, value=64, indicatoron=0)
        self.cook_5 = Radiobutton(win, text="", command=lambda: setattr(user, 'curr_item', Items[vars(user.inventory)[
                                                        'slot' + str(cook_list[5])][0]]), bg='grey',
                                  font=('Helvetica bold', 12), variable=cookvar, value=65, indicatoron=0)
        self.cook_6 = Radiobutton(win, text="", command=lambda: setattr(user, 'curr_item', Items[vars(user.inventory)[
                                                        'slot' + str(cook_list[6])][0]]), bg='grey',
                                  font=('Helvetica bold', 12), variable=cookvar, value=66, indicatoron=0)
        self.cook_7 = Radiobutton(win, text="", command=lambda: setattr(user, 'curr_item', Items[vars(user.inventory)[
                                                        'slot' + str(cook_list[7])][0]]), bg='grey',
                                  font=('Helvetica bold', 12), variable=cookvar, value=67, indicatoron=0)
        self.cook_8 = Radiobutton(win, text="", command=lambda: setattr(user, 'curr_item', Items[vars(user.inventory)[
                                                        'slot' + str(cook_list[8])][0]]), bg='grey',
                                  font=('Helvetica bold', 12), variable=cookvar, value=68, indicatoron=0)
        self.cook_9 = Radiobutton(win, text="", command=lambda: setattr(user, 'curr_item', Items[vars(user.inventory)[
                                                        'slot' + str(cook_list[9])][0]]), bg='grey',
                                  font=('Helvetica bold', 12), variable=cookvar, value=69, indicatoron=0)
        self.cook_10 = Radiobutton(win, text="", command=lambda: setattr(user, 'curr_item', Items[vars(user.inventory)[
                                                        'slot' + str(cook_list[10])][0]]), bg='grey',
                                   font=('Helvetica bold', 12), variable=cookvar, value=70, indicatoron=0)
        self.anvil = Button(win, text="Smith", command=list_smithing, bg='grey', font=('Helvetica bold', 16))
        self.furnace = Button(win, text="Smelt", command=list_smelting, bg='grey', font=('Helvetica bold', 16))
        self.bronze_bar = Radiobutton(win, text="Bronze bar\nLevel: 1\n1 Tin, 1 Copper", command=lambda: set_bar(
            79, 'bronze'), bg='grey', font=('Helvetica bold', 10), variable=smeltvar, value=80, indicatoron=0)
        self.iron_bar = Radiobutton(win, text="Iron bar\nLevel: 15\n1 Iron", command=lambda: set_bar(
            90, 'iron'), bg='grey', font=('Helvetica bold', 10), variable=smeltvar, value=81, indicatoron=0)
        self.steel_bar = Radiobutton(win, text="Steel bar\nLevel: 30\n1 Iron, 1 Coal", command=lambda: set_bar(
            101, 'steel'), bg='grey', font=('Helvetica bold', 10), variable=smeltvar, value=82, indicatoron=0)
        self.mithril_bar = Radiobutton(win, text="Mithril bar\nLevel: 45\n1 Mithril, 2 Coal", command=lambda: set_bar(
            112, 'mithril'), bg='grey', font=('Helvetica bold', 10), variable=smeltvar, value=83, indicatoron=0)
        self.adamant_bar = Radiobutton(win, text="Adamant bar\nLevel: 1\n1 Adamant, 3 Coal", command=lambda: set_bar(
            123, 'adamant'), bg='grey', font=('Helvetica bold', 10), variable=smeltvar, value=84, indicatoron=0)
        self.rune_bar = Radiobutton(win, text="Rune bar\nLevel: 1\n1 Runite, 4 Coal", command=lambda: set_bar(
            134, 'rune'), bg='grey', font=('Helvetica bold', 10), variable=smeltvar, value=85, indicatoron=0)
        self.start_smelt = Button(win, text="Start smelting", command=smelt_thread, bg='grey', font=(
            'Helvetica bold', 14))
        self.stop_smith = Button(win, text="Stop smithing", command=lambda: setattr(user, 'curr_action', 'flee'),
                                 bg='grey', font=('Helvetica bold', 14))
        self.start_smith = Button(win, text="Start smithing", command=smith_thread, bg='grey', font=(
            'Helvetica bold', 14))
        self.bronze_tab = Radiobutton(win, text="Bronze", command=lambda: smith_tab(0), bg='grey',
                                      font=('Helvetica bold', 12), variable=smith_tabvar, value=90, indicatoron=0)
        self.iron_tab = Radiobutton(win, text="Iron", command=lambda: smith_tab(1), bg='grey',
                                    font=('Helvetica bold', 12), variable=smith_tabvar, value=91, indicatoron=0)
        self.steel_tab = Radiobutton(win, text="Steel", command=lambda: smith_tab(2), bg='grey',
                                     font=('Helvetica bold', 12), variable=smith_tabvar, value=92, indicatoron=0)
        self.mithril_tab = Radiobutton(win, text="Mithril", command=lambda: smith_tab(3), bg='grey',
                                       font=('Helvetica bold', 12), variable=smith_tabvar, value=93, indicatoron=0)
        self.adamant_tab = Radiobutton(win, text="Adamant", command=lambda: smith_tab(4), bg='grey',
                                       font=('Helvetica bold', 12), variable=smith_tabvar, value=94, indicatoron=0)
        self.rune_tab = Radiobutton(win, text="Runite", command=lambda: smith_tab(5), bg='grey',
                                    font=('Helvetica bold', 12), variable=smith_tabvar, value=95, indicatoron=0)
        self.smith_item_0 = Radiobutton(win, text="", command=lambda: set_smith(smith_list[0]), bg='grey',
                                        font=('Helvetica bold', 10), variable=smithvar, value=100, indicatoron=0)
        self.smith_item_1 = Radiobutton(win, text="", command=lambda: set_smith(smith_list[1]), bg='grey',
                                        font=('Helvetica bold', 10), variable=smithvar, value=101, indicatoron=0)
        self.smith_item_2 = Radiobutton(win, text="", command=lambda: set_smith(smith_list[2]), bg='grey',
                                        font=('Helvetica bold', 10), variable=smithvar, value=102, indicatoron=0)
        self.smith_item_3 = Radiobutton(win, text="", command=lambda: set_smith(smith_list[3]), bg='grey',
                                        font=('Helvetica bold', 10), variable=smithvar, value=103, indicatoron=0)
        self.smith_item_4 = Radiobutton(win, text="", command=lambda: set_smith(smith_list[4]), bg='grey',
                                        font=('Helvetica bold', 10), variable=smithvar, value=104, indicatoron=0)
        self.smith_item_5 = Radiobutton(win, text="", command=lambda: set_smith(smith_list[5]), bg='grey',
                                        font=('Helvetica bold', 10), variable=smithvar, value=105, indicatoron=0)
        self.smith_item_6 = Radiobutton(win, text="", command=lambda: set_smith(smith_list[6]), bg='grey',
                                        font=('Helvetica bold', 10), variable=smithvar, value=106, indicatoron=0)
        self.smith_item_7 = Radiobutton(win, text="", command=lambda: set_smith(smith_list[7]), bg='grey',
                                        font=('Helvetica bold', 10), variable=smithvar, value=107, indicatoron=0)
        self.smith_item_8 = Radiobutton(win, text="", command=lambda: set_smith(smith_list[8]), bg='grey',
                                        font=('Helvetica bold', 10), variable=smithvar, value=108, indicatoron=0)
        self.fletching = Button(win, text="Fletch", command=lambda: list_fletching(user.inventory.curr_selection),
                                bg='grey', font=('Helvetica bold', 14))
        self.start_fletch = Button(win, text="Start fletching", command=fletch_thread, bg='grey', font=(
            'Helvetica bold', 14))
        self.stop_fletch = Button(win, text="Stop fletching", command=lambda: setattr(user, 'curr_action', 'flee'),
                                  bg='grey', font=('Helvetica bold', 14))
        self.fletch_0 = Radiobutton(win, text="", command=lambda: set_fletch(fletch_list[0], 0), bg='grey',
                                    font=('Helvetica bold', 10), variable=fletchvar, value=110, indicatoron=0)
        self.fletch_1 = Radiobutton(win, text="", command=lambda: set_fletch(fletch_list[1], 1), bg='grey',
                                    font=('Helvetica bold', 10), variable=fletchvar, value=111, indicatoron=0)
        self.fletch_2 = Radiobutton(win, text="", command=lambda: set_fletch(fletch_list[2], 2), bg='grey',
                                    font=('Helvetica bold', 10), variable=fletchvar, value=112, indicatoron=0)
        self.fletch_3 = Radiobutton(win, text="", command=lambda: set_fletch(fletch_list[3], 3), bg='grey',
                                    font=('Helvetica bold', 10), variable=fletchvar, value=113, indicatoron=0)
        self.fletch_4 = Radiobutton(win, text="", command=lambda: set_fletch(fletch_list[4], 4), bg='grey',
                                    font=('Helvetica bold', 10), variable=fletchvar, value=114, indicatoron=0)
        self.fletch_5 = Radiobutton(win, text="", command=lambda: set_fletch(fletch_list[5], 5), bg='grey',
                                    font=('Helvetica bold', 10), variable=fletchvar, value=115, indicatoron=0)
        self.selected_inv_item = Label(win, text="", bg='grey', font=('Helvetica bold', 12))
        self.npc_name = Label(win, text=f"{user.curr_area.npcs[user.curr_area.selection].name}", bg='grey',
                              font=('Helvetica bold', 16))
        self.npc_dialogue = Text(win, bd=1, font=('Helvetica bold', 14), fg='black', bg='grey', state=DISABLED, padx=50,
                                 wrap=WORD, selectbackground='grey')
        self.npc_response_1 = Button(win, text="", command=print(), bg='grey', font=('Helvetica bold', 12))
        self.npc_response_2 = Button(win, text="", command=print(), bg='grey', font=('Helvetica bold', 12))
        # self.test_quest = Button(win, text="TEST", command=lambda: print(user.quest_flags, "TESTFLAGS"),
        #                          bg='grey', font=('Helvetica bold', 12))
        # self.test_quest.place(relx=0.1, rely=0.05, relheight=0.05, relwidth=0.05)
        self.quest_obj = Button(win, text="Quest info", command=list_quest_info, bg='grey', font=('Helvetica bold', 16))
        self.quest_info = Text(win, bd=1, font=('Helvetica bold', 14), fg='white', bg='grey', state=DISABLED, padx=1,
                               wrap=WORD, selectbackground='grey')
        self.quest_info.tag_config('incomplete', foreground="red")
        self.quest_info.tag_config('title', foreground="white", font=('Helvetica bold', 14, 'bold'))
        self.quest_info.tag_config('complete', foreground="#5fe62e")
        self.continue_tut = Button(win, text="Continue", command=progress_tutorial, bg='grey',
                                   font=('Helvetica bold', 16))
        self.crafting = Button(win, text="Craft", command=lambda: list_crafting(user.inventory.curr_selection),
                               bg='grey', font=('Helvetica bold', 14))
        self.craft_0 = Radiobutton(win, text="Item_0", command=lambda: set_craft(craft_list[0], 0), bg='grey',
                                   font=('Helvetica bold', 10), variable=craftvar, value=120, indicatoron=0)
        self.craft_1 = Radiobutton(win, text="Item_1", command=lambda: set_craft(craft_list[1], 1), bg='grey',
                                   font=('Helvetica bold', 10), variable=craftvar, value=121, indicatoron=0)
        self.craft_2 = Radiobutton(win, text="Item_2", command=lambda: set_craft(craft_list[2], 2), bg='grey',
                                   font=('Helvetica bold', 10), variable=craftvar, value=122, indicatoron=0)
        self.craft_3 = Radiobutton(win, text="Item_3", command=lambda: set_craft(craft_list[3], 3), bg='grey',
                                   font=('Helvetica bold', 10), variable=craftvar, value=123, indicatoron=0)
        self.start_craft = Button(win, text="Start crafting", command=craft_thread, bg='grey', font=(
            'Helvetica bold', 14))
        self.stop_craft = Button(win, text="Stop crafting", command=lambda: setattr(user, 'curr_action', 'flee'),
                                 bg='grey', font=('Helvetica bold', 14))
        self.transport_btn = Button(win, text="", command=print, bg='grey', font=('Helvetica bold', 12))

    def toggle_pass(self):
        """Toggle whether password is visible in the entry boxes."""
        if self.reg_pass.winfo_viewable():
            if self.reg_pass.cget('show') == '':
                self.reg_pass.configure(show='*')
                self.reg_pass2.configure(show='*')
                self.pass_toggle.configure(text='Show password')
            else:
                self.reg_pass.configure(show='')
                self.reg_pass2.configure(show='')
                self.pass_toggle.configure(text='Hide password')
        else:
            if self.log_pass.cget('show') == '':
                self.log_pass.configure(show='*')
                self.pass_toggle.configure(text='Show password')
            else:
                self.log_pass.configure(show='')
                self.pass_toggle.configure(text='Hide password')

    def insert_text(self, string, state, new_line):
        """Insert the given text into the game console letter by letter to give a smoother feel.

        string = string, text to insert \n
        state = string, tag used to colour text \n
        new_line = bool, whether to add a new line before inserting text
        """
        with text_lock:
            try:
                self.main_console.configure(state=NORMAL)
                if new_line:
                    self.main_console.insert(END, "\n")
                self.main_console.see(END)
                self.main_console.configure(state=DISABLED)
                for character in string:
                    self.main_console.configure(state=NORMAL)
                    self.main_console.insert(END, character, state)
                    self.main_console.configure(state=DISABLED)
                    # perf_counter allows a shorter sleep interval than time.sleep()
                    now = time.perf_counter()
                    self.main_console.see(END)
                    end = now + 0.003
                    while now < end:
                        now = time.perf_counter()
                self.main_console.see(END)
                self.main_console.configure(state=DISABLED)
            except _tkinter.TclError:
                # A thread of this function will often be in progress when program exits
                print("Closing...")
                return

    def insert_text_thread(self, string, state='normal', new_line=True):
        """Create and launch a thread for the insert_text method.

        string = string, text to insert \n
        state = string, tag used to colour text (default 'normal') \n
        new_line = bool, whether to add a new line before inserting text (default True) \n
        Use a thread to prevent stalling the app during display.
        """
        t = Thread(target=self.insert_text, args=(string, state, new_line), daemon=True)
        t.start()


def register():
    """Display the registration interface."""
    mywin.login_btn.place_forget()
    mywin.register_btn.place_forget()
    mywin.reg_user.place(relx=0.35, rely=0.25, relwidth=0.3, relheight=0.05)
    mywin.reg_pass.place(relx=0.35, rely=0.45, relwidth=0.3, relheight=0.05)
    mywin.reg_pass2.place(relx=0.35, rely=0.65, relwidth=0.3, relheight=0.05)
    mywin.reg_user_lbl.place(relx=0.315, rely=0.18, relwidth=0.3, relheight=0.05)
    mywin.reg_pass_lbl.place(relx=0.315, rely=0.38, relwidth=0.3, relheight=0.05)
    mywin.reg_pass2_lbl.place(relx=0.33, rely=0.58, relwidth=0.3, relheight=0.05)
    mywin.submit_btn.place(relx=0.45, rely=0.75, relwidth=0.1, relheight=0.05)
    mywin.pass_toggle.place(relx=0.7, rely=0.55, relwidth=0.2, relheight=0.05)
    mywin.back_btn.place(relx=0.45, rely=0.1, relwidth=0.1, relheight=0.05)


def login():
    """Display the login interface."""
    mywin.login_btn.place_forget()
    mywin.register_btn.place_forget()
    mywin.log_user_lbl.place(relx=0.295, rely=0.18, relwidth=0.3, relheight=0.05)
    mywin.log_pass_lbl.place(relx=0.295, rely=0.38, relwidth=0.3, relheight=0.05)
    mywin.submit_btn.place(relx=0.45, rely=0.55, relwidth=0.1, relheight=0.05)
    mywin.log_user.place(relx=0.35, rely=0.25, relwidth=0.3, relheight=0.05)
    mywin.log_pass.place(relx=0.35, rely=0.45, relwidth=0.3, relheight=0.05)
    mywin.back_btn.place(relx=0.45, rely=0.1, relwidth=0.1, relheight=0.05)
    mywin.pass_toggle.place(relx=0.7, rely=0.55, relwidth=0.2, relheight=0.05)


def submit():
    """Submit registration or login information, before setting up the relevant user profile.

    Use a local SQLite database to store information.
    """
    global user
    with sql.connect("Pr_db") as conn:
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS user_profiles (
            UserId INTEGER PRIMARY KEY, Username TEXT UNIQUE NOT NULL, Password TEXT NOT NULL, Salt TEXT NOT NULL)""")
        cur.execute("""CREATE TABLE IF NOT EXISTS user_data (
            UserId INTEGER PRIMARY KEY, name TEXT, skills TEXT, flags TEXT, inventory TEXT, bank TEXT, 
            curr_area TEXT, curr_action TEXT, curr_shop TEXT, curr_spell TEXT, curr_item TEXT, att_style TEXT, 
            equipment TEXT, health TEXT, spawn TEXT, quest_flags TEXT,
            FOREIGN KEY (UserId)
                REFERENCES user_profiles (UserId)
                 ON DELETE CASCADE
                 ON UPDATE NO ACTION)""")
        if mywin.reg_pass.winfo_viewable():
            # Check for username availability to prevent duplicate usernames
            if mywin.reg_pass.get() != mywin.reg_pass2.get():
                mywin.reg_warning_lbl.configure(text="Passwords don't match!")
                mywin.reg_warning_lbl.place(relx=0.363, rely=0.85)
                return
            user_name = mywin.reg_user.get()
            cur.execute("""SELECT username FROM user_profiles WHERE ? = username""", [user_name.lower()])
            rows = cur.fetchall()
            print(rows)
            if rows:
                # Username is already taken i.e query found a result
                for row in rows:
                    # In case somehow there were multiple matching names
                    if row[0].upper() == user_name.upper():
                        # Usernames are not case sensitive to prevent confusion
                        mywin.reg_warning_lbl.configure(text="Username taken, try another!")
                        mywin.reg_warning_lbl.place(relx=0.335, rely=0.85)
                        return
            # Hash the password with salt for secure storage
            salt = urandom(32)
            key = pbkdf2_hmac('sha256', mywin.reg_pass.get().encode('utf-8'), salt, 100000)
            # Store user details in database
            cur.execute("BEGIN TRANSACTION")
            cur.execute("INSERT INTO user_profiles(username, password, salt) VALUES(?, ?, ?)", [user_name, key, salt])
            cur.execute("""INSERT INTO user_data(name, skills, flags, inventory, bank, curr_area, curr_action, 
            curr_shop, curr_spell, curr_item, att_style, equipment)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        [user_name,
                         "{'Attack': [1, 0], 'Cooking': [1, 0], 'Crafting': [1, 0], 'Defence': [1, 0], "
                         "'Firemaking': [1, 0], 'Fishing': [1, 0], 'Fletching': [1, 0], 'Hitpoints': [10, 1154], "
                         "'Magic': [1, 0], 'Mining': [1, 0], 'Ranged': [1, 0], 'Smithing': [1, 0], 'Strength': [1, 0], "
                         "'Woodcutting': [1, 0]}",
                         "{}", "[]", "[]", "None", 'idle', "[]", "0", "0", "Accurate", "{}"])
            cur.execute("COMMIT")
            user = Player(user_name, {'Attack': [1, 0], 'Cooking': [1, 0], 'Crafting': [1, 0], 'Defence': [1, 0],
                                      'Firemaking': [1, 0], 'Fishing': [1, 0], 'Fletching': [1, 0],
                                      'Hitpoints': [10, 1154], 'Magic': [1, 0], 'Mining': [1, 0], 'Ranged': [1, 0],
                                      'Smithing': [1, 0], 'Strength': [1, 0], 'Woodcutting': [1, 0]}, {}, [], [], None,
                          'idle', [], 0, 0, "Accurate", {})
            # Start the tutorial for new player
            t0 = Thread(target=tutorial, daemon=True)
            t0.name = "tutorial_thread"
            t0.start()
        else:
            # First, check details against the database. If can't verify then return with error
            cur.execute("SELECT password, salt FROM user_profiles WHERE username = ?", [mywin.log_user.get()])
            rows = cur.fetchall()
            if not rows or rows[0][0] != pbkdf2_hmac(
                    'sha256', mywin.log_pass.get().encode('utf-8'), rows[0][1], 100000):
                mywin.reg_warning_lbl.configure(text="Incorrect Username/Password combination!")
                mywin.reg_warning_lbl.place(relx=0.26, rely=0.65)
                return
            # Set up the loaded user profile
            load_data(mywin.log_user.get())
            # If user hasn't finished tutorial, load to the closest tutorial checkpoint
            if user.flags.get('tut_prog', 0) < 33:
                t0 = Thread(target=tutorial, daemon=True)
                t0.name = "tutorial_thread"
                t0.start()
            else:
                swap_area(user.curr_area, 'forced')
                mywin.insert_text_thread(f"Welcome back, {user.name}.", 'good')
        mywin.reg_user.place_forget()
        mywin.reg_pass.place_forget()
        mywin.reg_pass2.place_forget()
        mywin.reg_user_lbl.place_forget()
        mywin.reg_pass_lbl.place_forget()
        mywin.reg_pass2_lbl.place_forget()
        mywin.pass_toggle.place_forget()
        mywin.back_btn.place_forget()
        mywin.log_user_lbl.place_forget()
        mywin.log_pass_lbl.place_forget()
        mywin.submit_btn.place_forget()
        mywin.log_user.place_forget()
        mywin.log_pass.place_forget()
        mywin.back_btn.place_forget()
        mywin.reg_warning_lbl.place_forget()


def startup():
    """Display the initial interface on startup. Give user the choice to register or log in to an existing profile."""
    mywin.register_btn.place(relx=0.4, rely=0.4, relwidth=0.2, relheight=0.05)
    mywin.login_btn.place(relx=0.4, rely=0.6, relwidth=0.2, relheight=0.05)
    mywin.reg_user.place_forget()
    mywin.reg_pass.place_forget()
    mywin.reg_pass2.place_forget()
    mywin.reg_user_lbl.place_forget()
    mywin.reg_pass_lbl.place_forget()
    mywin.reg_pass2_lbl.place_forget()
    mywin.reg_warning_lbl.place_forget()
    mywin.pass_toggle.place_forget()
    mywin.back_btn.place_forget()
    mywin.log_user_lbl.place_forget()
    mywin.log_pass_lbl.place_forget()
    mywin.submit_btn.place_forget()
    mywin.log_user.place_forget()
    mywin.log_pass.place_forget()
    mywin.back_btn.place_forget()
    mywin.reg_pass.configure(show='*')
    mywin.reg_pass2.configure(show='*')
    mywin.pass_toggle.configure(text='Show password')
    mywin.log_pass.configure(show='*')


def flash_button(button):
    """Force the given interface element to flash periodically.

    button = string, button name \n
    Used during the tutorial for guidance.
    """
    global flashing
    flashing = True
    while flashing:
        vars(mywin)[button].configure(bg='grey')
        time.sleep(0.2)
        if not flashing or not running:
            break
        time.sleep(0.2)
        if not flashing or not running:
            break
        vars(mywin)[button].configure(bg='white')
        time.sleep(0.2)
        if not flashing or not running:
            break
        time.sleep(0.2)
    vars(mywin)[button].configure(bg='grey')


def swap_area(index, move_source='neighbour'):
    """Change the current area being displayed and used for all kinds of functions.

    index = integer: Area id or direction index depending on move_source \n
    move_source = string, determining how the area change is handled (default 'neighbour') \n
    Take new area input as either an explicit Area_id number or an index referencing a direction in the original
    area's neighbour list. The move_source value determines which of these behaviours is used.
    Apply multiple checks based on area requirements before successfully changing the area.
    """
    if user.curr_action != 'idle':
        # Display custom text depending on user's current activity
        action = user.curr_action
        if user.curr_action == 'combat':
            action = 'in ' + action
        if user.curr_action == 'flee':
            action = 'right now'
        else:
            action = 'while ' + action
        mywin.insert_text_thread(f"You can't leave the area {action}.", 'warning')
        return
    if index is None:
        index, move_source = 2, 'forced'
    if move_source == 'neighbour':
        new_area = Areas[user.curr_area.neighbours[index]]
    else:
        new_area = Areas[index]
    if new_area is None or type(new_area) != Area:
        return
    failed_check = False
    for skill, req in new_area.skill_reqs.items():
        if skill == 'Combat':
            if combat_level(user) < req:
                mywin.insert_text_thread(f"Your combat level is too low for this area. You need lvl "
                                         f"{req}.", 'warning')
                failed_check = True
        elif user.skills[skill][0] < req:
            mywin.insert_text_thread(f"Your {skill} is too low for this area. You need lvl "
                                     f"{req}.", 'warning')
            failed_check = True
    for q in new_area.quest_reqs:
        for q_ in user.quest_flags:
            if q_[0] == q:
                if q_[1] >= len(Quests[q].objectives):  # = Quest is complete
                    break
                failed_check = True
                mywin.insert_text_thread(f"You need to complete {Quests[q].name} before entering {new_area.name} "
                                         f"(Starts at {Quests[q].start}).",
                                         'warning')
                break
            if q_ == user.quest_flags[-1]:      # = Checked all user quests and not completed
                failed_check = True
                mywin.insert_text_thread(f"You need to complete {Quests[q].name} before entering {new_area.name} "
                                         f"(Starts at {Quests[q].start}).",
                                         'warning')
        # Catch case where user has no quests done, so loop never starts
        if len(user.quest_flags) == 0:
            mywin.insert_text_thread(f"You need to complete {Quests[q].name} before entering {new_area.name} "
                                     f"(Starts at {Quests[q].start}).",
                                     'warning')
            failed_check = True
    if failed_check:
        return
    current_items = []
    if move_source == 'transport':
        for skill, req in user.curr_area.transport.skill_reqs.items():
            if skill == "Combat":
                if combat_level(user) < req:
                    mywin.insert_text_thread(f"Your combat level is too low for this area. You need lvl "
                                             f"{req}.", 'warning')
                    failed_check = True
            elif user.skills[skill][0] < req:
                mywin.insert_text_thread(f"Your {skill} is too low to do that. You need lvl "
                                         f"{req}.", 'warning')
                failed_check = True
        for q in user.curr_area.transport.quest_reqs:
            for q_ in user.quest_flags:
                if q_[0] == q:
                    if q_[1] >= len(Quests[q].objectives):
                        break
                    failed_check = True
                    mywin.insert_text_thread(f"You need to complete {Quests[q].name} before doing that "
                                             f"(Starts at {Quests[q].start}).",
                                             'warning')
                    break
                if q_ == user.quest_flags[-1]:
                    failed_check = True
                    mywin.insert_text_thread(f"You need to complete {Quests[q].name} before doing that "
                                             f"(Starts at {Quests[q].start}).",
                                             'warning')
            if len(user.quest_flags) == 0:
                mywin.insert_text_thread(f"You need to complete {Quests[q].name} before entering {new_area.name} "
                                         f"(Starts at {Quests[q].start}).",
                                         'warning')
                failed_check = True
        for item, quantity in user.curr_area.transport.item_reqs.items():
            if (_ := user.inventory.is_in_inv(item)) and _[1] >= quantity:
                # Store items to remove if all checks succeed
                current_items.append([item, quantity])
                update_inventory()
            else:
                mywin.insert_text_thread(f"You need {quantity} {Items[item].name} to do that.", 'warning')
                failed_check = True
    if failed_check:
        return
    for i in current_items:
        user.inventory.remove_item(i[0], i[1])
    user.curr_area = new_area
    direction = ['north', 'east', 'south', 'west']
    area_setup()
    if move_source == 'transport':
        mywin.insert_text_thread(f"You continue to {new_area.name}.", 'good')
    if move_source == 'neighbour':
        mywin.insert_text_thread(f"\nYou continue {direction[index]} to {new_area.name}.\n", 'good')
    # Clear any temporary fires in progress
    global fire_timer
    fire_timer = 0


def area_setup():
    """Set up a new area's interface based on the values in the Area object."""
    # First close any open interface
    if mywin.bronze_tab.winfo_viewable():
        j = 0
        for i in ['bronze_', 'iron_', 'steel_', 'mithril_', 'adamant_', 'rune_']:
            vars(mywin)[i + 'tab'].place_forget()
            vars(mywin)[i + 'tab'].deselect()
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            j += 1
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            if j < 5:
                j += 1
        mywin.start_smith.place_forget()
        mywin.stop_smith.place_forget()
        user.curr_item = 0
    if mywin.start_smelt.winfo_viewable():
        mywin.bronze_bar.place_forget()
        mywin.iron_bar.place_forget()
        mywin.steel_bar.place_forget()
        mywin.mithril_bar.place_forget()
        mywin.adamant_bar.place_forget()
        mywin.rune_bar.place_forget()
        mywin.start_smelt.place_forget()
        mywin.stop_smith.place_forget()
        mywin.cooks_left.place_forget()
    if mywin.start_cook.winfo_viewable():
        for i in range(10):
            vars(mywin)['cook_' + str(i)].place_forget()
            vars(mywin)['cook_' + str(i)].deselect()
            mywin.start_cook.place_forget()
            mywin.stop_cook.place_forget()
            mywin.cooks_left.place_forget()
            user.curr_item = 0
    if mywin.spell_0.winfo_viewable() or mywin.spell_16.winfo_viewable():
        for i in range(20):
            vars(mywin)['spell_' + str(i)].place_forget()
        mywin.utility_spells.place_forget()
        mywin.combat_spells.place_forget()
    if mywin.skill_0.winfo_viewable():
        for i in range(14):
            vars(mywin)['skill_' + str(i)].place_forget()
        mywin.combat_lvl.place_forget()
    if mywin.equipment_ring.winfo_viewable():
        mywin.equipment_head.place_forget()
        mywin.equipment_neck.place_forget()
        mywin.equipment_body.place_forget()
        mywin.equipment_legs.place_forget()
        mywin.equipment_feet.place_forget()
        mywin.equipment_cape.place_forget()
        mywin.equipment_weapon.place_forget()
        mywin.equipment_hands.place_forget()
        mywin.equipment_ammo.place_forget()
        mywin.equipment_shield.place_forget()
        mywin.equipment_ring.place_forget()
        mywin.att_speed.place_forget()
        mywin.acc_melee.place_forget()
        mywin.acc_ranged.place_forget()
        mywin.acc_magic.place_forget()
        mywin.str_melee.place_forget()
        mywin.str_ranged.place_forget()
        mywin.str_magic.place_forget()
        mywin.melee_def.place_forget()
        mywin.ranged_def.place_forget()
        mywin.magic_def.place_forget()
    if mywin.inv_0.winfo_viewable():
        mywin.equip_item.place_forget()
        mywin.drop_item.place_forget()
        mywin.eat.place_forget()
        mywin.burn.place_forget()
        mywin.examine_item.place_forget()
        mywin.crafting.place_forget()
        mywin.fletching.place_forget()
        mywin.selected_inv_item.place_forget()
        for i in range(28):
            vars(mywin)['inv_' + str(i)].place_forget()
    if mywin.enemy_fight.winfo_viewable() or mywin.enemy_list1.winfo_viewable() or mywin.enemy_list2.winfo_viewable()\
            or mywin.enemy_list3.winfo_viewable() or mywin.enemy_list4.winfo_viewable():
        mywin.enemy_fight.place_forget()
        for i in range(1, 5):
            vars(mywin)['enemy_list' + str(i)].place_forget()
            vars(mywin)['enemy' + str(i) + '_lbl'].place_forget()
            vars(mywin)['enemy_list' + str(i)].deselect()
    if mywin.npc_list1.winfo_viewable() or mywin.npc_name.winfo_viewable() or mywin.npc_list2.winfo_viewable()\
            or mywin.npc_list3.winfo_viewable():
        for i in range(1, 4):
            vars(mywin)['npc_list' + str(i)].place_forget()
            vars(mywin)['npc' + str(i) + '_lbl'].place_forget()
            vars(mywin)['npc_list' + str(i)].deselect()
        mywin.interact_npc.place_forget()
        mywin.open_shop.place_forget()
        mywin.npc_name.place_forget()
        mywin.npc_dialogue.place_forget()
        mywin.npc_response_1.place_forget()
        mywin.npc_response_2.place_forget()
    if mywin.skill_list1.winfo_viewable():
        mywin.skill_start.place_forget()
        for i in range(1, 5):
            vars(mywin)['skill_list' + str(i)].place_forget()
            vars(mywin)['skill_list' + str(i)].deselect()
            vars(mywin)['skill' + str(i) + '_lbl'].place_forget()
    if mywin.fletch_0.winfo_viewable():
        for i in range(6):
            vars(mywin)['fletch_' + str(i)].place_forget()
            vars(mywin)['fletch_' + str(i)].deselect()
        mywin.start_fletch.place_forget()
        mywin.stop_fletch.place_forget()
        mywin.cooks_left.place_forget()
    if mywin.start_cook.winfo_viewable():
        for i in range(10):
            vars(mywin)['cook_' + str(i)].place_forget()
            vars(mywin)['cook_' + str(i)].deselect()
            mywin.start_cook.place_forget()
            mywin.stop_cook.place_forget()
            mywin.cooks_left.place_forget()
            user.curr_item = 0
    if mywin.quest_info.winfo_viewable():
        mywin.quest_info.place_forget()
    # Clear the interface elements that are area dependent
    mywin.transport_btn.place_forget()
    mywin.list_bank.place_forget()
    mywin.cooking.place_forget()
    mywin.anvil.place_forget()
    mywin.furnace.place_forget()
    mywin.north_btn.place_forget()
    mywin.east_btn.place_forget()
    mywin.south_btn.place_forget()
    mywin.west_btn.place_forget()
    mywin.area_title.configure(text=user.curr_area.name)
    window.configure(bg=user.curr_area.background)
    # Add all interface elements based on Area properties
    mywin.main_console.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.3)
    mywin.main_input.place(relx=0.25, rely=0.4, relwidth=0.5, relheight=0.05)
    mywin.list_enemies.place(relx=0, rely=0.6, relwidth=0.2, relheight=0.05)
    mywin.list_skill_obj.place(relx=0, rely=0.65, relwidth=0.2, relheight=0.05)
    if user.flags.get('tut_prog', 250) > 30:
        mywin.list_npcs.place(relx=0, rely=0.7, relwidth=0.2, relheight=0.05)
    if user.flags.get('tut_prog', 250) > 33:
        mywin.quest_obj.place(relx=0, rely=0.4, relwidth=0.1, relheight=0.05)
    mywin.list_skills.place(relx=0, rely=0.75, relwidth=0.2, relheight=0.05)
    mywin.list_backpack.place(relx=0, rely=0.8, relwidth=0.2, relheight=0.05)
    mywin.equipment.place(relx=0, rely=0.85, relwidth=0.2, relheight=0.05)
    mywin.hp_bar.place(relx=0.76, rely=0.4, relwidth=0.1, relheight=0.05)
    mywin.area_title.place(relx=0.3, rely=0.05, relwidth=0.4, relheight=0.05)
    mywin.spellbook.place(relx=0, rely=0.9, relwidth=0.2, relheight=0.05)
    if user.curr_area.has_bank:
        mywin.list_bank.place(relx=0, rely=0.25, relwidth=0.1, relheight=0.05)
    if user.curr_area.has_range:
        mywin.cooking.place(relx=0, rely=0.2, relwidth=0.1, relheight=0.05)
    if user.curr_area.has_furnace:
        mywin.furnace.place(relx=0, rely=0.15, relwidth=0.1, relheight=0.05)
    if user.curr_area.has_anvil:
        mywin.anvil.place(relx=0, rely=0.1, relwidth=0.1, relheight=0.05)
    if user.curr_area.neighbours[0] is not None:
        mywin.north_btn.place(relx=0.45, rely=0, relwidth=0.1, relheight=0.05)
    if user.curr_area.neighbours[1] is not None:
        mywin.east_btn.place(relx=0.9, rely=0.475, relwidth=0.1, relheight=0.05)
    if user.curr_area.neighbours[2] is not None:
        mywin.south_btn.place(relx=0.45, rely=0.95, relwidth=0.1, relheight=0.05)
    if user.curr_area.neighbours[3] is not None:
        mywin.west_btn.place(relx=0, rely=0.475, relwidth=0.1, relheight=0.05)
    if user.curr_area.transport is not None:
        t = user.curr_area.transport
        mywin.transport_btn.place(relx=0, rely=0.525, relwidth=0.2, relheight=0.075)
        mywin.transport_btn.configure(text=t.text1+"\n"+t.text2, command=lambda: swap_area(t.area_id, 'transport'))


def show_dialogue(text=None, response_1=None, response_2=None, button_type=None, quest_id=None, obj_num=None):
    """Display NPC dialogue interface using the given values.

    text = string that NPC uses as dialogue (default None) \n
    response_1, 2 = strings that are used for the response buttons (default None) \n
    button_type = string deciding which command to bind to the accept button (default None) \n
    quest_id = integer, quest id (default None) \n
    obj_num = integer, objective number for given quest (default None) \n
    Set up response buttons to progress quest if one is available.
    """
    if text is None or response_2 is None:
        # Default dialogue for an NPC after accepting a new quest objective
        response_2 = "Leave"
        text = "Good luck! Come see me again if you forget what to do."
    mywin.npc_dialogue.configure(state=NORMAL)
    mywin.npc_dialogue.delete(1.0, END)
    mywin.npc_dialogue.insert(END, text)
    mywin.npc_dialogue.configure(state=DISABLED)
    if response_1 is not None:
        mywin.npc_response_1.configure(text=response_1)
    mywin.npc_response_2.configure(text=response_2, command=list_npcs)
    # Change response button behaviour depending on quest state
    if button_type == "start":
        mywin.npc_response_1.configure(command=lambda: accept_quest(Quests[quest_id]))
    elif button_type == "finish":
        mywin.npc_response_1.configure(command=lambda: finish_quest(Quests[quest_id], obj_num))
    elif button_type == "remind":
        mywin.npc_response_1.configure(text="I'm on it.", command=show_dialogue)
    mywin.npc_name.place(relx=0.25, rely=0.5, relwidth=0.5, relheight=0.1)
    mywin.npc_dialogue.place(relx=0.25, rely=0.6, relwidth=0.5, relheight=0.2)
    if response_1 != "" and response_1 is not None:
        mywin.npc_response_1.place(relx=0.25, rely=0.85, relwidth=0.25, relheight=0.1)
    else:
        mywin.npc_response_1.place_forget()
    mywin.npc_response_2.place(relx=0.5, rely=0.85, relwidth=0.25, relheight=0.1)
    mywin.npc1_lbl.place_forget()
    mywin.npc2_lbl.place_forget()
    mywin.npc3_lbl.place_forget()


def talk_npc(npc):
    """Preparatory function for show_dialogue.

    npc = NPC object \n
    Check user's quest progress against an NPC's quest flags, then for each quest that the user is eligible for,
    check their levels and completed quests against that quest's requirements.
    If user is eligible for a certain quest, pass the relevant arguments to show_dialogue to start or progress the
    quest. Else, show some default dialogue stored in the NPC.
    """
    list_npcs()
    mywin.npc_name.configure(text=npc.name)
    quests_started = [q for [q, _] in user.quest_flags]
    for flag in npc.flags:
        quest, objective = flag             # As integers
        q = Quests[quest]                   # As a quest object
        obj = q.objectives[objective]
        # Check if user has started each quest, if not, then checks requirements. If any are not met, display them
        # in the console. (eg. You still need the following to start Quest_2: 40 Combat, Complete Quest_1,...)
        if quest not in quests_started and objective == 0:
            initial_text = False
            for new_quest in q.quest_reqs:      # Check each quest_req for completion
                if new_quest not in quests_started or [new_quest, len(Quests[new_quest].objectives)] not in \
                        user.quest_flags:
                    if not initial_text:
                        mywin.insert_text_thread(f"You need to do the following to start {q.name}:", 'warning')
                        initial_text = True
                    mywin.insert_text_thread(f"- Complete {Quests[new_quest].name} "
                                             f"(Starts at {Quests[new_quest].start}).", 'warning')
            for skill, req in q.skill_reqs.items():
                if skill == 'Combat' and combat_level(user) < req or skill != 'Combat' and user.skills[skill][0] < req:
                    if not initial_text:
                        mywin.insert_text_thread(f"You need to do the following to start {q.name}:", 'warning')
                        initial_text = True
                    mywin.insert_text_thread(f"- Reach {req} {skill}.", 'warning')
        # Check if user is currently doing each quest, and give the correct arguments to show_dialogue
        if [quest, objective] in user.quest_flags and obj.return_npc == npc.id:
            show_dialogue(obj.dialogue_progress, obj.response_progress_1,
                          obj.response_progress_2, "finish", quest, objective)
            if obj.start_npc == npc.id:
                # Give important quest items to user if not already claimed
                if (quest_items := obj.quest_items) is not None and not user.inventory.is_in_inv(quest_items[0]) and (
                        not user.bank.is_in_bank(quest_items[0])):
                    if user.inventory.free_spaces() >= len(quest_items):
                        for item in quest_items:
                            user.inventory.add_to_inv(item)
                        mywin.insert_text_thread(f"Accepted {len(quest_items)} quest items.", 'good')
                    else:
                        mywin.insert_text_thread(f"Inventory was too full to accept quest items.\n"
                                                 f"Talk to the NPC again to receive them.", 'warning')
            return
        # Remind user of quest objective when quest starts and ends at different NPC
        elif [quest, objective] in user.quest_flags:
            show_dialogue(obj.dialogue_start, obj.response_start_1,
                          obj.response_start_2, "remind", quest, objective)
            if obj.start_npc == npc.id:
                if (quest_items := obj.quest_items) is not None and not user.inventory.is_in_inv(quest_items[0]) and (
                        not user.bank.is_in_bank(quest_items[0])):
                    if user.inventory.free_spaces() >= len(quest_items):
                        for item in quest_items:
                            user.inventory.add_to_inv(item)
                        mywin.insert_text_thread(f"Accepted {len(quest_items)} quest items.", 'good')
                    else:
                        mywin.insert_text_thread(f"Inventory was too full to accept quest items.\n"
                                                 f"Talk to the NPC again to receive them.", 'warning')
            return
    # Reach this point if no quests are in progress relevant to the NPC. Start a quest if one can be started.
    for flag in npc.flags:
        quest, objective = flag
        q = Quests[quest]
        failed_reqs = False
        if objective == 0 and q.objectives[objective].start_npc == npc.id and q.id not in quests_started:
            for new_quest in q.quest_reqs:
                if new_quest not in quests_started or [new_quest, len(Quests[new_quest].objectives)] not in \
                        user.quest_flags:
                    failed_reqs = True
            for skill, req in q.skill_reqs.items():
                if skill == 'Combat' and combat_level(user) < req or skill != 'Combat' and user.skills[skill][0] < req:
                    failed_reqs = True
            if failed_reqs:
                continue
            show_dialogue(q.objectives[0].dialogue_start, q.objectives[0].response_start_1,
                          q.objectives[0].response_start_2, "start", quest, objective)
            return
    # Reach here if NPC has no quests that are currently able to be progressed or started. Show standard dialogue
    show_dialogue(npc.dialogue, "", "Leave")


def accept_quest(quest):
    """Check quest requirements, and set up the start of the quest if they are satisfied.

    quest = Quest object \n
    Give quest items and update the relevant flags in the user object.
    This function is used in the accept button from show_dialogue.
    """
    failed_check = False
    objective = quest.objectives[0]
    for skill in quest.skill_reqs.keys():
        if user.skills[skill][0] < quest.skill_reqs[skill]:
            mywin.insert_text_thread(f"Your {skill} is too low for this quest. You need lvl {quest.skill_reqs[skill]}.",
                                     'warning')
            failed_check = True
    for q in quest.quest_reqs:
        for q_ in user.quest_flags:
            if q_[0] == q:
                if q_[1] >= len(Quests[q].objectives):  # Quest is complete
                    break
                failed_check = True
                mywin.insert_text_thread(f"You need to complete {Quests[q].name} before starting this quest "
                                         f"(Starts at {Quests[q].start}).", 'warning')
                break
            if q_ == user.quest_flags[-1]:      # = Checked all user quests and not completed
                failed_check = True
                mywin.insert_text_thread(f"You need to complete {Quests[q].name} before starting this quest "
                                         f"(Starts at {Quests[q].start}).", 'warning')
        # Catch case where user has not started any quests, hence the loop never starts
        if len(user.quest_flags) == 0:
            mywin.insert_text_thread(f"You need to complete {Quests[q].name} before starting this quest "
                                     f"(Starts at {Quests[q].start}).", 'warning')
            failed_check = True
    if failed_check:
        return
    # By this point any requirements must have been satisfied, so start quest, give quest items, and
    # add the relevant flags to the user object including temporary kill tracking flags
    if (quest_items := objective.quest_items) is not None:
        if user.inventory.free_spaces() >= len(quest_items):
            for item in quest_items:
                user.inventory.add_to_inv(item)
            mywin.insert_text_thread(f"Accepted {len(quest_items)} quest items.", 'good')
        else:
            mywin.insert_text_thread(f"Inventory was too full to accept quest items.\n"
                                     f"Talk to the NPC again to receive them.", 'warning')
    user.quest_flags.append([quest.id, 0])
    if objective.enemies is not None:
        for enemy_id in objective.enemies.keys():
            user.flags["kill_"+str(enemy_id)] = 0
    show_dialogue()


def finish_quest(quest, objective):
    """Process the end of a given quest objective.

    quest = Quest object \n
    objective = integer \n
    Start the next objective if one exists, updating user flags and collecting / handing out quest items.
    If the current objective is the last for the current quest, then give rewards as long as there is sufficient
    inventory space to do so.
    """
    obj = quest.objectives[objective]
    failed_check = False
    if obj.quest_items is not None and not user.inventory.is_in_inv(obj.quest_items[0]) and \
            not user.bank.is_in_bank(obj.quest_items[0]):
        mywin.insert_text_thread(f"You should make space for the quest items before continuing.", 'warning')
        return
    # Check the flag that tracks enemy kill count for objective
    if obj.enemies is not None:
        for enemy_id, quantity in obj.enemies.items():
            if (kills := user.flags.get("kill_"+str(enemy_id), 0)) < quantity:
                mywin.insert_text_thread(f"You need to kill {quantity-kills} more {Enemies[enemy_id].name}.", 'warning')
                failed_check = True
    # Check each item and quantity for objective
    if obj.items is not None:
        for item, quantity in obj.items.items():
            curr_amount = 0
            if not user.inventory.is_in_inv(item) or (curr_amount := user.inventory.is_in_inv(item)[1]) < quantity:
                mywin.insert_text_thread(f"You need {quantity-curr_amount} more {Items[item].name}.", 'warning')
                failed_check = True
    # Check inventory has space for rewards if this is last step
    if objective + 1 >= len(quest.objectives):
        space_needed = 0
        for item, quantity in quest.item_rewards.items():
            if not Items[item].stackable:
                space_needed += quantity
            elif not user.inventory.is_in_inv(item):
                space_needed += 1
        if obj.items is not None:
            for item, quantity in obj.items.items():
                if not Items[item].stackable:
                    space_needed -= quantity
                elif user.inventory.is_in_inv(item) and user.inventory.is_in_inv(item)[1] == quantity:
                    space_needed -= 1
        if space_needed > (curr_space := user.inventory.free_spaces()):
            mywin.insert_text_thread(f"You need {space_needed-curr_space} more open inventory slots to hold the rewards"
                                     f" for this quest.", 'warning')
            return
    if failed_check:
        return
    # Clear the temp flags used to track the objective
    if obj.enemies is not None:
        for enemy_id in obj.enemies.keys():
            del user.flags["kill_"+str(enemy_id)]
    # Delete items that were "handed in" to the quest npc as part of the objective
    if obj.items is not None:
        for item, quantity in obj.items.items():
            user.inventory.remove_item(item, quantity)
    # Find and increment correct objective number
    for flag in user.quest_flags:
        if flag[0] == quest.id:
            flag[1] += 1
    objective += 1
    # Check if the quest has ended or set up next objective
    if objective < len(quest.objectives):
        obj = quest.objectives[objective]
        if obj.quest_items is not None:
            if user.inventory.free_spaces() >= len(obj.quest_items):
                for item in obj.quest_items:
                    user.inventory.add_to_inv(item)
            else:
                mywin.insert_text_thread(f"Inventory was too full to accept quest items.\n"
                                         f"Talk to the NPC again to receive them.", 'warning')
        if obj.enemies is not None:
            for enemy_id in obj.enemies.keys():
                user.flags["kill_" + str(enemy_id)] = 0
        show_dialogue(quest.objectives[objective].dialogue_start, quest.objectives[objective].response_start_1,
                      quest.objectives[objective].response_start_2, "remind", quest.id, objective)
        # Handle part of the tutorial
        if (quest, objective) == (Tut_quest, 3):
            tut_area_1.enemies[1] = Man_enemy
            tut_area_1.npcs.remove(Man_npc)
    # In this case user has completed quest, so give rewards and show rewards dialogue
    else:
        mywin.insert_text_thread(f"\nCongratulations! You've completed {quest.name}!", 'good')
        for item, quantity in quest.item_rewards.items():
            user.inventory.add_to_inv(item, quantity)
            mywin.insert_text_thread(f"You receive {quantity} {Items[item].name}.")
        for skill, xp in quest.xp_rewards.items():
            user.skills[skill][1] += xp
            mywin.insert_text_thread(f"You receive {xp} {skill} experience.")
            while xp_to_next(skill, silence=True) <= 0 and user.skills[skill][0] != 99:
                user.skills[skill][0] += 1
                mywin.insert_text_thread(f"Congratulations! Your {skill} is now level {user.skills[skill][0]}.", 'good')
        show_dialogue(quest.rewards_dialogue, response_2="Leave")
        # Clear any quest items if they weren't already handed in for some reason during quest
        user.bank.remove_from_bank(item_property='quest_item', property_value=quest.id)
        user.inventory.remove_special_item(item_property='quest_item', property_value=quest.id)
        update_inventory()
        if user.flags['tut_prog'] == 32:
            user.flags['tut_prog'] = 33


def burn_log(item):
    """Attempt to burn the selected log from the inventory.

    item = [item, quantity, slot] \n
    Create a temporary cooking fire and generate experience. Display error to user if skill or item requirements
    aren't met.
    """
    if user.skills['Firemaking'][0] < item[0].skill_reqs['Firemaking']:
        mywin.insert_text_thread(
            f"You need level {item[0].skill_reqs['Firemaking']} Firemaking to burn {item[0].name}.", 'warning')
        return
    if user.flags.get('tut_prog', 250) < 25:
        mywin.insert_text_thread(f"\nYou shouldn't do that just yet.", 'warning')
        return
    if not user.inventory.is_in_inv(39):
        mywin.insert_text_thread(f"You need a tinderbox to burn that.", 'warning')
        return
    mywin.insert_text_thread(f"Burned {item[0].name} for {item[0].xp} experience.")
    user.skills['Firemaking'][1] += item[0].xp * global_xp_multiplier
    # Level-up loop to take care of gaining multiple levels from one action
    while xp_to_next('Firemaking', True) <= 0 and user.skills['Firemaking'][0] != 99:
        user.skills['Firemaking'][0] += 1
        mywin.insert_text_thread(f"Congratulations! Your Firemaking is now level {user.skills['Firemaking'][0]}.",
                                 'good')
    if not mywin.cooking.winfo_viewable():
        mywin.cooking.place(relx=0, rely=0.2, relwidth=0.1, relheight=0.05)
    vars(user.inventory)['slot'+str(item[2])] = None
    user.inventory.shuffle_inv()
    update_skills()
    # Allow smooth multiple log burning without needing to select each log one by one
    if inv_item := user.inventory.is_in_inv(item[0].id):
        slot = inv_item[0][-1] if type(inv_item[0]) != int else inv_item[0]
        user.inventory.curr_selection = [item[0], 1, slot]
        user.inventory.shuffle_inv()
        update_inventory()
        if user.flags.get('tut_prog', 250) < 40:
            mywin.cooking.place(relx=0, rely=0.2, relwidth=0.1, relheight=0.05)
        else:
            fire_thread(item[0])
        if user.flags.get('tut_prog', 250) == 25:
            user.flags['tut_prog'] = 26
        return
    mywin.drop_item.place_forget()
    mywin.burn.place_forget()
    mywin.examine_item.place_forget()
    mywin.fletching.place_forget()
    mywin.crafting.place_forget()
    mywin.selected_inv_item.place_forget()
    update_inventory()
    # During tutorial, cooking fires are permanent until changing area for simplicity
    if user.flags.get('tut_prog', 250) < 40:
        mywin.cooking.place(relx=0, rely=0.2, relwidth=0.1, relheight=0.05)
    else:
        fire_thread(item[0])
    if user.flags.get('tut_prog', 250) == 25:
        user.flags['tut_prog'] = 26


def fire(log):
    """Create a temporary fire from burning a log. Remove it when the timer runs out.

    log = Items[log_id] \n
    Intended to run as a thread so it can keep time in the background.
    """
    fire_length = ((log.skill_reqs['Firemaking'] // 15) + 1) * 60
    global fire_timer
    fire_timer = fire_length
    while fire_timer > 0:
        fire_timer -= 1
        time.sleep(1)
    if not user.curr_area.has_range:
        mywin.cooking.place_forget()
    mywin.insert_text_thread(f"The fire you lit has burned out!", 'warning')


def progress_tutorial():
    """Progress the tutorial function.

    To prevent any potential multiple progressions by accidentally triggering this function multiple times, calls to
    this function should be careful.
    """
    if user.curr_action != 'idle':
        mywin.insert_text_thread(f"\nYou need to be idle before moving on.", 'warning')
        return
    if 'tut_prog' in user.flags and user.flags.get('tut_prog', 250) < 40:
        user.flags['tut_prog'] += 1


def smith_tab(num):
    """Display the selected smithing tab interface. Greys out inaccessible products.

    num = integer, 0 to 5, representing each tier of metal
    """
    # Take advantage of item id patterns to display the correct metal items
    base_id = 80 + num * 11
    for i in range(9):
        smith_list[i] = base_id + i
        item = Items[base_id + i]
        vars(mywin)['smith_item_'+str(i)].configure(text=f"{item.name}\nLevel:{item.skill_reqs['Smithing']}\nBars:"
                                                         f"{item.resources[base_id-1]}")
        vars(mywin)['smith_item_' + str(i)].place(relx=0.25 + 0.125*(i % 4), rely=0.65 + 0.1*(i // 4), relwidth=0.125,
                                                  relheight=0.1)
        if not user.inventory.is_in_inv(base_id-1) or user.inventory.is_in_inv(base_id-1)[1] < \
                item.resources[base_id-1] or user.skills['Smithing'][0] < item.skill_reqs['Smithing']:
            vars(mywin)['smith_item_'+str(i)].configure(bg='grey35')
        else:
            vars(mywin)['smith_item_' + str(i)].configure(bg='grey')


def set_smith(num):
    """Set the user's current item to the selected smithing product in preparation for smithing.

    num = integer, item id \n
    Check resource and level requirements before allowing selection.
    """
    bar_item = Items[num]
    bar = 0
    if user.curr_item == Items[num]:
        return
    if user.skills['Smithing'][0] < bar_item.skill_reqs['Smithing']:
        mywin.insert_text_thread(f"Smithing level is too low to smelt that.{num}", 'warning')
        vars(mywin)['smith_item_' + str((num - 80) % 11)].deselect()
        user.curr_item = 0
        return
    for i in bar_item.resources.keys():
        bar = i
    if not user.inventory.is_in_inv(bar) or user.inventory.is_in_inv(bar)[1] < bar_item.resources[bar]:
        mywin.insert_text_thread(f"Not enough bars to smith that.", 'warning')
        vars(mywin)['smith_item_' + str((num - 80) % 11)].deselect()
        user.curr_item = 0
        return
    user.curr_item = Items[num]
    mywin.insert_text_thread(f"Selected {user.curr_item.name}.")


def set_fletch(num, button_id):
    """Set the user's current item to the selected fletching product in preparation for fletching.

    num = integer, item id \n
    button_id = integer, button's integer suffix \n
    Check resource and level requirements before allowing selection.
    """
    product = Items[num]
    if user.curr_item == Items[num]:
        return
    # Related item that stores the fletching level requirement if needed
    alt_product = product
    # Bows: requirement is stored on the unstrung version only
    if num > 150 and num % 2 == 1:
        alt_product = Items[num - 1]
    # Arrows: requirement is stored on arrowhead
    elif num in range(144, 150):
        for index, resource in enumerate(product.resources.keys()):
            if index == 1:
                alt_product = Items[resource]
    if user.skills['Fletching'][0] < alt_product.skill_reqs['Fletching']:
        mywin.insert_text_thread(f"Fletching level is too low to fletch that.", 'warning')
        vars(mywin)['fletch_' + str(button_id)].deselect()
        user.curr_item = 0
        return
    # Deal with arrow shafts having multiple resource options
    if num == 29:
        curr_id = user.inventory.curr_selection[0].id
        curr_req = user.inventory.curr_selection[0].skill_reqs['Fletching']
        if curr_id in range(3, 11):
            log_id = curr_id
        else:
            # Compute correct log id for given unstrung bow (logs are 3 -> 10 skipping 6 and 8)
            log_id = 3 + (curr_req // 15) + ((curr_req // 15) // 3) + ((curr_req // 15) // 4)
        resources = [log_id]
    else:
        # Convert dict to array of keys for consistency
        resources = list(product.resources.keys())
    for i in resources:
        if not user.inventory.is_in_inv(i):
            mywin.insert_text_thread(f"You don't have the correct resources to fletch that.", 'warning')
            vars(mywin)['fletch_' + str(button_id)].deselect()
            user.curr_item = 0
            return
    user.curr_item = Items[num]
    mywin.insert_text_thread(f"Selected {user.curr_item.name}.")


def set_craft(num, button_id):
    """Set the user's current item to the selected crafting product in preparation for crafting.

    num = integer, item id \n
    button_id = integer, button's integer suffix \n
    Check resource and level requirements before allowing selection.
    """
    product = Items[num]
    if user.curr_item == Items[num]:
        return
    if user.skills['Crafting'][0] < product.skill_reqs['Crafting']:
        mywin.insert_text_thread(f"Crafting level is too low to craft that.", 'warning')
        vars(mywin)['craft_' + str(button_id)].deselect()
        user.curr_item = 0
        return
    for i in product.resources.keys():
        if not user.inventory.is_in_inv(i):
            mywin.insert_text_thread(f"You don't have the correct resources to craft that.", 'warning')
            vars(mywin)['craft_' + str(button_id)].deselect()
            user.curr_item = 0
            return
    user.curr_item = Items[num]
    mywin.insert_text_thread(f"Selected {user.curr_item.name}.")


def set_bar(bar_id, prefix):
    """Set the user's current item to the selected metal bar in preparation for smelting.

    bar_id = item_id of the metal bar type \n
    prefix = metal name as a string \n
    Check resource and level requirements before allowing selection.
    """
    bar = Items[bar_id]
    if user.curr_item == Items[bar_id]:
        return
    if user.skills['Smithing'][0] < bar.skill_reqs['Smithing']:
        mywin.insert_text_thread(f"Smithing level is too low to smelt that.", 'warning')
        vars(mywin)[prefix + '_bar'].deselect()
        user.curr_item = 0
        return
    for ore in bar.resources.keys():
        if not user.inventory.is_in_inv(ore) or user.inventory.is_in_inv(ore)[1] < bar.resources[ore]:
            mywin.insert_text_thread("You don't have the correct ores to smelt that.", 'warning')
            vars(mywin)[prefix + '_bar'].deselect()
            user.curr_item = 0
            return
    user.curr_item = Items[bar_id]
    mywin.insert_text_thread(f"Selected {user.curr_item.name}.")


def cast_spell(spell):
    """Cast the selected non-combat spell from the spellbook.

    spell = Spell (object) \n
    Currently only teleport spells exist. Check spell and target-area requirements before casting, then remove the
    appropriate number of runes and award experience before executing the area change.
    """
    # Teleports cannot be used in combat
    if user.curr_action == 'combat':
        mywin.insert_text_thread("You can't cast that in combat!", 'warning')
        return
    if user.skills['Magic'][0] < spell.level:
        mywin.insert_text_thread(f"Magic level is too low to cast this spell! ({spell.name})", 'warning')
        return
    if spell.type == 'Teleport':
        failed_check = False
        for skill, req in spell.skill_reqs.items():
            if skill == "Combat":
                if combat_level(user) < req:
                    mywin.insert_text_thread(f"Your combat level is too low for this area. You need lvl "
                                             f"{req}.", 'warning')
                    failed_check = True
            elif user.skills[skill][0] < req:
                mywin.insert_text_thread(f"Your {skill} is too low for this area. You need lvl "
                                         f"{req}.", 'warning')
                failed_check = True
        for q in spell.quest_reqs:
            for q_ in user.quest_flags:
                if q_[0] == q:
                    if q_[1] >= len(Quests[q].objectives):  # = Quest is complete
                        break
                    failed_check = True
                    mywin.insert_text_thread(f"You need to complete {Quests[q].name} before doing that "
                                             f"(Starts at {Quests[q].start}).",
                                             'warning')
                    break
                if q_ == user.quest_flags[-1]:  # = Checked all user quests and not completed
                    failed_check = True
                    mywin.insert_text_thread(f"You need to complete {Quests[q].name} before doing that "
                                             f"(Starts at {Quests[q].start}).",
                                             'warning')
            # Catch case where user has no quests done, so loop never starts
            if len(user.quest_flags) == 0:
                mywin.insert_text_thread(f"You need to complete {Quests[q].name} before doing that "
                                         f"(Starts at {Quests[q].start}).",
                                         'warning')
                failed_check = True
        if not failed_check:
            for rune in spell.runes:
                if not user.inventory.is_in_inv(rune[0]) or user.inventory.is_in_inv(rune[0])[1] < rune[1]:
                    mywin.insert_text_thread(f"Insufficient {Items[rune[0]].name}s remaining!", 'warning')
                    failed_check = True
            if failed_check:
                return 0
            # Remove the correct amount of each rune, clear inventory slot if necessary
            for rune in spell.runes:
                vars(user.inventory)['slot' + str(user.inventory.is_in_inv(rune[0])[0])][1] -= rune[1]
                if vars(user.inventory)['slot' + str(user.inventory.is_in_inv(rune[0])[0])][1] <= 0:
                    mywin.insert_text_thread(f"You use your last {Items[rune[0]].name}!", 'warning')
                    vars(user.inventory)['slot' + str(user.inventory.is_in_inv(rune[0])[0])] = None
                user.inventory.shuffle_inv()
                update_inventory()
            # Finally execute the teleport
            swap_area(spell.area, 'teleport')
            mywin.insert_text_thread(f"Teleporting to {Areas[spell.area].name}...\n", 'good')
            user.skills['Magic'][1] += spell.xp * global_xp_multiplier
    else:
        # Placeholder in the case of non-teleport type spells in future
        user.skills['Magic'][1] += spell.xp * global_xp_multiplier


def set_spell(spell):
    """Set the active combat spell for use with a staff in combat.

    spell = integer, spell id \n
    Only able to select spells for which the user has both the level and runes required.
    """
    spell = Spellbook[spell]
    if Spellbook[user.curr_spell] == spell:
        return
    if user.skills['Magic'][0] < spell.level:
        mywin.insert_text_thread(f"Magic level is too low to cast this spell. ({spell.name})", 'warning')
        vars(mywin)['spell_'+str(user.curr_spell)].invoke()
        return
    for rune in spell.runes:
        if not user.inventory.is_in_inv(rune[0]) or user.inventory.is_in_inv(rune[0])[1] < rune[1]:
            mywin.insert_text_thread("Insufficient runes to cast this spell.", 'warning')
            vars(mywin)['spell_' + str(user.curr_spell)].invoke()
            return
    setattr(user, 'curr_spell', spell.id)
    mywin.insert_text_thread(f"Set current spell to {spell.name}.")


def spell_tab(num):
    """Switch the spellbook interface between combat and utility spell selection.

    num = integer, 0 or 1 \n
    Greys out any spells that are not currently available due to level or rune cost.
    """
    if num == 0:
        if mywin.spell_0.winfo_viewable():
            return
        for i in range(16, 20):
            vars(mywin)['spell_' + str(i)].place_forget()
        for i in range(16):
            vars(mywin)['spell_' + str(i)].place(relx=0.25 + 0.125 * (i % 4), rely=0.65 + 0.075 * (i // 4),
                                                 relwidth=0.125, relheight=0.075)
            if Spellbook[i].level > user.skills['Magic'][0]:
                vars(mywin)['spell_' + str(i)].configure(bg='gray35')
            else:
                for rune in Spellbook[i].runes:
                    if not user.inventory.is_in_inv(rune[0]) or user.inventory.is_in_inv(rune[0])[1] < rune[1]:
                        vars(mywin)['spell_' + str(i)].configure(bg='gray35')
                        break
                    vars(mywin)['spell_' + str(i)].configure(bg='grey')
    else:
        if mywin.spell_16.winfo_viewable():
            return
        for i in range(16):
            vars(mywin)['spell_' + str(i)].place_forget()
        for i in range(16, 20):
            j = i - 16
            vars(mywin)['spell_' + str(i)].place(relx=0.25 + 0.125 * (j % 4), rely=0.65 + 0.1 * (j // 4),
                                                 relwidth=0.125, relheight=0.1)
            if Spellbook[i].level > user.skills['Magic'][0]:
                vars(mywin)['spell_' + str(i)].configure(bg='gray35')
            else:
                for rune in Spellbook[i].runes:
                    if not user.inventory.is_in_inv(rune[0]) or user.inventory.is_in_inv(rune[0])[1] < rune[1]:
                        vars(mywin)['spell_' + str(i)].configure(bg='gray35')
                        break
                    vars(mywin)['spell_' + str(i)].configure(bg='grey')


def bank_tab_swap(num):
    """Switch the active tab that is being used in the bank to the given one."""
    if num > 4 or num < 1 or type(num) != int:
        print("Tab change out of range!")
        return
    user.bank.active_tab = vars(user.bank)['tab_' + str(num)]
    update_bank()


def xp_to_next(skill_index, silence=False):
    """Get and display the remaining experience required for the next level in a particular skill.

    skill_index = integer, 0 to 13, or exact string of skill name \n
    silence = bool, whether to display additional output (default False) \n
    Has the option to work silently without displaying the result to the user, which is useful for some functions.
    """
    diff = 0
    if skill_index == -1:
        # Used for combat level button
        mywin.insert_text_thread(f"Your combat level is {combat_level(user)}. This is based on your combat skills.")
        return
    if type(skill_index) == str:
        # Allow use of precise skill names also
        if user.skills[skill_index][0] >= 99:
            if not silence:
                mywin.insert_text_thread(f"You are at the maximum level for {skill_index}.")
        else:
            diff = level_xp[user.skills[skill_index][0] + 1] - user.skills[skill_index][1]
            if not silence:
                mywin.insert_text_thread(f"You need {round(diff, 2)} experience to reach level "
                                         f"{user.skills[skill_index][0] + 1}.")
    else:
        if list(user.skills.values())[skill_index][0] >= 99:
            if not silence:
                mywin.insert_text_thread(f"You are at the maximum level for {list(user.skills.keys())[skill_index]}.")
        else:
            diff = level_xp[list(user.skills.values())[skill_index][0] + 1] - list(user.skills.values())[skill_index][1]
            if not silence:
                mywin.insert_text_thread(f"You need {round(diff, 2)} experience to reach level "
                                         f"{list(user.skills.values())[skill_index][0] + 1}.")
                if user.flags.get('tut_prog', 250) == 3:
                    user.flags['tut_prog'] = 4
    return diff


def checkinv(item_id):
    """Old function that was considered but never used, could still be expanded for some use in future."""
    if user.inventory.is_in_inv(item_id):
        slot = user.inventory.is_in_inv(item_id)[0]
        quantity = user.inventory.is_in_inv(item_id)[1]
        mywin.insert_text_thread(f"{Items[item_id].name} is in inventory.", 'warning')
        mywin.insert_text_thread(f"It is in slot(s) {slot} with total quantity {quantity}.")
    else:
        mywin.insert_text_thread(f"{Items[item_id].name} not in inventory.", 'warning')


def update_inventory():
    """Refresh the values displayed on the inventory buttons and equipment interface."""
    button_text = []
    for i in range(28):
        if vars(user.inventory)['slot'+str(i)] is None:
            button_text.append("None")
        else:
            button_text.append(Items[vars(user.inventory)['slot'+str(i)][0]].name + "\nx " +
                               str(vars(user.inventory)['slot'+str(i)][1]))
        vars(mywin)['inv_'+str(i)].configure(text=button_text[i])
    mywin.equipment_head.configure(text="Head:\n" + Items[user.equipment.get('Head', 'None')].name)
    mywin.equipment_neck.configure(text="Neck:\n" + Items[user.equipment.get('Neck', 'None')].name)
    mywin.equipment_body.configure(text="Body:\n" + Items[user.equipment.get('Body', 'None')].name)
    mywin.equipment_legs.configure(text="Legs:\n" + Items[user.equipment.get('Legs', 'None')].name)
    mywin.equipment_feet.configure(text="Feet:\n" + Items[user.equipment.get('Feet', 'None')].name)
    mywin.equipment_cape.configure(text="Cape:\n" + Items[user.equipment.get('Cape', 'None')].name)
    mywin.equipment_weapon.configure(text="Weapon:\n" + Items[user.equipment.get('Weapon', 'None')].name)
    mywin.equipment_hands.configure(text="Hands:\n" + Items[user.equipment.get('Hands', 'None')].name)
    mywin.equipment_ammo.configure(text="Ammo:\n"+Items[user.equipment.get('Ammo', ['None', ''])[0]].name+"\nx " +
                                   str(user.equipment.get('Ammo', ['None', '0'])[1]))
    mywin.equipment_shield.configure(text="Shield:\n" + Items[user.equipment.get('Shield', 'None')].name)
    mywin.equipment_ring.configure(text="Ring:\n" + Items[user.equipment.get('Ring', 'None')].name)


def update_skills():
    """Refresh the values displayed on the skill buttons."""
    for i in range(14):
        vars(mywin)['skill_'+str(i)].configure(text=str(list(user.skills.keys())[i]) + "\nLevel: " + str(list(
                            user.skills.values())[i][0]) + "\nExp: " + str(round(list(user.skills.values())[i][1])))


def update_bank():
    """Refresh the values displayed in the bank interface."""
    button_text = []
    for i in range(28):
        if vars(user.bank.active_tab)['slot' + str(i)] is None:
            button_text.append("None")
        else:
            button_text.append(Items[vars(user.bank.active_tab)['slot' + str(i)][0]].name + "\nx " +
                               str(vars(user.bank.active_tab)['slot' + str(i)][1]))
        vars(mywin)['bank_'+str(i)].configure(text=button_text[i])


def update_shop():
    """Refresh the values displayed in the shop interface."""
    button_text = []
    for i in range(28):
        if vars(user.curr_shop.stock)['slot' + str(i)] is None:
            button_text.append("None")
        else:
            button_text.append(Items[vars(user.curr_shop.stock)['slot' + str(i)][0]].name + "\n" +
                               str(Items[vars(user.curr_shop.stock)['slot' + str(i)][0]].value) + " gold")
        vars(mywin)['shop_'+str(i)].configure(text=button_text[i])


def update_spells():
    """Refresh the values displayed in the spellbook interface."""
    # Change greyed out spells to normal if level is reached
    for i in range(16):
        if user.skills['Magic'][0] > Spellbook[i].level:
            vars(mywin)['spell_' + str(i)].configure(bg='grey')
        else:
            break
    for i in range(16, 20):
        if user.skills['Magic'][0] > Spellbook[i].level:
            vars(mywin)['spell_' + str(i)].configure(bg='grey')
        else:
            break


def bank_withdraw(bank_item, slot):
    """Withdraw the selected item from the bank to the inventory.

    bank_item = [item_id, quantity] \n
    slot = integer, 0 to 27
    """
    if user.curr_action == 'banking':
        if bank_item is None:
            return
        success = user.inventory.add_to_inv(bank_item[0], min(bank_item[1],
                                            user.bank.quant))
        if success[1] == 'warning':
            # Inventory is full either before or during the withdrawal process
            added = success[2]
            if added == 0:
                mywin.insert_text_thread(f"Inventory full!", 'warning')
                return
            mywin.insert_text_thread(f"Withdrew {added} {Items[bank_item[0]].name}.")
            vars(user.bank.active_tab)['slot' + str(slot)][1] -= added
            if vars(user.bank.active_tab)['slot' + str(slot)][1] <= 0:
                vars(user.bank.active_tab)['slot' + str(slot)] = None
            user.inventory.shuffle_inv()
            user.bank.active_tab.shuffle_inv()
            update_bank()
            update_inventory()
            return
        mywin.insert_text_thread(f"Withdrew {min(vars(user.bank.active_tab)['slot'+str(slot)][1], user.bank.quant)} "
                                 f"{Items[bank_item[0]].name}.")
        vars(user.bank.active_tab)['slot'+str(slot)][1] -= min(vars(user.bank.active_tab)['slot'+str(slot)][1],
                                                               user.bank.quant)
        if vars(user.bank.active_tab)['slot'+str(slot)][1] <= 0:
            vars(user.bank.active_tab)['slot' + str(slot)] = None
        user.inventory.shuffle_inv()
        user.bank.active_tab.shuffle_inv()
        update_bank()
        update_inventory()
        return


def bank_full():
    """Check if the bank is currently full."""
    if user.bank.tab_1.slot27 is not None and user.bank.tab_2.slot27 is not None and user.bank.tab_3.slot27 is not None\
            and user.bank.tab_4.slot27 is not None:
        return True
    return False


def bank_deposit_all():
    """Attempt to deposit the user's entire inventory into the bank."""
    if user.curr_action == 'banking':
        pre_quant = user.bank.quant
        pre_free = user.inventory.free_spaces()
        user.bank.quant = max(50, user.inventory.max_stack())
        for i in range(27, -1, -1):
            # Try to deposit each item stack from inventory
            if vars(user.inventory)['slot'+str(i)] is None:
                continue
            interact_item(vars(user.inventory)['slot'+str(i)], i, True)
            if bank_full():
                post_free = user.inventory.free_spaces()
                mywin.insert_text_thread(f"Bank full! Deposited {post_free - pre_free} item stacks.", 'warning')
                break
        post_free = user.inventory.free_spaces()
        mywin.insert_text_thread(f"Deposited {post_free - pre_free} item stacks.")
        user.bank.quant = pre_quant


def sell_all():
    """Attempt to sell the user's entire inventory."""
    if user.curr_action == 'shopping':
        pre_quant = user.bank.quant
        pre_free = user.inventory.free_spaces()
        if not user.inventory.is_in_inv(0):
            pre_gold = 0
        else:
            pre_gold = user.inventory.is_in_inv(0)[1]
        user.bank.quant = max(50, user.inventory.max_stack())
        for i in range(27, -1, -1):
            # Try to sell each item stack from inventory
            if vars(user.inventory)['slot'+str(i)] is None or vars(user.inventory)['slot'+str(i)][0] == 0:
                continue
            sell_item([Items[vars(user.inventory)['slot'+str(i)][0]], vars(user.inventory)['slot'+str(i)][1], i], True)
        post_free = user.inventory.free_spaces()
        mywin.insert_text_thread(f"Sold {post_free-pre_free} item stacks for {user.inventory.slot0[1]-pre_gold} gold.")
        user.bank.quant = pre_quant


def interact_item(inv_item, slot, all_=False):
    """Display the possible actions for the selected item.

    inv_item = [item_id, quantity] \n
    slot = integer, 0 to 27 \n
    all_ = bool, whether being called from bank_deposit_all or not \n
    In the case of banking, instantly deposit the item instead.
    """
    if user.curr_action == 'banking':
        # Attempt to deposit the chosen quantity of the selected item
        if inv_item is None:
            return
        success = user.bank.add_to_inv(inv_item[0], min(inv_item[1], user.bank.quant))
        if not success:
            mywin.insert_text_thread("All bank tabs full! No items added.", 'warning')
            return
        # If succeeded, remove the correct quantity from inventory and clear the slot if needed
        sold = min(vars(user.inventory)['slot' + str(slot)][1], user.bank.quant)
        vars(user.inventory)['slot'+str(slot)][1] -= sold
        if vars(user.inventory)['slot'+str(slot)][1] <= 0:
            vars(user.inventory)['slot' + str(slot)] = None
        if not Items[inv_item[0]].stackable and user.inventory.is_in_inv(inv_item[0]) and user.bank.quant > 1:
            # If attempting to deposit more than one non-stackable item
            sold = 1
            if type(user.inventory.is_in_inv(inv_item[0])[0]) == int:
                # If there is only one more to deposit (hence there were 2 originally)
                vars(user.inventory)['slot' + str(user.inventory.is_in_inv(inv_item[0])[0])] = None
                user.bank.add_to_inv(inv_item[0])
                sold += 1
            else:
                for i in user.inventory.is_in_inv(inv_item[0])[0]:
                    if sold == user.bank.quant:
                        break
                    vars(user.inventory)['slot' + str(i)] = None
                    sold += 1
                    user.bank.add_to_inv(inv_item[0])
            if not all_:
                # Allow limiting of the text output when using a function like bank_deposit_all
                mywin.insert_text_thread(f"Deposited {sold} {Items[inv_item[0]].name}")
        else:
            if not all_:
                mywin.insert_text_thread(f"Deposited {sold} {Items[inv_item[0]].name}.")
        user.inventory.shuffle_inv()
        user.bank.active_tab.shuffle_inv()
        update_bank()
        update_inventory()
        i = 1
        # Change the active tab to the one where items were deposited eg. a stack existed in a different tab
        for j in range(1, 5):
            if vars(user.bank)['tab_'+str(j)] == user.bank.active_tab:
                i = j
        vars(mywin)['tab_'+str(i)].invoke()
        return
    if user.curr_action == 'shopping':
        # Display the shop specific actions instead
        if inv_item is None:
            return
        item = Items[inv_item[0]]
        quantity = inv_item[1]
        user.inventory.curr_selection = [item, quantity, slot]
        mywin.value_item.place(relx=0.825, rely=0.6, relwidth=0.1, relheight=0.05)
        mywin.sell_item.place(relx=0.825, rely=0.8, relwidth=0.1, relheight=0.05)
        mywin.selected_inv_item.configure(text=Items[inv_item[0]].name)
        mywin.selected_inv_item.place(relx=0.75, rely=0.55, relwidth=0.25, relheight=0.05)
        return
    if inv_item is None:
        user.inventory.curr_selection = None
        mywin.equip_item.place_forget()
        mywin.drop_item.place_forget()
        mywin.examine_item.place_forget()
        mywin.crafting.place_forget()
        mywin.fletching.place_forget()
        mywin.burn.place_forget()
        mywin.selected_inv_item.place_forget()
        return
    item = Items[inv_item[0]]
    quantity = inv_item[1]
    mywin.selected_inv_item.configure(text=Items[inv_item[0]].name)
    mywin.selected_inv_item.place(relx=0.75, rely=0.55, relwidth=0.25, relheight=0.05)
    mywin.drop_item.place(relx=0.825, rely=0.6, relwidth=0.1, relheight=0.05)
    mywin.examine_item.place(relx=0.825, rely=0.8, relwidth=0.1, relheight=0.05)
    user.inventory.curr_selection = [item, quantity, slot]
    if item.equippable:
        mywin.equip_item.place(relx=0.825, rely=0.7, relwidth=0.1, relheight=0.05)
    else:
        mywin.equip_item.place_forget()
    if Items[inv_item[0]].examine == '':
        mywin.examine_item.place_forget()
    if Items[inv_item[0]].burn:
        mywin.burn.place(relx=0.825, rely=0.7, relwidth=0.1, relheight=0.05)
    else:
        mywin.burn.place_forget()
    if Items[inv_item[0]].food != 0:
        mywin.eat.place(relx=0.825, rely=0.7, relwidth=0.1, relheight=0.05)
    else:
        mywin.eat.place_forget()
    if Items[inv_item[0]].skill_reqs.get('Fletching', -1) != -1:
        mywin.fletching.place(relx=0.825, rely=0.9, relwidth=0.1, relheight=0.05)
    else:
        mywin.fletching.place_forget()
    if inv_item[0] in range(175, 181):
        mywin.crafting.place(relx=0.825, rely=0.9, relwidth=0.1, relheight=0.05)
    else:
        mywin.crafting.place_forget()


def calc_equip_stats():
    """Compute the equipment stats that are used for combat and shown in the equipment interface.

    Stats are based on the items that the user currently has equipped.
    """
    att_speed = Items[user.equipment.get("Weapon", 82)].att_speed
    acc_rating_melee = acc_rating_ranged = acc_rating_magic = str_bonus_melee = str_bonus_ranged = \
        str_bonus_magic = melee_def = ranged_def = magic_def = 0
    for item_id in user.equipment.values():
        if not isinstance(item_id, list):
            item = Items[item_id]
        else:
            item = Items[item_id[0]]
        acc_rating_melee += item.acc_rating_melee
        acc_rating_ranged += item.acc_rating_ranged
        acc_rating_magic += item.acc_rating_magic
        str_bonus_melee += item.str_bonus_melee
        str_bonus_ranged += item.str_bonus_ranged
        str_bonus_magic += item.str_bonus_magic
        melee_def += item.melee_def
        ranged_def += item.ranged_def
        magic_def += item.magic_def
    return [att_speed, acc_rating_melee, acc_rating_ranged, acc_rating_magic, str_bonus_melee, str_bonus_ranged,
            str_bonus_magic, melee_def, ranged_def, magic_def]


def display_equip_stats():
    """Display the equipment stats from calc_equip_stats()."""
    equip_stats = calc_equip_stats()
    mywin.att_speed.configure(text="Attack speed(ms): "+str(equip_stats[0]))
    mywin.acc_melee.configure(text="Melee accuracy: "+str(equip_stats[1]))
    mywin.acc_ranged.configure(text="Ranged accuracy: "+str(equip_stats[2]))
    mywin.acc_magic.configure(text="Magic accuracy: "+str(equip_stats[3]))
    mywin.str_melee.configure(text="Melee strength: "+str(equip_stats[4]))
    mywin.str_ranged.configure(text="Ranged strength: "+str(equip_stats[5]))
    mywin.str_magic.configure(text="Magic strength: "+str(equip_stats[6]))
    mywin.melee_def.configure(text="Melee defence: "+str(equip_stats[7]))
    mywin.ranged_def.configure(text="Ranged defence: "+str(equip_stats[8]))
    mywin.magic_def.configure(text="Magic defence: "+str(equip_stats[9]))

    mywin.att_speed.place(relx=0.76, rely=0.6, relwidth=0.2, relheight=0.035)
    mywin.acc_melee.place(relx=0.76, rely=0.635, relwidth=0.2, relheight=0.035)
    mywin.acc_ranged.place(relx=0.76, rely=0.67, relwidth=0.2, relheight=0.035)
    mywin.acc_magic.place(relx=0.76, rely=0.705, relwidth=0.2, relheight=0.035)
    mywin.str_melee.place(relx=0.76, rely=0.74, relwidth=0.2, relheight=0.035)
    mywin.str_ranged.place(relx=0.76, rely=0.775, relwidth=0.2, relheight=0.035)
    mywin.str_magic.place(relx=0.76, rely=0.81, relwidth=0.2, relheight=0.035)
    mywin.melee_def.place(relx=0.76, rely=0.845, relwidth=0.2, relheight=0.035)
    mywin.ranged_def.place(relx=0.76, rely=0.88, relwidth=0.2, relheight=0.035)
    mywin.magic_def.place(relx=0.76, rely=0.915, relwidth=0.2, relheight=0.035)


def equip_item(item):
    """Attempt to equip the selected item from the inventory.

    item = [item, quantity, inv_slot] \n
    Check skill requirements, and ensure there is space in the inventory in special cases.
    """
    # Tutorial specific locks on certain actions to simplify the tutorial
    if user.flags.get('tut_prog', 250) <= 7:
        mywin.insert_text_thread(f"You don't know how to equip this just yet.", 'warning')
        return
    if user.flags.get('tut_prog', 250) == 9 and item[0].slot == 'Weapon' and user.equipment.get('Weapon', 0) == 83:
        if user.curr_action == 'combat':
            mywin.insert_text_thread(f"You should keep your Bronze sword equipped for now.", 'warning')
            return
    if user.flags.get('tut_prog', 250) == 11 and item[0].slot == 'Weapon' and user.equipment.get('Weapon', 0) == 151:
        if user.curr_action == 'combat':
            mywin.insert_text_thread(f"You should keep your Shortbow equipped for now.", 'warning')
            return
    if user.flags.get('tut_prog', 250) == 13 and item[0].slot == 'Weapon' and user.equipment.get('Weapon', 0) == 76:
        if user.curr_action == 'combat':
            mywin.insert_text_thread(f"You should keep your staff equipped for now.", 'warning')
            return
    if item[0].equip_reqs is not None:
        failed_equip = False
        # Check requirements to equip item
        for skill, req in item[0].equip_reqs.items():
            if user.skills[skill][0] < req:
                mywin.insert_text_thread(f"Your {skill} level is too low to wear that.", 'warning')
                mywin.insert_text_thread(f"{item[0].name} requires {req} {skill} to equip.", 'warning')
                failed_equip = True
        if failed_equip:
            return
    if item[0].slot == "Ammo":
        # Ammo slot takes a list instead of a value
        old_item = (user.equipment.get("Ammo", [None, None])[0], user.equipment.get("Ammo", [1, 1])[1])
        if old_item[0] is not None and item[0].id == old_item[0]:
            # Add to existing ammo instead of replacing it
            user.equipment["Ammo"] = [item[0].id, item[1] + old_item[1]]
            vars(user.inventory)['slot' + str(item[2])] = None
        else:
            user.equipment["Ammo"] = [item[0].id, item[1]]
            vars(user.inventory)['slot' + str(item[2])] = None
            user.inventory.add_to_inv(old_item[0], old_item[1])
        mywin.equip_item.place_forget()
        mywin.drop_item.place_forget()
        mywin.examine_item.place_forget()
        mywin.selected_inv_item.place_forget()
        user.inventory.shuffle_inv()
        update_inventory()
        mywin.insert_text_thread(f"Equipped {item[0].name}.")
        return
    # Make sure to remove any shield that might be equipped when equipping a two-handed item
    if item[0].two_handed and user.equipment.get('Shield', 1) != 1 and user.equipment.get('Weapon', 0) != 0:
        if user.inventory.slot27 is not None:
            # In the event that the inventory is full and both weapon and shield are currently equipped
            mywin.insert_text_thread("Inventory is too full to equip that right now.")
            return
        user.inventory.add_to_inv(user.equipment['Shield'])
        del user.equipment['Shield']
    old_item = user.equipment.get(item[0].slot, None)
    user.equipment[item[0].slot] = item[0].id
    if item[0].slot == "Weapon":
        # Equipping weapon sets default attack style based on combat style to prevent incorrect experience gain
        if item[0].att_style == "Melee":
            set_style("Accurate")
        elif item[0].att_style == "Ranged":
            set_style("Accurate(Ranged)")
        elif item[0].att_style == "Magic":
            set_style("Accurate(Magic)")
        style_swap()
    if item[0].slot == "Shield":
        # Remove two-handed weapon when equipping a shield
        if "Weapon" in user.equipment and Items[user.equipment["Weapon"]].two_handed:
            vars(user.inventory)['slot' + str(item[2])] = None
            user.inventory.add_to_inv(user.equipment["Weapon"])
            del user.equipment['Weapon']
            mywin.equip_item.place_forget()
            mywin.drop_item.place_forget()
            mywin.examine_item.place_forget()
            user.inventory.shuffle_inv()
            update_inventory()
            mywin.insert_text_thread(f"Equipped {item[0].name}.")
            return
    if item[1] == 1:
        vars(user.inventory)['slot' + str(item[2])] = None
        user.inventory.add_to_inv(old_item)
    else:
        # In case that the equipped item is stackable (currently not possible)
        item[1] -= 1
        vars(user.inventory)['slot' + str(item[2])] = item[0:2]
        user.inventory.add_to_inv(old_item)
    mywin.equip_item.place_forget()
    mywin.drop_item.place_forget()
    mywin.examine_item.place_forget()
    mywin.selected_inv_item.place_forget()
    user.inventory.shuffle_inv()
    update_inventory()
    mywin.insert_text_thread(f"Equipped {item[0].name}.")


def unequip_item(slot):
    """Attempt to un-equip the selected item from equipment. Ensure there is space in the inventory.

     slot = equipment_slot, ( eg. 'hands', 'ammo', 'weapon')
     """
    if user.flags.get('tut_prog', 250) == 9 and slot == 'Weapon' and user.equipment.get('Weapon', 0) == 83:
        if user.curr_action == 'combat':
            mywin.insert_text_thread(f"You should keep that equipped for now.", 'warning')
            return
    if user.flags.get('tut_prog', 250) == 11:
        if slot == 'Weapon' and user.equipment.get('Weapon', 0) == 151 or slot == 'Ammo':
            if user.curr_action == 'combat':
                mywin.insert_text_thread(f"You should keep that equipped for now.", 'warning')
                return
    if user.flags.get('tut_prog', 250) == 13 and slot == 'Weapon' and user.equipment.get('Weapon', 0) == 76:
        if user.curr_action == 'combat':
            mywin.insert_text_thread(f"You should keep that equipped for now.", 'warning')
            return
    if user.equipment.get(slot, 0) == 0:
        return
    # Check if inventory is full
    if user.inventory.slot27 is not None and slot != "Ammo":
        # Check for existing stacks of the item in inventory. If none, then no room to un-equip
        if Items[user.equipment[slot]].stackable and not user.inventory.is_in_inv(user.equipment[slot]) or not \
                Items[user.equipment[slot]].stackable:
            mywin.insert_text_thread("No room in inventory to do that.", 'warning')
            return
    if slot == "Ammo":
        # Check for existing stack of the ammo in a full inventory. If none found, then no room to un-equip
        if user.inventory.slot27 is not None and not user.inventory.is_in_inv(user.equipment["Ammo"][0]):
            mywin.insert_text_thread("No room in inventory to do that.", 'warning')
            return
        # By this point there is room to un-equip the item, so just add/remove the correct items in the correct places
        item = [user.equipment[slot][0], user.equipment[slot][1]]
        del user.equipment[slot]
        user.inventory.add_to_inv(item[0], item[1])
        update_inventory()
        mywin.insert_text_thread(f"Unequipped {Items[item[0]].name}.")
        return
    # Set the default attack style when removing weapon (eg. removing a staff so need the style changed to a melee one)
    if slot == "Weapon" and user.att_style not in ['Accurate', 'Aggressive', 'Defensive']:
        user.att_style = 'Accurate'
    item = user.equipment[slot]
    mywin.insert_text_thread(f"Unequipped {Items[item].name}.")
    del user.equipment[slot]
    user.inventory.add_to_inv(item)
    update_inventory()
    display_equip_stats()


def drop_item(item):
    """Drop the selected item, deleting it from the inventory permanently. Stacks of items are dropped all at once.

    item = [item, quantity, slot]
    """
    # Dropping is disabled during most of the tutorial to prevent soft-locking etc.
    if user.flags.get('tut_prog', 250) <= 31:
        mywin.insert_text_thread(f"You shouldn't drop this just yet.", 'warning')
        return
    # Unique quest items may not be dropped or sold. They can only be obtained at specific points of a quest, so this
    # ensures that the relevant quest can be completed fully
    if item[0].quest_item is not None:
        mywin.insert_text_thread(f"You can't drop that, you may need it.", 'warning')
        return
    mywin.insert_text_thread(f"Dropped {item[0].name}.", 'warning')
    vars(user.inventory)['slot' + str(item[2])] = None
    user.inventory.shuffle_inv()
    # Allow smooth multi-dropping of same item
    if inv_item := user.inventory.is_in_inv(item[0].id):
        slot = inv_item[0][-1] if type(inv_item[0]) != int else inv_item[0]
        user.inventory.curr_selection = [item[0], 1, slot]
        print(user.inventory.curr_selection)
        user.inventory.shuffle_inv()
        update_inventory()
        return
    # Clear all the context actions for the dropped item and deselects it
    mywin.equip_item.place_forget()
    mywin.drop_item.place_forget()
    mywin.examine_item.place_forget()
    mywin.fletching.place_forget()
    mywin.crafting.place_forget()
    mywin.burn.place_forget()
    mywin.selected_inv_item.place_forget()
    update_inventory()


def value_item(item):
    """Display the value of an item or stack of items to the user via the game console. Value is stored in the item.

    item = [item, quantity, slot]
    """
    value = int(item[0].value * 0.6)
    if item[0].id == 0:
        # Cannot sell gold coins
        mywin.insert_text_thread("You can't sell that.", 'warning')
        return
    if item[1] > 1:
        mywin.insert_text_thread(f"{item[0].name} is worth {value} gold coins. "
                                 f"The whole stack is worth {item[1] * value} gold coins.")
    else:
        mywin.insert_text_thread(f"{item[0].name} is worth {value} gold coins.")


def sell_item(item, all_=False):
    """Sell the selected item to the shop.

    item = [item, quantity, slot] \n
    all_ = bool, whether function is being called from sell_all or not \n
    Can sell multiple via the quantity options. Certain items are not to be sold, like coins.
    """
    if item[0].id == 0:
        mywin.insert_text_thread("You can't sell that.", 'warning')
        return
    if item[0].quest_item is not None:
        mywin.insert_text_thread(f"You can't sell that, you may need it.", 'warning')
        return
    value = int(item[0].value * 0.6)
    total = value * min(user.bank.quant, item[1])
    # For stacks of items, simply remove the correct amount and give user the correct gold
    if item[0].stackable:
        user.inventory.remove_item(item[0].id, user.bank.quant)
        # If selling whole stack, clear context options. Otherwise alter the stored quantity only
        if not user.inventory.is_in_inv(item[0].id):
            mywin.value_item.place_forget()
            mywin.sell_item.place_forget()
            mywin.selected_inv_item.place_forget()
        else:
            user.inventory.curr_selection = [item[0], item[1] - user.bank.quant, item[2]]
    else:
        # If selling all of a particular item, clear context options
        if user.inventory.is_in_inv(item[0].id)[1] <= user.bank.quant:
            mywin.value_item.place_forget()
            mywin.sell_item.place_forget()
            mywin.selected_inv_item.place_forget()
            vars(user.inventory)['slot' + str(item[2])] = None
        else:
            # If keeping context options, re-assign current slot to next copy of item in inventory
            vars(user.inventory)['slot' + str(item[2])] = None
            inv_item = user.inventory.is_in_inv(item[0].id)
            slot = inv_item[0][-1] if type(inv_item[0]) != int else inv_item[0]
            user.inventory.curr_selection = [item[0], 1, slot]
    # Have sold either part of a stack or a single non-stackable item by now, so give gold to the user
    user.inventory.add_to_inv(0, total)
    # Now deal with selling copies of the item from various different slots (non-stackable only) if required
    if not item[0].stackable and user.inventory.is_in_inv(item[0].id) and user.bank.quant > 1:
        sold = 1
        if type(user.inventory.is_in_inv(item[0].id)[0]) == int:
            # Here there is only one more to sell, so no loop needed
            vars(user.inventory)['slot' + str(user.inventory.is_in_inv(item[0].id)[0])] = None
            user.inventory.add_to_inv(0, total)
            sold += 1
        else:
            # Loop backwards through all slots that contain the item until enough have been sold
            for i in user.inventory.is_in_inv(item[0].id)[0][::-1]:
                if sold == user.bank.quant:
                    break
                vars(user.inventory)['slot'+str(i)] = None
                user.inventory.add_to_inv(0, total)
                sold += 1
        if not all_:
            mywin.insert_text_thread(f"Sold {sold} {item[0].name} for {sold * total} gold.")
        # Set the selected item to a remaining copy of the sold item if any still remain
        if inv_item := user.inventory.is_in_inv(item[0].id):
            slot = inv_item[0][-1] if type(inv_item[0]) != int else inv_item[0]
            user.inventory.curr_selection = [item[0], 1, slot]
    else:
        if not all_:
            mywin.insert_text_thread(f"Sold {min(user.bank.quant, item[1])} {item[0].name} for {total} gold.")
    user.inventory.shuffle_inv()
    update_inventory()


def shop_buy(slot):
    """Attempt to purchase an item from the shop.

    slot = integer, 0 to 27 \n
    When buying more of an item than the user can afford, purchase the maximum amount they can afford.
    When buying multiple non-stackable items that would fill the inventory, instead the maximum amount that
    will fit are purchased.
    """
    shop_item = vars(user.curr_shop.stock)['slot'+str(slot)][0]
    free_spaces = user.inventory.free_spaces()
    if user.inventory.is_in_inv(0):
        gold = user.inventory.is_in_inv(0)
        # Check that the user has enough gold for the entire purchase
        if (Items[shop_item].stackable and gold[1] >= Items[shop_item].value * user.bank.quant) or (
                not Items[shop_item].stackable and gold[1] >= Items[shop_item].value * min(
                                                                                        free_spaces, user.bank.quant)):
            if (user.inventory.slot27 is not None and not user.inventory.is_in_inv(shop_item)) or (
                    user.inventory.slot27 is not None and not Items[shop_item].stackable):
                mywin.insert_text_thread("Inventory is too full to buy that.", 'warning')
                return
            if not Items[shop_item].stackable:
                # If the quantity being bought would overfill inventory, only buy enough to fill it
                if user.bank.quant > 1:
                    num_buy = min(free_spaces, user.bank.quant)
                    user.inventory.add_to_inv(shop_item, num_buy)
                    mywin.insert_text_thread(f"Bought {num_buy} {Items[shop_item].name}.")
                    user.inventory.remove_item(0, Items[shop_item].value * num_buy)
                    # If the purchase causes user to run out of gold, clear context options in case gold was selected
                    if not user.inventory.is_in_inv(0):
                        mywin.value_item.place_forget()
                        mywin.sell_item.place_forget()
                        mywin.selected_inv_item.place_forget()
                    update_inventory()
                    return
            user.inventory.add_to_inv(shop_item, user.bank.quant)
            mywin.insert_text_thread(f"Bought {user.bank.quant} {Items[shop_item].name}.")
            user.inventory.remove_item(0, Items[shop_item].value * user.bank.quant)
            # If the purchase causes user to run out of gold, clear context options in case gold was selected
            if not user.inventory.is_in_inv(0):
                mywin.value_item.place_forget()
                mywin.sell_item.place_forget()
                mywin.selected_inv_item.place_forget()
            update_inventory()
            return
        else:
            # This section defines behaviour for over-quantity purchases to instead buy the max affordable amount
            if Items[shop_item].stackable:
                if user.inventory.slot27 is not None and not user.inventory.is_in_inv(shop_item):
                    mywin.insert_text_thread("Inventory is too full to buy that.", 'warning')
                    return
                # Max amount that user can afford
                num_buy = gold[1] // Items[shop_item].value
                if num_buy == 0:
                    mywin.insert_text_thread("You can't afford that.", 'warning')
                    return
                user.inventory.add_to_inv(shop_item, num_buy)
                mywin.insert_text_thread(f"Bought {num_buy} {Items[shop_item].name}.")
                user.inventory.remove_item(0, Items[shop_item].value * num_buy)
                # If the purchase causes user to run out of gold, clear context options in case gold was selected
                if not user.inventory.is_in_inv(0):
                    mywin.value_item.place_forget()
                    mywin.sell_item.place_forget()
                    mywin.selected_inv_item.place_forget()
                update_inventory()
                return
            else:
                if user.inventory.slot27 is not None:
                    mywin.insert_text_thread("Inventory is too full to buy that.3", 'warning')
                    return
                # Max amount that user can afford
                num_buy = gold[1] // Items[shop_item].value
                if num_buy == 0:
                    mywin.insert_text_thread("You can't afford that.", 'warning')
                    return
                # If the quantity being bought would overfill inventory, only buy enough to fill it
                num_buy = min(free_spaces, num_buy)
                user.inventory.add_to_inv(shop_item, num_buy)
                mywin.insert_text_thread(f"Bought {num_buy} {Items[shop_item].name}.")
                user.inventory.remove_item(0, Items[shop_item].value * num_buy)
                # If the purchase causes user to run out of gold, clear context options in case gold was selected
                if not user.inventory.is_in_inv(0):
                    mywin.value_item.place_forget()
                    mywin.sell_item.place_forget()
                    mywin.selected_inv_item.place_forget()
                update_inventory()
                return
    mywin.insert_text_thread("You can't afford that.", 'warning')


def combat_thread(enemy):
    """Create and launch a thread for the combat function.

    enemy = Enemy object \n
    Non-instant functions must run in a thread to prevent the app from stalling.
    """
    t = Thread(target=combat, args=(enemy,), daemon=True)
    t.start()


def flash_thread(button):
    """Create and launch a thread for the flash_button function.

    button = string, button name \n
    Non-instant functions must run in a thread to prevent the app from stalling.
    """
    t = Thread(target=flash_button, args=(button,), daemon=True)
    t.start()


def regen():
    """Provide the user with passive health regeneration over time. Current rate depends on Hitpoints level."""
    time_elapsed = 0
    while running:
        time.sleep(0.5)
        time_elapsed += 0.5
        if int(time_elapsed) % 60 == 0 and time_elapsed == int(time_elapsed):
            # Base regen rate of 1 per minute + 5% of current hitpoints level
            hp_regen_rate = (user.skills['Hitpoints'][0] // 20) + 1
            user.health = min(user.health + hp_regen_rate, user.skills['Hitpoints'][0])
            mywin.hp_bar.configure(text=f"HP: {str(user.health)}")
            if user.curr_action == "combat":
                # Maintain the dynamic colouring of HP bar during combat relative to enemy damage potential
                if user.health <= max(0.2 * user.skills['Hitpoints'][0],
                                      max_hit(user.curr_area.enemies[user.curr_area.selection])):
                    mywin.hp_bar.configure(text="HP: " + str(user.health), fg='red')
                else:
                    mywin.hp_bar.configure(text="HP: " + str(user.health), fg='black')
            elif user.health <= 0.2 * user.skills['Hitpoints'][0]:
                mywin.hp_bar.configure(text="HP: " + str(user.health), fg='red')
            else:
                mywin.hp_bar.configure(text="HP: " + str(user.health), fg='black')


def skill_thread(skill_obj):
    """Create and launch a thread for the skilling function.

    skill_obj = SkillObj object \n
    Non-instant functions must run in a thread to prevent the app from stalling.
    """
    t = Thread(target=skilling, args=(skill_obj,), daemon=True)
    t.start()


def cook_thread():
    """Create and launch a thread for the cooking function.

    Non-instant functions must run in a thread to prevent the app from stalling.
    """
    t = Thread(target=cook, daemon=True)
    t.start()


def smelt_thread():
    """Create and launch a thread for the smelting function.

    Non-instant functions must run in a thread to prevent the app from stalling.
    """
    t = Thread(target=smelt, daemon=True)
    t.start()


def smith_thread():
    """Create and launch a thread for the smithing function.

    Non-instant functions must run in a thread to prevent the app from stalling.
    """
    t = Thread(target=smith, daemon=True)
    t.start()


def fletch_thread():
    """Create and launch a thread for the fletching function.

     Non-instant functions must run in a thread to prevent the app from stalling.
     """
    t = Thread(target=fletch, daemon=True)
    t.start()


def craft_thread():
    """Create and launch a thread for the crafting function.

    Non-instant functions must run in a thread to prevent the app from stalling.
    """
    t = Thread(target=craft, daemon=True)
    t.start()


def fire_thread(log):
    """Create and launch a thread for the fire function unless one already exists.

    log = Items[log_id] \n
    Non-instant functions must run in a thread to prevent the app from stalling.
    """
    global fire_timer
    if fire_timer > 0:
        fire_timer = ((log.skill_reqs['Firemaking'] // 15) + 1) * 60
    else:
        t = Thread(target=fire, args=(log,), daemon=True)
        t.start()


def open_bank():
    """Open the banking interface.

    User must be idle to use the bank to avoid complications. No other interfaces can be used while the bank is open,
    and all activities are blocked.
    """
    if user.curr_action != 'idle' and user.curr_action != 'banking':
        mywin.insert_text_thread("Please stop what you're doing before opening the bank.", 'warning')
        return
    if user.curr_action == 'banking':
        # Close the bank if already open
        user.curr_action = 'idle'
        mywin.list_bank.configure(text="Bank")
        list_inv()
        # Clear the bank interface
        for i in range(28):
            vars(mywin)['bank_'+str(i)].place_forget()
            if 0 < i < 5:
                vars(mywin)['tab_'+str(i)].place_forget()
                vars(mywin)['quantity_'+str(i)].place_forget()
        mywin.quantity_5.place_forget()
        mywin.quantity_label.place_forget()
        mywin.bank_deposit_all.place_forget()
        # Reset the position of the console
        mywin.main_console.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.3)

    else:
        update_bank()
        # Close the inventory if open to make list_inv open it regardless of current state
        if mywin.inv_0.winfo_viewable():
            mywin.equip_item.place_forget()
            mywin.drop_item.place_forget()
            mywin.crafting.place_forget()
            mywin.fletching.place_forget()
            mywin.burn.place_forget()
            mywin.examine_item.place_forget()
            for i in range(28):
                vars(mywin)['inv_' + str(i)].place_forget()
        # Force open the inventory alongside the bank interface
        list_inv()
        user.curr_action = 'banking'
        mywin.list_bank.configure(text="Close bank")
        # Open the bank interface
        for i in range(28):
            vars(mywin)['bank_'+str(i)].place(relx=0.25+0.125*(i % 4), rely=0.1 + 0.05*(i // 4),
                                              relwidth=0.125, relheight=0.05)
            if 0 < i < 5:
                vars(mywin)['tab_' + str(i)].place(relx=0.175, rely=0.1 + 0.05*(i-1), relwidth=0.06, relheight=0.05)
                if i != 4:
                    vars(mywin)['quantity_' + str(i)].place(relx=0.785 + 0.05*(i-1), rely=0.15, relwidth=0.05,
                                                            relheight=0.05)
        mywin.quantity_4.place(relx=0.81, rely=0.2, relwidth=0.05, relheight=0.05)
        mywin.quantity_5.place(relx=0.86, rely=0.2, relwidth=0.05, relheight=0.05)
        mywin.bank_deposit_all.place(relx=0.785, rely=0.25, relwidth=0.15, relheight=0.1)
        mywin.quantity_label.place(relx=0.76, rely=0.1, relwidth=0.2, relheight=0.05)
        # Move console to a smaller but readable position below the bank
        mywin.main_console.place(relx=0.25, rely=0.45, relwidth=0.5, relheight=0.15)
        mywin.main_console.see(END)
        mywin.insert_text_thread(f"You open the bank.\n")
        if user.flags.get('tut_prog', 250) == 14:
            user.flags['tut_prog'] = 15


def open_shop():
    """Open the shopping interface.

    User must be idle to use the shop to avoid complications. No other interfaces can be used while the shop is open,
    and all activities are blocked.
    """
    if user.curr_action != 'idle' and user.curr_action != 'shopping':
        return
    if user.curr_action == 'idle':
        # Close inventory if open, clear all interfaces and then force open inventory
        if mywin.inv_0.winfo_viewable():
            mywin.equip_item.place_forget()
            mywin.drop_item.place_forget()
            mywin.crafting.place_forget()
            mywin.fletching.place_forget()
            mywin.burn.place_forget()
            mywin.examine_item.place_forget()
            for i in range(28):
                vars(mywin)['inv_' + str(i)].place_forget()
        list_inv()
        user.curr_action = 'shopping'
        mywin.open_shop.place_forget()
        mywin.main_input.place_forget()
        mywin.sell_item.place_forget()
        mywin.value_item.place_forget()
        mywin.close_shop.place(relx=0.1, rely=0.3, relwidth=0.15, relheight=0.05)
        j = 0
        update_shop()
        # Open shop interface
        while j != 28 and vars(user.curr_shop.stock)['slot'+str(j)] is not None:
            vars(mywin)['shop_'+str(j)].place(relx=(0.25 + 0.125*(j % 4)), rely=(0.1 + 0.05*(j // 4)), relwidth=0.125,
                                              relheight=0.05)
            j += 1
        mywin.quantity_1.place(relx=0.785, rely=0.15, relwidth=0.05, relheight=0.05)
        mywin.quantity_2.place(relx=0.835, rely=0.15, relwidth=0.05, relheight=0.05)
        mywin.quantity_3.place(relx=0.885, rely=0.15, relwidth=0.05, relheight=0.05)
        mywin.quantity_4.place(relx=0.81, rely=0.2, relwidth=0.05, relheight=0.05)
        mywin.quantity_5.place(relx=0.86, rely=0.2, relwidth=0.05, relheight=0.05)
        mywin.quantity_label.place(relx=0.76, rely=0.1, relwidth=0.2, relheight=0.05)
        mywin.shop_sell_all.place(relx=0.785, rely=0.25, relwidth=0.15, relheight=0.1)
        # Move console like in bank interface
        mywin.main_console.place(relx=0.25, rely=0.45, relwidth=0.5, relheight=0.15)
        mywin.main_console.see(END)
        mywin.insert_text_thread(f"You open the shop.\n")
    elif user.curr_action == 'shopping':
        user.curr_action = 'idle'
        mywin.close_shop.place_forget()
        list_inv()
        # Close the shop interface
        for i in range(28):
            vars(mywin)['shop_'+str(i)].place_forget()
        mywin.quantity_1.place_forget()
        mywin.quantity_2.place_forget()
        mywin.quantity_3.place_forget()
        mywin.quantity_4.place_forget()
        mywin.quantity_5.place_forget()
        mywin.quantity_label.place_forget()
        mywin.close_shop.place_forget()
        mywin.shop_sell_all.place_forget()
        # Move console back to original position
        mywin.main_console.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.3)
        mywin.main_input.place(relx=0.25, rely=0.4, relwidth=0.5, relheight=0.05)
        mywin.value_item.place_forget()
        mywin.sell_item.place_forget()
        mywin.selected_inv_item.place_forget()


def list_equipment():
    """Check for conflicting interfaces and close them before opening equipment interface.

    If this interface is already visible, close it instead.
    """
    # A list of activities that should prevent this interface from being opened
    if any([(user.curr_action == a) for a in ['banking', 'shopping', 'cooking', 'smithing', 'smelting', 'fletching',
                                              'crafting']]):
        return
    if mywin.spell_0.winfo_viewable() or mywin.spell_16.winfo_viewable():
        for i in range(20):
            vars(mywin)['spell_' + str(i)].place_forget()
        mywin.utility_spells.place_forget()
        mywin.combat_spells.place_forget()
    if mywin.fletch_0.winfo_viewable():
        for i in range(6):
            vars(mywin)['fletch_' + str(i)].place_forget()
            vars(mywin)['fletch_' + str(i)].deselect()
        mywin.start_fletch.place_forget()
        mywin.stop_fletch.place_forget()
        mywin.cooks_left.place_forget()
    if mywin.start_smelt.winfo_viewable():
        mywin.bronze_bar.place_forget()
        mywin.iron_bar.place_forget()
        mywin.steel_bar.place_forget()
        mywin.mithril_bar.place_forget()
        mywin.adamant_bar.place_forget()
        mywin.rune_bar.place_forget()
        mywin.start_smelt.place_forget()
        mywin.stop_smith.place_forget()
        mywin.cooks_left.place_forget()
    if mywin.enemy_fight.winfo_viewable() or mywin.enemy_list1.winfo_viewable() or mywin.enemy_list2.winfo_viewable()\
            or mywin.enemy_list3.winfo_viewable() or mywin.enemy_list4.winfo_viewable():
        # Keep fight button if currently in combat for quick restarting of combat with same enemy
        if user.curr_action != "combat":
            mywin.enemy_fight.place_forget()
        for i in range(1, 5):
            vars(mywin)['enemy_list' + str(i)].place_forget()
            vars(mywin)['enemy' + str(i) + '_lbl'].place_forget()
            vars(mywin)['enemy_list' + str(i)].deselect()
    if mywin.quest_info.winfo_viewable():
        mywin.quest_info.place_forget()
    if mywin.bronze_tab.winfo_viewable():
        j = 0
        for i in ['bronze_', 'iron_', 'steel_', 'mithril_', 'adamant_', 'rune_']:
            vars(mywin)[i + 'tab'].place_forget()
            vars(mywin)[i + 'tab'].deselect()
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            j += 1
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            if j < 5:
                j += 1
        mywin.start_smith.place_forget()
        mywin.stop_smith.place_forget()
        user.curr_item = 0
    if mywin.start_cook.winfo_viewable():
        for i in range(10):
            vars(mywin)['cook_' + str(i)].place_forget()
            vars(mywin)['cook_' + str(i)].deselect()
            mywin.start_cook.place_forget()
            mywin.stop_cook.place_forget()
            mywin.cooks_left.place_forget()
            user.curr_item = 0
    if mywin.skill_0.winfo_viewable():
        for i in range(14):
            vars(mywin)['skill_' + str(i)].place_forget()
        mywin.combat_lvl.place_forget()
    if mywin.craft_1.winfo_viewable():
        for i in range(4):
            vars(mywin)['craft_' + str(i)].place_forget()
            vars(mywin)['craft_' + str(i)].deselect()
        mywin.start_craft.place_forget()
        mywin.stop_craft.place_forget()
        mywin.cooks_left.place_forget()
    if mywin.npc_list1.winfo_viewable() or mywin.npc_name.winfo_viewable() or mywin.npc_list2.winfo_viewable()\
            or mywin.npc_list3.winfo_viewable():
        for i in range(1, 4):
            vars(mywin)['npc_list' + str(i)].place_forget()
            vars(mywin)['npc' + str(i) + '_lbl'].place_forget()
            vars(mywin)['npc_list' + str(i)].deselect()
        mywin.interact_npc.place_forget()
        mywin.open_shop.place_forget()
        mywin.npc_name.place_forget()
        mywin.npc_dialogue.place_forget()
        mywin.npc_response_1.place_forget()
        mywin.npc_response_2.place_forget()
    if mywin.skill_list1.winfo_viewable() or mywin.skill_start.winfo_viewable():
        # If skilling, keep start button visible to easily restart skilling
        if user.curr_action != "skilling":
            mywin.skill_start.place_forget()
        for i in range(1, 5):
            vars(mywin)['skill_list' + str(i)].place_forget()
            vars(mywin)['skill_list' + str(i)].deselect()
            vars(mywin)['skill' + str(i) + '_lbl'].place_forget()
    if mywin.inv_0.winfo_viewable():
        mywin.equip_item.place_forget()
        mywin.drop_item.place_forget()
        mywin.crafting.place_forget()
        mywin.examine_item.place_forget()
        mywin.eat.place_forget()
        mywin.burn.place_forget()
        mywin.selected_inv_item.place_forget()
        mywin.fletching.place_forget()
        for i in range(28):
            vars(mywin)['inv_' + str(i)].place_forget()
    if mywin.equipment_ring.winfo_viewable():
        mywin.equipment_head.place_forget()
        mywin.equipment_neck.place_forget()
        mywin.equipment_body.place_forget()
        mywin.equipment_legs.place_forget()
        mywin.equipment_feet.place_forget()
        mywin.equipment_cape.place_forget()
        mywin.equipment_weapon.place_forget()
        mywin.equipment_hands.place_forget()
        mywin.equipment_ammo.place_forget()
        mywin.equipment_shield.place_forget()
        mywin.equipment_ring.place_forget()
        mywin.att_speed.place_forget()
        mywin.acc_melee.place_forget()
        mywin.acc_ranged.place_forget()
        mywin.acc_magic.place_forget()
        mywin.str_melee.place_forget()
        mywin.str_ranged.place_forget()
        mywin.str_magic.place_forget()
        mywin.melee_def.place_forget()
        mywin.ranged_def.place_forget()
        mywin.magic_def.place_forget()
    else:
        # Display equipment interface
        mywin.equipment_head.place(relx=0.425, rely=0.6, relwidth=0.15, relheight=0.07)
        mywin.equipment_neck.place(relx=0.425, rely=0.67, relwidth=0.15, relheight=0.07)
        mywin.equipment_body.place(relx=0.425, rely=0.74, relwidth=0.15, relheight=0.07)
        mywin.equipment_legs.place(relx=0.425, rely=0.81, relwidth=0.15, relheight=0.07)
        mywin.equipment_feet.place(relx=0.425, rely=0.88, relwidth=0.15, relheight=0.07)
        mywin.equipment_cape.place(relx=0.275, rely=0.67, relwidth=0.15, relheight=0.07)
        mywin.equipment_weapon.place(relx=0.275, rely=0.74, relwidth=0.15, relheight=0.07)
        mywin.equipment_hands.place(relx=0.275, rely=0.88, relwidth=0.15, relheight=0.07)
        mywin.equipment_ammo.place(relx=0.575, rely=0.67, relwidth=0.15, relheight=0.07)
        mywin.equipment_shield.place(relx=0.575, rely=0.74, relwidth=0.15, relheight=0.07)
        mywin.equipment_ring.place(relx=0.575, rely=0.88, relwidth=0.15, relheight=0.07)
        display_equip_stats()
        update_inventory()
        if user.flags.get('tut_prog', 250) == 7:
            user.flags.get['tut_prog'] = 8


def list_inv():
    """Check for conflicting interfaces and close them before opening inventory interface.

    If inventory is already visible, close it instead.
    """
    # Activities that prevent this interface being opened
    if user.curr_action == 'banking' or user.curr_action == 'shopping':
        return
    user.inventory.shuffle_inv()
    update_inventory()
    if mywin.fletch_0.winfo_viewable():
        for i in range(6):
            vars(mywin)['fletch_' + str(i)].place_forget()
            vars(mywin)['fletch_' + str(i)].deselect()
        # If fletching, keep the key fletching information visible
        if user.curr_action != 'fletching':
            mywin.start_fletch.place_forget()
            mywin.stop_fletch.place_forget()
            mywin.cooks_left.place_forget()
    if mywin.start_cook.winfo_viewable():
        for i in range(10):
            vars(mywin)['cook_' + str(i)].place_forget()
            vars(mywin)['cook_' + str(i)].deselect()
            # If cooking, keep the key cooking information visible
            if user.curr_action != "cooking":
                mywin.start_cook.place_forget()
                mywin.stop_cook.place_forget()
                mywin.cooks_left.place_forget()
                user.curr_item = 0
    if mywin.spell_0.winfo_viewable() or mywin.spell_16.winfo_viewable():
        for i in range(20):
            vars(mywin)['spell_' + str(i)].place_forget()
        mywin.utility_spells.place_forget()
        mywin.combat_spells.place_forget()
    if mywin.bronze_tab.winfo_viewable():
        j = 0
        for i in ['bronze_', 'iron_', 'steel_', 'mithril_', 'adamant_', 'rune_']:
            vars(mywin)[i + 'tab'].place_forget()
            vars(mywin)[i + 'tab'].deselect()
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            j += 1
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            if j < 5:
                j += 1
        # If smithing, keep the key smithing information visible
        if user.curr_action != "smithing":
            mywin.start_smith.place_forget()
            mywin.stop_smith.place_forget()
            user.curr_item = 0
    if mywin.skill_0.winfo_viewable():
        for i in range(14):
            vars(mywin)['skill_' + str(i)].place_forget()
        mywin.combat_lvl.place_forget()
    if mywin.quest_info.winfo_viewable():
        mywin.quest_info.place_forget()
    if mywin.start_smelt.winfo_viewable():
        mywin.bronze_bar.place_forget()
        mywin.iron_bar.place_forget()
        mywin.steel_bar.place_forget()
        mywin.mithril_bar.place_forget()
        mywin.adamant_bar.place_forget()
        mywin.rune_bar.place_forget()
        # If smelting, keep the key smelting information visible
        if user.curr_action != "smelting":
            mywin.start_smelt.place_forget()
            mywin.stop_smith.place_forget()
            mywin.cooks_left.place_forget()
    if mywin.equipment_ring.winfo_viewable():
        mywin.equipment_head.place_forget()
        mywin.equipment_neck.place_forget()
        mywin.equipment_body.place_forget()
        mywin.equipment_legs.place_forget()
        mywin.equipment_feet.place_forget()
        mywin.equipment_cape.place_forget()
        mywin.equipment_weapon.place_forget()
        mywin.equipment_hands.place_forget()
        mywin.equipment_ammo.place_forget()
        mywin.equipment_shield.place_forget()
        mywin.equipment_ring.place_forget()
        mywin.att_speed.place_forget()
        mywin.acc_melee.place_forget()
        mywin.acc_ranged.place_forget()
        mywin.acc_magic.place_forget()
        mywin.str_melee.place_forget()
        mywin.str_ranged.place_forget()
        mywin.str_magic.place_forget()
        mywin.melee_def.place_forget()
        mywin.ranged_def.place_forget()
        mywin.magic_def.place_forget()
    if mywin.craft_1.winfo_viewable():
        for i in range(4):
            vars(mywin)['craft_' + str(i)].place_forget()
            vars(mywin)['craft_' + str(i)].deselect()
        # If crafting, keep the key crafting information visible
        if user.curr_action != 'crafting':
            mywin.start_craft.place_forget()
            mywin.stop_craft.place_forget()
            mywin.cooks_left.place_forget()
    if mywin.enemy_fight.winfo_viewable() or mywin.enemy_list1.winfo_viewable() or mywin.enemy_list2.winfo_viewable()\
            or mywin.enemy_list3.winfo_viewable() or mywin.enemy_list4.winfo_viewable():
        # If in combat, keep the fight button visible to easily restart combat
        if user.curr_action != "combat":
            mywin.enemy_fight.place_forget()
        for i in range(1, 5):
            vars(mywin)['enemy_list' + str(i)].place_forget()
            vars(mywin)['enemy' + str(i) + '_lbl'].place_forget()
            vars(mywin)['enemy_list' + str(i)].deselect()
    if mywin.npc_list1.winfo_viewable() or mywin.npc_name.winfo_viewable() or mywin.npc_list2.winfo_viewable()\
            or mywin.npc_list3.winfo_viewable():
        for i in range(1, 4):
            vars(mywin)['npc_list' + str(i)].place_forget()
            vars(mywin)['npc' + str(i) + '_lbl'].place_forget()
            vars(mywin)['npc_list' + str(i)].deselect()
        mywin.interact_npc.place_forget()
        mywin.open_shop.place_forget()
        mywin.npc_name.place_forget()
        mywin.npc_dialogue.place_forget()
        mywin.npc_response_1.place_forget()
        mywin.npc_response_2.place_forget()
    if mywin.skill_list1.winfo_viewable() or mywin.skill_start.winfo_viewable():
        # If skilling, keep the start button visible to easily restart skilling
        if user.curr_action != "skilling":
            mywin.skill_start.place_forget()
        for i in range(1, 5):
            vars(mywin)['skill_list' + str(i)].place_forget()
            vars(mywin)['skill_list' + str(i)].deselect()
            vars(mywin)['skill' + str(i) + '_lbl'].place_forget()
    if mywin.inv_0.winfo_viewable():
        mywin.equip_item.place_forget()
        mywin.drop_item.place_forget()
        mywin.crafting.place_forget()
        mywin.examine_item.place_forget()
        mywin.eat.place_forget()
        mywin.burn.place_forget()
        mywin.selected_inv_item.place_forget()
        mywin.fletching.place_forget()
        for i in range(28):
            vars(mywin)['inv_' + str(i)].place_forget()
    else:
        # Open the inventory interface
        for i in range(28):
            vars(mywin)['inv_'+str(i)].place(relx=0.25 + 0.125*(i % 4), rely=0.6 + 0.05*(i // 4),
                                             relwidth=0.125, relheight=0.05)
        if user.flags.get('tut_prog', 250) == 5:
            user.flags['tut_prog'] = 6


def list_skill_obj():
    """Check for conflicting interfaces and close them before opening the skill objects interface.

    If this interface is already visible, close it instead.
    """
    # A list of activities that prevent the interface from being opened
    if any([(user.curr_action == a) for a in ['banking', 'shopping', 'cooking', 'combat', 'smithing', 'smelting',
                                              'fletching', 'crafting']]):
        return
    user.curr_area.selection = None
    if mywin.bronze_tab.winfo_viewable():
        j = 0
        for i in ['bronze_', 'iron_', 'steel_', 'mithril_', 'adamant_', 'rune_']:
            vars(mywin)[i + 'tab'].place_forget()
            vars(mywin)[i + 'tab'].deselect()
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            j += 1
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            if j < 5:
                j += 1
        mywin.start_smith.place_forget()
        mywin.stop_smith.place_forget()
        user.curr_item = 0
    if mywin.quest_info.winfo_viewable():
        mywin.quest_info.place_forget()
    if mywin.fletch_0.winfo_viewable():
        for i in range(6):
            vars(mywin)['fletch_' + str(i)].place_forget()
            vars(mywin)['fletch_' + str(i)].deselect()
        mywin.start_fletch.place_forget()
        mywin.stop_fletch.place_forget()
        mywin.cooks_left.place_forget()
    if mywin.start_smelt.winfo_viewable():
        mywin.bronze_bar.place_forget()
        mywin.iron_bar.place_forget()
        mywin.steel_bar.place_forget()
        mywin.mithril_bar.place_forget()
        mywin.adamant_bar.place_forget()
        mywin.rune_bar.place_forget()
        mywin.start_smelt.place_forget()
        mywin.stop_smith.place_forget()
        mywin.cooks_left.place_forget()
    if mywin.start_cook.winfo_viewable():
        for i in range(10):
            vars(mywin)['cook_' + str(i)].place_forget()
            vars(mywin)['cook_' + str(i)].deselect()
            mywin.start_cook.place_forget()
            mywin.stop_cook.place_forget()
            mywin.cooks_left.place_forget()
            user.curr_item = 0
    if mywin.spell_0.winfo_viewable() or mywin.spell_16.winfo_viewable():
        for i in range(20):
            vars(mywin)['spell_' + str(i)].place_forget()
        mywin.utility_spells.place_forget()
        mywin.combat_spells.place_forget()
    if mywin.skill_0.winfo_viewable():
        for i in range(14):
            vars(mywin)['skill_' + str(i)].place_forget()
        mywin.combat_lvl.place_forget()
    if mywin.craft_1.winfo_viewable():
        for i in range(4):
            vars(mywin)['craft_' + str(i)].place_forget()
            vars(mywin)['craft_' + str(i)].deselect()
        mywin.start_craft.place_forget()
        mywin.stop_craft.place_forget()
        mywin.cooks_left.place_forget()
    if mywin.equipment_ring.winfo_viewable():
        mywin.equipment_head.place_forget()
        mywin.equipment_neck.place_forget()
        mywin.equipment_body.place_forget()
        mywin.equipment_legs.place_forget()
        mywin.equipment_feet.place_forget()
        mywin.equipment_cape.place_forget()
        mywin.equipment_weapon.place_forget()
        mywin.equipment_hands.place_forget()
        mywin.equipment_ammo.place_forget()
        mywin.equipment_shield.place_forget()
        mywin.equipment_ring.place_forget()
        mywin.att_speed.place_forget()
        mywin.acc_melee.place_forget()
        mywin.acc_ranged.place_forget()
        mywin.acc_magic.place_forget()
        mywin.str_melee.place_forget()
        mywin.str_ranged.place_forget()
        mywin.str_magic.place_forget()
        mywin.melee_def.place_forget()
        mywin.ranged_def.place_forget()
        mywin.magic_def.place_forget()
    if mywin.inv_0.winfo_viewable():
        mywin.equip_item.place_forget()
        mywin.drop_item.place_forget()
        mywin.crafting.place_forget()
        mywin.eat.place_forget()
        mywin.burn.place_forget()
        mywin.examine_item.place_forget()
        mywin.selected_inv_item.place_forget()
        mywin.fletching.place_forget()
        for i in range(28):
            vars(mywin)['inv_' + str(i)].place_forget()
    if mywin.enemy_fight.winfo_viewable() or mywin.enemy_list1.winfo_viewable() or mywin.enemy_list2.winfo_viewable()\
            or mywin.enemy_list3.winfo_viewable() or mywin.enemy_list4.winfo_viewable():
        mywin.enemy_fight.place_forget()
        for i in range(1, 5):
            vars(mywin)['enemy_list' + str(i)].place_forget()
            vars(mywin)['enemy' + str(i) + '_lbl'].place_forget()
            vars(mywin)['enemy_list' + str(i)].deselect()
    if mywin.npc_list1.winfo_viewable() or mywin.npc_name.winfo_viewable() or mywin.npc_list2.winfo_viewable()\
            or mywin.npc_list3.winfo_viewable():
        for i in range(1, 4):
            vars(mywin)['npc_list' + str(i)].place_forget()
            vars(mywin)['npc' + str(i) + '_lbl'].place_forget()
            vars(mywin)['npc_list' + str(i)].deselect()
        mywin.interact_npc.place_forget()
        mywin.open_shop.place_forget()
        mywin.npc_name.place_forget()
        mywin.npc_dialogue.place_forget()
        mywin.npc_response_1.place_forget()
        mywin.npc_response_2.place_forget()
    if mywin.skill_list1.winfo_viewable():
        # If skilling, keep the start button visible to easily restart skilling
        if user.curr_action != 'skilling':
            mywin.skill_start.place_forget()
        for i in range(1, 5):
            vars(mywin)['skill_list' + str(i)].place_forget()
            vars(mywin)['skill_list' + str(i)].deselect()
            vars(mywin)['skill' + str(i) + '_lbl'].place_forget()
    else:
        # Display skill objects interface
        if len(user.curr_area.skill_obj) == 0:
            mywin.insert_text_thread(f"There are no skilling objects in this area.", 'warning')
        # Can add quest_lock stuff here in future, currently only used for enemies + NPCs
        for i in range(len(user.curr_area.skill_obj)):
            vars(mywin)['skill_list' + str(i + 1)].place(relx=0.25, rely=0.65 + i * 0.05, relwidth=0.15, relheight=0.05)
            vars(mywin)['skill_list' + str(i + 1)].configure(text=user.curr_area.skill_obj[i].name)
        if user.flags.get('tut_prog', 250) == 16:
            user.flags['tut_prog'] = 17


def list_enemies():
    """Check for conflicting interfaces and close them before opening the enemies interface.

    If this interface is already visible, closes it instead.
    """
    # List of activities that prevent this interface from opening
    if any([(user.curr_action == a) for a in ['banking', 'shopping', 'cooking', 'smithing', 'smelting',
                                              'fletching', 'crafting', 'skilling']]):
        return
    if not mywin.enemy_fight.winfo_viewable():
        user.curr_area.selection = None
    if mywin.fletch_0.winfo_viewable():
        for i in range(6):
            vars(mywin)['fletch_' + str(i)].place_forget()
            vars(mywin)['fletch_' + str(i)].deselect()
        mywin.start_fletch.place_forget()
        mywin.stop_fletch.place_forget()
        mywin.cooks_left.place_forget()
    if mywin.bronze_tab.winfo_viewable():
        j = 0
        for i in ['bronze_', 'iron_', 'steel_', 'mithril_', 'adamant_', 'rune_']:
            vars(mywin)[i + 'tab'].place_forget()
            vars(mywin)[i + 'tab'].deselect()
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            j += 1
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            if j < 5:
                j += 1
        mywin.start_smith.place_forget()
        mywin.stop_smith.place_forget()
        user.curr_item = 0
    if mywin.start_smelt.winfo_viewable():
        mywin.bronze_bar.place_forget()
        mywin.iron_bar.place_forget()
        mywin.steel_bar.place_forget()
        mywin.mithril_bar.place_forget()
        mywin.adamant_bar.place_forget()
        mywin.rune_bar.place_forget()
        mywin.start_smelt.place_forget()
        mywin.stop_smith.place_forget()
        mywin.cooks_left.place_forget()
    if mywin.quest_info.winfo_viewable():
        mywin.quest_info.place_forget()
    if mywin.start_cook.winfo_viewable():
        for i in range(10):
            vars(mywin)['cook_' + str(i)].place_forget()
            vars(mywin)['cook_' + str(i)].deselect()
            mywin.start_cook.place_forget()
            mywin.stop_cook.place_forget()
            mywin.cooks_left.place_forget()
            user.curr_item = 0
    if mywin.spell_0.winfo_viewable() or mywin.spell_16.winfo_viewable():
        for i in range(20):
            vars(mywin)['spell_' + str(i)].place_forget()
        mywin.utility_spells.place_forget()
        mywin.combat_spells.place_forget()
    if mywin.skill_0.winfo_viewable():
        for i in range(14):
            vars(mywin)['skill_' + str(i)].place_forget()
        mywin.combat_lvl.place_forget()
    if mywin.craft_1.winfo_viewable():
        for i in range(4):
            vars(mywin)['craft_' + str(i)].place_forget()
            vars(mywin)['craft_' + str(i)].deselect()
        mywin.start_craft.place_forget()
        mywin.stop_craft.place_forget()
        mywin.cooks_left.place_forget()
    if mywin.equipment_ring.winfo_viewable():
        mywin.equipment_head.place_forget()
        mywin.equipment_neck.place_forget()
        mywin.equipment_body.place_forget()
        mywin.equipment_legs.place_forget()
        mywin.equipment_feet.place_forget()
        mywin.equipment_cape.place_forget()
        mywin.equipment_weapon.place_forget()
        mywin.equipment_hands.place_forget()
        mywin.equipment_ammo.place_forget()
        mywin.equipment_shield.place_forget()
        mywin.equipment_ring.place_forget()
        mywin.att_speed.place_forget()
        mywin.acc_melee.place_forget()
        mywin.acc_ranged.place_forget()
        mywin.acc_magic.place_forget()
        mywin.str_melee.place_forget()
        mywin.str_ranged.place_forget()
        mywin.str_magic.place_forget()
        mywin.melee_def.place_forget()
        mywin.ranged_def.place_forget()
        mywin.magic_def.place_forget()
    if mywin.inv_0.winfo_viewable():
        mywin.equip_item.place_forget()
        mywin.drop_item.place_forget()
        mywin.crafting.place_forget()
        mywin.eat.place_forget()
        mywin.burn.place_forget()
        mywin.examine_item.place_forget()
        mywin.selected_inv_item.place_forget()
        mywin.fletching.place_forget()
        for i in range(28):
            vars(mywin)['inv_' + str(i)].place_forget()
    if mywin.skill_list1.winfo_viewable() or mywin.skill_start.winfo_viewable():
        mywin.skill_start.place_forget()
        for i in range(1, 5):
            vars(mywin)['skill_list' + str(i)].place_forget()
            vars(mywin)['skill_list' + str(i)].deselect()
            vars(mywin)['skill' + str(i) + '_lbl'].place_forget()
    if mywin.npc_list1.winfo_viewable() or mywin.npc_name.winfo_viewable() or mywin.npc_list2.winfo_viewable()\
            or mywin.npc_list3.winfo_viewable():
        for i in range(1, 4):
            vars(mywin)['npc_list' + str(i)].place_forget()
            vars(mywin)['npc' + str(i) + '_lbl'].place_forget()
            vars(mywin)['npc_list' + str(i)].deselect()
        mywin.interact_npc.place_forget()
        mywin.open_shop.place_forget()
        mywin.npc_name.place_forget()
        mywin.npc_dialogue.place_forget()
        mywin.npc_response_1.place_forget()
        mywin.npc_response_2.place_forget()
    if mywin.enemy_list1.winfo_viewable() or mywin.enemy_list2.winfo_viewable() or mywin.enemy_list3.winfo_viewable()\
            or mywin.enemy_list4.winfo_viewable():
        # If in combat, keep fight button visible to easily restart combat afterwards
        if user.curr_action != 'combat':
            mywin.enemy_fight.place_forget()
        for i in range(1, 5):
            vars(mywin)['enemy_list' + str(i)].place_forget()
            vars(mywin)['enemy' + str(i) + '_lbl'].place_forget()
            vars(mywin)['enemy_list' + str(i)].deselect()
    else:
        # Display the list of enemies to fight
        if len(user.curr_area.enemies) == 0 or user.curr_area.enemies[0] == None_enemy:
            mywin.insert_text_thread(f"There are no enemies in this area.", 'warning')
        # quest_lock format:
        # quest_lock=[[0, 2], 'spawn'] => only show enemy once user completes [0,2] quest objective
        # quest_lock = [[0,2], 'kill'] => only show enemy before user completes [0,2] quest objective
        quests_started = [i for [i, _] in user.quest_flags]
        j = 0  # Count displayed enemies to prevent gaps when one is hidden
        for i in range(len(user.curr_area.enemies)):
            if user.curr_area.enemies[i] == None_enemy:
                continue
            enemy = user.curr_area.enemies[i]
            if enemy.quest_lock is not None:
                quest = enemy.quest_lock[0][0]
                obj = enemy.quest_lock[0][1]
                behaviour = enemy.quest_lock[1]
                # Choose to display each enemy based on quest progress
                if (quest in quests_started and user.quest_flags[quests_started.index(quest)][
                    1] >= obj) and behaviour == 'kill' or \
                        not (quest in quests_started and user.quest_flags[quests_started.index(quest)][
                            1] >= obj) and behaviour == 'spawn':
                    continue
                else:
                    vars(mywin)['enemy_list' + str(i + 1)].place(relx=0.25, rely=0.65 + j * 0.05, relwidth=0.15,
                                                                 relheight=0.05)
                    vars(mywin)['enemy_list' + str(i + 1)].configure(text=user.curr_area.enemies[i].name)
                    j += 1
            else:
                vars(mywin)['enemy_list' + str(i + 1)].place(relx=0.25, rely=0.65 + j * 0.05, relwidth=0.15,
                                                             relheight=0.05)
                vars(mywin)['enemy_list' + str(i + 1)].configure(text=user.curr_area.enemies[i].name)
                j += 1
        if user.flags.get('tut_prog', 250) in [9, 11, 13]:
            global flashing
            flashing = False


def list_npcs():
    """Check for conflicting interfaces and closes them before opening the NPC interface.

    If this interface is already visible, close it instead.
    """
    # List of activities that prevent this interface from opening
    if any([(user.curr_action == a) for a in ['banking', 'shopping', 'cooking', 'smithing', 'smelting',
                                              'fletching', 'crafting', 'skilling', 'combat']]):
        return
    user.curr_area.selection = None
    if mywin.fletch_0.winfo_viewable():
        for i in range(6):
            vars(mywin)['fletch_' + str(i)].place_forget()
            vars(mywin)['fletch_' + str(i)].deselect()
        mywin.start_fletch.place_forget()
        mywin.stop_fletch.place_forget()
        mywin.cooks_left.place_forget()
    if mywin.quest_info.winfo_viewable():
        mywin.quest_info.place_forget()
    if mywin.bronze_tab.winfo_viewable():
        j = 0
        for i in ['bronze_', 'iron_', 'steel_', 'mithril_', 'adamant_', 'rune_']:
            vars(mywin)[i + 'tab'].place_forget()
            vars(mywin)[i + 'tab'].deselect()
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            j += 1
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            if j < 5:
                j += 1
        mywin.start_smith.place_forget()
        mywin.stop_smith.place_forget()
        user.curr_item = 0
    if mywin.start_cook.winfo_viewable():
        for i in range(10):
            vars(mywin)['cook_' + str(i)].place_forget()
            vars(mywin)['cook_' + str(i)].deselect()
            mywin.start_cook.place_forget()
            mywin.stop_cook.place_forget()
            mywin.cooks_left.place_forget()
            user.curr_item = 0
    if mywin.start_smelt.winfo_viewable():
        mywin.bronze_bar.place_forget()
        mywin.iron_bar.place_forget()
        mywin.steel_bar.place_forget()
        mywin.mithril_bar.place_forget()
        mywin.adamant_bar.place_forget()
        mywin.rune_bar.place_forget()
        mywin.start_smelt.place_forget()
        mywin.stop_smith.place_forget()
        mywin.cooks_left.place_forget()
    if mywin.spell_0.winfo_viewable() or mywin.spell_16.winfo_viewable():
        for i in range(20):
            vars(mywin)['spell_' + str(i)].place_forget()
        mywin.utility_spells.place_forget()
        mywin.combat_spells.place_forget()
    if mywin.skill_0.winfo_viewable():
        for i in range(14):
            vars(mywin)['skill_' + str(i)].place_forget()
        mywin.combat_lvl.place_forget()
    if mywin.equipment_ring.winfo_viewable():
        mywin.equipment_head.place_forget()
        mywin.equipment_neck.place_forget()
        mywin.equipment_body.place_forget()
        mywin.equipment_legs.place_forget()
        mywin.equipment_feet.place_forget()
        mywin.equipment_cape.place_forget()
        mywin.equipment_weapon.place_forget()
        mywin.equipment_hands.place_forget()
        mywin.equipment_ammo.place_forget()
        mywin.equipment_shield.place_forget()
        mywin.equipment_ring.place_forget()
        mywin.att_speed.place_forget()
        mywin.acc_melee.place_forget()
        mywin.acc_ranged.place_forget()
        mywin.acc_magic.place_forget()
        mywin.str_melee.place_forget()
        mywin.str_ranged.place_forget()
        mywin.str_magic.place_forget()
        mywin.melee_def.place_forget()
        mywin.ranged_def.place_forget()
        mywin.magic_def.place_forget()
    if mywin.craft_1.winfo_viewable():
        for i in range(4):
            vars(mywin)['craft_' + str(i)].place_forget()
            vars(mywin)['craft_' + str(i)].deselect()
        mywin.start_craft.place_forget()
        mywin.stop_craft.place_forget()
        mywin.cooks_left.place_forget()
    if mywin.inv_0.winfo_viewable():
        mywin.equip_item.place_forget()
        mywin.drop_item.place_forget()
        mywin.crafting.place_forget()
        mywin.examine_item.place_forget()
        mywin.eat.place_forget()
        mywin.burn.place_forget()
        mywin.selected_inv_item.place_forget()
        mywin.fletching.place_forget()
        for i in range(28):
            vars(mywin)['inv_' + str(i)].place_forget()
    if mywin.enemy_fight.winfo_viewable() or mywin.enemy_list1.winfo_viewable() or mywin.enemy_list2.winfo_viewable()\
            or mywin.enemy_list3.winfo_viewable() or mywin.enemy_list4.winfo_viewable():
        mywin.enemy_fight.place_forget()
        for i in range(1, 5):
            vars(mywin)['enemy_list' + str(i)].place_forget()
            vars(mywin)['enemy' + str(i) + '_lbl'].place_forget()
            vars(mywin)['enemy_list' + str(i)].deselect()
    if mywin.skill_list1.winfo_viewable() or mywin.skill_start.winfo_viewable():
        mywin.skill_start.place_forget()
        for i in range(1, 5):
            vars(mywin)['skill_list' + str(i)].place_forget()
            vars(mywin)['skill_list' + str(i)].deselect()
            vars(mywin)['skill' + str(i) + '_lbl'].place_forget()
    if mywin.npc_list1.winfo_viewable() or mywin.npc_name.winfo_viewable() or mywin.npc_list2.winfo_viewable()\
            or mywin.npc_list3.winfo_viewable():
        for i in range(1, 4):
            vars(mywin)['npc_list' + str(i)].place_forget()
            vars(mywin)['npc' + str(i) + '_lbl'].place_forget()
            vars(mywin)['npc_list' + str(i)].deselect()
        mywin.interact_npc.place_forget()
        mywin.open_shop.place_forget()
        mywin.npc_name.place_forget()
        mywin.npc_dialogue.place_forget()
        mywin.npc_response_1.place_forget()
        mywin.npc_response_2.place_forget()
    else:
        # Display NPC list
        if len(user.curr_area.npcs) == 0:
            mywin.insert_text_thread(f"There are no NPCs in this area.", 'warning')

        quests_started = [i for [i, _] in user.quest_flags]
        j = 0     # Count visible NPCs so that button placement will not have gaps if middle entry is hidden
        for i in range(len(user.curr_area.npcs)):
            npc = user.curr_area.npcs[i]
            if npc.quest_lock is not None:
                quest = npc.quest_lock[0][0]
                obj = npc.quest_lock[0][1]
                behaviour = npc.quest_lock[1]
                # Choose to display each NPC based on quest progress
                if (quest in quests_started and user.quest_flags[quests_started.index(quest)][
                    1] >= obj) and behaviour == 'kill' or \
                        not (quest in quests_started and user.quest_flags[quests_started.index(quest)][
                            1] >= obj) and behaviour == 'spawn':
                    continue
                else:
                    vars(mywin)['npc_list' + str(i + 1)].place(relx=0.25, rely=0.65 + j * 0.05, relwidth=0.15,
                                                               relheight=0.05)
                    vars(mywin)['npc_list' + str(i + 1)].configure(text=user.curr_area.npcs[i].name)
                    j += 1
            else:
                vars(mywin)['npc_list' + str(i + 1)].place(relx=0.25, rely=0.65 + j * 0.05, relwidth=0.15,
                                                           relheight=0.05)
                vars(mywin)['npc_list' + str(i + 1)].configure(text=user.curr_area.npcs[i].name)
                j += 1


def list_skills():
    """Check for conflicting interfaces and close them before opening the skills interface.
    If this interface is already visible, close it instead.
    """
    # List of activities that prevent this interface from being opened
    if user.curr_action == 'banking' or user.curr_action == 'shopping':
        return
    if mywin.fletch_0.winfo_viewable():
        for i in range(6):
            vars(mywin)['fletch_' + str(i)].place_forget()
            vars(mywin)['fletch_' + str(i)].deselect()
        # If fletching, keep key information visible
        if user.curr_action != 'fletching':
            mywin.start_fletch.place_forget()
            mywin.stop_fletch.place_forget()
            mywin.cooks_left.place_forget()
    if mywin.start_cook.winfo_viewable():
        for i in range(10):
            vars(mywin)['cook_' + str(i)].place_forget()
            vars(mywin)['cook_' + str(i)].deselect()
            # If cooking, keep key information visible
            if user.curr_action != "cooking":
                mywin.start_cook.place_forget()
                mywin.stop_cook.place_forget()
                mywin.cooks_left.place_forget()
                user.curr_item = 0
    if mywin.spell_0.winfo_viewable() or mywin.spell_16.winfo_viewable():
        for i in range(20):
            vars(mywin)['spell_' + str(i)].place_forget()
        mywin.utility_spells.place_forget()
        mywin.combat_spells.place_forget()
    if mywin.bronze_tab.winfo_viewable():
        j = 0
        for i in ['bronze_', 'iron_', 'steel_', 'mithril_', 'adamant_', 'rune_']:
            vars(mywin)[i + 'tab'].place_forget()
            vars(mywin)[i + 'tab'].deselect()
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            j += 1
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            if j < 5:
                j += 1
        # If smithing, keep key information visible
        if user.curr_action != "smithing":
            mywin.start_smith.place_forget()
            mywin.stop_smith.place_forget()
            user.curr_item = 0
    if mywin.quest_info.winfo_viewable():
        mywin.quest_info.place_forget()
    if mywin.start_smelt.winfo_viewable():
        mywin.bronze_bar.place_forget()
        mywin.iron_bar.place_forget()
        mywin.steel_bar.place_forget()
        mywin.mithril_bar.place_forget()
        mywin.adamant_bar.place_forget()
        mywin.rune_bar.place_forget()
        # If smelting, keep key information visible
        if user.curr_action != "smelting":
            mywin.start_smelt.place_forget()
            mywin.stop_smith.place_forget()
            mywin.cooks_left.place_forget()
    if mywin.equipment_ring.winfo_viewable():
        mywin.equipment_head.place_forget()
        mywin.equipment_neck.place_forget()
        mywin.equipment_body.place_forget()
        mywin.equipment_legs.place_forget()
        mywin.equipment_feet.place_forget()
        mywin.equipment_cape.place_forget()
        mywin.equipment_weapon.place_forget()
        mywin.equipment_hands.place_forget()
        mywin.equipment_ammo.place_forget()
        mywin.equipment_shield.place_forget()
        mywin.equipment_ring.place_forget()
        mywin.att_speed.place_forget()
        mywin.acc_melee.place_forget()
        mywin.acc_ranged.place_forget()
        mywin.acc_magic.place_forget()
        mywin.str_melee.place_forget()
        mywin.str_ranged.place_forget()
        mywin.str_magic.place_forget()
        mywin.melee_def.place_forget()
        mywin.ranged_def.place_forget()
        mywin.magic_def.place_forget()
    if mywin.enemy_fight.winfo_viewable() or mywin.enemy_list1.winfo_viewable() or mywin.enemy_list2.winfo_viewable()\
            or mywin.enemy_list3.winfo_viewable() or mywin.enemy_list4.winfo_viewable():
        # If in combat, keep fight button visible for easy restarting
        if user.curr_action != "combat":
            mywin.enemy_fight.place_forget()
        for i in range(1, 5):
            vars(mywin)['enemy_list' + str(i)].place_forget()
            vars(mywin)['enemy' + str(i) + '_lbl'].place_forget()
            vars(mywin)['enemy_list' + str(i)].deselect()
    if mywin.npc_list1.winfo_viewable() or mywin.npc_name.winfo_viewable() or mywin.npc_list2.winfo_viewable()\
            or mywin.npc_list3.winfo_viewable():
        for i in range(1, 4):
            vars(mywin)['npc_list' + str(i)].place_forget()
            vars(mywin)['npc' + str(i) + '_lbl'].place_forget()
            vars(mywin)['npc_list' + str(i)].deselect()
        mywin.interact_npc.place_forget()
        mywin.open_shop.place_forget()
        mywin.npc_name.place_forget()
        mywin.npc_dialogue.place_forget()
        mywin.npc_response_1.place_forget()
        mywin.npc_response_2.place_forget()
    if mywin.craft_1.winfo_viewable():
        for i in range(4):
            vars(mywin)['craft_' + str(i)].place_forget()
            vars(mywin)['craft_' + str(i)].deselect()
        # If crafting, keep key information visible
        if user.curr_action != 'crafting':
            mywin.start_craft.place_forget()
            mywin.stop_craft.place_forget()
            mywin.cooks_left.place_forget()
    if mywin.skill_list1.winfo_viewable() or mywin.skill_start.winfo_viewable():
        # If skilling, keep start button visible for easy restarting
        if user.curr_action != "skilling":
            mywin.skill_start.place_forget()
        for i in range(1, 5):
            vars(mywin)['skill_list' + str(i)].place_forget()
            vars(mywin)['skill_list' + str(i)].deselect()
            vars(mywin)['skill' + str(i) + '_lbl'].place_forget()
    if mywin.inv_0.winfo_viewable():
        mywin.equip_item.place_forget()
        mywin.drop_item.place_forget()
        mywin.crafting.place_forget()
        mywin.examine_item.place_forget()
        mywin.eat.place_forget()
        mywin.burn.place_forget()
        mywin.selected_inv_item.place_forget()
        mywin.fletching.place_forget()
        for i in range(28):
            vars(mywin)['inv_' + str(i)].place_forget()
    if mywin.skill_0.winfo_viewable():
        for i in range(14):
            vars(mywin)['skill_' + str(i)].place_forget()
        mywin.combat_lvl.place_forget()
    else:
        # Display skills interface
        update_skills()
        mywin.combat_lvl.configure(text=f"Combat level:\n{combat_level(user)}")
        if user.flags.get('tut_prog', 250) == 2:
            user.flags['tut_prog'] = 3
        for i in range(14):
            vars(mywin)['skill_'+str(i)].place(relx=0.25 + 0.125*(i % 4), rely=0.6 + 0.0875*(i // 4), relwidth=0.125,
                                               relheight=0.0875)
        mywin.combat_lvl.place(relx=0.5, rely=0.8625, relwidth=0.125, relheight=0.0875)


def list_spells():
    """Check for conflicting interfaces and close them before opening the spellbook interface.

    If this interface is already visible, close it instead.
    """
    # List of activities that prevent this interface from opening
    if any([(user.curr_action == a) for a in ['banking', 'shopping', 'cooking', 'smithing', 'smelting',
                                              'fletching', 'crafting', 'skilling']]):
        return
    if mywin.fletch_0.winfo_viewable():
        for i in range(6):
            vars(mywin)['fletch_' + str(i)].place_forget()
            vars(mywin)['fletch_' + str(i)].deselect()
        mywin.start_fletch.place_forget()
        mywin.stop_fletch.place_forget()
        mywin.cooks_left.place_forget()
    if mywin.quest_info.winfo_viewable():
        mywin.quest_info.place_forget()
    if mywin.start_smelt.winfo_viewable():
        mywin.bronze_bar.place_forget()
        mywin.iron_bar.place_forget()
        mywin.steel_bar.place_forget()
        mywin.mithril_bar.place_forget()
        mywin.adamant_bar.place_forget()
        mywin.rune_bar.place_forget()
        mywin.start_smelt.place_forget()
        mywin.stop_smith.place_forget()
        mywin.cooks_left.place_forget()
    if mywin.start_cook.winfo_viewable():
        for i in range(10):
            vars(mywin)['cook_' + str(i)].place_forget()
            vars(mywin)['cook_' + str(i)].deselect()
            mywin.start_cook.place_forget()
            mywin.stop_cook.place_forget()
            mywin.cooks_left.place_forget()
            user.curr_item = 0
    if mywin.bronze_tab.winfo_viewable():
        j = 0
        for i in ['bronze_', 'iron_', 'steel_', 'mithril_', 'adamant_', 'rune_']:
            vars(mywin)[i + 'tab'].place_forget()
            vars(mywin)[i + 'tab'].deselect()
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            j += 1
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            if j < 5:
                j += 1
        mywin.start_smith.place_forget()
        mywin.stop_smith.place_forget()
        user.curr_item = 0
    if mywin.equipment_ring.winfo_viewable():
        mywin.equipment_head.place_forget()
        mywin.equipment_neck.place_forget()
        mywin.equipment_body.place_forget()
        mywin.equipment_legs.place_forget()
        mywin.equipment_feet.place_forget()
        mywin.equipment_cape.place_forget()
        mywin.equipment_weapon.place_forget()
        mywin.equipment_hands.place_forget()
        mywin.equipment_ammo.place_forget()
        mywin.equipment_shield.place_forget()
        mywin.equipment_ring.place_forget()
        mywin.att_speed.place_forget()
        mywin.acc_melee.place_forget()
        mywin.acc_ranged.place_forget()
        mywin.acc_magic.place_forget()
        mywin.str_melee.place_forget()
        mywin.str_ranged.place_forget()
        mywin.str_magic.place_forget()
        mywin.melee_def.place_forget()
        mywin.ranged_def.place_forget()
        mywin.magic_def.place_forget()
    if mywin.enemy_fight.winfo_viewable() or mywin.enemy_list1.winfo_viewable() or mywin.enemy_list2.winfo_viewable()\
            or mywin.enemy_list3.winfo_viewable() or mywin.enemy_list4.winfo_viewable():
        # If in combat, keep fight button visible for easy restarting
        if user.curr_action != "combat":
            mywin.enemy_fight.place_forget()
        for i in range(1, 5):
            vars(mywin)['enemy_list' + str(i)].place_forget()
            vars(mywin)['enemy' + str(i) + '_lbl'].place_forget()
            vars(mywin)['enemy_list' + str(i)].deselect()
    if mywin.npc_list1.winfo_viewable() or mywin.npc_name.winfo_viewable() or mywin.npc_list2.winfo_viewable()\
            or mywin.npc_list3.winfo_viewable():
        for i in range(1, 4):
            vars(mywin)['npc_list' + str(i)].place_forget()
            vars(mywin)['npc' + str(i) + '_lbl'].place_forget()
            vars(mywin)['npc_list' + str(i)].deselect()
        mywin.interact_npc.place_forget()
        mywin.open_shop.place_forget()
        mywin.npc_name.place_forget()
        mywin.npc_dialogue.place_forget()
        mywin.npc_response_1.place_forget()
        mywin.npc_response_2.place_forget()
    if mywin.skill_list1.winfo_viewable() or mywin.skill_start.winfo_viewable():
        mywin.skill_start.place_forget()
        for i in range(1, 5):
            vars(mywin)['skill_list' + str(i)].place_forget()
            vars(mywin)['skill_list' + str(i)].deselect()
            vars(mywin)['skill' + str(i) + '_lbl'].place_forget()
    if mywin.craft_1.winfo_viewable():
        for i in range(4):
            vars(mywin)['craft_' + str(i)].place_forget()
            vars(mywin)['craft_' + str(i)].deselect()
        mywin.start_craft.place_forget()
        mywin.stop_craft.place_forget()
        mywin.cooks_left.place_forget()
    if mywin.inv_0.winfo_viewable():
        mywin.equip_item.place_forget()
        mywin.drop_item.place_forget()
        mywin.examine_item.place_forget()
        mywin.crafting.place_forget()
        mywin.eat.place_forget()
        mywin.burn.place_forget()
        mywin.selected_inv_item.place_forget()
        mywin.fletching.place_forget()
        for i in range(28):
            vars(mywin)['inv_' + str(i)].place_forget()
    if mywin.skill_0.winfo_viewable():
        for i in range(14):
            vars(mywin)['skill_' + str(i)].place_forget()
        mywin.combat_lvl.place_forget()
    if mywin.spell_0.winfo_viewable() or mywin.spell_16.winfo_viewable():
        for i in range(20):
            vars(mywin)['spell_' + str(i)].place_forget()
        mywin.utility_spells.place_forget()
        mywin.combat_spells.place_forget()
    else:
        # Display spellbook interface, default to combat spells
        mywin.combat_spells.place(relx=0.35, rely=0.6, relwidth=0.15, relheight=0.05)
        mywin.utility_spells.place(relx=0.5, rely=0.6, relwidth=0.15, relheight=0.05)
        mywin.combat_spells.invoke()


def list_cooking():
    """Check for conflicting interfaces and close them before opening the cooking interface.

    If this interface is already visible, close it instead.
    """
    # List of activities that prevent this interface from opening
    if any([(user.curr_action == a) for a in ['banking', 'shopping', 'smithing', 'smelting',
                                              'fletching', 'crafting', 'skilling', 'combat']]):
        return
    # Check for items to cook
    if not user.inventory.is_cookable() and user.curr_action != "cooking":
        mywin.insert_text_thread("You don't have anything to cook right now.", 'warning')
        mywin.start_cook.place_forget()
        return
    user.curr_area.selection = None
    user.curr_item = 0
    if mywin.fletch_0.winfo_viewable():
        for i in range(6):
            vars(mywin)['fletch_' + str(i)].place_forget()
            vars(mywin)['fletch_' + str(i)].deselect()
        mywin.start_fletch.place_forget()
        mywin.stop_fletch.place_forget()
        mywin.cooks_left.place_forget()
    if mywin.spell_0.winfo_viewable() or mywin.spell_16.winfo_viewable():
        for i in range(20):
            vars(mywin)['spell_' + str(i)].place_forget()
        mywin.utility_spells.place_forget()
        mywin.combat_spells.place_forget()
    if mywin.bronze_tab.winfo_viewable():
        j = 0
        for i in ['bronze_', 'iron_', 'steel_', 'mithril_', 'adamant_', 'rune_']:
            vars(mywin)[i + 'tab'].place_forget()
            vars(mywin)[i + 'tab'].deselect()
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            j += 1
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            if j < 5:
                j += 1
        mywin.start_smith.place_forget()
        mywin.stop_smith.place_forget()
        user.curr_item = 0
    if mywin.quest_info.winfo_viewable():
        mywin.quest_info.place_forget()
    if mywin.start_smelt.winfo_viewable():
        mywin.bronze_bar.place_forget()
        mywin.iron_bar.place_forget()
        mywin.steel_bar.place_forget()
        mywin.mithril_bar.place_forget()
        mywin.adamant_bar.place_forget()
        mywin.rune_bar.place_forget()
        mywin.start_smelt.place_forget()
        mywin.stop_smith.place_forget()
        mywin.cooks_left.place_forget()
    if mywin.skill_0.winfo_viewable():
        for i in range(14):
            vars(mywin)['skill_' + str(i)].place_forget()
        mywin.combat_lvl.place_forget()
    if mywin.equipment_ring.winfo_viewable():
        mywin.equipment_head.place_forget()
        mywin.equipment_neck.place_forget()
        mywin.equipment_body.place_forget()
        mywin.equipment_legs.place_forget()
        mywin.equipment_feet.place_forget()
        mywin.equipment_cape.place_forget()
        mywin.equipment_weapon.place_forget()
        mywin.equipment_hands.place_forget()
        mywin.equipment_ammo.place_forget()
        mywin.equipment_shield.place_forget()
        mywin.equipment_ring.place_forget()
        mywin.att_speed.place_forget()
        mywin.acc_melee.place_forget()
        mywin.acc_ranged.place_forget()
        mywin.acc_magic.place_forget()
        mywin.str_melee.place_forget()
        mywin.str_ranged.place_forget()
        mywin.str_magic.place_forget()
        mywin.melee_def.place_forget()
        mywin.ranged_def.place_forget()
        mywin.magic_def.place_forget()
    if mywin.inv_0.winfo_viewable():
        mywin.equip_item.place_forget()
        mywin.drop_item.place_forget()
        mywin.crafting.place_forget()
        mywin.eat.place_forget()
        mywin.burn.place_forget()
        mywin.examine_item.place_forget()
        mywin.selected_inv_item.place_forget()
        mywin.fletching.place_forget()
        for i in range(28):
            vars(mywin)['inv_' + str(i)].place_forget()
    if mywin.craft_1.winfo_viewable():
        for i in range(4):
            vars(mywin)['craft_' + str(i)].place_forget()
            vars(mywin)['craft_' + str(i)].deselect()
        mywin.start_craft.place_forget()
        mywin.stop_craft.place_forget()
        mywin.cooks_left.place_forget()
    if mywin.enemy_fight.winfo_viewable() or mywin.enemy_list1.winfo_viewable() or mywin.enemy_list2.winfo_viewable()\
            or mywin.enemy_list3.winfo_viewable() or mywin.enemy_list4.winfo_viewable():
        mywin.enemy_fight.place_forget()
        for i in range(1, 5):
            vars(mywin)['enemy_list' + str(i)].place_forget()
            vars(mywin)['enemy' + str(i) + '_lbl'].place_forget()
            vars(mywin)['enemy_list' + str(i)].deselect()
    if mywin.skill_list1.winfo_viewable() or mywin.skill_start.winfo_viewable():
        mywin.skill_start.place_forget()
        for i in range(1, 5):
            vars(mywin)['skill_list' + str(i)].place_forget()
            vars(mywin)['skill_list' + str(i)].deselect()
            vars(mywin)['skill' + str(i) + '_lbl'].place_forget()
    if mywin.npc_list1.winfo_viewable() or mywin.npc_name.winfo_viewable() or mywin.npc_list2.winfo_viewable()\
            or mywin.npc_list3.winfo_viewable():
        for i in range(1, 4):
            vars(mywin)['npc_list' + str(i)].place_forget()
            vars(mywin)['npc' + str(i) + '_lbl'].place_forget()
            vars(mywin)['npc_list' + str(i)].deselect()
        mywin.interact_npc.place_forget()
        mywin.open_shop.place_forget()
        mywin.npc_name.place_forget()
        mywin.npc_dialogue.place_forget()
        mywin.npc_response_1.place_forget()
        mywin.npc_response_2.place_forget()
    if mywin.start_cook.winfo_viewable():
        for i in range(10):
            vars(mywin)['cook_' + str(i)].place_forget()
            vars(mywin)['cook_' + str(i)].deselect()
            # If cooking, keep key information visible
            if user.curr_action != "cooking":
                mywin.start_cook.place_forget()
                mywin.stop_cook.place_forget()
                mywin.cooks_left.place_forget()
                user.curr_item = 0
    else:
        # Display cooking interface:
        # Find inventory slots with cook-able items, display info about these items on each button and store slot
        # number for each button command to use when pressed
        slots = user.inventory.is_cookable()
        cook_items = [vars(user.inventory)['slot'+str(i)][0] for i in slots]
        cook_slots = [x for _, x in sorted(zip(cook_items, slots))]
        cook_items.sort()
        cook_items = [Items[i] for i in cook_items]
        for i in range(len(cook_items)):
            vars(mywin)['cook_' + str(i)].place(relx=0.25 + 0.125 * (i % 4), rely=0.6 + 0.0875 * (i//4),
                                                relwidth=0.125, relheight=0.0875)
            vars(mywin)['cook_' + str(i)].configure(text=f"{cook_items[i].name}\nLevel: "
                                                         f"{max(cook_items[i].skill_reqs['Cooking'], 1)}")
            cook_list[i] = cook_slots[i]
        mywin.start_cook.place(relx=0.6, rely=0.5, relwidth=0.15, relheight=0.1)


def list_smelting():
    """Check for conflicting interfaces and close them before opening the smelting interface.

    If this interface is already visible, close it instead.
    """
    # List of activities that prevent this interface from opening
    if any([(user.curr_action == a) for a in ['banking', 'shopping', 'smithing', 'cooking',
                                              'fletching', 'crafting', 'skilling', 'combat']]):
        return
    user.curr_area.selection = None
    user.curr_item = 0
    if mywin.fletch_0.winfo_viewable():
        for i in range(6):
            vars(mywin)['fletch_' + str(i)].place_forget()
            vars(mywin)['fletch_' + str(i)].deselect()
        mywin.start_fletch.place_forget()
        mywin.stop_fletch.place_forget()
        mywin.cooks_left.place_forget()
    if mywin.quest_info.winfo_viewable():
        mywin.quest_info.place_forget()
    if mywin.spell_0.winfo_viewable() or mywin.spell_16.winfo_viewable():
        for i in range(20):
            vars(mywin)['spell_' + str(i)].place_forget()
        mywin.utility_spells.place_forget()
        mywin.combat_spells.place_forget()
    if mywin.bronze_tab.winfo_viewable():
        j = 0
        for i in ['bronze_', 'iron_', 'steel_', 'mithril_', 'adamant_', 'rune_']:
            vars(mywin)[i + 'tab'].place_forget()
            vars(mywin)[i + 'tab'].deselect()
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            j += 1
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            if j < 5:
                j += 1
        mywin.start_smith.place_forget()
        mywin.stop_smith.place_forget()
        user.curr_item = 0
    if mywin.skill_0.winfo_viewable():
        for i in range(14):
            vars(mywin)['skill_' + str(i)].place_forget()
        mywin.combat_lvl.place_forget()
    if mywin.equipment_ring.winfo_viewable():
        mywin.equipment_head.place_forget()
        mywin.equipment_neck.place_forget()
        mywin.equipment_body.place_forget()
        mywin.equipment_legs.place_forget()
        mywin.equipment_feet.place_forget()
        mywin.equipment_cape.place_forget()
        mywin.equipment_weapon.place_forget()
        mywin.equipment_hands.place_forget()
        mywin.equipment_ammo.place_forget()
        mywin.equipment_shield.place_forget()
        mywin.equipment_ring.place_forget()
        mywin.att_speed.place_forget()
        mywin.acc_melee.place_forget()
        mywin.acc_ranged.place_forget()
        mywin.acc_magic.place_forget()
        mywin.str_melee.place_forget()
        mywin.str_ranged.place_forget()
        mywin.str_magic.place_forget()
        mywin.melee_def.place_forget()
        mywin.ranged_def.place_forget()
        mywin.magic_def.place_forget()
    if mywin.inv_0.winfo_viewable():
        mywin.equip_item.place_forget()
        mywin.drop_item.place_forget()
        mywin.crafting.place_forget()
        mywin.eat.place_forget()
        mywin.burn.place_forget()
        mywin.examine_item.place_forget()
        mywin.selected_inv_item.place_forget()
        mywin.fletching.place_forget()
        for i in range(28):
            vars(mywin)['inv_' + str(i)].place_forget()
    if mywin.craft_1.winfo_viewable():
        for i in range(4):
            vars(mywin)['craft_' + str(i)].place_forget()
            vars(mywin)['craft_' + str(i)].deselect()
        mywin.start_craft.place_forget()
        mywin.stop_craft.place_forget()
        mywin.cooks_left.place_forget()
    if mywin.enemy_fight.winfo_viewable() or mywin.enemy_list1.winfo_viewable() or mywin.enemy_list2.winfo_viewable()\
            or mywin.enemy_list3.winfo_viewable() or mywin.enemy_list4.winfo_viewable():
        mywin.enemy_fight.place_forget()
        for i in range(1, 5):
            vars(mywin)['enemy_list' + str(i)].place_forget()
            vars(mywin)['enemy' + str(i) + '_lbl'].place_forget()
            vars(mywin)['enemy_list' + str(i)].deselect()
    if mywin.skill_list1.winfo_viewable() or mywin.skill_start.winfo_viewable():
        mywin.skill_start.place_forget()
        for i in range(1, 5):
            vars(mywin)['skill_list' + str(i)].place_forget()
            vars(mywin)['skill_list' + str(i)].deselect()
            vars(mywin)['skill' + str(i) + '_lbl'].place_forget()
    if mywin.npc_list1.winfo_viewable() or mywin.npc_name.winfo_viewable() or mywin.npc_list2.winfo_viewable()\
            or mywin.npc_list3.winfo_viewable():
        for i in range(1, 4):
            vars(mywin)['npc_list' + str(i)].place_forget()
            vars(mywin)['npc' + str(i) + '_lbl'].place_forget()
            vars(mywin)['npc_list' + str(i)].deselect()
        mywin.interact_npc.place_forget()
        mywin.open_shop.place_forget()
        mywin.npc_name.place_forget()
        mywin.npc_dialogue.place_forget()
        mywin.npc_response_1.place_forget()
        mywin.npc_response_2.place_forget()
    if mywin.start_cook.winfo_viewable():
        for i in range(10):
            vars(mywin)['cook_' + str(i)].place_forget()
            vars(mywin)['cook_' + str(i)].deselect()
            mywin.start_cook.place_forget()
            mywin.stop_cook.place_forget()
            mywin.cooks_left.place_forget()
            user.curr_item = 0
    if mywin.start_smelt.winfo_viewable():
        for i in ['bronze_', 'iron_', 'steel_', 'mithril_', 'adamant_', 'rune_']:
            vars(mywin)[i + 'bar'].place_forget()
            vars(mywin)[i + 'bar'].deselect()
        # If smelting, keep key information visible
        if user.curr_action != 'smelting':
            mywin.start_smelt.place_forget()
            mywin.stop_smith.place_forget()
            mywin.cooks_left.place_forget()
            mywin.curr_item = 0
    else:
        # Display smelting interface
        # Grey out anything that user doesn't have resources for
        mywin.bronze_bar.place(relx=0.25, rely=0.6, relwidth=0.125, relheight=0.15)
        mywin.bronze_bar.configure(bg='gray35')
        mywin.iron_bar.place(relx=0.375, rely=0.6, relwidth=0.125, relheight=0.15)
        mywin.iron_bar.configure(bg='gray35')
        mywin.steel_bar.place(relx=0.5, rely=0.6, relwidth=0.125, relheight=0.15)
        mywin.steel_bar.configure(bg='gray35')
        mywin.mithril_bar.place(relx=0.625, rely=0.6, relwidth=0.125, relheight=0.15)
        mywin.mithril_bar.configure(bg='gray35')
        mywin.adamant_bar.place(relx=0.25, rely=0.75, relwidth=0.125, relheight=0.15)
        mywin.adamant_bar.configure(bg='gray35')
        mywin.rune_bar.place(relx=0.375, rely=0.75, relwidth=0.125, relheight=0.15)
        mywin.rune_bar.configure(bg='gray35')
        mywin.start_smelt.place(relx=0.6, rely=0.5, relwidth=0.15, relheight=0.1)
        if user.inventory.is_in_inv(77) and user.inventory.is_in_inv(78):
            mywin.bronze_bar.configure(bg='grey')
        if user.inventory.is_in_inv(89):
            mywin.iron_bar.configure(bg='grey')
        if user.inventory.is_in_inv(100):
            if user.inventory.is_in_inv(90):
                mywin.steel_bar.configure(bg='grey')
            if user.inventory.is_in_inv(111) and user.inventory.is_in_inv(100)[1] >= 2:
                mywin.mithril_bar.configure(bg='grey')
            if user.inventory.is_in_inv(122) and user.inventory.is_in_inv(100)[1] >= 3:
                mywin.adamant_bar.configure(bg='grey')
            if user.inventory.is_in_inv(133) and user.inventory.is_in_inv(100)[1] >= 4:
                mywin.rune_bar.configure(bg='grey')


def list_smithing():
    """Check for conflicting interfaces and close them before opening the smithing interface.

    If this interface is already visible, close it instead.
    """
    # List of activities that prevent this interface from opening
    if any([(user.curr_action == a) for a in ['banking', 'shopping', 'smelting', 'cooking',
                                              'fletching', 'crafting', 'skilling', 'combat']]):
        return
    user.curr_area.selection = None
    user.curr_item = 0
    if mywin.fletch_0.winfo_viewable():
        for i in range(6):
            vars(mywin)['fletch_' + str(i)].place_forget()
            vars(mywin)['fletch_' + str(i)].deselect()
        mywin.start_fletch.place_forget()
        mywin.stop_fletch.place_forget()
        mywin.cooks_left.place_forget()
    if mywin.quest_info.winfo_viewable():
        mywin.quest_info.place_forget()
    if mywin.spell_0.winfo_viewable() or mywin.spell_16.winfo_viewable():
        for i in range(20):
            vars(mywin)['spell_' + str(i)].place_forget()
        mywin.utility_spells.place_forget()
        mywin.combat_spells.place_forget()
    if mywin.skill_0.winfo_viewable():
        for i in range(14):
            vars(mywin)['skill_' + str(i)].place_forget()
        mywin.combat_lvl.place_forget()
    if mywin.equipment_ring.winfo_viewable():
        mywin.equipment_head.place_forget()
        mywin.equipment_neck.place_forget()
        mywin.equipment_body.place_forget()
        mywin.equipment_legs.place_forget()
        mywin.equipment_feet.place_forget()
        mywin.equipment_cape.place_forget()
        mywin.equipment_weapon.place_forget()
        mywin.equipment_hands.place_forget()
        mywin.equipment_ammo.place_forget()
        mywin.equipment_shield.place_forget()
        mywin.equipment_ring.place_forget()
        mywin.att_speed.place_forget()
        mywin.acc_melee.place_forget()
        mywin.acc_ranged.place_forget()
        mywin.acc_magic.place_forget()
        mywin.str_melee.place_forget()
        mywin.str_ranged.place_forget()
        mywin.str_magic.place_forget()
        mywin.melee_def.place_forget()
        mywin.ranged_def.place_forget()
        mywin.magic_def.place_forget()
    if mywin.inv_0.winfo_viewable():
        mywin.equip_item.place_forget()
        mywin.drop_item.place_forget()
        mywin.eat.place_forget()
        mywin.crafting.place_forget()
        mywin.burn.place_forget()
        mywin.examine_item.place_forget()
        mywin.selected_inv_item.place_forget()
        mywin.fletching.place_forget()
        for i in range(28):
            vars(mywin)['inv_' + str(i)].place_forget()
    if mywin.enemy_fight.winfo_viewable() or mywin.enemy_list1.winfo_viewable() or mywin.enemy_list2.winfo_viewable()\
            or mywin.enemy_list3.winfo_viewable() or mywin.enemy_list4.winfo_viewable():
        mywin.enemy_fight.place_forget()
        for i in range(1, 5):
            vars(mywin)['enemy_list' + str(i)].place_forget()
            vars(mywin)['enemy' + str(i) + '_lbl'].place_forget()
            vars(mywin)['enemy_list' + str(i)].deselect()
    if mywin.skill_list1.winfo_viewable() or mywin.skill_start.winfo_viewable():
        mywin.skill_start.place_forget()
        for i in range(1, 5):
            vars(mywin)['skill_list' + str(i)].place_forget()
            vars(mywin)['skill_list' + str(i)].deselect()
            vars(mywin)['skill' + str(i) + '_lbl'].place_forget()
    if mywin.npc_list1.winfo_viewable() or mywin.npc_name.winfo_viewable() or mywin.npc_list2.winfo_viewable()\
            or mywin.npc_list3.winfo_viewable():
        for i in range(1, 4):
            vars(mywin)['npc_list' + str(i)].place_forget()
            vars(mywin)['npc' + str(i) + '_lbl'].place_forget()
            vars(mywin)['npc_list' + str(i)].deselect()
        mywin.interact_npc.place_forget()
        mywin.open_shop.place_forget()
        mywin.npc_name.place_forget()
        mywin.npc_dialogue.place_forget()
        mywin.npc_response_1.place_forget()
        mywin.npc_response_2.place_forget()
    if mywin.craft_1.winfo_viewable():
        for i in range(4):
            vars(mywin)['craft_' + str(i)].place_forget()
            vars(mywin)['craft_' + str(i)].deselect()
        mywin.start_craft.place_forget()
        mywin.stop_craft.place_forget()
        mywin.cooks_left.place_forget()
    if mywin.start_cook.winfo_viewable():
        for i in range(10):
            vars(mywin)['cook_' + str(i)].place_forget()
            vars(mywin)['cook_' + str(i)].deselect()
            mywin.start_cook.place_forget()
            mywin.stop_cook.place_forget()
            mywin.cooks_left.place_forget()
            user.curr_item = 0
    if mywin.start_smelt.winfo_viewable():
        for i in ['bronze_', 'iron_', 'steel_', 'mithril_', 'adamant_', 'rune_']:
            vars(mywin)[i + 'bar'].place_forget()
            vars(mywin)[i + 'bar'].deselect()
        mywin.start_smelt.place_forget()
        mywin.stop_smith.place_forget()
        mywin.cooks_left.place_forget()
        mywin.curr_item = 0
    if mywin.bronze_tab.winfo_viewable():
        j = 0
        for i in ['bronze_', 'iron_', 'steel_', 'mithril_', 'adamant_', 'rune_']:
            vars(mywin)[i + 'tab'].place_forget()
            vars(mywin)[i + 'tab'].deselect()
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            j += 1
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            if j < 5:
                j += 1
        # If smithing, keep key information visible
        if user.curr_action != 'smithing':
            mywin.start_smith.place_forget()
            mywin.stop_smith.place_forget()
            mywin.cooks_left.place_forget()
            user.curr_item = 0
    else:
        # Display smithing interface
        j = 0
        mywin.start_smith.place(relx=0.6, rely=0.5, relwidth=0.15, relheight=0.1)
        for i in ['bronze_', 'iron_', 'steel_', 'mithril_', 'adamant_', 'rune_']:
            vars(mywin)[i + 'tab'].place(relx=0.25 + (0.5/6)*j, rely=0.6, relwidth=(0.5/6), relheight=0.05)
            j += 1


def list_fletching(inv_selection):
    """Check for conflicting interfaces and close them before opening the fletching interface.

    inv_selection = [item_id, quantity] \n
    If this interface is already visible, close it instead.
    """
    # List of activities that prevent this interface from opening
    if any([(user.curr_action == a) for a in ['banking', 'shopping', 'smelting', 'cooking',
                                              'smithing', 'crafting', 'skilling', 'combat']]):
        return
    item = inv_selection[0]
    # Check that user can perform at least one action with the selected item
    if user.skills['Fletching'][0] < item.skill_reqs['Fletching']:
        mywin.insert_text_thread(f"You aren't experienced enough to fletch anything with that.", 'warning')
        return
    user.curr_area.selection = None
    user.curr_item = 0
    if mywin.spell_0.winfo_viewable() or mywin.spell_16.winfo_viewable():
        for i in range(20):
            vars(mywin)['spell_' + str(i)].place_forget()
        mywin.utility_spells.place_forget()
        mywin.combat_spells.place_forget()
    if mywin.skill_0.winfo_viewable():
        for i in range(14):
            vars(mywin)['skill_' + str(i)].place_forget()
        mywin.combat_lvl.place_forget()
    if mywin.equipment_ring.winfo_viewable():
        mywin.equipment_head.place_forget()
        mywin.equipment_neck.place_forget()
        mywin.equipment_body.place_forget()
        mywin.equipment_legs.place_forget()
        mywin.equipment_feet.place_forget()
        mywin.equipment_cape.place_forget()
        mywin.equipment_weapon.place_forget()
        mywin.equipment_hands.place_forget()
        mywin.equipment_ammo.place_forget()
        mywin.equipment_shield.place_forget()
        mywin.equipment_ring.place_forget()
        mywin.att_speed.place_forget()
        mywin.acc_melee.place_forget()
        mywin.acc_ranged.place_forget()
        mywin.acc_magic.place_forget()
        mywin.str_melee.place_forget()
        mywin.str_ranged.place_forget()
        mywin.str_magic.place_forget()
        mywin.melee_def.place_forget()
        mywin.ranged_def.place_forget()
        mywin.magic_def.place_forget()
    if mywin.quest_info.winfo_viewable():
        mywin.quest_info.place_forget()
    if mywin.inv_0.winfo_viewable():
        mywin.equip_item.place_forget()
        mywin.drop_item.place_forget()
        mywin.eat.place_forget()
        mywin.burn.place_forget()
        mywin.crafting.place_forget()
        mywin.examine_item.place_forget()
        mywin.selected_inv_item.place_forget()
        mywin.fletching.place_forget()
        for i in range(28):
            vars(mywin)['inv_' + str(i)].place_forget()
    if mywin.enemy_fight.winfo_viewable() or mywin.enemy_list1.winfo_viewable() or mywin.enemy_list2.winfo_viewable()\
            or mywin.enemy_list3.winfo_viewable() or mywin.enemy_list4.winfo_viewable():
        mywin.enemy_fight.place_forget()
        for i in range(1, 5):
            vars(mywin)['enemy_list' + str(i)].place_forget()
            vars(mywin)['enemy' + str(i) + '_lbl'].place_forget()
            vars(mywin)['enemy_list' + str(i)].deselect()
    if mywin.skill_list1.winfo_viewable() or mywin.skill_start.winfo_viewable():
        mywin.skill_start.place_forget()
        for i in range(1, 5):
            vars(mywin)['skill_list' + str(i)].place_forget()
            vars(mywin)['skill_list' + str(i)].deselect()
            vars(mywin)['skill' + str(i) + '_lbl'].place_forget()
    if mywin.npc_list1.winfo_viewable() or mywin.npc_name.winfo_viewable() or mywin.npc_list2.winfo_viewable()\
            or mywin.npc_list3.winfo_viewable():
        for i in range(1, 4):
            vars(mywin)['npc_list' + str(i)].place_forget()
            vars(mywin)['npc' + str(i) + '_lbl'].place_forget()
            vars(mywin)['npc_list' + str(i)].deselect()
        mywin.interact_npc.place_forget()
        mywin.open_shop.place_forget()
        mywin.npc_name.place_forget()
        mywin.npc_dialogue.place_forget()
        mywin.npc_response_1.place_forget()
        mywin.npc_response_2.place_forget()
    if mywin.start_cook.winfo_viewable():
        for i in range(10):
            vars(mywin)['cook_' + str(i)].place_forget()
            vars(mywin)['cook_' + str(i)].deselect()
            mywin.start_cook.place_forget()
            mywin.stop_cook.place_forget()
            mywin.cooks_left.place_forget()
            user.curr_item = 0
    if mywin.start_smelt.winfo_viewable():
        for i in ['bronze_', 'iron_', 'steel_', 'mithril_', 'adamant_', 'rune_']:
            vars(mywin)[i + 'bar'].place_forget()
            vars(mywin)[i + 'bar'].deselect()
        mywin.start_smelt.place_forget()
        mywin.stop_smith.place_forget()
        mywin.cooks_left.place_forget()
        mywin.curr_item = 0
    if mywin.craft_1.winfo_viewable():
        for i in range(4):
            vars(mywin)['craft_' + str(i)].place_forget()
            vars(mywin)['craft_' + str(i)].deselect()
        mywin.start_craft.place_forget()
        mywin.stop_craft.place_forget()
        mywin.cooks_left.place_forget()
    if mywin.bronze_tab.winfo_viewable():
        j = 0
        for i in ['bronze_', 'iron_', 'steel_', 'mithril_', 'adamant_', 'rune_']:
            vars(mywin)[i + 'tab'].place_forget()
            vars(mywin)[i + 'tab'].deselect()
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            j += 1
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            if j < 5:
                j += 1
        mywin.start_smith.place_forget()
        mywin.stop_smith.place_forget()
        mywin.cooks_left.place_forget()
        user.curr_item = 0
    if mywin.fletch_0.winfo_viewable():
        for i in range(6):
            vars(mywin)['fletch_' + str(i)].place_forget()
            vars(mywin)['fletch_' + str(i)].deselect()
        # If fletching, keep key information visible
        if user.curr_action != 'fletching':
            mywin.start_fletch.place_forget()
            mywin.stop_fletch.place_forget()
            mywin.cooks_left.place_forget()
    else:
        # Display the fletching interface, differing based on selected item (show all possible products from item)
        if user.flags.get('tut_prog', 250) == 18:
            user.flags['tut_prog'] = 19
        for i in range(6):
            vars(mywin)['fletch_' + str(i)].configure(bg='grey')
        mywin.start_fletch.place(relx=0.6, rely=0.5, relwidth=0.15, relheight=0.1)
        num_buttons = 1
        log_bow_conversion = {3: 150, 4: 154, 5: 158, 7: 162, 9: 166, 10: 170}
        # Logs / unstrung bows selected
        if item.id > 149 or item.id < 11:
            fletch_list[0] = 29
            num_buttons = 5
            curr_req = Items[item.id].skill_reqs['Fletching']
            # Convert unstrung bow id to log id
            log_id = item.id if item.id < 20 else (3 + (curr_req // 15) + ((curr_req // 15) // 3) +
                                                   ((curr_req // 15) // 4))
            # All log types can make arrow shafts but at different quantities
            mywin.fletch_0.configure(text=f"Arrow shafts\n({15 + 15*(Items[log_id].skill_reqs['Fletching'] // 15)})\n"
                                          f"Level: 1\n1 x {Items[log_id].name}")
            if not user.inventory.is_in_inv(log_id):
                mywin.fletch_0.configure(bg='grey35')
            base_id = log_bow_conversion[log_id] - 1
            for i in range(1, 5):
                # Display the possible products which can be calculated from log id
                fletch_list[i] = base_id + i
                product = Items[base_id + i]
                num = base_id + i
                alt_product = product
                # alt_product is used where resources or requirements are not stored on the product
                # Item id alternates between strung and unstrung bows, so this keeps required resources accurate
                if i % 2 == 0:
                    vars(mywin)['fletch_' + str(i)].configure(
                     text=f"{Items[base_id+i].name}\n\nLevel: {Items[base_id+i - 1].skill_reqs['Fletching']}\n1 x "
                          f"{Items[base_id+i-1].name},\n1 x Bow string")
                    if not user.inventory.is_in_inv(base_id+i-1) or not user.inventory.is_in_inv(37):
                        vars(mywin)['fletch_' + str(i)].configure(bg='grey35')
                    alt_product = Items[num - 1]
                else:
                    vars(mywin)['fletch_' + str(i)].configure(
                        text=f"{Items[base_id+i].name}\n\nLevel: {Items[base_id+i].skill_reqs['Fletching']}\n1 x"
                             f" {Items[log_id].name}")
                    if not user.inventory.is_in_inv(log_id):
                        vars(mywin)['fletch_' + str(i)].configure(bg='grey35')
                if user.skills['Fletching'][0] < alt_product.skill_reqs['Fletching']:
                    vars(mywin)['fletch_' + str(i)].configure(bg='grey35')
        # Arrow shafts selected
        if item.id == 29:
            fletch_list[0] = 30
            mywin.fletch_0.configure(text="Headless arrows\nLevel: 1\n 15 x Arrow shafts\n15 x Feathers")
            num_buttons = 1
            if not user.inventory.is_in_inv(29) or not user.inventory.is_in_inv(36):
                mywin.fletch_0.configure(bg='grey35')
        # Headless arrows or arrowheads selected
        if item.id == 30 or item.id in range(80, 136, 11):
            arrowheads = [80, 91, 102, 113, 124, 135]
            num_buttons = 6
            for i in range(6):
                product = Items[144 + i]
                alt_product = product
                fletch_list[i] = 144 + i
                vars(mywin)['fletch_' + str(i)].configure(
                    text=f"{Items[144+i].name}\n\nLevel: {Items[arrowheads[i]].skill_reqs['Fletching']}"
                         f"\n15 x Headless arrows,\n15 x {Items[arrowheads[i]].name}")
                for index, resource in enumerate(product.resources.keys()):
                    if index == 1:
                        alt_product = Items[resource]
                if user.skills['Fletching'][0] < alt_product.skill_reqs['Fletching']:
                    vars(mywin)['fletch_' + str(i)].configure(bg='grey35')
                elif not user.inventory.is_in_inv(30) or not user.inventory.is_in_inv(arrowheads[i]):
                    vars(mywin)['fletch_' + str(i)].configure(bg='grey35')
        for i in range(num_buttons):
            vars(mywin)['fletch_' + str(i)].place(relx=0.25 + 0.125*(i % 4), rely=0.6 + 0.15*(i // 4), relwidth=0.125,
                                                  relheight=0.15)


def list_crafting(inv_selection):
    """Check for conflicting interfaces and close them before opening the crafting interface.

    inv_selection = [item_id, quantity] \n
    If this interface is already visible, close it instead.
    """
    # List of activities that prevent this interface from opening
    if any([(user.curr_action == a) for a in ['banking', 'shopping', 'smelting', 'cooking',
                                              'smithing', 'skilling', 'combat', 'fletching']]):
        return
    item = inv_selection[0]
    user.curr_area.selection = None
    user.curr_item = 0
    if mywin.spell_0.winfo_viewable() or mywin.spell_16.winfo_viewable():
        for i in range(20):
            vars(mywin)['spell_' + str(i)].place_forget()
        mywin.utility_spells.place_forget()
        mywin.combat_spells.place_forget()
    if mywin.skill_0.winfo_viewable():
        for i in range(14):
            vars(mywin)['skill_' + str(i)].place_forget()
        mywin.combat_lvl.place_forget()
    if mywin.equipment_ring.winfo_viewable():
        mywin.equipment_head.place_forget()
        mywin.equipment_neck.place_forget()
        mywin.equipment_body.place_forget()
        mywin.equipment_legs.place_forget()
        mywin.equipment_feet.place_forget()
        mywin.equipment_cape.place_forget()
        mywin.equipment_weapon.place_forget()
        mywin.equipment_hands.place_forget()
        mywin.equipment_ammo.place_forget()
        mywin.equipment_shield.place_forget()
        mywin.equipment_ring.place_forget()
        mywin.att_speed.place_forget()
        mywin.acc_melee.place_forget()
        mywin.acc_ranged.place_forget()
        mywin.acc_magic.place_forget()
        mywin.str_melee.place_forget()
        mywin.str_ranged.place_forget()
        mywin.str_magic.place_forget()
        mywin.melee_def.place_forget()
        mywin.ranged_def.place_forget()
        mywin.magic_def.place_forget()
    if mywin.quest_info.winfo_viewable():
        mywin.quest_info.place_forget()
    if mywin.inv_0.winfo_viewable():
        mywin.equip_item.place_forget()
        mywin.drop_item.place_forget()
        mywin.eat.place_forget()
        mywin.crafting.place_forget()
        mywin.burn.place_forget()
        mywin.examine_item.place_forget()
        mywin.selected_inv_item.place_forget()
        mywin.fletching.place_forget()
        for i in range(28):
            vars(mywin)['inv_' + str(i)].place_forget()
    if mywin.enemy_fight.winfo_viewable() or mywin.enemy_list1.winfo_viewable() or mywin.enemy_list2.winfo_viewable()\
            or mywin.enemy_list3.winfo_viewable() or mywin.enemy_list4.winfo_viewable():
        mywin.enemy_fight.place_forget()
        for i in range(1, 5):
            vars(mywin)['enemy_list' + str(i)].place_forget()
            vars(mywin)['enemy' + str(i) + '_lbl'].place_forget()
            vars(mywin)['enemy_list' + str(i)].deselect()
    if mywin.skill_list1.winfo_viewable() or mywin.skill_start.winfo_viewable():
        mywin.skill_start.place_forget()
        for i in range(1, 5):
            vars(mywin)['skill_list' + str(i)].place_forget()
            vars(mywin)['skill_list' + str(i)].deselect()
            vars(mywin)['skill' + str(i) + '_lbl'].place_forget()
    if mywin.npc_list1.winfo_viewable() or mywin.npc_name.winfo_viewable() or mywin.npc_list2.winfo_viewable()\
            or mywin.npc_list3.winfo_viewable():
        for i in range(1, 4):
            vars(mywin)['npc_list' + str(i)].place_forget()
            vars(mywin)['npc' + str(i) + '_lbl'].place_forget()
            vars(mywin)['npc_list' + str(i)].deselect()
        mywin.interact_npc.place_forget()
        mywin.open_shop.place_forget()
        mywin.npc_name.place_forget()
        mywin.npc_dialogue.place_forget()
        mywin.npc_response_1.place_forget()
        mywin.npc_response_2.place_forget()
    if mywin.start_cook.winfo_viewable():
        for i in range(10):
            vars(mywin)['cook_' + str(i)].place_forget()
            vars(mywin)['cook_' + str(i)].deselect()
            mywin.start_cook.place_forget()
            mywin.stop_cook.place_forget()
            mywin.cooks_left.place_forget()
            user.curr_item = 0
    if mywin.start_smelt.winfo_viewable():
        for i in ['bronze_', 'iron_', 'steel_', 'mithril_', 'adamant_', 'rune_']:
            vars(mywin)[i + 'bar'].place_forget()
            vars(mywin)[i + 'bar'].deselect()
        mywin.start_smelt.place_forget()
        mywin.stop_smith.place_forget()
        mywin.cooks_left.place_forget()
        mywin.curr_item = 0
    if mywin.bronze_tab.winfo_viewable():
        j = 0
        for i in ['bronze_', 'iron_', 'steel_', 'mithril_', 'adamant_', 'rune_']:
            vars(mywin)[i + 'tab'].place_forget()
            vars(mywin)[i + 'tab'].deselect()
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            j += 1
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            if j < 5:
                j += 1
        mywin.start_smith.place_forget()
        mywin.stop_smith.place_forget()
        mywin.cooks_left.place_forget()
        user.curr_item = 0
    if mywin.fletch_0.winfo_viewable():
        for i in range(6):
            vars(mywin)['fletch_' + str(i)].place_forget()
            vars(mywin)['fletch_' + str(i)].deselect()
        mywin.start_fletch.place_forget()
        mywin.stop_fletch.place_forget()
        mywin.cooks_left.place_forget()
    if mywin.craft_1.winfo_viewable():
        for i in range(4):
            vars(mywin)['craft_' + str(i)].place_forget()
            vars(mywin)['craft_' + str(i)].deselect()
        # If crafting, keep key information visible
        if user.curr_action != 'crafting':
            mywin.start_craft.place_forget()
            mywin.stop_craft.place_forget()
            mywin.cooks_left.place_forget()
    else:
        # Display crafting interface based on selected item (show possible products from item)
        for i in range(4):
            vars(mywin)['craft_' + str(i)].configure(bg='grey')
        mywin.start_craft.place(relx=0.6, rely=0.5, relwidth=0.15, relheight=0.1)
        num_buttons = 4
        # Normal leather selected (item ids don't work as nicely as the others)
        if item.id == 175:
            for i in range(4):
                # Set up the product item id
                product = Items[31 + i]
                craft_list[i] = 31 + i
                vars(mywin)['craft_' + str(i)].configure(
                    text=f"{product.name}\n\nLevel: {product.skill_reqs['Crafting']}"
                         f"\n{str(max(i, 1))} x {item.name}")
                if user.skills['Crafting'][0] < product.skill_reqs['Crafting']:
                    vars(mywin)['craft_' + str(i)].configure(bg='grey35')
                elif not user.inventory.is_in_inv(175) or user.inventory.is_in_inv(175)[1] < max(i, 1):
                    vars(mywin)['craft_' + str(i)].configure(bg='grey35')
        # Any other leather type selected
        else:
            for i in range(4):
                # Translate item id to product item id
                product = Items[(item.id - 176) * 4 + 181 + i]
                craft_list[i] = (item.id - 176) * 4 + 181 + i
                # Allow wrapping text on button for long names
                name = product.name.split()
                name_0 = ' '.join([name[0], name[1]])
                name_1 = '\n' + name[2]
                name = name_0 + name_1
                item_name = item.name
                item_split = item.name.split(' ')
                if len(item_split) == 3:
                    item_name = ' '.join(item_split[:2]) + '\n' + item_split[2]
                vars(mywin)['craft_' + str(i)].configure(
                    text=f"{name}\n\nLevel: {product.skill_reqs['Crafting']}"
                         f"\n{str(max(i, 1))} x {item_name}")
                if user.skills['Crafting'][0] < product.skill_reqs['Crafting']:
                    vars(mywin)['craft_' + str(i)].configure(bg='grey35')
                elif not user.inventory.is_in_inv(item.id) or user.inventory.is_in_inv(item.id)[1] < max(i, 1):
                    vars(mywin)['craft_' + str(i)].configure(bg='grey35')
        for i in range(num_buttons):
            vars(mywin)['craft_' + str(i)].place(relx=0.25 + 0.125*i, rely=0.6, relwidth=0.125, relheight=0.15)


def list_quest_info(update=False):
    """Check for conflicting interfaces and close them before opening the quest info interface.

    update = bool, doesn't close quest interface if True (default False) \n
    If this interface is already visible, close it instead.
    """
    # List of activities that prevent this interface from opening
    if user.curr_action == 'banking' or user.curr_action == 'shopping':
        return
    if mywin.fletch_0.winfo_viewable():
        for i in range(6):
            vars(mywin)['fletch_' + str(i)].place_forget()
            vars(mywin)['fletch_' + str(i)].deselect()
        # If fletching, keep key information visible
        if user.curr_action != 'fletching':
            mywin.start_fletch.place_forget()
            mywin.stop_fletch.place_forget()
            mywin.cooks_left.place_forget()
    if mywin.spell_0.winfo_viewable() or mywin.spell_16.winfo_viewable():
        for i in range(20):
            vars(mywin)['spell_' + str(i)].place_forget()
        mywin.utility_spells.place_forget()
        mywin.combat_spells.place_forget()
    if mywin.bronze_tab.winfo_viewable():
        j = 0
        for i in ['bronze_', 'iron_', 'steel_', 'mithril_', 'adamant_', 'rune_']:
            vars(mywin)[i + 'tab'].place_forget()
            vars(mywin)[i + 'tab'].deselect()
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            j += 1
            vars(mywin)['smith_item_' + str(j)].place_forget()
            vars(mywin)['smith_item_' + str(j)].deselect()
            if j < 5:
                j += 1
        # If smithing, keep key information visible
        if user.curr_action != 'smithing':
            mywin.start_smith.place_forget()
            mywin.stop_smith.place_forget()
            user.curr_item = 0
    if mywin.start_smelt.winfo_viewable():
        mywin.bronze_bar.place_forget()
        mywin.iron_bar.place_forget()
        mywin.steel_bar.place_forget()
        mywin.mithril_bar.place_forget()
        mywin.adamant_bar.place_forget()
        mywin.rune_bar.place_forget()
        # If smelting, keep key information visible
        if user.curr_action != 'smelting':
            mywin.start_smelt.place_forget()
            mywin.stop_smith.place_forget()
            mywin.cooks_left.place_forget()
    if mywin.skill_0.winfo_viewable():
        for i in range(14):
            vars(mywin)['skill_' + str(i)].place_forget()
        mywin.combat_lvl.place_forget()
    if mywin.equipment_ring.winfo_viewable():
        mywin.equipment_head.place_forget()
        mywin.equipment_neck.place_forget()
        mywin.equipment_body.place_forget()
        mywin.equipment_legs.place_forget()
        mywin.equipment_feet.place_forget()
        mywin.equipment_cape.place_forget()
        mywin.equipment_weapon.place_forget()
        mywin.equipment_hands.place_forget()
        mywin.equipment_ammo.place_forget()
        mywin.equipment_shield.place_forget()
        mywin.equipment_ring.place_forget()
        mywin.att_speed.place_forget()
        mywin.acc_melee.place_forget()
        mywin.acc_ranged.place_forget()
        mywin.acc_magic.place_forget()
        mywin.str_melee.place_forget()
        mywin.str_ranged.place_forget()
        mywin.str_magic.place_forget()
        mywin.melee_def.place_forget()
        mywin.ranged_def.place_forget()
        mywin.magic_def.place_forget()
    if mywin.inv_0.winfo_viewable():
        mywin.equip_item.place_forget()
        mywin.drop_item.place_forget()
        mywin.eat.place_forget()
        mywin.burn.place_forget()
        mywin.examine_item.place_forget()
        mywin.selected_inv_item.place_forget()
        mywin.fletching.place_forget()
        mywin.crafting.place_forget()
        for i in range(28):
            vars(mywin)['inv_' + str(i)].place_forget()
    if mywin.craft_1.winfo_viewable():
        for i in range(4):
            vars(mywin)['craft_' + str(i)].place_forget()
            vars(mywin)['craft_' + str(i)].deselect()
        # If crafting, keep key information visible
        if user.curr_action != 'crafting':
            mywin.start_craft.place_forget()
            mywin.stop_craft.place_forget()
            mywin.cooks_left.place_forget()
    if mywin.enemy_fight.winfo_viewable() or mywin.enemy_list1.winfo_viewable() or mywin.enemy_list2.winfo_viewable()\
            or mywin.enemy_list3.winfo_viewable() or mywin.enemy_list4.winfo_viewable():
        # If in combat, keep fight button visible for easy restarting
        if user.curr_action != 'combat':
            mywin.enemy_fight.place_forget()
        for i in range(1, 5):
            vars(mywin)['enemy_list' + str(i)].place_forget()
            vars(mywin)['enemy' + str(i) + '_lbl'].place_forget()
            vars(mywin)['enemy_list' + str(i)].deselect()
    if mywin.skill_list1.winfo_viewable() or mywin.skill_start.winfo_viewable():
        # If skilling, keep start button visible for easy restarting
        if user.curr_action != 'skilling':
            mywin.skill_start.place_forget()
        for i in range(1, 5):
            vars(mywin)['skill_list' + str(i)].place_forget()
            vars(mywin)['skill_list' + str(i)].deselect()
            vars(mywin)['skill' + str(i) + '_lbl'].place_forget()
    if mywin.npc_list1.winfo_viewable() or mywin.npc_name.winfo_viewable() or mywin.npc_list2.winfo_viewable()\
            or mywin.npc_list3.winfo_viewable():
        for i in range(1, 4):
            vars(mywin)['npc_list' + str(i)].place_forget()
            vars(mywin)['npc' + str(i) + '_lbl'].place_forget()
            vars(mywin)['npc_list' + str(i)].deselect()
        mywin.interact_npc.place_forget()
        mywin.open_shop.place_forget()
        mywin.npc_name.place_forget()
        mywin.npc_dialogue.place_forget()
        mywin.npc_response_1.place_forget()
        mywin.npc_response_2.place_forget()
    if mywin.start_cook.winfo_viewable():
        for i in range(10):
            vars(mywin)['cook_' + str(i)].place_forget()
            vars(mywin)['cook_' + str(i)].deselect()
            # If cooking, keep key information visible
            if user.curr_action != "cooking":
                mywin.start_cook.place_forget()
                mywin.stop_cook.place_forget()
                mywin.cooks_left.place_forget()
                user.curr_item = 0
    if mywin.quest_info.winfo_viewable() and not update:
        mywin.quest_info.place_forget()
    else:
        # Display quest information interface
        if user.flags['tut_prog'] == 31:
            user.flags['tut_prog'] = 32
        mywin.quest_info.place(relx=0.25, rely=0.6, relwidth=0.5, relheight=0.35)
        mywin.quest_info.configure(state=NORMAL)
        mywin.quest_info.delete('1.0', END)
        # For each quest in progress, display the active objectives eg. enemy kills, items collected
        for quest in user.quest_flags:              # eg. [1,4] = quest in list format
            q = Quests[quest[0]]    # q is the actual Quest object
            if quest[1] >= len(q.objectives) or ((obj := q.objectives[quest[1]]).items is None
                                                 and obj.enemies is None):
                # This means the quest is already completed or has no meaningful objectives to track
                continue
            mywin.quest_info.insert(END, q.name + ":", 'title')
            # Display enemy type objectives
            if obj.enemies is not None:
                for enemy_id in obj.enemies.keys():
                    killed = user.flags['kill_' + str(enemy_id)]
                    total = obj.enemies[enemy_id]
                    status = 'complete' if killed >= total else 'incomplete'
                    mywin.quest_info.insert(END, f"\n{Enemies[enemy_id].name}: {killed} / {total}", status)
            # Display item type objectives
            if obj.items is not None:
                for item_id in obj.items.keys():
                    in_inv = user.inventory.is_in_inv(item_id)[1] if user.inventory.is_in_inv(item_id) else 0
                    quant_req = obj.items[item_id]
                    status = 'complete' if in_inv >= quant_req else 'incomplete'
                    mywin.quest_info.insert(END, f"\n{Items[item_id].name}: {in_inv} / {quant_req}", status)
            # End with some space between quests
            mywin.quest_info.insert(END, "\n\n")
        # If no information to show, display default message instead
        if mywin.quest_info.get("1.0", "end-1c") == '':
            mywin.quest_info.insert(END, "There are currently no quests in progress that have trackable objectives.")
        mywin.quest_info.configure(state=DISABLED)


def select(num, list_type):
    """Display further interface elements based on the currently selected button.

    num = integer, 0 to 3 based on button's position from top \n
    list_type = string describing the type of interface currently open \n
    This is used for the skill objects, NPCs and enemy interfaces.
    """
    user.curr_area.selection = num
    mywin.open_shop.place_forget()
    # Enemy interface
    if list_type == 'enemy':
        # Place the fight button for any enemy selection
        mywin.enemy_fight.place(relx=0.35, rely=0.5, relwidth=0.15, relheight=0.1)
        for i in range(len(user.curr_area.enemies)):
            if i == num:
                # Configure the correct enemy info based on current area, then place it
                vars(mywin)['enemy' + str(i + 1) + '_lbl'].configure(
                    text=f"Combat level: {combat_level(user.curr_area.enemies[i])}\n"
                         f"Health:            {user.curr_area.enemies[i].skills['Hitpoints'][0]}\n"
                         f"Attack style:           {user.curr_area.enemies[i].att_style}\nMax hit:         "
                         f"   {max_hit(user.curr_area.enemies[i])}")
                vars(mywin)['enemy' + str(i + 1) + '_lbl'].place(relx=0.45, rely=0.65, relwidth=0.4,
                                                                 relheight=0.2)
            else:
                # Clear the previous labels if open
                vars(mywin)['enemy' + str(i + 1) + '_lbl'].place_forget()
        for i in range(len(user.curr_area.enemies), 4):
            # If coming from an area with more enemies, ensure all extra labels are removed
            vars(mywin)['enemy' + str(i + 1) + '_lbl'].place_forget()
    # Skill object interface
    if list_type == 'skills':
        # Place the start skill button for any selection
        mywin.skill_start.configure(text="Start " + user.curr_area.skill_obj[user.curr_area.selection].skill)
        if user.flags.get('tut_prog', 250) == 17:
            global flashing
            flashing = False
        # Update the text on the stop button
        if user.curr_action != "skilling":
            mywin.skill_stop.configure(text="Stop " + user.curr_area.skill_obj[user.curr_area.selection].skill)
        mywin.skill_start.place(relx=0.35, rely=0.5, relwidth=0.15, relheight=0.1)
        for i in range(len(user.curr_area.skill_obj)):
            if i == num:
                # Configure the correct skill object info based on current area, then place it
                vars(mywin)['skill' + str(i + 1) + '_lbl'].configure(
                    text=f"Level req: {user.curr_area.skill_obj[i].req}"
                    f"\n\nResource: {Items[user.curr_area.skill_obj[i].resources].name}")
                vars(mywin)['skill' + str(i + 1) + '_lbl'].place(relx=0.45, rely=0.65, relwidth=0.4,
                                                                 relheight=0.2)
            else:
                # Clear the previous labels if open
                vars(mywin)['skill' + str(i + 1) + '_lbl'].place_forget()
        for i in range(len(user.curr_area.skill_obj), 4):
            # If coming from an area with more skill objects, ensure all extra labels are removed
            vars(mywin)['skill' + str(i + 1) + '_lbl'].place_forget()
    # NPC interface
    if list_type == 'npcs':
        # Place the talk button for any selection
        mywin.interact_npc.configure(text="Talk to \n" + user.curr_area.npcs[user.curr_area.selection].name)
        mywin.interact_npc.place(relx=0.35, rely=0.5, relwidth=0.15, relheight=0.1)
        # Show the shop button and set up shop if selected a ShopNPC
        if type(user.curr_area.npcs[num]) == ShopNpc:
            user.curr_shop = user.curr_area.npcs[num].shop
            mywin.open_shop.place(relx=0.55, rely=0.5, relwidth=0.15, relheight=0.1)
        for i in range(len(user.curr_area.npcs)):
            if i == num:
                # Configure the correct NPC info based on current area, then place it
                vars(mywin)['npc' + str(i + 1) + '_lbl'].configure(text=f"{user.curr_area.npcs[i].desc}")
                vars(mywin)['npc' + str(i + 1) + '_lbl'].place(relx=0.45, rely=0.65 + num * 0.05, relwidth=0.4,
                                                               relheight=0.05)
            else:
                # Clear the previous labels if open
                vars(mywin)['npc' + str(i + 1) + '_lbl'].place_forget()
        for i in range(len(user.curr_area.npcs), 3):
            # If coming from an area with more NPCs, ensure all extra labels are removed
            vars(mywin)['npc' + str(i + 1) + '_lbl'].place_forget()


def stop_skill():
    """Smoothly exit an existing skill thread. Set current action to 'flee' which the skilliong function checks for ."""
    if user.curr_action == 'skilling':
        user.curr_action = 'flee'
        mywin.insert_text_thread(f"You stop skilling.")


def flee():
    """Smoothly exit an existing combat thread. Set current action to 'flee' which the combat function checks for."""
    if user.curr_action == 'combat':
        user.curr_action = 'flee'
        mywin.insert_text_thread(f"You try to flee, and barely escape!", 'good')


def eat(item):
    """Try to eat a piece of food to heal some health. If user is full health already, don't eat it.

    item = Item object
    """
    if user.health == user.skills['Hitpoints'][0]:
        mywin.insert_text_thread(f"You are already at full health.")
        return
    food = item[0].food
    healed = min(user.skills['Hitpoints'][0] - user.health, food)
    # Prevent over-healing
    user.health = min(food + user.health, user.skills['Hitpoints'][0])
    user.eating = True
    mywin.insert_text_thread(f"You ate some {item[0].name}! It healed {healed} health. "
                             f"You now have {user.health}hp.", 'good')
    # Set the colour of the HP bar based on current health relative to enemy damage
    if user.curr_action == "combat":
        if user.health <= max(0.2 * user.skills['Hitpoints'][0], max_hit(
                user.curr_area.enemies[user.curr_area.selection])):
            mywin.hp_bar.configure(text="HP: " + str(user.health), fg='red')
        else:
            mywin.hp_bar.configure(text="HP: " + str(user.health), fg='black')
    elif user.health <= 0.2 * user.skills['Hitpoints'][0]:
        mywin.hp_bar.configure(text="HP: " + str(user.health), fg='red')
    else:
        mywin.hp_bar.configure(text="HP: " + str(user.health), fg='black')
    user.inventory.remove_item(item[0].id)
    # Warn user if they are now out of a particular food type
    if not user.inventory.is_in_inv(item[0].id):
        mywin.insert_text_thread(f"That was your last {item[0].name}!", 'warning')
    mywin.drop_item.place_forget()
    mywin.examine_item.place_forget()
    mywin.eat.place_forget()
    update_inventory()


def max_hit(enemy):
    """Compute the maximum damage that an enemy can do.

    enemy = Enemy object
    """
    style = enemy.att_style
    if style == 'Ranged':
        eff_str = enemy.skills.get('Ranged', [1])[0]
    elif style == 'Magic':
        eff_str = enemy.skills.get('Magic', [1])[0]
    else:
        eff_str = enemy.skills.get('Strength', [1])[0]
    max_damage = int(eff_str * 0.05) + int((eff_str ** 3) / 40000) - int((eff_str ** 4) / 10000000) + 1
    return max_damage


def attack(attacker, defender, defender_hp):
    """Calculate the amount of damage an attack should do, and if it should successfully hit.

    attacker/defender = Player/Enemy objects (or vice versa) \n
    defender_hp = integer, current health of the defender
    """
    equip_stats = calc_equip_stats()
    magic = False
    if attacker == user:
        # Set the stats based on current combat style, levels and equipment
        style = Items[attacker.equipment.get('Weapon', 82)].att_style
        if style == "Melee":
            str_bonus = equip_stats[4]
            acc_rating = equip_stats[1]
            eff_att = attacker.skills['Attack'][0] + 8
            eff_str = attacker.skills['Strength'][0]
            eff_def = defender.skills['Defence'][0] + 8
            def_rating = defender.equipment.get('Melee_def', 0)
            # Attack style gives invisible level benefits
            if attacker.att_style == "Accurate":
                eff_att += 3
            elif attacker.att_speed == "Aggressive":
                eff_str += 3
        elif style == "Ranged":
            if user.equipment.get("Ammo", [0, 0])[1] == 0:
                # Stored ammo as list with quantity as 2nd value
                mywin.insert_text_thread("No suitable ammo!", 'warning')
                return 0
            if user.equipment.get('Cape', 0) != 236 or random.random() > 0.8:
                # 80% ammo preservation from Cape of arrows
                user.equipment["Ammo"][1] -= 1
                if user.equipment["Ammo"][1] == 0:
                    # If user runs out of arrows, warn them
                    mywin.insert_text_thread(f"You use your last {Items[user.equipment['Ammo'][0]].name}!", 'warning')
                    del user.equipment["Ammo"]
                update_inventory()
            str_bonus = equip_stats[5]
            acc_rating = equip_stats[2]
            eff_att = attacker.skills['Ranged'][0] + 8
            eff_str = attacker.skills['Ranged'][0]
            eff_def = defender.skills['Defence'][0] + 8
            def_rating = defender.equipment.get('Ranged_def', 0)
            if attacker.att_style == "Accurate(Ranged)":
                eff_att += 3
                eff_str += 3
        else:  # Style == "Magic"
            spell = Spellbook[user.curr_spell]
            magic = True
            for rune in spell.runes:
                if not user.inventory.is_in_inv(rune[0]) or user.inventory.is_in_inv(rune[0])[1] < rune[1]:
                    # If rune quantity < required rune quantity
                    mywin.insert_text_thread(f"Insufficient {Items[rune[0]].name}s remaining!", 'warning')
                    return 0
            for rune in spell.runes:
                # Remove correct amount of each rune, clear inventory slot if necessary
                if random.random() > Items[attacker.equipment.get('Weapon', 76)].equip_reqs['Magic'] / 200:
                    # Rune preservation chance from staff: 50% of Tier (lvl 60 staff = 30% chance to not use runes)
                    vars(user.inventory)['slot'+str(user.inventory.is_in_inv(rune[0])[0])][1] -= rune[1]
                    if vars(user.inventory)['slot'+str(user.inventory.is_in_inv(rune[0])[0])][1] <= 0:
                        # Warning when out of runes
                        mywin.insert_text_thread(f"You use your last {Items[rune[0]].name}!", 'warning')
                        vars(user.inventory)['slot' + str(user.inventory.is_in_inv(rune[0])[0])] = None
                    user.inventory.shuffle_inv()
                    update_inventory()
            # Magic 'strength' is heavily based on spell choice
            str_bonus = equip_stats[6] // 6 + Spellbook[user.curr_spell].damage
            acc_rating = equip_stats[3]
            eff_att = attacker.skills['Magic'][0] + 8
            eff_str = attacker.skills['Magic'][0]
            eff_def = 0.3*defender.skills['Defence'][0] + 0.7*defender.skills['Magic'][0] + 8
            def_rating = defender.equipment.get('Magic_def', 0)
            if attacker.att_style == "Accurate(Magic)":
                eff_att += 3
        if not magic:
            max_damage = int(1.3 + eff_str / 10 + str_bonus / 80 + (eff_str * str_bonus) / 640)
        else:
            # Magic damage scales differently due to spell damage being a large part of it
            max_damage = str_bonus + eff_str // 12
    else:                       # Enemies currently have no equipment stats, so some simplifications made here
        style = attacker.att_style
        if style == "Melee":
            # str_bonus = attacker.equipment.get('Str_bonus', 0)
            acc_rating = attacker.skills['Attack'][0] // 2
            eff_att = attacker.skills['Attack'][0] + 8
            eff_str = attacker.skills['Strength'][0]
            eff_def = defender.skills['Defence'][0] + 8
            def_rating = equip_stats[7]
        elif style == "Ranged":
            # str_bonus = attacker.equipment.get('Str_bonus', 0)
            acc_rating = attacker.skills['Ranged'][0] // 2
            eff_att = attacker.skills['Ranged'][0] + 8
            eff_str = attacker.skills['Ranged'][0]
            eff_def = defender.skills['Defence'][0] + 8
            def_rating = equip_stats[8]
        else:  # Style == "Magic"
            # str_bonus = attacker.equipment.get('Str_bonus', 0)
            acc_rating = attacker.skills['Magic'][0] // 2
            eff_att = attacker.skills['Magic'][0] + 8
            eff_str = attacker.skills['Magic'][0]
            eff_def = 0.3*defender.skills['Defence'][0] + 0.7*defender.skills['Magic'][0] + 8
            def_rating = equip_stats[9]
        if "Defensive" in defender.att_style:
            eff_def += 3
        # Enemies use a different calculation due to lack of equipment stats
        max_damage = int(eff_str * 0.05) + int((eff_str ** 3) / 40000) - int((eff_str ** 4) / 10000000) + 1
    # Accuracy calculation
    att_roll = eff_att * (acc_rating + 64)
    def_roll = eff_def * (def_rating + 64)
    if att_roll > def_roll:
        hit_chance = 1 - (def_roll + 2) / (2 * (att_roll + 1))
    else:
        hit_chance = att_roll / (2 * (def_roll + 1))
    # Slight alteration to allow 100% accuracy with massive attack-defence differences for quality of life
    if hit_chance > 0.95:
        hit_chance = 1
    # Smooth out the hard cut-off at 95% accuracy
    else:
        hit_chance *= 1.052
    # print(f"Max dmg = {max_damage},\nHit chance = {hit_chance}")
    damage = random.randint(1, max_damage)
    if random.random() > hit_chance:
        if user == attacker:
            mywin.insert_text_thread(f"You try to attack the {defender.name}, but miss!")
        else:
            mywin.insert_text_thread(f"The {attacker.name} tries to attack you, but misses!", 'good')
        return 0
    if damage > defender_hp:
        # If the attack did too much damage then overkill is included
        overkill = damage - defender_hp
        if attacker == user:
            mywin.insert_text_thread(f"You attack the {defender.name}, dealing {damage} damage! ({overkill} overkill)")
        else:
            mywin.insert_text_thread(f"The {attacker.name} attacks you, dealing {damage} damage! ({overkill} overkill)",
                                     'warning')
        return damage
    if attacker == user:
        mywin.insert_text_thread(f"You attack the {defender.name}, dealing {damage} damage!")
    else:
        mywin.insert_text_thread(f"The {attacker.name} attacks you, dealing {damage} damage!", 'warning')
    return damage


def combat(enemy):
    """Start the combat process with the given enemy.

    enemy = Enemy object \n
    Process the sequence of attacks between user and enemy, changing health values with each hit until one reaches
    0 or the user flees. If the user is successful, give them some randomised loot from the enemy. If they die,
    teleport them to their spawn point but do not remove any items from them.
    """
    # Some tutorial checks
    if user.flags.get('tut_prog', 250) == 9:
        if user.equipment.get('Weapon', 0) != 83:
            mywin.insert_text_thread(f"Try equipping the Bronze sword before attacking.", 'warning')
            return
    if user.flags.get('tut_prog', 250) == 11:
        if user.equipment.get('Weapon', 0) != 151 or user.equipment.get('Ammo', [0, 0])[0] != 144:
            mywin.insert_text_thread(f"Try equipping the Shortbow and arrows before attacking.", 'warning')
            return
    if user.flags.get('tut_prog', 250) == 13:
        if user.equipment.get('Weapon', 0) != 76:
            mywin.insert_text_thread(f"Try equipping the Fractured staff before attacking.", 'warning')
            return
    user.curr_action = 'combat'
    mywin.enemy_fight["state"] = "disabled"
    user.eating = False
    # Set up all the interface elements
    mywin.curr_style.place(relx=0.2, rely=0.5, relwidth=0.15, relheight=0.1)
    mywin.style1.place(relx=0.35, rely=0.45, relwidth=0.1, relheight=0.05)
    mywin.style2.place(relx=0.45, rely=0.45, relwidth=0.1, relheight=0.05)
    mywin.style3.place(relx=0.55, rely=0.45, relwidth=0.1, relheight=0.05)
    style_swap()
    mywin.flee.place(relx=0.5, rely=0.5, relwidth=0.15, relheight=0.1)
    # Attack speed is ignored for first hit
    user_tta = 600
    # Enemy takes a small amount of time to start attacking back
    enemy_tta = 1800
    enemy_health = enemy.skills['Hitpoints'][0]
    mywin.enemy_bar.configure(text="Enemy HP: "+str(max(enemy_health, 0)), bg='#b32d00')
    mywin.enemy_bar.place(relx=0.76, rely=0.35, relwidth=0.15, relheight=0.05)
    mywin.insert_text_thread(f"You approach the {enemy.name}.", 'warning')
    while user.health > 0 and enemy_health > 0:
        # Check whether user or enemy is attacking next by comparing time_to_attack values
        if user_tta < enemy_tta:
            # Case where user is attacking next
            start = time.time()
            # Provide a more responsive flee check
            for i in range(int(user_tta/100)):
                time.sleep(0.1)
                if not running:
                    return
                if user.curr_action == 'flee':
                    # If user flees, end combat and close relevant interfaces
                    user.curr_action = 'idle'
                    mywin.flee.place_forget()
                    mywin.enemy_fight["state"] = "normal"
                    mywin.style1.place_forget()
                    mywin.style2.place_forget()
                    mywin.style3.place_forget()
                    mywin.curr_style.place_forget()
                    mywin.enemy_bar.place_forget()
                    return
                # Give more consistency to the time that the loop terminates due to variance in sleep times
                if time.time() >= start + user_tta/1000 - 0.15:
                    time.sleep(max(start + user_tta/1000 - time.time() - 0.01, 0))
                    break
            if user.eating:
                # If user eats food during combat, delay their next attack slightly
                user.eating = False
                enemy_tta -= user_tta
                user_tta += user.att_speed
            else:
                # Process the attack, reset attack time to attack speed, change enemy hp
                damage = attack(user, enemy, enemy_health)
                enemy_health -= damage
                mywin.enemy_bar.configure(text=" Enemy HP: "+str(max(enemy_health, 0)))
                gen_xp(damage)
                enemy_tta -= user_tta
                user_tta = user.att_speed
                if user.att_style == "Rapid":
                    user_tta -= 600
        elif user_tta > enemy_tta:
            # Case where enemy is attacking next
            start = time.time()
            # Provide a more responsive flee check
            for i in range(int(enemy_tta/100)):
                time.sleep(0.1)
                if not running:
                    return
                if user.curr_action == 'flee':
                    # If user flees, end combat and close relevant interfaces
                    user.curr_action = 'idle'
                    mywin.flee.place_forget()
                    mywin.enemy_fight["state"] = "normal"
                    mywin.style1.place_forget()
                    mywin.style2.place_forget()
                    mywin.style3.place_forget()
                    mywin.curr_style.place_forget()
                    mywin.enemy_bar.place_forget()
                    return
                if time.time() >= start + enemy_tta/1000 - 0.15:
                    # Give more consistency to the time that the loop terminates due to variance in sleep times
                    time.sleep(max(start + enemy_tta/1000 - time.time() - 0.01, 0))
                    break
            if user.eating:
                # If user eats food during combat, delay their next attack slightly
                user.eating = False
                user_tta += user.att_speed
            # Process the attack, change user health, reset enemy attack time to attack speed
            user.health -= attack(enemy, user, user.health)
            # Change colour of user HP bar based on current health relative to enemy max hit
            if user.health <= max(0.2 * user.skills['Hitpoints'][0], max_hit(enemy)):
                mywin.hp_bar.configure(text="HP: " + str(user.health), fg='red')
            else:
                mywin.hp_bar.configure(text="HP: " + str(user.health), fg='black')
            user_tta -= enemy_tta
            enemy_tta = enemy.att_speed
        else:
            # Case where enemy and user have equal attack timings, so both attack at once
            start = time.time()
            # Provide a more responsive flee check
            for i in range(int(enemy_tta / 100)):
                time.sleep(0.1)
                if not running:
                    return
                if user.curr_action == 'flee':
                    # If user flees, end combat and close relevant interfaces
                    user.curr_action = 'idle'
                    mywin.flee.place_forget()
                    mywin.enemy_fight["state"] = "normal"
                    mywin.style1.place_forget()
                    mywin.style2.place_forget()
                    mywin.style3.place_forget()
                    mywin.curr_style.place_forget()
                    mywin.enemy_bar.place_forget()
                    return
                if time.time() >= start + user_tta/1000 - 0.15:
                    # Give more consistency to the time that the loop terminates due to variance in sleep times
                    time.sleep(max(start + user_tta/1000 - time.time() - 0.01, 0))
                    break
            if user.eating:
                # If user eats food during combat, delay their next attack slightly
                user.eating = False
                user_tta = user.att_speed
                if user.att_style == "Rapid":
                    user_tta -= 600
                # Since user ate food, they are no longer attacking at same time as enemy, so only process enemy attack
                user.health -= attack(enemy, user, user.health)
                if user.health <= max(0.2 * user.skills['Hitpoints'][0], max_hit(enemy)):
                    mywin.hp_bar.configure(text="HP: " + str(user.health), fg='red')
                else:
                    mywin.hp_bar.configure(text="HP: " + str(user.health), fg='black')
                enemy_tta = enemy.att_speed
            else:
                # If user doesn't eat, process both user and enemy attacks
                damage = attack(user, enemy, enemy_health)
                enemy_health -= damage
                mywin.enemy_bar.configure(text="Enemy HP: "+str(max(enemy_health, 0)))
                gen_xp(damage)
                if enemy_health <= 0:
                    # If user kills the enemy, the enemy does not get to attack back before dying
                    continue
                user.health -= attack(enemy, user, user.health)
                if user.health <= max(0.2 * user.skills['Hitpoints'][0], max_hit(enemy)):
                    mywin.hp_bar.configure(text="HP: " + str(user.health), fg='red')
                else:
                    mywin.hp_bar.configure(text="HP: " + str(user.health), fg='black')
                user_tta = user.att_speed
                if user.att_style == "Rapid":
                    user_tta -= 600
                enemy_tta = enemy.att_speed
    # Now process post-combat outcomes
    if user.health > enemy_health:
        # Case where enemy was killed successfully
        mywin.insert_text_thread(f"{enemy.name} has died!", 'good')
        # Check if user has a flag tracking kills for this enemy and progress it
        if user.flags.get("kill_"+str(enemy.id), -1) != -1:
            user.flags["kill_"+str(enemy.id)] += 1
        # Generate random loot from the enemy loot table
        loot = enemy.gen_loot(user)
        # Sometimes enemies will drop nothing, -1 represents this on the drop table
        if loot[0] != -1:
            # Add the loot to user inventory if possible
            mywin.insert_text_thread(f"You loot {loot[1]} {Items[loot[0]].name}.")
            item, msg_type = user.inventory.add_to_inv(loot[0], loot[1])[:2]
            mywin.insert_text_thread(item, msg_type)
        else:
            mywin.insert_text_thread(f"You don't find anything to loot.", 'warning')
        user.inventory.shuffle_inv()
        update_inventory()
        # Clear interfaces and reset some user values
        mywin.flee.place_forget()
        mywin.enemy_fight["state"] = "normal"
        user.eating = False
        mywin.style1.place_forget()
        mywin.style2.place_forget()
        mywin.style3.place_forget()
        mywin.curr_style.place_forget()
        mywin.enemy_bar.place_forget()
        if mywin.quest_info.winfo_viewable():
            # Update the quest info text in case a quest was progressed
            curr_pos = mywin.quest_info.yview()
            list_quest_info(True)
            # Scroll back to original position after rewriting the info text
            mywin.quest_info.yview_moveto(curr_pos[0])
        user.curr_action = 'idle'
        # Some tutorial stuff
        if enemy == Man_enemy:
            tut_area_1.enemies[1] = None_enemy
            mywin.enemy_fight.place_forget()
            mywin.inv_0.place(relx=0.25, rely=0.6, relwidth=0.125, relheight=0.05)
            list_inv()
            time.sleep(0.5)
            mywin.insert_text_thread(f"\nThe man decides that adventuring is too much for him, and sits down to tend "
                                     f"to his wounds. You should return to his wife.", 'good')
        if user.flags.get('tut_prog', 250) in [9, 11, 13]:
            user.flags['tut_prog'] += 1
            print(user.flags.get('tut_prog', 250), "progress")
    else:
        # Case where user dies to enemy
        mywin.flee.place_forget()
        mywin.insert_text_thread(f"You have died!", 'warning')
        # Health is reset to max after death
        user.health = user.skills['Hitpoints'][0]
        mywin.enemy_fight["state"] = "normal"
        user.eating = False
        user.curr_action = 'idle'
        if user.health <= max(0.2 * user.skills['Hitpoints'][0], max_hit(enemy)):
            mywin.hp_bar.configure(text="HP: " + str(user.health), fg='red')
        else:
            mywin.hp_bar.configure(text="HP: " + str(user.health), fg='black')
        mywin.style1.place_forget()
        mywin.style2.place_forget()
        mywin.style3.place_forget()
        mywin.curr_style.place_forget()
        mywin.enemy_bar.place_forget()
        # Teleport user to their spawn point unless still in tutorial
        if user.flags.get('tut_prog', 250) <= 32:
            time.sleep(1)
            mywin.insert_text_thread(f"\nOh dear, you died! Don't worry, you've been revived good as new for now. In "
                                     f"future you might not be as lucky, so watch your health and eat food if you need"
                                     f" to.")
        else:
            swap_area(user.spawn, 'forced')
            mywin.insert_text_thread(f"You respawn in {user.curr_area.name}, in perfect condition.", 'good')


def gen_xp(damage):
    """Generate experience in the relevant combat skills after doing damage in combat.

    damage = integer, to base calculation off
    """
    if damage == 0:
        return
    skill = skill2 = ""
    # Figure out which skill(s) should get the experience
    if user.att_style == 'Accurate':
        skill = 'Attack'
    elif user.att_style == 'Aggressive':
        skill = 'Strength'
    elif user.att_style == 'Defensive':
        skill = 'Defence'
    elif user.att_style == "Accurate(Ranged)" or user.att_style == "Rapid":
        skill = 'Ranged'
    elif user.att_style == "Defensive(Ranged)":
        skill = 'Ranged'
        skill2 = "Defence"
    elif user.att_style == "Accurate(Magic)":
        skill = "Magic"
    elif user.att_style == "Defensive(Magic)":
        skill = "Magic"
        skill2 = "Defence"
    if skill2 == "":
        # If not using a split attack style, all experience goes to the main skill and 1/3 of that to Hitpoints
        user.skills[skill][1] += 4 * damage * global_xp_multiplier
        user.skills['Hitpoints'][1] += (4 / 3) * damage * global_xp_multiplier
        # mywin.insert_text_thread(f"You gained {4 * damage} experience in {skill}, and "
        #                          f"{round((4 / 3) * damage, 1)} Hitpoints experience.")
        new_lvls = [[get_current_lvl(user.skills[skill][1]), skill],
                    [get_current_lvl(user.skills['Hitpoints'][1]), 'Hitpoints']]
        # Process any level-ups that the experience caused
        for new_lvl, skl in new_lvls:
            if new_lvl != user.skills[skl][0]:
                user.skills[skl][0] = new_lvl
                mywin.insert_text_thread(f"Congratulations! Your {skl} is now level {new_lvl}.", 'good')
                if skill == "Magic":
                    update_spells()
    else:
        # If using a split attack style, split the experience but Hitpoints still gets 1/3 of the total
        user.skills[skill][1] += 2 * damage * global_xp_multiplier
        user.skills[skill2][1] += 2 * damage * global_xp_multiplier
        user.skills['Hitpoints'][1] += (4 / 3) * damage * global_xp_multiplier
        # mywin.insert_text_thread(f"You gained {2 * damage} experience in {skill} and {skill2}, and "
        #                          f"{round((4 / 3) * damage, 1)} Hitpoints experience.")
        new_lvls = [[get_current_lvl(user.skills[skill][1]), skill], [get_current_lvl(user.skills[skill2][1]),
                                                                      skill2],
                    [get_current_lvl(user.skills['Hitpoints'][1]), 'Hitpoints']]
        # Process level-ups
        for new_lvl, skl in new_lvls:
            if new_lvl != user.skills[skl][0]:
                user.skills[skl][0] = new_lvl
                mywin.insert_text_thread(f"Congratulations! Your {skl} is now level {new_lvl}.", 'good')
                if skill == "Magic":
                    update_spells()
    update_skills()


def style_swap():
    """Configure the style switching buttons to the current weapon's style. Used when switching weapons."""
    # No weapon equipped is treated the same as a melee weapon
    if user.equipment.get("Weapon", -1) == -1 or Items[user.equipment["Weapon"]].att_style == "Melee":
        mywin.style1.configure(text="Accurate", command=lambda: set_style('Accurate'))
        mywin.style2.configure(text="Aggressive", command=lambda: set_style('Aggressive'))
        mywin.style3.configure(text="Defensive", command=lambda: set_style('Defensive'))
    elif Items[user.equipment["Weapon"]].att_style == "Ranged":
        mywin.style1.configure(text="Accurate", command=lambda: set_style('Accurate(Ranged)'))
        mywin.style2.configure(text="Rapid", command=lambda: set_style('Rapid'))
        mywin.style3.configure(text="Defensive", command=lambda: set_style('Defensive(Ranged)'))
    elif Items[user.equipment["Weapon"]].att_style == "Magic":
        mywin.style1.configure(text="Accurate", command=lambda: set_style('Accurate(Magic)'))
        mywin.style2.place_forget()
        mywin.style3.configure(text="Defensive", command=lambda: set_style('Defensive(Magic)'))


def set_style(style=None):
    """Set the user's attack style.

    style = string containing an attack style (default None)
    """
    if style is None:
        # A default attack style is set for each combat style when first equipping a weapon
        if user.equipment['Weapon'].att_style == "Melee":
            user.att_style = 'Accurate'
        elif user.equipment['Weapon'].att_style == "Ranged":
            user.att_style = 'Accurate(Ranged)'
        elif user.equipment['Weapon'].att_style == "Magic":
            user.att_style = 'Accurate(Magic)'
    else:
        user.att_style = style
    mywin.curr_style.configure(text="Current style:\n" + user.att_style)


def combat_level(entity):
    """Compute a combat level from the relevant skill levels for either user or enemy.

    entity = Player or Enemy object
    """
    if type(entity) not in [Player, Enemy]:
        return 0

    defence = entity.skills.get('Defence', [1])[0]
    hitpoints = entity.skills.get('Hitpoints', [10])[0]
    attack_ = entity.skills.get('Attack', [1])[0]
    strength = entity.skills.get('Strength', [1])[0]
    ranged = entity.skills.get('Ranged', [1])[0]
    magic = entity.skills.get('Magic', [1])[0]

    # A base level is calculated before considering the style specific combat skills
    base = 0.2875*(defence + hitpoints)
    # One of the following is added to the base level depending on the user's skill level distribution
    melee = (14/40)*(attack_ + strength)
    ranged = (14/40)*(1.5*ranged)
    magic = (14/40)*(1.5*magic)

    final = int(base + max(melee, ranged, magic))
    return final


def skilling(skill_obj):
    """Start the gathering skill process.

    skill_obj = SkillObj object \n
    Check the user's level and look for a relevant skilling tool before starting.
    Begin gathering resources with a success chance based on user's level, tool tier, and resource level requirement.
    Continue until stopped by user or the resource depletes randomly.
    """
    # Level check
    if user.skills[skill_obj.skill][0] < skill_obj.req:
        mywin.insert_text_thread(f"You don't have a high enough level to do that.\n{skill_obj.name} requires "
                                 f"{skill_obj.req} {skill_obj.skill}.", 'warning')
        return
    if user.flags.get('tut_prog', 250) == 17 and user.inventory.free_spaces() < 3:
        mywin.insert_text_thread(f"You should make some more space before doing that.", 'warning')
        return
    # Tool check, consider the best tool that the user has for the success chance calculation
    tool = None
    for tool_id in range(45, 66):
        # Loop through all tools in ascending tier order (end with best available tool)
        if (user.equipment.get('Weapon', 0) == tool_id or user.inventory.is_in_inv(tool_id)) and Items[
                tool_id].skill == skill_obj.skill and user.skills[Items[tool_id].skill][0] >= Items[tool_id].req:
            tool = Items[tool_id]
    if tool is None:
        mywin.insert_text_thread(f"You need one of the following to do that:\n{skill_obj.tool}.", 'warning')
        return
    # Set up the interface and calculates the relevant numbers
    user.curr_action = "skilling"
    mywin.skill_start["state"] = "disabled"
    mywin.skill_stop.configure(text="Stop " + user.curr_area.skill_obj[user.curr_area.selection].skill)
    mywin.skill_stop.place(relx=0.5, rely=0.5, relwidth=0.15, relheight=0.1)
    depletion_rate = skill_obj.depletion_chance
    tool_tier = tool.tier
    # Compute the success rate at 1 and 99 based on skill object's values
    low = (skill_obj.rate_1*((1 + tool_tier)/2)) / 255
    high = (skill_obj.rate_99*((1 + tool_tier)/2)) / 255
    # Interpolate between these values for the actual chance at a given level
    success_chance = min(low*(99-user.skills[skill_obj.skill][0]) / 98 + high*(user.skills[skill_obj.skill][0]-1)/98, 1)
    depleted = False
    mywin.insert_text_thread(f"You start {skill_obj.skill.lower()}.")
    # Begin the gathering process
    while not depleted:
        # Start the timer and initialise the progress bar
        start = time.time()
        mywin.progress.configure(value=0)
        mywin.progress.place(relx=0.1, rely=0.25, relheight=0.05)
        for i in range(18):
            mywin.progress.configure(value=100 - min(max((15 - i) * 6, 0), 100))
            # Attempt to keep duration as close to 1.8 seconds as possible due to sleep variation
            if time.time() >= 1.65 + start:
                time.sleep((start + 1.79 - time.time())/2)
                mywin.progress.configure(value=100 - min(max((15 - i - 1) * 6, 0), 100))
                time.sleep(max((start + 1.8 - time.time()) / 2, 0))
                break
            time.sleep(0.1)
            if not running:
                return
            # Constantly check for flee action
            if user.curr_action == "flee":
                # If user flees, clear interfaces and stop skilling
                user.curr_action = 'idle'
                mywin.skill_stop.place_forget()
                mywin.skill_start["state"] = "normal"
                mywin.progress.place_forget()
                mywin.progress.configure(value=0)
                if user.flags.get('tut_prog', 250) == 17 and user.inventory.is_in_inv(skill_obj.resources):
                    user.flags['tut_prog'] = 18
                return
        # Use random numbers to decide whether the action is successful or not and if the resource depletes
        deplete = random.random()
        success = random.random()
        print(success)
        if deplete < depletion_rate and success < success_chance:
            # Resource can only deplete after a successful action
            depleted = True
        if success < success_chance:
            # Case where user successfully gathers a resource
            mywin.insert_text_thread(f"You gather some {Items[skill_obj.resources].name}.")
            # Experience is given to the relevant skill
            user.skills[skill_obj.skill][1] += skill_obj.xp * global_xp_multiplier
            new_lvl = get_current_lvl(user.skills[skill_obj.skill][1])
            # Process level-ups
            if new_lvl != user.skills[skill_obj.skill][0]:
                user.skills[skill_obj.skill][0] = new_lvl
                mywin.insert_text_thread(f"Congratulations! Your {skill_obj.skill} is now level {new_lvl}.", 'good')
                success_chance = min(low * (99 - user.skills[skill_obj.skill][0]) / 98 + high * (
                            user.skills[skill_obj.skill][0] - 1) / 98, 1)
            # Add the resource to inventory
            item, msg_type = user.inventory.add_to_inv(skill_obj.resources, 1)[:2]
            mywin.insert_text_thread(item, msg_type)
            user.inventory.shuffle_inv()
            update_inventory()
            update_skills()
        else:
            mywin.insert_text_thread(f"You fail to get anything.")
        mywin.progress.place_forget()
        mywin.progress.configure(value=0)
        update_skills()
        if mywin.quest_info.winfo_viewable():
            # Update the quest info in case the resource was part of a quest objective
            curr_pos = mywin.quest_info.yview()
            list_quest_info(True)
            # Scroll back to previous position after rewriting the info
            mywin.quest_info.yview_moveto(curr_pos[0])
    # At this point the resource has depleted
    mywin.insert_text_thread(f"The {skill_obj.name} has depleted.", 'warning')
    user.curr_action = 'idle'
    mywin.skill_stop.place_forget()
    mywin.skill_start["state"] = "normal"
    update_skills()
    if user.flags.get('tut_prog', 250) == 17 and user.inventory.is_in_inv(skill_obj.resources):
        user.flags['tut_prog'] = 18


def cook():
    """Start the cooking process.

    Attempt to cook the selected item after checking user's level. Each item has a chance to burn when cooking,
    being less likely with a higher level. Continue cooking until out of a given item or user manually presses the
    stop button.
    """
    # Check that the selected item can be cooked
    if type(user.curr_item) != Item or not user.curr_item.cook:
        mywin.insert_text_thread("Select an item to cook!", 'warning')
        return
    # Final check in case item disappears after selection, but before starting cooking eg. dropping it
    if not user.inventory.is_in_inv(user.curr_item.id):
        mywin.insert_text_thread(f"No {user.curr_item.name} left to cook.", 'warning')
        mywin.start_cook.place_forget()
        mywin.stop_cook.place_forget()
        return
    # Check user level against item requirements
    if user.skills['Cooking'][0] < user.curr_item.skill_reqs['Cooking']:
        mywin.insert_text_thread(f"You need level {user.curr_item.skill_reqs['Cooking']} "
                                 f"Cooking to cook that.", 'warning')
        return
    # Initialise variables before cooking
    user.curr_action = "cooking"
    mywin.cooking["state"] = "disabled"
    mywin.insert_text_thread(f"Cooking {user.curr_item.name}")
    mywin.stop_cook.place(relx=0.45, rely=0.5, relwidth=0.15, relheight=0.1)
    # Keep track of the number of current items left in inventory
    cook_remaining = user.inventory.is_in_inv(user.curr_item.id)[1]
    mywin.cooks_left.configure(text=f"{cook_remaining} {user.curr_item.name}\nin inventory.")
    mywin.cooks_left.place(relx=0.25, rely=0.5, relwidth=0.2, relheight=0.1)
    # Compute the success chance based on the difference between user's level and the item's requirement
    success_chance = min(0.2 + (user.skills['Cooking'][0] - user.curr_item.skill_reqs['Cooking']) ** (1 / 3) * 0.3, 1)
    burned = False
    while cook_remaining > 0:
        # Start the cooking loop, with timer and progress bar
        start = time.time()
        mywin.progress.configure(value=0)
        mywin.progress.place(relx=0.1, rely=0.25, relheight=0.05)
        # Short interval loop for responsive progress bar and stop button
        for i in range(18):
            mywin.progress.configure(value=100 - min(max((15 - i) * 6, 0), 100))
            if time.time() >= 1.65 + start:
                # Attempt to keep duration as close to 1.8 as possible due to sleep time variation
                mywin.progress.configure(value=100 - min(max((15 - i - 1) * 6, 0), 100))
                time.sleep((start + 1.79 - time.time()) / 2)
                mywin.progress.configure(value=100)
                time.sleep(max((start + 1.8 - time.time()) / 2, 0))
                break
            time.sleep(0.1)
            if not running:
                return
            # Stop cooking if user presses the stop button or somehow loses resources
            if user.curr_action == "flee" or not user.inventory.is_in_inv(user.curr_item.id):
                # Clear interfaces and reset values
                mywin.insert_text_thread(f"Stopping cooking...")
                user.curr_action = "idle"
                mywin.cooking["state"] = "normal"
                mywin.stop_cook.place_forget()
                mywin.cooks_left.place_forget()
                mywin.progress.place_forget()
                mywin.progress.configure(value=0)
                return
        mywin.progress.configure(value=100)
        # Update the remaining number of items to cook and delete one copy of the item from inventory
        cook_remaining = max(user.inventory.is_in_inv(user.curr_item.id)[1] - 1, 0)
        user.inventory.remove_item(user.curr_item.id)
        # Decide if the action was a success
        if random.random() > success_chance:
            mywin.insert_text_thread(f"You burn the {user.curr_item.name}.", 'warning')
            burned = True
        else:
            # Success: add the cooked version to inventory and grant experience
            burned = False
            mywin.insert_text_thread(f"You cook the {user.curr_item.name}.", 'good')
            user.inventory.add_to_inv(user.curr_item.id + 1)
            user.skills['Cooking'][1] += user.curr_item.xp * global_xp_multiplier
            # Deal with level-ups and update success chance based on new level
            while xp_to_next('Cooking', True) <= 0 and user.skills['Cooking'][0] != 99:
                user.skills['Cooking'][0] += 1
                mywin.insert_text_thread(f"Congratulations! Your Cooking is now level {user.skills['Cooking'][0]}.",
                                         'good')
                success_chance = min(
                    0.2 + (user.skills['Cooking'][0] - user.curr_item.skill_reqs['Cooking']) ** (1 / 3) * 0.3, 1)
        # Update label of items remaining and reset progress bar, clear inventory context actions
        mywin.cooks_left.configure(text=f"{cook_remaining} {user.curr_item.name}\nin inventory.")
        mywin.progress.place_forget()
        mywin.progress.configure(value=0)
        mywin.equip_item.place_forget()
        mywin.drop_item.place_forget()
        mywin.crafting.place_forget()
        mywin.eat.place_forget()
        mywin.burn.place_forget()
        mywin.examine_item.place_forget()
        mywin.fletching.place_forget()
        user.inventory.shuffle_inv()
        update_inventory()
        # Refresh quest info if it is open
        if mywin.quest_info.winfo_viewable():
            curr_pos = mywin.quest_info.yview()
            list_quest_info(True)
            mywin.quest_info.yview_moveto(curr_pos[0])
    # By this point the user has run out of food to cook, so clear interfaces and reset user action
    mywin.insert_text_thread(f"Stopping cooking...(No more {user.curr_item.name} found.)")
    mywin.cooking["state"] = "normal"
    mywin.stop_cook.place_forget()
    mywin.cooks_left.place_forget()
    list_cooking()
    user.inventory.shuffle_inv()
    update_inventory()
    list_cooking()
    user.curr_action = "idle"
    if user.flags.get('tut_prog', 250) == 26:
        user.flags['tut_prog'] = 27
        if burned:
            time.sleep(2)
            mywin.insert_text_thread(f"\nUnfortunately you burned the shrimp.")


def smelt():
    """Start the smelting process.

    Attempt to smelt the selected bar from the associated ores after checking user's level
    against the bar requirement. Continue until out of ores or user presses the stop button.
    """
    # Check the selected item is a valid metal bar
    if type(user.curr_item) != Item or user.curr_item.id not in [79, 90, 101, 112, 123, 134]:
        mywin.insert_text_thread("Select an item to smelt!", 'warning')
        return
    # Check user's level against the bar's requirement
    if user.skills['Smithing'][0] < user.curr_item.skill_reqs['Smithing']:
        mywin.insert_text_thread(f"You need level {user.curr_item.skill_reqs['Smithing']} "
                                 f"Smithing to smelt that.", 'warning')
        return
    user.curr_action = "smelting"
    bar = user.curr_item
    # Set up the ore types being used. Iron is the only bar using a single resource
    if bar.id == 90:
        ore = 89
        ore_2 = None
        smelt_remaining = user.inventory.is_in_inv(ore)[1]
    else:
        ore, ore_2 = bar.resources.keys()
        smelt_remaining = min(user.inventory.is_in_inv(ore)[1] // bar.resources[ore],
                              user.inventory.is_in_inv(ore_2)[1] // bar.resources[ore_2])
    # Configure and place the interface elements
    mywin.start_smelt.configure(state=DISABLED)
    mywin.insert_text_thread(f"Smelting {bar.name}")
    mywin.stop_smith.place(relx=0.45, rely=0.5, relwidth=0.15, relheight=0.1)
    mywin.cooks_left.configure(text=f"{smelt_remaining} {bar.name}\nready to smelt.")
    mywin.cooks_left.place(relx=0.25, rely=0.5, relwidth=0.2, relheight=0.1)
    # Start smelting if user has the correct resources
    while smelt_remaining > 0:
        # Start the smelting loop, with timer and progress bar
        smelt_remaining -= 1
        start = time.time()
        mywin.progress.configure(value=0)
        mywin.progress.place(relx=0.1, rely=0.25, relheight=0.05)
        # Short interval loop for responsive progress bar and stop button
        for i in range(18):
            mywin.progress.configure(value=100 - min(max((15 - i) * 6, 0), 100))
            if time.time() >= 1.65 + start:
                # Attempt to keep duration as close to 1.8 as possible due to sleep time variation
                mywin.progress.configure(value=100 - min(max((15 - i - 1) * 6, 0), 100))
                time.sleep((start + 1.79 - time.time()) / 2)
                mywin.progress.configure(value=100)
                time.sleep(max((start + 1.8 - time.time()) / 2, 0))
                break
            time.sleep(0.1)
            if not running:
                return
            # Stop smelting if user presses the stop button or somehow loses resources
            if user.curr_action == "flee" or not user.inventory.is_in_inv(bar.id - 1):
                # Clear interfaces and reset values
                mywin.insert_text_thread(f"Stopping smelting...")
                user.curr_action = "idle"
                mywin.start_smelt["state"] = "normal"
                mywin.stop_smith.place_forget()
                mywin.cooks_left.place_forget()
                mywin.progress.place_forget()
                mywin.progress.configure(value=0)
                list_smelting()
                list_smelting()
                return
        mywin.progress.configure(value=100)
        # Delete the correct amount of each ore from inventory and add the bar
        user.inventory.remove_item(ore, bar.resources[ore])
        user.inventory.remove_item(ore_2, bar.resources.get(ore_2, 0))
        mywin.insert_text_thread(f"You smelt a {bar.name}.", 'good')
        user.inventory.add_to_inv(bar.id)
        # Generate experience and process level-ups
        user.skills['Smithing'][1] += bar.xp * global_xp_multiplier
        while xp_to_next('Smithing', True) <= 0 and user.skills['Smithing'][0] != 99:
            user.skills['Smithing'][0] += 1
            mywin.insert_text_thread(f"Congratulations! Your Smithing is now level {user.skills['Smithing'][0]}.",
                                     'good')
        update_skills()
        # Reset progress bar and clear inventory context actions
        mywin.equip_item.place_forget()
        mywin.drop_item.place_forget()
        mywin.crafting.place_forget()
        mywin.eat.place_forget()
        mywin.burn.place_forget()
        mywin.examine_item.place_forget()
        mywin.fletching.place_forget()
        mywin.progress.place_forget()
        mywin.progress.configure(value=0)
        user.inventory.shuffle_inv()
        update_inventory()
        # Refresh quest info if it is open
        if mywin.quest_info.winfo_viewable():
            curr_pos = mywin.quest_info.yview()
            list_quest_info(True)
            mywin.quest_info.yview_moveto(curr_pos[0])
        # Re-calculate the remaining number of bars that can be made based on inventory resources
        if ore_2 is None:
            if user.inventory.is_in_inv(ore):
                smelt_remaining = user.inventory.is_in_inv(ore)[1]
            else:
                smelt_remaining = 0
        elif user.inventory.is_in_inv(ore) and user.inventory.is_in_inv(ore_2):
            smelt_remaining = min(user.inventory.is_in_inv(ore)[1] // bar.resources[ore],
                                  user.inventory.is_in_inv(ore_2)[1] // bar.resources[ore_2])
        else:
            smelt_remaining = 0
        mywin.cooks_left.configure(text=f"{smelt_remaining} {Items[ore].name}\nready to smelt.")
    # By this point the user has run out of resources, so clear interfaces and reset user action
    mywin.insert_text_thread(f"Stopping smelting...(No more resources found.)")
    mywin.stop_smith.place_forget()
    mywin.cooks_left.place_forget()
    list_smelting()
    user.curr_action = "idle"
    mywin.start_smelt["state"] = "normal"
    user.inventory.shuffle_inv()
    update_inventory()
    list_smelting()
    if user.flags.get('tut_prog', 250) == 22:
        user.flags['tut_prog'] = 23


def smith():
    """Start the smithing process.

    Attempt to smith the selected item from the associated bar(s) after checking user's level against the item
    requirement. Continue until out of bars or user presses the stop button.
    """
    # Check that selected item is valid
    if type(user.curr_item) not in [Item, Equipment] or user.curr_item.id not in [i for i in range(80, 144)]:
        mywin.insert_text_thread("Select an item to smith!", 'warning')
        return
    # Check user's level against the item's requirement
    if user.skills['Smithing'][0] < user.curr_item.skill_reqs['Smithing']:
        mywin.insert_text_thread(f"You need level {user.curr_item.skill_reqs['Smithing']} "
                                 f"Smithing to make that.", 'warning')
        return
    # Smithing requires a hammer
    if not user.inventory.is_in_inv(28):
        mywin.insert_text_thread(f"You need a hammer to smith that.", 'warning')
        return
    if user.flags.get('tut_prog', 250) == 23 and user.curr_item.id != 81:
        mywin.insert_text_thread(f"\nYou should stick to making Bronze boots.", 'warning')
        return
    user.curr_action = "smithing"
    # Extract bar and quantity from resource dictionary
    bar, num_bars = list(user.curr_item.resources.items())[0]
    # Compute the maximum number of actions possible based on current resources
    smith_remaining = user.inventory.is_in_inv(bar)[1] // num_bars
    # Configure and place interface elements
    mywin.start_smith.configure(state=DISABLED)
    mywin.insert_text_thread(f"Smithing {user.curr_item.name}...")
    mywin.stop_smith.place(relx=0.45, rely=0.5, relwidth=0.15, relheight=0.1)
    # Arrowheads are smithed 15 at a time
    if user.curr_item.id in [80, 91, 102, 113, 124, 135]:
        add_quant = 15
    else:
        add_quant = 1
    mywin.cooks_left.configure(text=f"{smith_remaining * add_quant} {user.curr_item.name}\nready to smith.")
    mywin.cooks_left.place(relx=0.25, rely=0.5, relwidth=0.2, relheight=0.1)
    while smith_remaining > 0:
        # Start the smithing loop, with timer and progress bar
        start = time.time()
        mywin.progress.configure(value=0)
        mywin.progress.place(relx=0.1, rely=0.25, relheight=0.05)
        # Short interval loop for responsive progress bar and stop button
        for i in range(18):
            mywin.progress.configure(value=100 - min(max((15 - i) * 6, 0), 100))
            if time.time() >= 1.65 + start:
                # Attempt to keep duration as close to 1.8 as possible due to sleep time variation
                mywin.progress.configure(value=100 - min(max((15 - i - 1) * 6, 0), 100))
                time.sleep((start + 1.79 - time.time()) / 2)
                mywin.progress.configure(value=100)
                time.sleep(max((start + 1.8 - time.time()) / 2, 0))
                break
            time.sleep(0.1)
            if not running:
                return
            # Stop smithing if user presses the stop button or somehow loses resources
            if user.curr_action == "flee" or not user.inventory.is_in_inv(bar):
                # Clear interfaces and reset values
                mywin.insert_text_thread(f"Stopping smithing...")
                user.curr_action = "idle"
                mywin.start_smith["state"] = "normal"
                mywin.stop_smith.place_forget()
                mywin.cooks_left.place_forget()
                mywin.progress.place_forget()
                mywin.progress.configure(value=0)
                list_smithing()
                list_smithing()
                return
        mywin.progress.configure(value=100)
        # Delete the correct number of the bars from inventory, add one of the finished item
        user.inventory.remove_item(bar, num_bars)
        mywin.insert_text_thread(f"You smith {add_quant} {user.curr_item.name}.", 'good')
        user.inventory.add_to_inv(user.curr_item.id, add_quant)
        # Give experience and process level-ups
        user.skills['Smithing'][1] += Items[bar].xp * num_bars * global_xp_multiplier
        while xp_to_next('Smithing', True) <= 0 and user.skills['Smithing'][0] != 99:
            user.skills['Smithing'][0] += 1
            mywin.insert_text_thread(f"Congratulations! Your Smithing is now level {user.skills['Smithing'][0]}.",
                                     'good')
        update_skills()
        # Reset progress bar and clear inventory context buttons
        mywin.progress.place_forget()
        mywin.equip_item.place_forget()
        mywin.drop_item.place_forget()
        mywin.crafting.place_forget()
        mywin.eat.place_forget()
        mywin.burn.place_forget()
        mywin.examine_item.place_forget()
        mywin.fletching.place_forget()
        mywin.progress.configure(value=0)
        user.inventory.shuffle_inv()
        update_inventory()
        # Refresh quest info if it is open
        if mywin.quest_info.winfo_viewable():
            curr_pos = mywin.quest_info.yview()
            list_quest_info(True)
            mywin.quest_info.yview_moveto(curr_pos[0])
        # Update the number of items remaining to smith
        if not user.inventory.is_in_inv(bar) or user.inventory.is_in_inv(bar)[1] < num_bars:
            smith_remaining = 0
        else:
            smith_remaining = user.inventory.is_in_inv(bar)[1] // num_bars
        mywin.cooks_left.configure(text=f"{smith_remaining * add_quant} {user.curr_item.name}\nleft to make.")
    # By this point the user has run out of bars, so clear interfaces and reset user action
    mywin.insert_text_thread(f"Stopping smithing...(Not enough bars found.)")
    mywin.stop_smith.place_forget()
    mywin.cooks_left.place_forget()
    list_smithing()
    mywin.start_smelt["state"] = "normal"
    user.curr_action = "idle"
    user.inventory.shuffle_inv()
    update_inventory()
    list_smithing()
    if user.flags.get('tut_prog', 250) == 23:
        user.flags['tut_prog'] = 24


def fletch():
    """Start the fletching process.

    Attempt to fletch the selected item from its resources after checking user's level against the item's requirement.
    Continue until out of resources or user presses the stop button. The quantity of the product being made per
    action varies, with arrow type items creating 15 at a time.
    """
    # Check selected item is valid
    if type(user.curr_item) != Item and type(user.curr_item) != Equipment:
        mywin.insert_text_thread("Select an item to fletch!", 'warning')
        return
    item = user.curr_item
    if user.flags.get('tut_prog', 250) == 20:
        if user.curr_item.id not in [30, 144]:
            print(user.curr_item.id)
            mywin.insert_text_thread(f"Stick to making Bronze arrows for now.", 'warning')
            return
    if user.flags.get('tut_prog', 250) == 21:
        if user.curr_item.id not in [150, 151]:
            if user.inventory.is_in_inv(150):
                mywin.insert_text_thread(f"You should make the Shortbow.", 'warning')
            else:
                mywin.insert_text_thread(f"You should make the Shortbow (u).", 'warning')
            return
    # Fletching requires a knife when processing logs
    if (item.id in range(150, 173, 2) or item.id == 29) and not user.inventory.is_in_inv(27):
        mywin.insert_text_thread(f"You need a knife to cut that.", 'warning')
        return
    # Change quantity of resources/products being processed based on the item eg. arrows are made 15 at a time
    if item.id in {144, 145, 146, 147, 148, 149, 29, 30}:
        quantity = 15
    else:
        quantity = 1
    # Initialise some variables
    user.curr_action = "fletching"
    curr_min = 99999
    max_req = 1
    resources = []
    tier = 1
    # Collect the resources into a list and grab important information from them
    if item.id != 29:
        for resource in item.resources.keys():
            # Find the limiting resource and calculate how many products can be produced
            curr_min = min(user.inventory.is_in_inv(resource)[1] // quantity, curr_min)
            resources.append(resource)
            # Calculate the maximum fletching requirement from the resources to get the product's requirement
            max_req = max(max_req, Items[resource].skill_reqs.get('Fletching', 0))
    # Special case for arrow shafts since they have multiple valid resources (any log type works)
    else:
        # Check the item that was used to open the fletching interface (can be a log or an unstrung bow)
        curr_id = user.inventory.curr_selection[0].id
        curr_req = user.inventory.curr_selection[0].skill_reqs['Fletching']
        # If item is a log, then things are simple
        if curr_id in range(3, 11):
            log_id = curr_id
        else:
            # Compute related log id for a given unstrung bow (log ids are 3 -> 10 skipping 6 and 8)
            log_id = 3 + (curr_req // 15) + ((curr_req // 15) // 3) + ((curr_req // 15) // 4)
        # Check the number of logs in inventory and store the tier and level requirement for this log type
        curr_min = user.inventory.is_in_inv(log_id)[1]
        max_req = Items[log_id].skill_reqs['Fletching']
        resources.append(log_id)
        tier = (Items[log_id].skill_reqs['Fletching'] // 15) + 1
    # Check user's level against the item's requirement
    if user.skills['Fletching'][0] < max_req:
        mywin.insert_text_thread(f"You need level {max_req} fletching to fletch that.", 'warning')
        return
    # Get the quantity of the limiting resource to display as the remaining quantity
    min_input = min(user.inventory.is_in_inv(resources[0])[1], user.inventory.is_in_inv(resources[-1])[1])
    # Allow one run of fletching even when curr_min = 0. This allows resource amounts less than 15 to be processed
    # when the base quantity is 15
    fletch_remaining = max(1, curr_min)
    # Configure the interface elements
    mywin.start_fletch.configure(state=DISABLED)
    mywin.insert_text_thread(f"Fletching {item.name}:")
    mywin.stop_fletch.place(relx=0.45, rely=0.5, relwidth=0.15, relheight=0.1)
    mywin.cooks_left.configure(text=f"{min_input if item.id!=29 else min_input*tier*15} {item.name}\nready to fletch.")
    mywin.cooks_left.place(relx=0.25, rely=0.5, relwidth=0.2, relheight=0.1)
    items_made = 0
    while fletch_remaining > 0:
        # Start the fletching loop, with timer and progress bar
        fletch_remaining -= 1
        start = time.time()
        mywin.progress.configure(value=0)
        mywin.progress.place(relx=0.1, rely=0.25, relheight=0.05)
        # Short interval loop for responsive progress bar and stop button
        for i in range(18):
            mywin.progress.configure(value=100 - min(max((15 - i) * 6, 0), 100))
            if time.time() >= 1.65 + start:
                # Attempt to keep duration as close to 1.8 as possible due to sleep time variation
                mywin.progress.configure(value=100 - min(max((15 - i - 1) * 6, 0), 100))
                time.sleep((start + 1.79 - time.time()) / 2)
                mywin.progress.configure(value=100)
                time.sleep(max((start + 1.8 - time.time()) / 2, 0))
                break
            time.sleep(0.1)
            if not running:
                return
            for r in resources:
                # Stop fletching if user presses the stop button or loses resources somehow
                if not user.inventory.is_in_inv(r) or user.curr_action == "flee":
                    # Clear interfaces and reset values
                    mywin.insert_text_thread(f"Stopping fletching...")
                    user.curr_action = "idle"
                    mywin.start_fletch["state"] = "normal"
                    mywin.stop_fletch.place_forget()
                    mywin.cooks_left.place_forget()
                    mywin.progress.place_forget()
                    mywin.progress.configure(value=0)
                    # Make interface close correctly if viewing inventory or something
                    if not mywin.fletch_0.winfo_viewable():
                        mywin.fletch_0.place(relx=0.1, rely=0.1, relwidth=0.01, relheight=0.01)
                    list_fletching([Items[3], 0, 0])
                    if items_made >= 1:
                        # If user cancels fletching after making 1 item, still progress tutorial
                        if user.flags.get('tut_prog', 250) == 20 and user.curr_item.id == 144:
                            user.flags['tut_prog'] = 21
                        if user.flags.get('tut_prog', 250) == 21 and user.curr_item.id == 151:
                            user.flags['tut_prog'] = 22
                    user.curr_item = 0
                    return
        mywin.progress.configure(value=100)
        # Set the number of resources to remove
        min_input = quantity
        if len(resources) == 2 and quantity == 15:
            if user.inventory.is_in_inv(resources[0]) and user.inventory.is_in_inv(resources[1]):
                min_input = min(user.inventory.is_in_inv(resources[0])[1], user.inventory.is_in_inv(resources[1])[1],
                                quantity)
        # Remove the correct resource quantities, separating the arrow shaft case from the rest
        if len(resources) == 1:
            user.inventory.remove_item(resources[0], 1)
        else:
            user.inventory.remove_item(resources[0], min_input)
            user.inventory.remove_item(resources[1], min_input)
        mywin.insert_text_thread(f"You fletch {min_input*tier} {item.name}.", 'good')
        items_made += 1
        # Add the correct amount of the product to inventory, give experience and process level-ups
        user.inventory.add_to_inv(item.id, min_input if item.id != 29 else 15*tier)
        user.skills['Fletching'][1] += int((tier-1)*45 + item.xp * global_xp_multiplier * (min_input / quantity))
        while xp_to_next('Fletching', True) <= 0 and user.skills['Fletching'][0] != 99:
            user.skills['Fletching'][0] += 1
            mywin.insert_text_thread(f"Congratulations! Your Fletching is now level {user.skills['Fletching'][0]}.",
                                     'good')
        # Clear inventory item context actions, reset progress bar
        update_skills()
        mywin.progress.place_forget()
        mywin.progress.configure(value=0)
        user.inventory.shuffle_inv()
        update_inventory()
        mywin.equip_item.place_forget()
        mywin.drop_item.place_forget()
        mywin.crafting.place_forget()
        mywin.eat.place_forget()
        mywin.burn.place_forget()
        mywin.examine_item.place_forget()
        mywin.fletching.place_forget()
        # Refresh quest info if it is open
        if mywin.quest_info.winfo_viewable():
            curr_pos = mywin.quest_info.yview()
            list_quest_info(True)
            mywin.quest_info.yview_moveto(curr_pos[0])
        # Re-calculate the number of remaining items to fletch
        if user.inventory.is_in_inv(resources[0]) and user.inventory.is_in_inv(resources[-1]):
            if item.id != 29:
                for resource in resources:
                    curr_min = min(user.inventory.is_in_inv(resource)[1] // quantity, curr_min)
                min_resources = min(user.inventory.is_in_inv(resources[0])[1],
                                    user.inventory.is_in_inv(resources[-1])[1])
                mywin.cooks_left.configure(text=f"{curr_min * quantity + (min_resources % quantity)} "
                                           f"{item.name}\nready to fletch.")
            else:
                curr_min = user.inventory.is_in_inv(resources[0])[1]
                mywin.cooks_left.configure(text=f"{curr_min * quantity * tier} {item.name}\nready to fletch.")
            fletch_remaining = max(1, curr_min)
        else:
            fletch_remaining = 0
    # By this point the user has run out of items to fletch, so clear interfaces and reset user action
    mywin.insert_text_thread(f"Stopping fletching...(No more resources found).")
    mywin.stop_fletch.place_forget()
    mywin.cooks_left.place_forget()
    user.curr_action = "idle"
    user.inventory.shuffle_inv()
    update_inventory()
    if not mywin.fletch_0.winfo_viewable():
        mywin.fletch_0.place(relx=0.1, rely=0.1, relwidth=0.01, relheight=0.01)
    list_fletching([Items[3], 0, 0])
    mywin.start_fletch["state"] = "normal"
    if user.flags.get('tut_prog', 250) == 19:
        user.flags['tut_prog'] = 20
    if user.flags.get('tut_prog', 250) == 20 and user.curr_item.id == 144:
        user.flags['tut_prog'] = 21
    if user.flags.get('tut_prog', 250) == 21 and user.curr_item.id == 151:
        user.flags['tut_prog'] = 22
    user.curr_item = 0


def craft():
    """Start the crafting process.

    Attempt to craft the selected item from its resources after checking user's level against the item's requirement.
    Continue until out of resources or user presses the stop button.
    """
    # Check that selected item is valid
    if type(user.curr_item) != Item and type(user.curr_item) != Equipment:
        mywin.insert_text_thread("Select an item to craft!", 'warning')
        return
    item = user.curr_item
    # Crafting requires needle and thread
    if not user.inventory.is_in_inv(44) or not user.inventory.is_in_inv(174):
        mywin.insert_text_thread(f"You need a needle and thread to craft that.", 'warning')
        return
    user.curr_action = "crafting"
    # Store resource in list instead of a variable since this function is mostly copied from fletching
    resources = list(item.resources.keys())
    # Check user's level against item requirement
    if user.skills['Crafting'][0] < (req := item.skill_reqs['Crafting']):
        mywin.insert_text_thread(f"You need level {req} crafting to craft that.", 'warning')
        return
    # Calculate maximum crafts based on current inventory resources and configures interface elements
    craft_remaining = user.inventory.is_in_inv(resources[0])[1] // item.resources[resources[0]]
    mywin.start_craft.configure(state=DISABLED)
    mywin.insert_text_thread(f"Crafting {item.name}:")
    mywin.stop_craft.place(relx=0.45, rely=0.5, relwidth=0.15, relheight=0.1)
    mywin.cooks_left.configure(text=f"{craft_remaining} {item.name}\nready to craft.")
    mywin.cooks_left.place(relx=0.25, rely=0.5, relwidth=0.2, relheight=0.1)
    thread_remaining = user.inventory.is_in_inv(174)[1]
    while craft_remaining > 0 and thread_remaining > 0:
        # Start the crafting loop, with timer and progress bar
        craft_remaining -= 1
        start = time.time()
        mywin.progress.configure(value=0)
        mywin.progress.place(relx=0.1, rely=0.25, relheight=0.05)
        # Short interval loop for responsive progress bar and stop button
        for i in range(18):
            mywin.progress.configure(value=100 - min(max((15 - i) * 6, 0), 100))
            if time.time() >= 1.65 + start:
                # Attempt to keep duration as close to 1.8 as possible due to sleep time variation
                mywin.progress.configure(value=100 - min(max((15 - i - 1) * 6, 0), 100))
                time.sleep((start + 1.79 - time.time()) / 2)
                mywin.progress.configure(value=100)
                time.sleep(max((start + 1.8 - time.time()) / 2, 0))
                break
            time.sleep(0.1)
            if not running:
                return
            for r in resources:
                # Stop crafting if user presses the stop button or somehow loses resources
                if not user.inventory.is_in_inv(r) or user.curr_action == "flee":
                    # Clear interfaces and reset values
                    mywin.insert_text_thread(f"Stopping crafting...")
                    user.curr_action = "idle"
                    mywin.start_craft["state"] = "normal"
                    mywin.stop_craft.place_forget()
                    mywin.cooks_left.place_forget()
                    mywin.progress.place_forget()
                    mywin.progress.configure(value=0)
                    if not mywin.craft_0.winfo_viewable():
                        mywin.craft_0.place(relx=0.1, rely=0.1, relwidth=0.01, relheight=0.01)
                    list_crafting([Items[180], 1, 1])
                    user.curr_item = 0
                    return
        mywin.progress.configure(value=100)
        # Remove the correct number of resources from inventory, has a chance to remove a single thread
        user.inventory.remove_item(resources[0], item.resources[resources[0]])
        if random.random() < 0.2:
            user.inventory.remove_item(174)
        mywin.insert_text_thread(f"You craft a {item.name}.", 'good')
        # Add the crafted item to inventory, generate experience and processes level-ups
        user.inventory.add_to_inv(item.id)
        user.skills['Crafting'][1] += item.xp * global_xp_multiplier
        while xp_to_next('Crafting', True) <= 0 and user.skills['Crafting'][0] != 99:
            user.skills['Crafting'][0] += 1
            mywin.insert_text_thread(f"Congratulations! Your Crafting is now level {user.skills['Crafting'][0]}.",
                                     'good')
        update_skills()
        # Reset progress bar and clear inventory context buttons
        mywin.progress.place_forget()
        mywin.progress.configure(value=0)
        user.inventory.shuffle_inv()
        update_inventory()
        mywin.equip_item.place_forget()
        mywin.drop_item.place_forget()
        mywin.crafting.place_forget()
        mywin.eat.place_forget()
        mywin.burn.place_forget()
        mywin.examine_item.place_forget()
        mywin.fletching.place_forget()
        # Check if thread has run out
        if user.inventory.is_in_inv(174):
            thread_remaining = user.inventory.is_in_inv(174)[1]
        else:
            thread_remaining = 0
            mywin.insert_text_thread(f"You ran out of thread!", 'warning')
        # Refresh quest info if it is open
        if mywin.quest_info.winfo_viewable():
            curr_pos = mywin.quest_info.yview()
            list_quest_info(True)
            mywin.quest_info.yview_moveto(curr_pos[0])
        # Re-calculate the remaining number of items to craft based on resources
        if user.inventory.is_in_inv(resources[0]) and thread_remaining > 0:
            craft_remaining = user.inventory.is_in_inv(resources[0])[1] // item.resources[resources[0]]
            mywin.cooks_left.configure(text=f"{craft_remaining} {item.name}\nready to craft.")
        else:
            craft_remaining = 0
    # By this point the user has run out of things to craft, so clear interfaces and reset user action
    mywin.insert_text_thread(f"Stopping crafting...(No more resources found).")
    mywin.stop_craft.place_forget()
    mywin.cooks_left.place_forget()
    user.curr_action = "idle"
    user.inventory.shuffle_inv()
    update_inventory()
    if not mywin.craft_0.winfo_viewable():
        mywin.craft_0.place(relx=0.1, rely=0.1, relwidth=0.01, relheight=0.01)
    list_crafting([Items[180], 1, 1])
    mywin.start_craft["state"] = "normal"
    if user.flags.get('tut_prog', 250) == 28:
        user.flags['tut_prog'] = 29
    user.curr_item = 0


def tutorial():
    """Start the all-in-one tutorial function.

    This is used when a new account is registered. The user will be guided through
    each of the main features via small tasks with instructions. Elements of the standard interface are gradually
    introduced to prevent overwhelming the user. \n
    The tutorial takes place in two custom areas that are only available until it is complete. Plenty of restrictions
    are added to ensure smooth progression, like blocking the drop function to prevent key items being removed before
    they are used. Progression through the tutorial is tracked by the tut_prog flag, which allows the user to quit
    during the tutorial and continue approximately where they left off. The flag also allows other core functions to
    behave differently or trigger progression.
    """
    # Set up the tutorial presets and the initial interface
    global flashing
    user.inventory = tut_inv
    user.curr_area = tut_area_0
    user.bank = Bank(tab_1=bank_tut)
    window.configure(bg=user.curr_area.background)
    mywin.main_console.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.3)
    mywin.continue_tut.place(relx=0.9, rely=0.95, relwidth=0.1, relheight=0.05)
    # Wrap it all in a try block to catch tkinter error when closing
    try:
        # Use a checkpoint via the tut_prog flag to manage progression for each section
        if user.flags.get('tut_prog', 0) <= 1:
            # Introduce the most basic elements
            user.flags['tut_prog'] = 0
            # Use flash_thread throughout to highlight buttons
            flash_thread('continue_tut')
            mywin.insert_text_thread(f"Welcome. \nTo introduce the basic elements, a guided tutorial"
                                     f" will now begin. Please press the 'Continue' button to proceed.\n")
            # Use basic loops to wait for correct user input that increments tut_prog flag
            while user.flags.get('tut_prog', 250) == 0:
                time.sleep(0.5)
            # Turn off any flashing buttons and disable unwanted actions
            flashing = False
            mywin.continue_tut['state'] = 'disabled'
            # Set flag to expected value in case button is pressed multiple times
            user.flags['tut_prog'] = 1
            # Use the game console to give instructions, with sleep periods between paragraphs for easier reading
            mywin.insert_text_thread(f"First things first, a quick overview of the console. \nThis is where "
                                     f"most of the feedback will come from that is generated by your actions, like "
                                     f"killing enemies, levelling up skills, or progressing quests. ")
            time.sleep(5)
            mywin.insert_text_thread(f"\nMessages will often be colour coded to denote the importance or "
                                     f"positive/negative impact of an action. Look out for ")
            mywin.insert_text_thread(f"red ", 'warning', False)
            mywin.insert_text_thread(f"in particular, which signifies warnings, while ", new_line=False)
            mywin.insert_text_thread(f"green ", 'good', False)
            mywin.insert_text_thread(f"is normally a good thing.", new_line=False)
            # Enable the progression button once user has been given instructions
            mywin.continue_tut['state'] = 'normal'
            flash_thread('continue_tut')
            # Another waiting loop
            while user.flags.get('tut_prog', 250) == 1:
                time.sleep(0.5)
            mywin.continue_tut['state'] = 'disabled'
            user.flags['tut_prog'] = 2
        # Between each section set up any interfaces needed for the next one
        mywin.list_skills.place(relx=0, rely=0.75, relwidth=0.2, relheight=0.05)
        # To allow checkpoints to work correctly, repeat any lasting changes made during the skipped sections
        mywin.continue_tut['state'] = 'disabled'
        # Check the flag again for checkpoint functionality before starting next section
        if user.flags.get('tut_prog', 250) <= 4:
            # Skills
            # Set the flag to the expected value again at the start of each section
            user.flags['tut_prog'] = 2
            flashing = False
            mywin.insert_text_thread(f"\n\nBefore going further, let's take a look at the skills you will be levelling "
                                     f"during the game. Press the skills button to continue.")
            time.sleep(2)
            flash_thread('list_skills')
            time.sleep(0.5)
            # Again use a waiting loop...
            while user.flags.get('tut_prog', 250) == 2:
                time.sleep(0.5)
            user.flags['tut_prog'] = 3
            flashing = False
            mywin.insert_text_thread(f"\nYou begin at level 1 in most skills, with Hitpoints being the exception at 10."
                                     f" Each level takes longer than the previous, and you can check your progress by"
                                     f" pressing one of the buttons.")
            time.sleep(4)
            mywin.insert_text_thread("\nTry pressing the Attack skill or any other for an example.")
            flash_thread('skill_0')
            while user.flags.get('tut_prog', 250) == 3:
                time.sleep(0.5)
            user.flags['tut_prog'] = 4
            flashing = False
            time.sleep(1)
            mywin.insert_text_thread(f"\nThe skills can be categorised into groups, based on how you train them. "
                                     f"Obviously we have the combat skills:\nAttack, Defence, Hitpoints, Magic, Ranged,"
                                     f" Strength.")
            time.sleep(3)
            mywin.insert_text_thread(f"\nThese all improve your combat power and can be levelled by killing enemies. "
                                     f"Attack improves accuracy, Strength improves damage, and Defence reduces the "
                                     f"chance of an enemy hitting you.\n\nEach of the Ranged and Magic skills instead "
                                     f"combine accuracy and damage into one skill.")
            time.sleep(6)
            mywin.insert_text_thread(f"\nNext we have gathering skills:\nFishing, Mining and Woodcutting.")
            time.sleep(3)
            mywin.insert_text_thread(f"These are pretty simple; you level by collecting resources that can be used "
                                     f"elsewhere.")
            time.sleep(3)
            mywin.insert_text_thread(f"\nFinally there are production skills:\nCooking, Crafting, Firemaking, "
                                     f"Fletching, Smithing.")
            time.sleep(3)
            mywin.insert_text_thread(f"These mainly produce more useful items from raw materials, which can be gained "
                                     f"from gathering skills and enemy loot. They usually require more specific "
                                     f"conditions to train, like an anvil or a fire in the current area.")
            time.sleep(3)
            # Set the relevant button states to allow progression when desired
            mywin.continue_tut['state'] = 'normal'
            flash_thread('continue_tut')
            mywin.insert_text_thread(f"Take some time to review the information, then press the flashing button.")
            while user.flags.get('tut_prog', 250) == 4:
                time.sleep(0.5)
            user.flags['tut_prog'] = 5
            flashing = False
            mywin.continue_tut['state'] = 'disabled'
        # Set up new interface for next section
        mywin.list_backpack.place(relx=0, rely=0.8, relwidth=0.2, relheight=0.05)
        if user.flags.get('tut_prog', 250) <= 6:
            # Inventory
            # Again set the progression flag to the correct number
            user.flags['tut_prog'] = 5
            mywin.insert_text_thread(f"\nNow you're familiar with skills, it's time to learn how you will be carrying "
                                     f"items on your adventures. Press the flashing Inventory button to open it.")
            time.sleep(0.5)
            flash_thread('list_backpack')
            while user.flags.get('tut_prog', 250) == 5:
                time.sleep(0.5)
            flashing = False
            user.flags['tut_prog'] = 6
            mywin.insert_text_thread(f"\nYou have 28 inventory slots to store items. Most will be 'non-stackable', "
                                     f"and take up a new slot for each one, but some items are 'stackable' and a "
                                     f"single slot can hold as many as you want.")
            time.sleep(4)
            mywin.insert_text_thread(f"\nIn most cases, if you receive an item with a full inventory it will be "
                                     f"deleted, so be careful.", 'warning')
            time.sleep(3)
            mywin.insert_text_thread(f"\nYou can select an item in your inventory by clicking it, which will show the "
                                     f"available actions related to it. Every item can be dropped, most can be "
                                     f"examined, combat equipment can be equipped, and some items can be used in "
                                     f"production skills.")
            time.sleep(6)
            mywin.continue_tut['state'] = 'normal'
            mywin.insert_text_thread(f"\nTry interacting with a few items in your inventory, then press the flashing "
                                     f"button. Some actions won't work at this stage, but you'll find out more about "
                                     f"them later.")
            flash_thread('continue_tut')
            while user.flags.get('tut_prog', 250) == 6:
                time.sleep(0.2)
            flashing = False
        # Give items to the user between sections where possible for checkpoint compatibility
        mywin.equipment.place(relx=0, rely=0.85, relwidth=0.2, relheight=0.05)
        user.inventory.add_to_inv([144, 83, 84, 85, 87, 88, 32, 151], [20])
        # Make sure to refresh the inventory and similar interfaces when making changes
        update_inventory()
        if user.flags.get('tut_prog', 250) <= 11:
            # Equipment, melee/ranged combat, food, attack styles
            user.flags['tut_prog'] = 7
            mywin.continue_tut['state'] = 'disabled'
            mywin.insert_text_thread(f"\nIt's time to equip some items. Open the equipment tab to get started.")
            time.sleep(0.5)
            flash_thread('equipment')
            while user.flags.get('tut_prog', 250) == 7:
                time.sleep(0.5)
            flashing = False
            user.flags['tut_prog'] = 8
            user.inventory.shuffle_inv()
            update_inventory()
            mywin.insert_text_thread(f"\nHere you can view your equipped items and their stats, which are mostly self "
                                     f"explanatory. Some items have been added to your inventory to play around with."
                                     f"\n")
            time.sleep(2)
            mywin.insert_text_thread(f"Open your inventory again to equip them and see how your equipment stats change."
                                     f" You can un-equip items by clicking them within the equipment view.")
            time.sleep(4)
            mywin.insert_text_thread(f"\nWhen you are ready to continue, press the flashing button.")
            mywin.continue_tut['state'] = 'normal'
            flash_thread('continue_tut')
            while user.flags.get('tut_prog', 250) == 8:
                time.sleep(0.5)
            user.flags['tut_prog'] = 9
            flashing = False
            mywin.continue_tut['state'] = 'disabled'
            mywin.insert_text_thread(f"\nEach area has a selection of monsters to fight, which drop something from a "
                                     f"set of items specific to them. For now there is just one, where you can try some"
                                     f" combat. You can view them by pressing the 'enemies' button.")
            time.sleep(2)
            # Place new interfaces during a section if needed
            mywin.list_enemies.place(relx=0, rely=0.6, relwidth=0.2, relheight=0.05)
            flash_thread('list_enemies')
            mywin.insert_text_thread(f"\nThere are 3 main combat styles:\nMelee, Ranged, Magic.\n\nThis is dictated by "
                                     f"the weapon you have equipped at the time. First you should try melee combat, so"
                                     f" equip the sword from your inventory and try fighting the Rat.")
            # Flash enemy button, then switch to flashing one of the new buttons it creates when pressed
            while flashing:
                time.sleep(0.1)
            time.sleep(0.2)
            flash_thread('enemy_list1')
            # Add the health bar for combat
            mywin.hp_bar.place(relx=0.76, rely=0.4, relwidth=0.1, relheight=0.05)
            while user.flags.get('tut_prog', 250) == 9:
                time.sleep(0.2)
            flashing = False
            user.flags['tut_prog'] = 10
            # Disable actions like combat while other parts of the tutorial are played to keep things smooth
            mywin.enemy_fight['state'] = 'disabled'
            time.sleep(5)
            mywin.insert_text_thread(f"\nCongratulations on defeating your first enemy!\nYou might have noticed your "
                                     f"HP being displayed on the right, which is equal to your Hitpoints level "
                                     f"until lowered by an enemy. This will regenerate at a slow pace over time.")
            time.sleep(5)
            mywin.insert_text_thread(f"\nWhen you need to heal faster or in combat, you should eat some food. This "
                                     f"will delay your next attack slightly for each food you eat, so use them "
                                     f"carefully or between fights. Try using the shrimp from your inventory in your "
                                     f"next fight. Press the flashing button to continue.")
            flash_thread('continue_tut')
            mywin.continue_tut['state'] = 'normal'
            while user.flags.get('tut_prog', 250) == 10:
                time.sleep(0.2)
            flashing = False
            user.flags['tut_prog'] = 11
            mywin.continue_tut['state'] = 'disabled'
            # Display the attack styles for the explanations
            mywin.style1.place(relx=0.35, rely=0.45, relwidth=0.1, relheight=0.05)
            mywin.style2.place(relx=0.45, rely=0.45, relwidth=0.1, relheight=0.05)
            mywin.style3.place(relx=0.55, rely=0.45, relwidth=0.1, relheight=0.05)
            time.sleep(1)
            mywin.insert_text_thread(f"\nDuring a fight, you can choose a style of attack based on your weapon. These "
                                     f"change the skills which gain experience in combat, and may also provide a "
                                     f"combat benefit in accuracy, speed or damage depending on the style. The current "
                                     f"options based on your weapon have been displayed below.")
            time.sleep(5)
            mywin.insert_text_thread(f"\nAny defensive style will split your gained experience between defence and your"
                                     f" current combat style, except for melee which gives all of it to defence."
                                     f"\n\nRanged is the only combat style with an attack speed modifier, given by the "
                                     f"Rapid style. Most others will provide an invisible level boost to the relevant "
                                     f"skill that improves damage rolls.")
            time.sleep(6)
            mywin.insert_text_thread(f"\nAnother important part of combat to know is the flee option, which allows you "
                                     f"to escape from a bad situation and is easily done by pressing the big 'flee' "
                                     f"button that shows up in combat.")
            time.sleep(5)
            mywin.insert_text_thread(f"\nNow you should try using the Shortbow in your inventory to kill "
                                     f"another rat.\nDon't forget to also equip Bronze arrows, since Ranged uses an "
                                     f"ammo system and requires an arrow for each attack.")
            # Re-enable the combat when needed
            mywin.enemy_fight['state'] = 'normal'
            flash_thread('list_enemies')
            flash_thread('enemy_list1')
            while user.flags.get('tut_prog', 250) == 11:
                time.sleep(0.2)
                # Keep the user from running out of ammo while using a bow
                if not user.inventory.is_in_inv(144) and user.equipment.get('Ammo', [0, 0])[0] != 144:
                    # User out of arrows
                    user.equipment['Ammo'] = [144, 20]
                    mywin.insert_text_thread(f"\nSome more arrows have been added to your quiver. Keep trying!", 'good')
            flashing = False
            user.flags['tut_prog'] = 12
            mywin.enemy_fight['state'] = 'disabled'
            time.sleep(3)
            mywin.insert_text_thread(f"\nThe final combat style to try is a little more complicated.")
            time.sleep(2)
        # Repeat the placement of interfaces that were added during the previous section, for checkpoints
        mywin.list_enemies.place(relx=0, rely=0.6, relwidth=0.2, relheight=0.05)
        mywin.hp_bar.place(relx=0.76, rely=0.4, relwidth=0.1, relheight=0.05)
        # Again, add items outside of sections only
        user.inventory.add_to_inv([66, 70, 76], [500, 500])
        update_inventory()
        # Update button states if previous section altered them
        mywin.enemy_fight['state'] = 'disabled'
        if user.flags.get('tut_prog', 250) <= 13:
            # Magic
            user.flags['tut_prog'] = 12
            mywin.continue_tut['state'] = 'disabled'
            mywin.insert_text_thread(f"\nMagic combat requires the use of a staff along with some magical ammo known "
                                     f"as 'runes'. These have been added to your inventory.\n\nBefore you jump into "
                                     f"action, take a look at the Spells tab on the left. By default the weakest spell "
                                     f"is selected, which you have the runes for. ")
            mywin.spellbook.place(relx=0, rely=0.9, relwidth=0.2, relheight=0.05)
            time.sleep(4)
            mywin.insert_text_thread(f"\nIn addition to combat spells, magic provides teleports to various areas "
                                     f"throughout the world. These require a higher magic level so you can't try them "
                                     f"out just yet.\nTake a look around the interface and press the flashing button "
                                     f"when ready to continue.")
            flash_thread('continue_tut')
            mywin.continue_tut['state'] = 'normal'
            while user.flags.get('tut_prog', 250) == 12:
                time.sleep(0.2)
            flashing = False
            user.flags['tut_prog'] = 13
            mywin.continue_tut['state'] = 'disabled'
            time.sleep(0.5)
            mywin.insert_text_thread(f"\nNow you can use magic in combat. Similar to before, make sure you equip the "
                                     f"staff and then try fighting another rat.\nYou have been given sufficient runes "
                                     f"for the fight, but in future you will want to keep your runes stocked up;"
                                     f" magic staves are fragile, and will not work as a melee weapon when you run "
                                     f"out of runes.")
            time.sleep(2)
            flash_thread('list_enemies')
            time.sleep(2)
            mywin.enemy_fight['state'] = 'normal'
            flash_thread('enemy_list1')
            while user.flags.get('tut_prog', 250) == 13:
                time.sleep(0.2)
            flashing = False
            user.flags['tut_prog'] = 14
            mywin.enemy_fight['state'] = 'disabled'
            mywin.insert_text_thread(f"\nThat concludes the combat portion of the tutorial.")
            time.sleep(3)
        # Update states, place interfaces again
        mywin.enemy_fight['state'] = 'disabled'
        mywin.spellbook.place(relx=0, rely=0.9, relwidth=0.2, relheight=0.05)
        if user.flags.get('tut_prog', 250) <= 15:
            # Bank
            user.flags['tut_prog'] = 14
            mywin.continue_tut['state'] = 'disabled'
            mywin.insert_text_thread(f"\nYour inventory is only enough for so long. In addition, you can store items "
                                     f"in a bank to be retrieved later.\n\nBanks are not everywhere however, only "
                                     f"certain areas will allow you to access one. All banks have the same storage"
                                     f" so you don't need to worry about which bank you used before.")
            time.sleep(6)
            mywin.insert_text_thread(f"\nOne of the important things about bank storage is that items become "
                                     f"'stackable', and you can store as many as you like in a single storage slot, "
                                     f"even if that item normally wouldn't stack in your inventory.")
            time.sleep(3)
            mywin.list_bank.place(relx=0, rely=0.25, relwidth=0.1, relheight=0.05)
            flash_thread('list_bank')
            mywin.insert_text_thread(f"\nTry opening the bank with the flashing button.")
            while user.flags.get('tut_prog', 250) == 14:
                time.sleep(0.2)
            flashing = False
            user.flags['tut_prog'] = 15
            mywin.insert_text_thread(f"\nThis is your bank. Some useful items have been placed in it for you to use in "
                                     f"the tutorial later on.\n")
            time.sleep(5)
            mywin.insert_text_thread(f"On the left side of the bank interface is the tab system. Here"
                                     f" you can switch between tabs of storage in your bank, useful for organising or "
                                     f"just overflow from the first tab.")
            time.sleep(5)
            mywin.insert_text_thread(f"Any items deposited into a full tab will be placed in"
                                     f" the next available tab to make banking as easy as possible.")
            time.sleep(5)
            mywin.insert_text_thread(f"\nWithdrawing or depositing items is as easy as clicking one. You can control "
                                     f"the quantity with the options to the right of the bank, or even deposit your "
                                     f"whole inventory if you so wish.")
            time.sleep(5)
            mywin.insert_text_thread(f"\nThe bank takes priority over other interfaces, so you"
                                     f" can only close it using the 'close bank' button that replaced the one you used"
                                     f" to open it.")
            time.sleep(3)
            mywin.insert_text_thread(f"\nYou might want to make some space and withdraw the bronze axe, pickaxe and net"
                                     f" for the next section. Press the flashing button when you are ready to "
                                     f"continue.")
            flash_thread('continue_tut')
            mywin.continue_tut['state'] = 'normal'
            while user.flags.get('tut_prog', 250) == 15:
                time.sleep(0.2)
            flashing = False
            user.flags['tut_prog'] = 16
            mywin.continue_tut['state'] = 'disabled'
        # Add the interface from previous section
        mywin.list_bank.place(relx=0, rely=0.25, relwidth=0.1, relheight=0.05)
        if user.flags.get('tut_prog', 250) <= 17:
            # Gathering skills
            user.flags['tut_prog'] = 16
            mywin.insert_text_thread(f"\nEach of the gathering skills is trained in about the same way. They require a "
                                     f"tool relevant to the skill, like an axe for Woodcutting, which must be either "
                                     f"equipped or in the inventory.")
            time.sleep(4)
            mywin.insert_text_thread(f"\nThroughout the world there are skilling locations that"
                                     f" allow you to train one of the skills and collect resources. A few of these "
                                     f"have been placed in the current area, accessible by the new flashing button "
                                     f"on the left.")
            mywin.list_skill_obj.place(relx=0, rely=0.65, relwidth=0.2, relheight=0.05)
            flash_thread('list_skill_obj')
            mywin.skill_start['state'] = 'disabled'
            while user.flags.get('tut_prog', 250) == 16:
                time.sleep(0.2)
            flashing = False
            user.flags['tut_prog'] = 17
            mywin.insert_text_thread(f"\nThe tools in your bank should allow you to try any of the shown skilling "
                                     f"objects. When you begin, you will see a progress bar indicating how long until "
                                     f"you have a chance at a successful action.")
            time.sleep(4)
            mywin.insert_text_thread(f"\nThis chance increases with level, tool tier and "
                                     f"varies by resource, with higher level resources being harder to succeed at. "
                                     f"If you succeed, you will receive one of the relevant resource and some "
                                     f"experience.")
            time.sleep(4)
            mywin.insert_text_thread(f"\nEach action also carries a chance of depleting the object, which means you "
                                     f"need to manually restart the skilling process. If it doesn't deplete, you "
                                     f"will continue gathering resources automatically until it does.")
            time.sleep(4)
            mywin.insert_text_thread(f"\nMake sure you have the correct tool from the bank, along with some "
                                     f"free space, and then try any of the skill objects to continue.")
            # Flash all the possible options in a row with small delay
            for i in range(4):
                flash_thread('skill_list'+str(i+1))
                time.sleep(0.05)
            mywin.skill_start['state'] = 'normal'
            while user.flags.get('tut_prog', 250) == 17:
                time.sleep(0.2)
            flashing = False
            user.flags['tut_prog'] = 18
            mywin.skill_start['state'] = 'disabled'
            time.sleep(2)
        # Update states and interfaces
        mywin.skill_start['state'] = 'disabled'
        mywin.list_skill_obj.place(relx=0, rely=0.65, relwidth=0.2, relheight=0.05)
        # This is the first point where the user's inventory could be filled, so check for free space
        if user.inventory.free_spaces() >= 4:
            user.inventory.add_to_inv([80, 36, 37, 3], [15, 15])
        else:
            # If inventory is full somehow, then just put items in bank instead
            user.bank.add_to_inv([80, 36, 37, 3], [15, 15])
            mywin.insert_text_thread(f"Items added to bank since inventory is too full.", 'warning')
        mywin.continue_tut['state'] = 'disabled'
        if user.flags.get('tut_prog', 250) <= 21:
            # Fletching
            user.flags['tut_prog'] = 18
            mywin.insert_text_thread(f"Next up are the production skills. Each works in nearly the same way, but with "
                                     f"variance in the interface style.\n\nStarting with Fletching, you will need to "
                                     f"grab the knife from your bank to perform some actions involving log cutting.")
            time.sleep(4)
            mywin.insert_text_thread(f"\nAll Fletching actions can be started via the fletch option on relevant "
                                     f"fletching items. An interface will show which contains all products involving "
                                     f"the item you selected.")
            time.sleep(3)
            mywin.insert_text_thread(f"\nTry using the fletch option on the logs that were placed in your inventory "
                                     f"while carrying a knife from the bank.")
            flash_thread('fletching')
            mywin.start_fletch['state'] = 'disabled'
            while user.flags.get('tut_prog', 250) == 18:
                time.sleep(0.2)
            flashing = False
            user.flags['tut_prog'] = 19
            mywin.insert_text_thread(f"\nAt level 1 you only have access to one option for logs. Select it and see "
                                     f"what the Fletching process looks like.")
            # Keep managing the button states for the current activity
            mywin.start_fletch['state'] = 'normal'
            while user.flags.get('tut_prog', 250) == 19:
                time.sleep(0.2)
            flashing = False
            user.flags['tut_prog'] = 20
            mywin.start_fletch['state'] = 'disabled'
            time.sleep(2)
            mywin.insert_text_thread(f"\nYou've made some arrow shafts! These are the first step in making arrows. "
                                     f"You may have noticed some feathers and Bronze arrowheads in your inventory as"
                                     f" well.")
            time.sleep(3)
            mywin.insert_text_thread("\nUse the fletch option on the shafts and then the resulting headless arrows to "
                                     "finish the process.\n")
            mywin.start_fletch['state'] = 'normal'
            while user.flags.get('tut_prog', 250) == 20:
                time.sleep(0.2)
            flashing = False
            user.flags['tut_prog'] = 21
            mywin.start_fletch['state'] = 'disabled'
            time.sleep(2)
            mywin.insert_text_thread(f"\nNice arrows!\n\nFletching is the main way to get ammo and weaponry for "
                                     f"Ranged combat. To finish this little introduction you should make a Shortbow."
                                     f"\nUse the logs again but this time choose the Shortbow (u) option, which you've "
                                     f"been given the level for.")
            # Check free space again before adding an item
            if user.inventory.free_spaces() > 1:
                user.inventory.add_to_inv(3)
            # Advance the user's level slightly so they can try making different items
            user.skills['Fletching'] = [5, 388]
            time.sleep(4)
            mywin.insert_text_thread(f"\nAfterwards, you can finish the process of making a full Shortbow by using the "
                                     f"fletch option on the un-strung Shortbow.")
            mywin.start_fletch['state'] = 'normal'
            while user.flags.get('tut_prog', 250) == 21:
                time.sleep(0.2)
            flashing = False
            user.flags['tut_prog'] = 22
        # Change user's level to match the final result of the previous section
        user.skills['Fletching'] = [5, 466]
        mywin.start_fletch['state'] = 'disabled'
        # Free space check
        if user.inventory.free_spaces() >= 2:
            user.inventory.add_to_inv([77, 78])
        else:
            # Add to bank if inventory full
            user.bank.add_to_inv([77, 78])
            mywin.insert_text_thread(f"Items added to bank since inventory is too full.", 'warning')
        # States and interface updates: west_btn is disabled now since it will be added soon
        mywin.west_btn['state'] = 'disabled'
        mywin.furnace.place(relx=0, rely=0.15, relwidth=0.1, relheight=0.05)
        if user.flags.get('tut_prog', 250) <= 24:
            # Smelting and Smithing with area switching
            user.flags['tut_prog'] = 22
            mywin.insert_text_thread(f"\nNext up is Smithing. This is split into two slightly different elements:"
                                     f"\nSmelting ores into bars and then smithing bars into items.\n")
            time.sleep(3)
            mywin.insert_text_thread(f"The first of these requires a furnace in the current area, while the second "
                                     f"step needs both an anvil in the area and a hammer in your inventory.")
            time.sleep(3)
            mywin.insert_text_thread(f"\nTry smelting a Bronze bar through the new flashing button. The relevant ore "
                                     f"has been given to you.\n")
            flash_thread('furnace')
            while user.flags.get('tut_prog', 250) == 22:
                time.sleep(0.2)
            flashing = False
            user.flags['tut_prog'] = 23
            mywin.start_smelt['state'] = 'disabled'
            time.sleep(2)
            mywin.insert_text_thread(f"\nYou've made a Bronze bar, but the current area doesn't have an anvil for you "
                                     f"to use!\nThis is common, you won't find an anvil and furnace in the same "
                                     f"location very often. This means it's time to learn more about areas and how you "
                                     f"can move between them.")
            time.sleep(5)
            mywin.insert_text_thread(f"\nMost things vary between areas in some way, whether that be a type of enemy "
                                     f"or the existence of a furnace.\n\nAn area is defined by:\n- The enemies you can "
                                     f"fight\n- The gathering skill locations available\n- The non-player characters "
                                     f"you can talk to. (More later)\n- If it has a bank, anvil, furnace and range.")
            time.sleep(6)
            mywin.insert_text_thread(f"\nEach area has up to 4 neighbouring areas. These are placed in the standard"
                                     f" compass directions of North, East, South, and West.\nA button with the relevant"
                                     f" direction will be displayed on that side of the window when a neighbouring"
                                     f" area exists.")
            time.sleep(5)
            mywin.insert_text_thread(f"\nAs long as you are currently 'idle', (not engaged in combat, banking, "
                                     f"shopping or skilling of any kind), you can press one of the direction buttons "
                                     f"to switch to that area.")
            time.sleep(5)
            mywin.insert_text_thread("\nA new area has been added to the East, which contains the anvil you need to"
                                     f" finish what you were doing. Try heading to this area.\n")
            # Add button for area change
            mywin.east_btn.place(relx=0.9, rely=0.475, relwidth=0.1, relheight=0.05)
            flash_thread('east_btn')
            # Wait for area change
            while user.curr_area == tut_area_0:
                time.sleep(0.2)
            flashing = False
            time.sleep(2)
            mywin.insert_text_thread(f"\nWelcome to the new area! Here you can see the anvil exists, so try smithing "
                                     f"that bar into some boots.\nDon't forget your hammer!\n")
            flash_thread('anvil')
            while user.flags.get('tut_prog', 250) == 23:
                time.sleep(0.2)
            user.flags['tut_prog'] = 24
            flashing = False
            time.sleep(2)
            mywin.insert_text_thread(f"\nNice boots!\nSmithing experience scales linearly with the number of bars an "
                                     f"item needs to be made. Larger items like platebodies will thus grant faster XP. "
                                     f"Making items in Smithing is a great way to get melee combat gear.\n")
            # Flash the continue button to remind user to press it to continue
            flash_thread('continue_tut')
            mywin.continue_tut['state'] = 'normal'
            while user.flags.get('tut_prog', 250) == 24:
                time.sleep(0.2)
            user.flags['tut_prog'] = 25
            flashing = False
            mywin.continue_tut['state'] = 'disabled'
            time.sleep(2)
        # Update the area and run the area_setup to get an exact replica of the expected interfaces for checkpoints
        user.curr_area = tut_area_1
        area_setup()
        # Update button states
        mywin.start_smelt['state'] = 'disabled'
        mywin.start_smith['state'] = 'disabled'
        # Check for space
        if user.inventory.free_spaces() >= 2:
            user.inventory.add_to_inv([3, 11])
        else:
            # Add to bank if inventory full
            user.bank.add_to_inv([3, 11])
            mywin.insert_text_thread(f"Items added to bank since inventory is too full.", 'warning')
        if user.flags.get('tut_prog', 250) <= 27:
            # Cooking
            user.flags['tut_prog'] = 25
            mywin.burn['state'] = 'disabled'
            mywin.insert_text_thread(f"\nFood is an important part of surviving combat, so it's about time you learned"
                                     f" how to make some.\n\nThe Cooking skill allows you to create edible versions of"
                                     f" fish you catch during Fishing, if you have the level for it.")
            time.sleep(5)
            mywin.insert_text_thread(f"\nYou will need some form of fire or cooking range to do so, which can be"
                                     f" provided by the Firemaking skill if a certain area doesn't contain one.\n")
            time.sleep(4)
            mywin.insert_text_thread(f"Requiring a tinderbox, you can select the burn option on any logs to instantly"
                                     f" start a fire, granting some experience and a place to cook on. This is only "
                                     f"temporary: higher tier logs will provide a longer lasting fire for you to use.")
            time.sleep(5)
            mywin.insert_text_thread(f"\nTry burning some logs to start a fire. For now, this fire will be permanent "
                                     f"for tutorial purposes, but be aware that in the future you will need to keep "
                                     f"refreshing it with logs if you wish to continue cooking.\n\nThere should be a "
                                     f"tinderbox in your bank if you need one.\n")
            mywin.burn['state'] = 'normal'
            while user.flags.get('tut_prog', 250) == 25:
                time.sleep(0.2)
            user.flags['tut_prog'] = 26
            mywin.cooking.place(relx=0, rely=0.2, relwidth=0.1, relheight=0.05)
            mywin.start_cook['state'] = 'disabled'
            time.sleep(2)
            mywin.burn['state'] = 'disabled'
            mywin.insert_text_thread(f"\nThere is now a fire for you to cook on. Especially at lower levels, there is"
                                     f" a chance to burn your food instead of cooking it. If this occurs, you will "
                                     f"simply lose the raw food and gain no experience.")
            time.sleep(3)
            mywin.insert_text_thread(f"You should have some raw shrimp, so try cooking it via the flashing button.")
            flash_thread('cooking')
            mywin.start_cook['state'] = 'normal'
            while user.flags.get('tut_prog', 250) == 26:
                time.sleep(0.2)
            user.flags['tut_prog'] = 27
            flashing = False
            time.sleep(3)
            mywin.insert_text_thread(f"\nCooking food like that is the best way to get some, even if you burn it "
                                     f"occasionally. Press the flashing button when ready to continue.")
            mywin.continue_tut['state'] = 'normal'
            flash_thread('continue_tut')
            while user.flags.get('tut_prog', 250) == 27:
                time.sleep(0.2)
            user.flags['tut_prog'] = 28
            mywin.continue_tut['state'] = 'disabled'
            flashing = False
        # Update states, interfaces and add items directly to bank
        mywin.cooking.place(relx=0, rely=0.2, relwidth=0.1, relheight=0.05)
        mywin.burn['state'] = 'disabled'
        mywin.start_cook['state'] = 'disabled'
        user.bank.add_to_inv([44, 174, 175], [1, 10, 5])
        if user.flags.get('tut_prog', 250) == 28:
            # Crafting
            mywin.start_craft['state'] = 'disabled'
            mywin.insert_text_thread(f"\nCrafting is the final production skill to look at. It is the main way to "
                                     f"obtain Ranged combat armour, and requires leather gained from monsters along "
                                     f"with a needle and some thread. The thread may be used up in the process, but "
                                     f"it's cheap to grab from a shop. ")
            time.sleep(5)
            mywin.insert_text_thread(f"\nSimilar to Smithing, XP scales with the number of leather you use for an item."
                                     f" On the other hand the interface style is more akin to Fletching, being "
                                     f"accessible from the inventory item options on any type of leather.")
            time.sleep(4)
            mywin.insert_text_thread(f"\nYou should check the bank for some crafting supplies. Grab a needle, some "
                                     f"thread and cow leather, then make yourself a Leather cowl.\n")
            # Flash both buttons that should be pressed
            flash_thread('crafting')
            flash_thread('start_craft')
            mywin.start_craft['state'] = 'normal'
            # Wait for user to create the correct item and stop crafting
            while not (user.inventory.is_in_inv(31) and user.curr_action == 'idle'):
                time.sleep(0.2)
            user.flags['tut_prog'] = 29
            mywin.start_craft['state'] = 'disabled'
            flashing = False
        mywin.start_craft['state'] = 'disabled'
        if user.flags['tut_prog'] <= 30:
            # NPCs: shops
            user.flags['tut_prog'] = 29
            mywin.insert_text_thread(f"\nThat's about all you need to know about skills. Next you need to learn how"
                                     f" to interact with NPCs (non-player characters), who you can talk to for "
                                     f"information, shopping or questing.")
            time.sleep(4)
            mywin.insert_text_thread(f"\nThe final gap in the lower left menu has now been filled. This is where you"
                                     f" can view the NPCs in your current area, and interact with them there. When "
                                     f"talking to one, you will be presented with one or two options as responses, "
                                     f"mostly used to accept or make choices in quests.")
            mywin.list_npcs.place(relx=0, rely=0.7, relwidth=0.2, relheight=0.05)
            mywin.interact_npc['state'] = 'disabled'
            time.sleep(5)
            mywin.insert_text_thread(f"\nFirst you should try talking to the only one available, by opening the NPC "
                                     f"interface and using the flashing button. Use the leave button afterwards to "
                                     f"continue.")
            mywin.interact_npc['state'] = 'normal'
            # Flash every relevant button for the current step
            flash_thread('list_npcs')
            flash_thread('npc_list1')
            flash_thread('interact_npc')
            flash_thread('npc_response_2')
            # Wait for both the NPC to be selected and spoken to
            while not mywin.npc_dialogue.winfo_viewable():
                time.sleep(0.2)
            while mywin.npc_dialogue.winfo_viewable():
                # Make sure user actually tries the talking option
                time.sleep(0.2)
            flashing = False
            user.flags['tut_prog'] = 30
            # Add the shopkeeper to the current area so it will appear next time NPC list is opened
            tut_area_1.npcs.append(Tut_shop)
            if mywin.npc_list1.winfo_viewable():
                # If user has npc tab open already, just add shopkeeper NPC directly
                mywin.npc_list2.place(relx=0.25, rely=0.7, relwidth=0.15, relheight=0.05)
            # Don't let user open shop until explanation is done
            mywin.open_shop['state'] = 'disabled'
            mywin.insert_text_thread(f"\nTalk is cheap, but some NPCs are a little richer. They own shops, where you"
                                     f" can buy and sell a selection of items for a fair price. If you haven't realised"
                                     f" by now, the universal currency in this world is gold pieces, which you can "
                                     f"gain through killing or selling primarily.")
            time.sleep(5)
            mywin.insert_text_thread(f"\nGenerally an item sells for 60% of the price you can buy it for, so don't "
                                     f"buy anything you won't use. The shop interface is similar to the bank, using the"
                                     f" same quantity options, but without the tabs.")
            time.sleep(5)
            mywin.insert_text_thread(f"\nOn the other hand, interacting with items is slightly different:"
                                     f"\nYou will be presented some options like getting the value of an item before "
                                     f"you sell, rather than selling items in a single press. This does not apply to "
                                     f"purchases however, so be wary of accidentally buying the wrong thing.")
            time.sleep(6)
            mywin.insert_text_thread(f"\nA new shop NPC has appeared, so you can try buying and selling things. To "
                                     f"access the shop, select the new NPC and then the flashing 'Open shop' button. "
                                     f"When you are done shopping, close the shop and use the Continue button.")
            # Flash buttons and allow shop to be opened
            flash_thread('open_shop')
            flash_thread('close_shop')
            mywin.open_shop['state'] = 'normal'
            # Wait for the shop to be closed before allowing user to continue
            while not mywin.shop_0.winfo_viewable():
                time.sleep(0.2)
            flashing = False
            mywin.continue_tut['state'] = 'normal'
            time.sleep(0.5)
            flash_thread('continue_tut')
            while user.flags['tut_prog'] == 30:
                time.sleep(0.2)
            flashing = False
            user.flags['tut_prog'] = 31
            mywin.continue_tut['state'] = 'disabled'
        # Add the shopkeeper if using checkpoints
        if Tut_shop not in tut_area_1.npcs:
            tut_area_1.npcs.append(Tut_shop)
        if user.flags['tut_prog'] >= 31:
            # Quests and final test
            user.flags['tut_prog'] = 31
            # If user is using checkpoints, update the areas to the correct state for their quest progress
            if [1, 3] in user.quest_flags:
                tut_area_1.enemies[1] = Man_enemy
                tut_area_1.npcs.remove(Man_npc)
            elif [1, 4] in user.quest_flags:
                tut_area_1.enemies[1] = None_enemy
            mywin.insert_text_thread(f"\nYou've seen the basics, and it's almost time to give you full control, but "
                                     f"first the other function of NPCs will be introduced: Quests.")
            time.sleep(4)
            mywin.insert_text_thread(f"\nOften an NPC will have a task or series of tasks for you to complete, which "
                                     f"may involve killing enemies, visiting another NPC, or acquiring a selection of"
                                     f" items through whatever means necessary.")
            time.sleep(4)
            mywin.insert_text_thread(f"\nThese will sometimes require a minimum set of skill levels to begin, in order"
                                     f" to add a barrier to potential rewards or simply because the quest involves "
                                     f"using a certain skill.")
            time.sleep(5)
            mywin.insert_text_thread(f"\nFinishing the entirety of a quest will reward you with relevant experience "
                                     f"in skills, along with gold or some useful items in some cases. Certain areas"
                                     f" may even be locked behind a quest completion. ")
            time.sleep(4)
            mywin.quest_obj.place(relx=0, rely=0.4, relwidth=0.1, relheight=0.05)
            flash_thread('quest_obj')
            mywin.insert_text_thread(f"\nKeeping track of all these tasks can get tricky, so you can check your "
                                     f"progress in the quest info tab, accessible by the new flashing button to the "
                                     f"left. Currently it's empty, but it should come in handy pretty soon. Take a "
                                     f"look at it to continue.")
            while user.flags['tut_prog'] == 31:
                time.sleep(0.2)
            flashing = False
            user.flags['tut_prog'] = 32
            time.sleep(1)
            mywin.insert_text_thread(f"\nTo navigate quests, simply talk to a quest-giving NPC and the quest dialogue "
                                     f"will automatically begin if you meet the requirements. From here you can accept "
                                     f"or decline the start of the quest, but once you finish one part of a quest, "
                                     f"the next will be started for you after talking to the correct NPC.")
            time.sleep(4)
            mywin.insert_text_thread(f"\nFollow the given instructions to progress a quest, you can always return to "
                                     f"the NPC or check your quest info for a reminder.")
            time.sleep(3)
            mywin.insert_text_thread(f"\nNow you are on your own. All actions have been unlocked, and you can move "
                                     f"freely between the two tutorial areas. Use what you've learned to complete the "
                                     f"quest given by the 'Man' in the western tutorial area.")
            time.sleep(3)
            mywin.insert_text_thread(f"\nBe aware that any items in your inventory, equipment or bank will be deleted "
                                     f"when you finish the tutorial, but skill levels will remain.", 'warning')
            # Add the tutorial quest to the Man NPC
            Man_npc.flags = [[1, 0], [1, 1], [1, 2]]
            # Enable all actions for the user during this section
            mywin.skill_start['state'] = 'normal'
            mywin.start_smelt['state'] = 'normal'
            mywin.start_cook['state'] = 'normal'
            mywin.start_smith['state'] = 'normal'
            mywin.start_fletch['state'] = 'normal'
            mywin.start_craft['state'] = 'normal'
            mywin.enemy_fight['state'] = 'normal'
            mywin.burn['state'] = 'normal'
            mywin.west_btn['state'] = 'normal'
            mywin.open_shop['state'] = 'normal'
            # Wait for full quest completion. User is free to do whatever they want before this happens
            while user.flags['tut_prog'] == 32:
                time.sleep(1)
            user.flags['tut_prog'] = 33
            time.sleep(1)
            mywin.insert_text_thread(f"\nGood job on that quest. It's finally time to head to the mainland and forge "
                                     f"your own journey. Whenever you're ready, press the Continue button.")
            mywin.insert_text_thread(f"\nRemember, all items will be removed, but skills will remain.", 'warning')
            mywin.continue_tut['state'] = 'normal'
            while user.flags['tut_prog'] == 33:
                time.sleep(0.2)
            # Tutorial is complete
            # Set the area to the spawn area, clear the tutorial continue button
            user.curr_area = Lum
            mywin.continue_tut.place_forget()
            # Set tutorial progress to arbitrarily large value
            user.flags['tut_prog'] = 250
            # Set up the starting area
            area_setup()
            mywin.insert_text_thread(f"\nYou take the boat to the mainland...\n", 'good')
            # Set up user's inventory and bank

            user.inventory = Inventory([83, 1], [85, 1], [151, 1], [76, 1],  [45, 1], [52, 1], [59, 1], [39, 1],
                                       [28, 1], [66, 100], [67, 100], [68, 100], [69, 100], [70, 100], [144, 100],
                                       [12, 5])
            user.bank = Bank(tab_1=Inventory([0, 25]))
            time.sleep(2)
            # Recommend cooks assistant quest to give user direction
            mywin.insert_text_thread(f"\nConsider paying a visit to the local Cook if you're looking for something "
                                     f"to do.")
    except _tkinter.TclError:
        pass


def save_data():
    """Save user data to the local database."""
    with sql.connect("Pr_db") as conn:
        my_data = list(user.list_data())
        my_data.append(my_data[0])
        cur = conn.cursor()
        cur.execute("""UPDATE user_data
        SET name = ?, skills = ?, flags = ?, inventory = ?, bank = ?, curr_area = ?, curr_action = ?, curr_shop = ?, 
        curr_spell = ?, curr_item = ?, att_style = ?, equipment = ?, health = ?, spawn = ?, quest_flags = ?
        WHERE name = ?""", my_data)


def load_data(name):
    """Load user data from the local database.

    name = string containing the user's username.
    """
    global user
    with sql.connect("Pr_db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM user_data WHERE name = ?", [name])
        rows = cur.fetchall()
        save_string = ""
        # Join all the columns from the database together into one string
        for row in rows:
            for i, c in enumerate(row[1:]):
                if i in [0, 6, 10]:
                    # Keep intended strings as strings after next steps
                    c = "'" + c + "'"
                if i < len(row) - 2:
                    save_string += c + ", "
                else:
                    # Don't add comma for final entry
                    save_string += c
        save_string = "[" + save_string + "]"
        # Using eval here is easy but could look for a better method in future
        user = Player(*eval(save_string))


def exit_func():
    """Run on exit: save user data and close processes as needed."""
    global running
    global flashing
    # Globally announce that the application is closing, and stop any flashing buttons
    running = False
    flashing = False
    mywin.insert_text_thread("\nCLOSING, SAVING YOUR DATA...")
    user.curr_action = 'idle'
    mywin.skill_start["state"] = "normal"
    user.curr_item = 0
    # Save user data
    if user.flags.get('DEFAULT', -1) == -1:
        save_data()
    # Arbitrary sleep time to make sure things are done before killing the window
    time.sleep(1)
    window.destroy()


def start_exit():
    """Start the exit function as a thread.

    Allows it to display text to the user instead of instantly freezing all functions. Block duplicate exit calls.
    """
    if running:
        t = Thread(target=exit_func, daemon=True)
        t.name = "exit_thread"
        t.start()


# Set up the window
window = Tk()
mywin = MyWindow(window)
window.configure(bg='#4f0781')
window.title('PruneScape Client')
window.geometry("1080x720+100+200")
window.resizable(False, False)
# Set the default tab/quantity to 1 on startup, and depress default buttons
mywin.tab_1.invoke()
mywin.quantity_1.invoke()
vars(mywin)['spell_'+str(user.curr_spell)].invoke()
# area_setup()
# t0 = Thread(target=tutorial, daemon=True)
# t0.name = "tutorial_thread"
# t0.start()

# Start the passive HP regen thread
t1 = Thread(target=regen, daemon=True)
t1.name = "regen_thread"
t1.start()

# 1,4,6,11,13,15,17,21,24,27,28,30,31+ = tutorial checkpoint flags for quick reference
user.flags['tut_prog'] = 255
window.protocol("WM_DELETE_WINDOW", start_exit)

# Start the app, showing the initial register/login screen
startup()
window.mainloop()
