from firepup650 import clear, randint, sql, e
import random as r
from fkeycapture import get, getnum, getchars
import os, time, sys, re
from time import sleep

db = sql("dev-database.db")

alphanum = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

def multipleOf(num: int, mult: int = 5) -> bool:
    return num%mult == 0

# TODO: Add some sleeps to make this seem like it's doing something
print("Loading Loge City v 0.0.1...")
print("Checking system compatibility...")
print("OK.")  # TODO: This should beep or something
print("Checking imports...")
print("import ID UcO80qfR7o2BW3owpAQRsD6Q")
print("OK.")
print("Loaded successfully")
print("Starting...")
clear()
print("Welcome to the city!")
print("Do you have an existing account?\n1. Yes\n2. No")
log = getchars()
un = ""
if log == "1":
    clear()
    print("Please enter your 5 character username")
    pw = ""
    while 1:
        un.append(getchars(alphanum))
        clear()
        print("Please enter your 5 character username")
        print(un, end="")
        match un.length():
            case 0:
                print("-----")
            case 1:
                print("----")
            case 2:
                print("---")
            case 3:
                print("--")
            case 4:
                print("-")
            case _:
                pass
        if un.length() == 5:
            break
    while 1:
        pw.append(getchars(alphanum))
        clear()
        print("Please enter your 5 character username")
        match pw.length():
            case 0:
                print("-----")
            case 1:
                print("*----")
            case 2:
                print("**---")
            case 3:
                print("***--")
            case 4:
                print("****-")
            case _:
                print("*****")
        if pw.length() == 5:
            break
    uData = db.get(un)
    if not uData:
        print("Sorry, that username is not recognized.")
        e(3)
    elif pw != uData["password"]:
        print("Incorrect password")
        e(2)
    else:
        print("Logged in.")
else:
    pw = ""
    while 1:
        clear()
        print("Please enter a 5 character (alphanumeric) username")
        print(un, end="")
        match un.length():
            case 0:
                print("-----")
            case 1:
                print("----")
            case 2:
                print("---")
            case 3:
                print("--")
            case 4:
                print("-")
            case _:
                pass
        if un.length() == 5:
            break
        un.append(getchars(alphanum))
    while 1:
        clear()
        print("Please enter a 5 character (alphanumeric) password")

        match pw.length():
            case 0:
                print("-----")
            case 1:
                print("*----")
            case 2:
                print("**---")
            case 3:
                print("***--")
            case 4:
                print("****-")
            case _:
                print("*****")
        if pw.length() == 5:
            break
        pw.append(getchars(alphanum))
    uData = db.get(un)
    if uData:
        print("Sorry, that username is already registered, please log in instead.")
        e(4)
    else:
        db.set(
            un,
            {
                "password": pw,
                "permissionLevel": 10,
                "logins": 0,
                "vehicles": [],
                "houseLevel": 0,
                "energyTanks": 0,
                "studsGained": 0,
                "studsLost": 0,
                "highestStuds": 20,
                "studs": 20,
                "debug": False,
                "o": 0, # I have no clue what this is supposed to be, doesn't seem to be used in the original doc?
            },
        )
        print("Account created successfully!")
sleep(1)
clear()
uData = db.get(un)
uData["logins"] += 1
if uData["logins"] == 1:
    print(f"Welcome {un}, to Loge City!")
else:
    print(f"Welcome back to Loge City {un}.")
sleep(1)
while 1:
    print("""What would you like to do?
1. Stats
2. Gamble
3. Research
4. Vehicle Shop
5. Rare Parts Shop
6. Energy Tank Shop
7. Resturant
E. Exit""") # TODO: Put shops in their own menu
    if uData["debug"]:
        print("D. [DEBUG]")
    go = getchars("1234567ED")
    match go:
        case "1":
            print(f"""Stats:
 Studs:
  Current:          {uData["studs"]}
  All-time Highest: {uData["highestStuds"]}
  All-time Losses:  {uData["studsLost"]}
  All-time Gains:   {uData["studsGained"]}
 Vehicles:          {uData["vechicles"]}
 House Level:       {uData["houseLevel"]}
 Energy Tanks:      {uData["energyTanks"]}""")
            if uData["debug"]:
                print("""Debug Stats:
 Bebug bit:         {uData["debug"]}
 Permission Level:  {uData["permissionLevel"]}
 Idk what o is:     {uData["o"]}""")
            print("Press any key to exit")
            get()
            clear()
        case "2":
            print("""How many studs would you like to bet?
1. 10
2. 20
3. 30
4. 40
5. 50
6. 60
7. 70
8. 80
9. 90
0. 100
E. Exit""")
            bet = getchars("0123456789E")
            betSt = 0
            match bet:
                case "1":
                    betSt = 20
                case "2":
                    betSt = 40
                case "3":
                    betSt = 60
                case "4":
                    betSt = 80
                case "5":
                    betSt = 100
                case "6":
                    betSt = 120
                case "7":
                    betSt = 140
                case "8":
                    betSt = 160
                case "9":
                    betSt = 180
                case "0":
                    betSt = 200
                case _:
                    betSt = 0
            winnings = 0
            while 1:
                winnings = randint(0 - max, max)
                if multipleOf(winnings):
                    break
            if betSt:
                if uData["studs"] >= int(bet) * 10:
                    uData["studs"] += winnings
                    # And this is the end of the old code docs... (basically, this part is modified however)
                    if winnings == 0:
                        print("You won nothing. (You kept your bet though)")
                    elif winnings == (0 - (int(bet) * 10)):
                        print("You lost your bet!")
                        uData["studsLost"] -= winnings
                    elif winnings >= 0:
                        print(f"You won {winnings} studs!")
                        uData["studsGained"] += winnings
                    elif winnings <= 0:
                        print(f"You lost {winnings} studs!")
                        uData["studsLost"] -= winnings
                    else:
                        print("wtf")
                    if uData["studs"] > uData["highestStuds"]:
                        uData["highestStuds"] = uData["studs"]
                else:
                    print("You don't have enough studs to bet that much.")
