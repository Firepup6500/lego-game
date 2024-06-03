from firepup650 import clear, randint, sql, e, menu, gp, gh, cur, flushPrint
import random as r
from fkeycapture import get, getnum, getchars
import os, time, sys, re
from time import sleep

db = sql("dev-database.db")

alphanum = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")

def multipleOf(num: int, mult: int = 5) -> bool:
    return num%mult == 0

cur.hide()
clear()
print("Loading Loge City v 0.0.1...")
sleep(1)
flushPrint("Checking system compatibility...")
sleep(1)
print(" \aOK.")
sleep(1)
flushPrint("Checking data...")
sleep(1)
print(" \aOK.")
sleep(1)
print("Loaded successfully")
print("Starting...")
sleep(2)
cur.show()
log = menu({"Yes": 1, "No": 0, "Exit": "E"}, "Welcome to the city!\nDo you have an existing account?")
clear()
un = ""
if log == "E":
    exit(0)
if log:
    print("Login")
    print("Username: ", end="")
    un = gp(5, alphanum, allowDelete=True)
    print("Password: ", end="")
    pw = gh(5, alphanum, allowDelete=True)
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
    print("Signup")
    print("Username (alphanumeric): ", end="")
    un = gp(5, alphanum, allowDelete=True)
    print("Password (alphanumeric):", end="")
    pw = gh(5, alphanum, allowDelete=True)
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
            print("Calculating avaliable bets, this shouldn't take long...")
            bets = {str(i): i for i in range(5, min(uData["studs"], 50000000), 5)}
            bets["Exit"] = "E"
            bet = menu(bets, "How many studs would you like to bet?")
            betHigh = 0 if type(bet) != int else bet*2
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
            price1 = 10 + (5 * uData["energyTanks"])
            price5 = 5 * price1
            price10 = 2 * price5
            count = menu({f"1 ({price1} studs)": 1, "5 ({price5} studs)": 5, "10 ({price10} studs)": 10}, "How many energy tanks do you want?")
            print("TODO: Energy Tank Shop Functionality")
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
                        print("User Data dump: {")
                        for k in uData:
                            print(f'    "{k}": {str(uData[k])}')
                        print("}")
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
