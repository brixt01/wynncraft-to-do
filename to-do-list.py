#import libraries
import requests
import json
import os

def makeJSON():
    # Get data from API
    requestedData = requests.get('https://api.wynncraft.com/v2/player/'+username+'/stats/').json()

    # Check if username exists
    if requestedData["data"] == []:
        return "null"
    else:
        # Set up dictionary
        global data
        data = {
            "metadata":{},
            "characters":[]
        }

        # Add metadata
        data["metadata"]["username"] = requestedData["data"][0]["username"]
        data["metadata"]["server"] = requestedData["data"][0]["meta"]["location"]["server"]
        data["metadata"]["playtime"] = int(requestedData["data"][0]["meta"]["playtime"]/12.76821773)
        data["metadata"]["rank"] =  requestedData["data"][0]["meta"]["tag"]["value"]

        firstJoin = requestedData["data"][0]["meta"]["firstJoin"][0:10:1].split("-")
        data["metadata"]["firstJoin"] = firstJoin[2]+"/"+firstJoin[1]+"/"+firstJoin[0]

        # Add class data
        for item in requestedData["data"][0]["classes"]:

            # Add indexes
            currentIndex = requestedData["data"][0]["classes"].index(item)
            data["characters"].append({"index":currentIndex})

            # Add class names
            className = item["name"]
            while className not in ["archer", "hunter", "warrior", "knight", "mage", "darkwizard", "assassin", "ninja", "shaman", "skyseer"]:
                className = className[:-1]
            data["characters"][currentIndex]["class"] = className

            # Add combat level
            data["characters"][currentIndex]["level"] = item["professions"]["combat"]["level"]

            # Add class metadata
            data["characters"][currentIndex]["metadata"] = {}
            data["characters"][currentIndex]["metadata"]["playtime"] = int(item["playtime"]/12.76821773)
            data["characters"][currentIndex]["metadata"]["deaths"] = item["deaths"]
            data["characters"][currentIndex]["metadata"]["logins"] = item["logins"]
            data["characters"][currentIndex]["metadata"]["gamemode"] = item["gamemode"]
            data["characters"][currentIndex]["metadata"]["mobsKilled"] = item["mobsKilled"]
            data["characters"][currentIndex]["metadata"]["blocksWalked"] = item["blocksWalked"]

            # Add levels
            data["characters"][currentIndex]["professions"] = []
            for profession in item["professions"]:
                if profession != "combat":
                    data["characters"][currentIndex]["professions"].append({"name": profession, "level" : item["professions"][profession]["level"]})

            # Add dungeons/raids
            data["characters"][currentIndex]["dungeons"] = item["dungeons"]["list"]
            data["characters"][currentIndex]["raids"] = item["raids"]["list"]

            # Add quests
            data["characters"][currentIndex]["quests"] = []
            for quest in item["quests"]["list"]:
                if quest.startswith("Mini-Quest") == False:
                    data["characters"][currentIndex]["quests"].append(quest)

            # Add mini-quests
            data["characters"][currentIndex]["miniQuests"] = []
            for miniQuest in item["quests"]["list"]:
                if miniQuest.startswith("Mini-Quest") == True:
                    data["characters"][currentIndex]["miniQuests"].append(miniQuest)

    # Return JSON
    return data

def choose():
    choice = input("\nWould you like to see information about: \n[1] Combat levels \n[2] Dungeons \n[3] Raids \n[4] Quests \n[5] Mini-quests \n[6] Professions \n[7] Print all data \n")
    if choice == "1":
        combatToDo()
    elif choice == "2":
        dungeonsToDo()
    elif choice == "3":
        raidsToDo()
    elif choice == "4":
        questsToDo()
    elif choice == "5":
        miniQuestsToDo()
    elif choice == "6":
        profsToDo()
    elif choice == "7":
        printAll()
    choose()

def printAll():
    print("\n", json.dumps(data, indent=4))

def combatToDo():
    print("\nCombat levels remaining to be completed for each class:")
    for item in data["characters"]:
        currentIndex = data["characters"].index(item)

        print("\n"+str(data["characters"][currentIndex]["index"]+1)+". "+data["characters"][currentIndex]["class"].capitalize(), "("+str(data["characters"][currentIndex]["level"])+")", "\n")
        print("Current level:", data["characters"][currentIndex]["level"])
        print("Levels remaining:", 106-data["characters"][currentIndex]["level"])

