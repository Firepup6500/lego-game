from firepup650 import clear, randint, sql, e, menu
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
log = menu({"Yes": 1, "No": 0}, "Welcome to the city!\nDo you have an existing account?")
un = ""
if log:
    pw = ""
    while 1:
        clear()
        print("Please enter your 5 character username")
        print(un, end="")
        match len(un):
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
        if len(un) == 5:
            break
        un += getchars(1, alphanum)
    while 1:
        clear()
        print("Please enter your 5 character password")
        match len(pw):
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
        if len(pw) == 5:
            break
        pw += getchars(1, alphanum)
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
        match len(un):
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
        if len(un) == 5:
            break
        un += getchars(1, alphanum)
    while 1:
        clear()
        print("Please enter a 5 character (alphanumeric) password")
        match len(pw):
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
        if len(pw) == 5:
            break
        pw += getchars(1, alphanum)
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
sleep(2)
while 1:
    go = menu({"Stats": 1, "Gamble": 2, "Research": 3, "Vehicle Shop": 4, "Rare Parts Shop": 5, "Energy Tank Shop": 6, "Resturant": 7, "[DEBUG]": "D", "Exit": "E"}, "What would you like to do?") # TODO: Put shops in their own menu
    clear()
    match go:
        case 1:
            print(f"""Stats:
 Studs:
  Current:          {uData["studs"]}
  All-time Highest: {uData["highestStuds"]}
  All-time Losses:  {uData["studsLost"]}
  All-time Gains:   {uData["studsGained"]}
 Vehicles:          {uData["vehicles"]}
 House Level:       {uData["houseLevel"]}
 Energy Tanks:      {uData["energyTanks"]}""")
            if uData["debug"]:
                print(f"""Debug Stats:
 Bebug bit:         {uData["debug"]}
 Permission Level:  {uData["permissionLevel"]}
 Idk what o is:     {uData["o"]}""")
            print("Press any key to exit")
            get()
        case 2:
            bet = menu({"5": 5, "10": 10, "20": 20, "30": 30, "40": 40, "50": 50, "60": 60, "70": 70, "80": 80, "90": 90, "100": 100, "1000": 1000, "Exit": "E"}, "How many studs would you like to bet?")
            betHigh = 0
            match bet:
                case 10:
                    betHigh = 20
                case 20:
                    betHigh = 40
                case 30:
                    betHigh = 60
                case 40:
                    betHigh = 80
                case 50:
                    betHigh = 100
                case 60:
                    betHigh = 120
                case 70:
                    betHigh = 140
                case 80:
                    betHigh = 160
                case 90:
                    betHigh = 180
                case 100:
                    betHigh = 200
                case 1000:
                    betHigh = 2000
                case _:
                    betHigh = 0
            winnings = 0
            betLow = -bet if betHigh else 0
            while betHigh:
                winnings = randint(betLow, betHigh)
                if multipleOf(winnings):
                    break
            if betHigh:
                if uData["studs"] >= abs(betLow):
                    uData["studs"] += winnings
                    # And this is the end of the old code docs... (basically, this part is modified however)
                    if winnings == 0:
                        print("You won nothing. (You kept your bet though)")
                    elif winnings == betLow:
                        print("You lost your bet!")
                        uData["studsLost"] += abs(winnings)
                    elif winnings >= 0:
                        print(f"You won {winnings} studs!")
                        uData["studsGained"] += winnings
                    elif winnings <= 0:
                        print(f"You lost {abs(winnings)} studs!")
                        uData["studsLost"] += abs(winnings)
                    else:
                        print("This should be impossible. Cue the panic attacks.")
                else:
                    print("You don't have enough studs to bet that much.")
                sleep(5)
        case 3:
            print("TODO: Research Menu")
            sleep(1)
        case 4:
            print("TODO: Vehicle Shop")
            sleep(1)
        case 5:
            print("TODO: Rare Parts Shop")
            sleep(1)
        case 6:
            print("TODO: Energy Tank Shop")
            sleep(1)
        case 7:
            print("TODO: Resturant")
            sleep(1)
        case "E":
            exit(0)
        case "D":
            if uData["debug"]:
                deb = menu({"Dump User Data": 1, "Reset Studs": 2, "Full data reset": 3, "Exit": "E"}, "[DEBUG MENU]")
                match deb:
                    case 1:
                        print(f"User Data dump: {uData}")
                    case 2:
                        uData["studs"] = 20
                        uData["studsLost"] = 0
                        uData["studsGained"] = 0
                        uData["highestStuds"] = 20
                        print("Studs (and related stats) have been reset.")
                    case 3:
                        uData["studs"] = 20
                        uData["studsLost"] = 0
                        uData["studsGained"] = 0
                        uData["highestStuds"] = 20
                        uData["vehicles"] = {}
                        uData["energyTanks"] = 0
                        uData["logins"] = 0
                        uData["houseLevel"] = 0
                        uData["o"] = 0
                        print("User data has been reset.")
                    case "E":
                        print("SLEEP 5")
                    case _:
                        print("Firepup forgot to implement a debug menu option\nSLEEP 10")
                        sleep(5)
                sleep(5)
            else:
                print("Operation not permitted")
                sleep(5)
        case _:
            print("Invalid option, this should have been impossible.")
            sleep(60)
    clear()
    if uData["studs"] > uData["highestStuds"]:
        uData["highestStuds"] = uData["studs"]
    db.set(un, uData) # Update user data after each loop so it actually saves changes to the data
