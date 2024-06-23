from firepup650 import clear, randint, sql, e, menu, gp, gh, cur, flushPrint, randint
import random as r
from fkeycapture import get, getnum, getchars
import os, time, sys, re
from time import sleep

db = sql("dev-database.db")

alphanum = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")


def multipleOf(num: int, mult: int = 5) -> bool:
    return num % mult == 0


# Function from https://stackoverflow.com/a/2556252, merged with https://stackoverflow.com/a/59082116
def rreplace(s: str, old: str, new: str, occurrence: int) -> str:
    return new.join(s.rsplit(old, occurence))


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
log = menu(
    {"Yes": 1, "No": 0, "Exit": "E"},
    "Welcome to the city!\nDo you have an existing account?",
)
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
                "o": 0,  # I have no clue what this is supposed to be, doesn't seem to be used in the original doc?
                "racScore": 0,
                "richScore": 0,
                "rare": {},
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
    go = menu(
        {
            "Stats": 1,
            "Gamble": 2,
            "Research": 3,
            "Vehicle Shop": 4,
            "Rare Parts Shop": 5,
            "Energy Tank Shop": 6,
            "Resturant": 7,
            "Fix my save data": 8,
            "[DEBUG]": "D",
            "Exit": "E",
        },
        "What would you like to do?",
    )
    clear()
    match go:
        case 1:
            rares = ""
            for item in uData["rare"]:
                if rares:
                    rares = f"{rares}, {uData['rare'][item]} {item}{'s' if uData['rare'][item] > 1 else ''}"
                else:
                    rares = f"{uData['rare'][item]} {item}{'s' if uData['rare'][item] > 1 else ''}"
            rares = rreplace(rares, ", ", ", and", 1)
            print(
                f"""Stats:
 Studs:
  Current:          {uData["studs"]}
  All-time Highest: {uData["highestStuds"]}
  All-time Losses:  {uData["studsLost"]}
  All-time Gains:   {uData["studsGained"]}
 Vehicles:          {rreplace(", ".join(uData["vehicles"]), ", ", ", and", 1) if uData["vehicles"] else "None"}
 Rare Items:        {rares if rares else "None"}
 House Level:       {uData["houseLevel"]}
 Energy Tanks:      {uData["energyTanks"]}
 Misc:
  Raccoon Score:    {uData["racScore"]}
  Rich:             {uData["richScore"]}"""
            )
            if uData["debug"] or uData["permissionLevel"] >= 50:
                print(
                    f"""Debug Stats:
 Bebug bit:         {uData["debug"]}
 Permission Level:  {uData["permissionLevel"]}
 Idk what o is:     {uData["o"]}"""
                )
            print("Press any key to exit")
            get()
        case 2:
            print("Calculating avaliable bets, this shouldn't take long...")
            bets = {str(i): i for i in range(5, min(uData["studs"], 50000000), 5)}
            bets["Exit"] = "E"
            bets["5"] = 5  # Bugfix: menu crashes if you have 0 studs
            bet = menu(bets, "How many studs would you like to bet?")
            betHigh = 0 if type(bet) != int else bet
            winnings = 0
            betLow = -2 * bet if betHigh else 0
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
            sel = menu(
                {
                    "A bike (20 studs)": 20,
                    "A 4-wheeler (50 studs)": 50,
                    "An old rusty little car (100 studs)": 100,
                    "A car (200 studs)": 200,
                    "A minivan (500 studs)": 500,
                    "A van (750 studs)": 750,
                    "A truck (1k studs)": 1000,
                    "A food truck (2k studs)": 2000,
                    "A semi-truck (5k studs)": 5000,
                    "A hover bike (10k studs)": 10000,
                    "A hover car (20k studs)": 20000,
                    "A hover truck (50k studs)": 50000,
                    "A hover semi-truck (100k studs)": 100000,
                    "A pod racer (500k studs)": 500000,
                    "A rocketship (1m studs)": 1000000,
                    "A spaceship (5m studs)": 5000000,
                    "A spaceship with a hyperdrive (10m studs)": 10000000,
                    "A yacht (50m studs)": 50000000,
                    "A space yacht (100m studs)": 100000000,
                    "A teleporter (1b studs)": 1000000000,
                    "Exit": "E",
                },
                "Welcome to the Vehicle Shop, please make a selection",
            )
            match sel:  # Bugfix: Accidentally inverted the check for owning a vehicle
                case 20:
                    if sel <= uData["studs"] and "bike" not in uData["vehicles"]:
                        uData["vehicles"].append("bike")
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        print("You purchased a bike!")
                    elif "bike" in uData["vehicles"]:
                        print("Sorry, you already have a bike!")
                    else:
                        print("You're too poor to buy a bike.")
                case 50:
                    if sel <= uData["studs"] and "4-wheeler" not in uData["vehicles"]:
                        uData["vehicles"].append("4-wheeler")
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        print("You purchased a 4-wheeler!")
                    elif "4-wheeler" in uData["vehicles"]:
                        print("Sorry, you already have a 4-wheeler!")
                    else:
                        print("You're too poor to buy a 4-wheeler.")
                case 100:
                    if (
                        sel <= uData["studs"]
                        and "old rusty car" not in uData["vehicles"]
                    ):
                        uData["vehicles"].append("old rusty car")
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        print("You purchased an old rusty car!")
                    elif "old rusty car" in uData["vehicles"]:
                        print("Sorry, you already have an old rusty car!")
                    else:
                        print("You're too poor to buy an old rusty car.")
                case 200:
                    if sel <= uData["studs"] and "car" not in uData["vehicles"]:
                        uData["vehicles"].append("car")
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        print("You purchased a car!")
                    elif "car" in uData["vehicles"]:
                        print("Sorry, you already have a car!")
                    else:
                        print("You're too poor to buy a car.")
                case 500:
                    if sel <= uData["studs"] and "minivan" not in uData["vehicles"]:
                        uData["vehicles"].append("minivan")
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        print("You purchased a minivan!")
                    elif "minivan" in uData["vehicles"]:
                        print("Sorry, you already have a minivan!")
                    else:
                        print("You're too poor to buy a minivan.")
                case 750:
                    if sel <= uData["studs"] and "van" not in uData["vehicles"]:
                        uData["vehicles"].append("van")
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        print("You purchased a van!")
                    elif "van" in uData["vehicles"]:
                        print("Sorry, you already have a van!")
                    else:
                        print("You're too poor to buy a van.")
                case 1000:
                    if sel <= uData["studs"] and "truck" not in uData["vehicles"]:
                        uData["vehicles"].append("truck")
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        print("You purchased a truck!")
                    elif "truck" in uData["vehicles"]:
                        print("Sorry, you already have a truck!")
                    else:
                        print("You're too poor to buy a truck.")
                case 2000:
                    if sel <= uData["studs"] and "food truck" not in uData["vehicles"]:
                        uData["vehicles"].append("food truck")
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        print("You purchased a food truck!")
                    elif "food truck" in uData["vehicles"]:
                        print("Sorry, you already have a food truck!")
                    else:
                        print("You're too poor to buy a food truck.")
                case 5000:
                    if sel <= uData["studs"] and "semi-truck" not in uData["vehicles"]:
                        uData["vehicles"].append("semi-truck")
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        print("You purchased a semi-truck!")
                    elif "semi-truck" in uData["vehicles"]:
                        print("Sorry, you already have a semi-truck!")
                    else:
                        print("You're too poor to buy a semi-truck.")
                case 10000:
                    if (
                        sel <= uData["studs"]
                        and "hover bike" not in uData["vehicles"]
                    ):
                        uData["vehicles"].append("hover bike")
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        print("You purchased a hover bike!")
                    elif "hover bike" in uData["vehicles"]:
                        print("Sorry, you already have a hover bike!")
                    else:
                        print("You're too poor to buy a hover bike.")
                case 20000:
                    if sel <= uData["studs"] and "hover car" not in uData["vehicles"]:
                        uData["vehicles"].append("hover car")
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        print("You purchased a hover car!")
                    elif "hover car" in uData["vehicles"]:
                        print("Sorry, you already have a hover car!")
                    else:
                        print("You're too poor to buy a hover car.")
                case 50000:
                    if (
                        sel <= uData["studs"]
                        and "hover truck" not in uData["vehicles"]
                    ):
                        uData["vehicles"].append("hover truck")
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        print("You purchased a hover truck!")
                    elif "hover truck" in uData["vehicles"]:
                        print("Sorry, you already have a hover truck!")
                    else:
                        print("You're too poor to buy a hover truck.")
                case 100000:
                    if (
                        sel <= uData["studs"]
                        and "hover semi-truck" not in uData["vehicles"]
                    ):
                        uData["vehicles"].append("hover semi-truck")
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        print("You purchased a hover semi-truck!")
                    elif "hover semi-truck" in uData["vehicles"]:
                        print("Sorry, you already have a hover semi-truck!")
                    else:
                        print("You're too poor to buy a hover semi-truck.")
                case 500000:
                    if (
                        sel <= uData["studs"]
                        and "pod racer" not in uData["vehicles"]
                    ):
                        uData["vehicles"].append("pod racer")
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        print("You purchased a pod racer!")
                    elif "pod racer" in uData["vehicles"]:
                        print("Sorry, you already have a pod racer!")
                    else:
                        print("You're too poor to buy a pod racer.")
                case 1000000:
                    if (
                        sel <= uData["studs"]
                        and "rocketship" not in uData["vehicles"]
                    ):
                        uData["vehicles"].append("rocketship")
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        print("You purchased a rocketship!")
                    elif "rocketship" in uData["vehicles"]:
                        print("Sorry, you already have a rocketship!")
                    else:
                        print("You're too poor to buy a rocketship.")
                case 5000000:
                    if (
                        sel <= uData["studs"]
                        and "spaceship" not in uData["vehicles"]
                    ):
                        uData["vehicles"].append("spaceship")
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        print("You purchased a spaceship!")
                    elif "spaceship" in uData["vehicles"]:
                        print("Sorry, you already have a spaceship!")
                    else:
                        print("You're too poor to buy a spaceship.")
                case 10000000:
                    if (
                        sel <= uData["studs"]
                        and "spaceship with a hyperdrive" not in uData["vehicles"]
                    ):
                        uData["vehicles"].append("spaceship with a hyperdrive")
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        print("You purchased a spaceship with a hyperdrive!")
                    elif "spaceship with a hyperdrive" in uData["vehicles"]:
                        print("Sorry, you already have a spaceship with a hyperdrive!")
                    else:
                        print("You're too poor to buy a spaceship with a hyperdrive.")
                case 50000000:
                    if sel <= uData["studs"] and "yacht" not in uData["vehicles"]:
                        uData["vehicles"].append("yacht")
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        print("You purchased a yacht!")
                    elif "yacht" in uData["vehicles"]:
                        print("Sorry, you already have a yacht!")
                    else:
                        print("You're too poor to buy a yacht.")
                case 100000000:
                    if (
                        sel <= uData["studs"]
                        and "space yacht" not in uData["vehicles"]
                    ):
                        uData["vehicles"].append("space yacht")
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        print("You purchased a space yacht!")
                    elif "space yacht" in uData["vehicles"]:
                        print("Sorry, you already have a space yacht!")
                    else:
                        print("You're too poor to buy a space yacht.")
                case 1000000000:
                    if (
                        sel <= uData["studs"]
                        and "teleporter" not in uData["vehicles"]
                    ):
                        uData["vehicles"].append("teleporter")
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        print("You purchased a teleporter!")
                    elif "teleporter" in uData["vehicles"]:
                        print("Sorry, you already have a teleporter!")
                    else:
                        print("You're too poor to buy a teleporter.")
                case "E":
                    pass
                case _:
                    print("Firepup forgot to add a menu option, smh")
                    sleep(2)
            sleep(2)
        case 5:
            # Each item in this menu grants 1 more rich than the previous item
            sel = menu(
                {
                    "Gold bar (250 studs)": 250,
                    "Golden cup (500 studs)": 500,
                    "Golden plate (1k studs)": 1000,
                    "Golden table (5k studs)": 5000,
                    "Crystal (250k studs)": 250000,
                    "Crystal cup (500k studs)": 500000,
                    "Crystal plate (1m studs)": 1000000,
                    "Crystal table (5m studs)": 5000000,
                    "Double studded 1x1 plate (10m studs)": 10000000,
                    "Double studded 2x2 plate (50m studs)": 50000000,
                    "Hinge joint (100m studs)": 100000000,
                    "Vault door (500m studs)": 500000000,
                    "Exit": "E",
                },
                "What rare items do you want to buy today?",
            )
            match sel:
                case 250:
                    if sel <= uData["studs"]:
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        uData["rich"] += 1
                        if "gold bar" in uData["rare"]:
                            uData["rare"]["gold bar"] += 1
                        else:
                            uData["rare"]["gold bar"] = 1
                        print("You bought a gold bar!")
                    else:
                        print("You're too poor to buy a gold bar.")
                case 500:
                    if sel <= uData["studs"]:
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        uData["rich"] += 2
                        if "golden cup" in uData["rare"]:
                            uData["rare"]["golden cup"] += 1
                        else:
                            uData["rare"]["golden cup"] = 1
                        print("You bought a golden cup!")
                    else:
                        print("You're too poor to buy a golden cup.")
                case 1000:
                    if sel <= uData["studs"]:
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        uData["rich"] += 3
                        if "golden plate" in uData["rare"]:
                            uData["rare"]["golden plate"] += 1
                        else:
                            uData["rare"]["golden plate"] = 1
                        print("You bought a golden plate!")
                    else:
                        print("You're too poor to buy a golden plate.")
                case 5000:
                    if sel <= uData["studs"]:
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        uData["rich"] += 4
                        if "golden table" in uData["rare"]:
                            uData["rare"]["golden table"] += 1
                        else:
                            uData["rare"]["golden table"] = 1
                        print("You bought a golden table!")
                    else:
                        print("You're too poor to buy a golden table.")
                case 250000:
                    if sel <= uData["studs"]:
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        uData["rich"] += 5
                        if "crystal" in uData["rare"]:
                            uData["rare"]["crystal"] += 1
                        else:
                            uData["rare"]["crystal"] = 1
                        print("You bought a crystal!")
                    else:
                        print("You're too poor to buy a crystal.")
                case 500000:
                    if sel <= uData["studs"]:
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        uData["rich"] += 6
                        if "crystal cup" in uData["rare"]:
                            uData["rare"]["crystal cup"] += 1
                        else:
                            uData["rare"]["crystal cup"] = 1
                        print("You bought a crystal cup!")
                    else:
                        print("You're too poor to buy a crystal cup.")
                case 1000000:
                    if sel <= uData["studs"]:
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        uData["rich"] += 7
                        if "crystal plate" in uData["rare"]:
                            uData["rare"]["crystal plate"] += 1
                        else:
                            uData["rare"]["crystal plate"] = 1
                        print("You bought a crystal plate!")
                    else:
                        print("You're too poor to buy a crystal plate.")
                case 5000000:
                    if sel <= uData["studs"]:
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        uData["rich"] += 8
                        if "crystal table" in uData["rare"]:
                            uData["rare"]["crystal table"] += 1
                        else:
                            uData["rare"]["crystal table"] = 1
                        print("You bought a crystal table!")
                    else:
                        print("You're too poor to buy a crystal table.")
                case 10000000:
                    if sel <= uData["studs"]:
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        uData["rich"] += 9
                        if "double studded 1x1 plate" in uData["rare"]:
                            uData["rare"]["double studded 1x1 plate"] += 1
                        else:
                            uData["rare"]["double studded 1x1 plate"] = 1
                        print("You bought a double studded 1x1 plate!")
                    else:
                        print("You're too poor to buy a double studded 1x1 plate.")
                case 50000000:
                    if sel <= uData["studs"]:
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        uData["rich"] += 10
                        if "double studded 2x2 plate" in uData["rare"]:
                            uData["rare"]["double studded 2x2 plate"] += 1
                        else:
                            uData["rare"]["double studded 2x2 plate"] = 1
                        print("You bought a double studded 2x2 plate!")
                    else:
                        print("You're too poor to buy a double studded 2x2 plate.")
                case 100000000:
                    if sel <= uData["studs"]:
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        uData["rich"] += 11
                        if "hinge joint" in uData["rare"]:
                            uData["rare"]["hinge joint"] += 1
                        else:
                            uData["rare"]["hinge joint"] = 1
                        print("You bought a hinge joint!")
                    else:
                        print("You're too poor to buy a hinge joint.")
                case 500000000:
                    if sel <= uData["studs"]:
                        uData["studs"] -= sel
                        uData["studsLost"] += sel
                        uData["rich"] += 12
                        if "vault door" in uData["rare"]:
                            uData["rare"]["vault door"] += 1
                        else:
                            uData["rare"]["vault door"] = 1
                        print("You bought a vault door!")
                    else:
                        print("You're too poor to buy a vault door.")
                case "E":
                    pass
                case _:
                    print("Firepup forgot to add a menu option, smh")
                    sleep(2)
            sleep(2)
        case 6:
            price1 = 10 + (5 * uData["energyTanks"])
            price5 = 0
            for i in range(5):
                price5 += 10 + (5 * (uData["energyTanks"] + i))
                print(price5)
            price10 = 0
            for i in range(10):
                price10 += 10 + (5 * (uData["energyTanks"] + i))
            count = menu(
                {
                    f"1 ({price1} studs)": 1,
                    f"5 ({price5} studs)": 5,
                    f"10 ({price10} studs)": 10,
                    "Exit": "E",
                },
                "How many energy tanks do you want?",
            )
            match count:
                case 1:
                    if price1 <= uData["studs"]:
                        uData["studs"] -= price1
                        uData["studsLost"] += price1
                        uData["energyTanks"] += 1
                        print("You bought a single energy tank!")
                    else:
                        print("You're too poor to buy a single energy tank.")
                    sleep(2)
                case 5:
                    if price5 <= uData["studs"]:
                        uData["studs"] -= price5
                        uData["studsLost"] += price5
                        uData["energyTanks"] += 5
                        print("You bought 5 energy tanks!")
                    else:
                        print("You're too poor to buy 5 energy tanks.")
                    sleep(2)
                case 10:
                    if price10 <= uData["studs"]:
                        uData["studs"] -= price10
                        uData["studsLost"] += price10
                        uData["energyTanks"] += 10
                        print("You bought 10 energy tanks!")
                    else:
                        print("You're too poor to buy 10 energy tanks.")
                    sleep(2)
                case "E":
                    pass
                case _:
                    print("Firepup forgot to add a menu option, smh.")
                    sleep(2)
        case 7:
            sel = menu(
                {
                    "Pizza (5 studs)": 1,
                    "Drink (10 studs)": 2,
                    "Box of Tacos (20 studs)": 3,
                    "Box of doughnuts (50 studs)": 4,
                    "Trash (What are you, a raccoon? We're not even supposed to sell this...) (200 studs)": 5,
                    "Money (Excuse me?) (500 studs)": 6,
                    "Oh actually I don't want to eat anything I just want to waste money (1000 studs)": 7,
                    "Pure gold pizza (5000 studs)": 8,
                    "Liquid Gold (10000 studs)": 9,
                    "Box of golden tacos (20000 studs)": 10,
                    "Box of golden doughnuts (50000 studs)": 11,
                    "Golden trash (I... why do we even sell this.) (200000 studs)": 12,
                    "5 cubic meters of gold (...You know there's better uses of your money right?) (500000 studs)": 13,
                    "I REALLY want to waste money (1 million studs)": 14,
                    "Exit": 0,
                },
                "What would you like to order?",
            )
            thing, price, message, weird = ("Nothing", 0, "You bought nothing", True)
            match sel:
                case 1:
                    thing, price, message, weird = ("a pizza", 5, "delicious!", False)
                case 2:
                    match randint(0, 9):
                        case 0:
                            thing = "a can of strawberry fanta"
                        case 1:
                            thing = "a can of liquid death"
                        case 2:
                            thing = "a can of water"
                        case 3:
                            thing = "a can of generic soda"
                        case 4:
                            thing = 'a can of "fresh spring" water'
                        case 5:
                            thing = "a paper cup of tap water"
                        case 6:
                            thing = "a can of motor oil"
                        case 7:
                            thing = "a can of rehyderated water"
                        case 8:
                            thing = "a can of blueberry"
                        case 9:
                            thing = "a can of rain water"
                    price, message, weird = (
                        10,
                        "tastes just like you remember it!",
                        False,
                    )
                case 3:
                    thing, price, message, weird = (
                        "a box of tacos",
                        20,
                        "there was a good amount of variety in that!",
                        False,
                    )
                case 4:
                    thing, price, message, weird = (
                        "a box of doughnuts",
                        50,
                        "you can tell you're gonna reget all that sugar later.",
                        False,
                    )
                case 5:
                    thing, price, message, weird = (
                        "  trash",
                        200,
                        (
                            "You... eat the trash? (+1 raccoon score)"
                            if uData["racScore"] < 10
                            else "You eagerly consume the trash pile! (+1 raccoon score)"
                        ),
                        True,
                    )
                    uData["racScore"] += 1
                case 6:
                    thing, price, message, weird = (
                        "  money",
                        500,
                        "You literally just eat money. Disgusting.",
                        True,
                    )
                case 7:
                    thing, price, message, weird = (
                        'a "tip"',
                        1000,
                        'You just give the cashier 1000 studs as a "tip". (+1 rich)',
                        True,
                    )
                    uData["richScore"] += 1
                case 8:
                    thing, price, message, weird = (
                        "a golden pizza",
                        5000,
                        "You add the golden pizza to your home. You can't eat it after all. (+1 rich)",
                        True,
                    )
                    uData["richScore"] += 1
                case 9:
                    thing, price, message, weird = (
                        "liquid gold",
                        10000,
                        "You chug the liquid gold. You are in severe pain for at least 20 minutes. (+1 rich)",
                        True,
                    )
                    uData["richScore"] += 1
                case 10:
                    thing, price, message, weird = (
                        "golden tacos",
                        20000,
                        "You add the golden tacos to your home. The box was too poor for them. (+1 rich)",
                        True,
                    )
                    uData["richScore"] += 1
                case 11:
                    thing, price, message, weird = (
                        "golden doughnuts",
                        50000,
                        "You add the golden doughtnuts to your home. Very sophisticated! (+1 rich)",
                        True,
                    )
                    uData["richScore"] += 1
                case 12:
                    thing, price, message, weird = (
                        "golden trash",
                        200000,
                        (
                            "You... eat... GOLDEN TRASH. What is worng with you? (+1 rich, +1 raccoon)"
                            if uData["racScore"] < 10
                            else "You eagerly consume the golden trash pile! (+1 rich, +1 raccoon)"
                        ),
                        True,
                    )
                    uData["richScore"] += 1
                    uData["racScore"] += 1
                case 13:
                    thing, price, message, weird = (
                        "5 cubic meters of gold",
                        500000,
                        "You EAT 5 cubic meters of gold. I don't even know how you managed that. (+5 rich)",
                        True,
                    )
                    uData["richScore"] += 5
                case 14:
                    thing, price, message, weird = (
                        'a hefty "tip"',
                        1000000,
                        'You "tip" the cashier a million studs. That\'s just not a tip man. (+5 rich)',
                        True,
                    )
                case "E":
                    pass
                case _:
                    print("Firepup forgot to add a menu option, smh.")
                    sleep(5)
            if price > 0 and price <= uData["studs"]:
                uData["studs"] -= price
                uData["studsLost"] += price
                if not weird:
                    print(
                        f"You {'eat' if sel!=2 else 'drink'} your {thing[2:]}... {message}"
                    )
                else:
                    print(message)
            elif price > 0:
                print(f"You're too poor to buy {thing} right now.")
            sleep(2)
        case 8:
            migrations = {
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
                "o": 0,
                "racScore": 0,
                "richScore": 0,
                "rare": {}
            }
            fixed = False
            for key in migrations:
                if key not in uData:
                    fixed = True
                    print(
                        f'Found missing save data key "{key}"! Resetting to default value...'
                    )
                    uData[key] = migrations[key]
            print(
                "Your save data has been fixed!"
                if fixed
                else "There was nothing I could find that was wrong with your save data!"
            )
            sleep(2)
        case "E":
            exit(0)
        case "D":
            if uData["debug"]:
                deb = menu(
                    {
                        "Dump User Data": 1,
                        "Reset Studs": 2,
                        "Full data reset": 3,
                        "Exit": "E",
                    },
                    "[DEBUG MENU]",
                )
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
                        uData["racScore"] = 0
                        uData["richScore"] = 0
                        print("User data has been reset.")
                    case "E":
                        print("SLEEP 5")
                    case _:
                        print(
                            "Firepup forgot to implement a debug menu option\nSLEEP 10"
                        )
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
    db.set(
        un, uData
    )  # Update user data after each loop so it actually saves changes to the data