def dungeonsToDo():
    print("\nDungeons remaining to be completed for each class:")
    for item in data["characters"]:
        currentIndex = data["characters"].index(item)

        listOfDungeons = ["Decrepit Sewers", "Infested Pit", "Lost Sanctuary", "Underworld Crypt", "Sand-Swept Tomb", "Ice Barrows", "Undergrowth Ruins", "Galleon's Graveyard", "Corrupted Decrepit Sewers", "Corrupted Infested Pit", "Corrupted Lost Sanctuary", "Corrupted Underworld Crypt", "Corrupted Sand-Swept Tomb", "Corrupted Ice Barrows", "Fallen Factory", "Corrupted Undergrowth Ruins", "Eldritch Outlook"]
        dungeonsLeft = listOfDungeons.copy()
        for listDungeon in listOfDungeons:
            for JSONDungeon in data["characters"][currentIndex]["dungeons"]:#
                if listDungeon == JSONDungeon["name"]:
                    dungeonsLeft.remove(listDungeon)
        print("\n"+str(data["characters"][currentIndex]["index"]+1)+". "+data["characters"][currentIndex]["class"].capitalize(), "("+str(data["characters"][currentIndex]["level"])+")", "\n")
        if dungeonsLeft != []:
            for dungeon in dungeonsLeft:
                print("- ", dungeon)
        else:
            print("- None")

def raidsToDo():
    print("\nRaids remaining to be completed for each class:")
    for item in data["characters"]:
        currentIndex = data["characters"].index(item)

        listOfRaids = ["Nest of the Grootslangs", "The Canyon Colossus", "The Nameless Anomaly"]
        raidsLeft = listOfRaids.copy()
        for listRaid in listOfRaids:
            for JSONRaid in data["characters"][currentIndex]["raids"]:#
                if listRaid == JSONRaid["name"]:
                    raidsLeft.remove(listRaid)
        print("\n"+str(data["characters"][currentIndex]["index"]+1)+". "+data["characters"][currentIndex]["class"].capitalize(), "("+str(data["characters"][currentIndex]["level"])+")", "\n")
        if raidsLeft != []:
            for raid in raidsLeft:
                print("- ", raid)
        else:
            print("- None")

def questsToDo():
    print("\nQuests remaining to be completed for each class:")
    for item in data["characters"]:
        currentIndex = data["characters"].index(item)

        listOfQuests = ["A Hunter's Calling", 'Point of No Return', 'A Journey Further', 'A Journey Beyond', 'The Olmic Rune', 'The Hero of Gavel', 'One Thousand Meters Under', 'Dwarves and Doguns Part IV', 'Dwarves and Doguns Part III', 'The Feathers Fly Part II', 'Dwarves and Doguns Part II', 'Dwarves and Doguns Part I', 'The Feathers Fly Part I', 'Fantastic Voyage', 'The Envoy Part II', 'Enter the Dojo', 'The Hidden City', 'Beyond the Grave', 'Mixed Feelings', 'Desperate Metal', 'The Envoy Part I', 'From the Bottom', '???', 'The Qira Hive', 'Fallen Delivery', 'Realm of Light V - The Realm of Light', 'The Bigger Picture', 'Flight in Distress', "Aldorei's Secret Part I", 'Reincarnation', 'Acquiring Credentials', 'Murder Mystery', 'Troubled Tribesmen', 'Forbidden Prison', 'Lexdale Witch Trials', 'Realm of Light IV - Finding the Light', 'WynnExcavation Site D', 'Haven Antiquity', 'Shattered Minds', 'Grand Youth', 'Lazarus Pit', 'Temple of the Legends', 'Memory Paranoia', 'From the Mountains', 'Lost Soles', 'Lost Royalty', 'Realm of Light III - A Headless History', 'Out of my Mind', 'Lost in the Jungle', 'Realm of Light II - Taproot', "Redbeard's Booty", 'Reclaiming the House', 'Beneath the Depths', 'The Order of the Grook', 'An Iron Heart Part II', 'The Passage', 'Zhight Island', 'WynnExcavation Site C', 'The Shadow of the Beast', 'Realm of Light I - The Worm Holes', 'Master Piece', 'Death Whistle', 'Corrupted Betrayal', 'Jungle Fever', 'Crop Failure', 'The Maiden Tower', 'A Grave Mistake', 'The House of Twain', 'Rise of the Quartron', 'An Iron Heart Part I', 'Frost Bite', 'WynnExcavation Site B', "Bob's Lost Soul", 'Blazing Retribution', 'Underice', 'Fate of the Fallen', 'Star Thief', 'Heart of Llevigar', 'Ice Nations', 'Tower of Ascension', 'Clearing the Camps', "Pirate's Trove", 'Canyon Condor', 'Wrath of the Mummy', 'WynnExcavation Site A', 'Tribal Aggression', 'Kingdom of Sand', 'Meaningful Holiday', 'A Sandy Scandal', 'Green Gloop', 'Craftmas Chaos', 'The Mercenary', 'Misadventure on the Sea', 'Deja Vu', 'Lost Tower', 'The Corrupted Village', 'Recover the Past', 'The Dark Descent', 'Dwelling Walls', 'Cluck Cluck', 'Pit of the Dead', 'Studying the Corrupt', "Macabre Masquerade ''Hallowynn 2014''", 'Grave Digger', "Maltic's Well", 'Creeper Infiltration', "Arachnids' Ascent", 'Stable Story', 'Potion Making', 'Elemental Exercise', 'Mushroom Man', 'Underwater', 'Tunnel Trouble', 'The Sewers of Ragni', 'Infested Plants', 'Cook Assistant', 'Poisoning the Pest', "King's Recruit", "Enzan's Brother"]
        questsLeft = listOfQuests.copy()

        for listQuest in listOfQuests:
            for JSONQuest in data["characters"][currentIndex]["quests"]:#
                if listQuest == JSONQuest:
                    questsLeft.remove(listQuest)
        print("\n"+str(data["characters"][currentIndex]["index"]+1)+". "+data["characters"][currentIndex]["class"].capitalize(), "("+str(data["characters"][currentIndex]["level"])+")", "\n")
        if questsLeft != []:
            for quest in questsLeft:
                print("- ", quest)
        else:
            print("- None")

def miniQuestsToDo():
    print("\Mini-quests remaining to be completed for each class:")
    for item in data["characters"]:
        currentIndex = data["characters"].index(item)

        listOfMiniQuests = ['Mini-Quest - Slay Dragonlings', 'Mini-Quest - Slay Angels', 'Mini-Quest - Slay Conures', 'Mini-Quest - Slay Creatures of the Void', 'Mini-Quest - Slay Astrochelys Manis', 'Mini-Quest - Slay Ifrits', 'Mini-Quest - Slay Azers', 'Mini-Quest - Slay Frosted Guards & Cryostone Golems', 'Mini-Quest - Slay Magma Entities', 'Mini-Quest - Slay Pernix Monkeys', 'Mini-Quest - Slay Ailuropodas', 'Mini-Quest - Slay Robots', 'Mini-Quest - Slay Jinkos', 'Mini-Quest - Slay Hobgoblins', 'Mini-Quest - Slay Felrocs', 'Mini-Quest - Slay Myconids', 'Mini-Quest - Slay Dead Villagers', 'Mini-Quest - Slay Idols', 'Mini-Quest - Slay Wraiths & Phantasms', 'Mini-Quest - Slay Lizardmen', 'Mini-Quest - Slay Slimes', 'Mini-Quest - Slay Orcs', 'Mini-Quest - Slay Creatures of Nesaak Forest', 'Mini-Quest - Slay Coyotes', 'Mini-Quest - Slay Scarabs', 'Mini-Quest - Slay Skeletons', 'Mini-Quest - Slay Mooshrooms', 'Mini-Quest - Slay Spiders', 'Mini-Quest - Gather Copper', 'Mini-Quest - Gather Trout', 'Mini-Quest - Gather Koi', 'Mini-Quest - Gather Gylia Fish', 'Mini-Quest - Gather Gylia Fish II', 'Mini-Quest - Gather Kanderstone', 'Mini-Quest - Gather Kanderstone II', 'Mini-Quest - Gather Decay Roots', 'Mini-Quest - Gather Decay Roots II', 'Mini-Quest - Gather Gylia Fish III', 'Mini-Quest - Gather Kanderstone III', 'Mini-Quest - Gather Decay Roots III', 'Mini-Quest - Gather Diamonds', 'Mini-Quest - Gather Diamonds II', 'Mini-Quest - Gather Diamonds IV', 'Mini-Quest - Gather Rice', 'Mini-Quest - Gather Rice II', 'Mini-Quest - Gather Rice III', 'Mini-Quest - Gather Rice IV', 'Mini-Quest - Gather Bass III', 'Mini-Quest - Gather Bass II', 'Mini-Quest - Gather Bass IV', 'Mini-Quest - Gather Sorghum', 'Mini-Quest - Gather Sorghum II', 'Mini-Quest - Gather Sorghum III', 'Mini-Quest - Gather Sorghum IV', 'Mini-Quest - Gather Molten Eel', 'Mini-Quest - Gather Molten Eel II', 'Mini-Quest - Gather Molten Eel III', 'Mini-Quest - Gather Molten Eel IV', 'Mini-Quest - Gather Spruce Logs', 'Mini-Quest - Gather Spruce Logs II', 'Mini-Quest - Gather Jungle Logs', 'Mini-Quest - Gather Jungle Logs II', 'Mini-Quest - Gather Dark Logs', 'Mini-Quest - Gather Dark Logs II', 'Mini-Quest - Gather Gudgeon', 'Mini-Quest - Gather Oak Logs', 'Mini-Quest - Gather Wheat', 'Mini-Quest - Gather Barley', 'Mini-Quest - Gather Birch Logs', 'Mini-Quest - Gather Granite', 'Mini-Quest - Gather Willow Logs', 'Mini-Quest - Gather Salmon', 'Mini-Quest - Gather Salmon II', 'Mini-Quest - Gather Willow Logs II', 'Mini-Quest - Gather Gold', 'Mini-Quest - Gather Gold II', 'Mini-Quest - Gather Oats II', 'Mini-Quest - Gather Acacia Logs', 'Mini-Quest - Gather Malt', 'Mini-Quest - Gather Sandstone II', 'Mini-Quest - Gather Carp', 'Mini-Quest - Gather Sandstone', 'Mini-Quest - Gather Acacia Logs II', 'Mini-Quest - Gather Carp II', 'Mini-Quest - Gather Malt II', 'Mini-Quest - Gather Icefish', 'Mini-Quest - Gather Iron II', 'Mini-Quest - Gather Molten Ore II', 'Mini-Quest - Gather Molten Ore', 'Mini-Quest - Gather Molten Ore IV', 'Mini-Quest - Gather Molten Ore III', 'Mini-Quest - Gather Iron', 'Mini-Quest - Gather Icefish II', 'Mini-Quest - Gather Oats', 'Mini-Quest - Gather Hops', 'Mini-Quest - Gather Hops II', 'Mini-Quest - Gather Silver', 'Mini-Quest - Gather Rye', 'Mini-Quest - Gather Rye II', 'Mini-Quest - Gather Millet', 'Mini-Quest - Gather Cobalt II', 'Mini-Quest - Gather Millet II', 'Mini-Quest - Gather Millet III', 'Mini-Quest - Gather Koi III', 'Mini-Quest - Gather Bass', 'Mini-Quest - Gather Diamonds III', 'Mini-Quest - Gather Silver II', 'Mini-Quest - Gather Cobalt III', 'Mini-Quest - Gather Piranhas', 'Mini-Quest - Gather Cobalt', 'Mini-Quest - Gather Koi II', 'Mini-Quest - Gather Piranhas II', 'Mini-Quest - Gather Light Logs', 'Mini-Quest - Gather Dark Logs III', 'Mini-Quest - Gather Light Logs II', 'Mini-Quest - Gather Light Logs III', 'Mini-Quest - Gather Pine Logs', 'Mini-Quest - Gather Pine Logs II', 'Mini-Quest - Gather Pine Logs III', 'Mini-Quest - Gather Bamboo', 'Mini-Quest - Gather Avo Logs', 'Mini-Quest - Gather Avo Logs II', 'Mini-Quest - Gather Avo Logs III', 'Mini-Quest - Gather Avo Logs IV']
        miniQuestsLeft = listOfMiniQuests.copy()

        for listMiniQuest in listOfMiniQuests:
            for JSONMiniQuest in data["characters"][currentIndex]["miniQuests"]:#
                if listMiniQuest == JSONMiniQuest:
                    miniQuestsLeft.remove(listMiniQuest)
        print("\n"+str(data["characters"][currentIndex]["index"]+1)+". "+data["characters"][currentIndex]["class"].capitalize(), "("+str(data["characters"][currentIndex]["level"])+")", "\n")
        if miniQuestsLeft != []:
            for miniQuest in miniQuestsLeft:
                print("- ", miniQuest)
        else:
            print("- None")

def profsToDo():
    print("\nProfession levels remaining to be completed for each class:")
    for item in data["characters"]:
        currentIndex = data["characters"].index(item)

        print("\n"+str(data["characters"][currentIndex]["index"]+1)+". "+data["characters"][currentIndex]["class"].capitalize(), "("+str(data["characters"][currentIndex]["level"])+")", "\n")
        for profession in data["characters"][currentIndex]["professions"]:
            if profession["level"] < 100:
                print(profession["name"].capitalize()+":", profession["level"], "("+str(100-profession["level"])+" left)")
            else:
                print(profession["name"].capitalize()+":", profession["level"])

##########                                           MAIN                                              ##########
username = input("This program will display information about the progress remaining for a wynncraft player \nto reach completion on all classes. \n\nPlease enter a username: ")
makeJSON()
print(data["characters"][0]["miniQuests"])
choose()
