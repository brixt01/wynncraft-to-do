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
            data["characters"][currentIndex]["professions"] = {}
            for profession in item["professions"]:
                if profession != "combat":
                    data["characters"][currentIndex]["professions"][profession] = item["professions"][profession]["level"]

            # Add dungeons/raids/quets
            data["characters"][currentIndex]["dungeons"] = item["dungeons"]["list"]
            data["characters"][currentIndex]["raids"] = item["raids"]["list"]
            data["characters"][currentIndex]["quests"] = item["quests"]["list"]

    # Return JSON
    return data

def choose():
    choice = input("\nWould you like to see information about: \n[1] Dungeons \n")
    if choice == "1":
        dungeonsToDo()
    choose()

def dungeonsToDo():
    print("\nDungeons remaining to be completed for each class:")
    # Dungeons
    for item in data["characters"]:
        currentIndex = data["characters"].index(item)

        listOfDungeons = ["Decrepit Sewers", "Infested Pit", "Lost Sanctuary", "Underworld Crypt", "Sand-Swept Tomb", "Ice Barrows", "Undergrowth Ruins", "Galleon's Graveyard", "Corrupted Decrepit Sewers", "Corrupted Infested Pit", "Corrupted Lost Sanctuary", "Corrupted Underworld Crypt", "Corrupted Sand-Swept Tomb", "Corrupted Ice Barrows", "Fallen Factory", "Corrupted Undergrowth Ruins", "Eldritch Outlook"]
        dungeonsLeft = ["Decrepit Sewers", "Infested Pit", "Lost Sanctuary", "Underworld Crypt", "Sand-Swept Tomb", "Ice Barrows", "Undergrowth Ruins", "Galleon's Graveyard", "Corrupted Decrepit Sewers", "Corrupted Infested Pit", "Corrupted Lost Sanctuary", "Corrupted Underworld Crypt", "Corrupted Sand-Swept Tomb", "Corrupted Ice Barrows", "Fallen Factory", "Corrupted Undergrowth Ruins", "Eldritch Outlook"]
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



##########                                           MAIN                                              ##########
username = input("This program will display information about the progress remaining for a wynncraft player \nto reach completion on all classes. \n\nPlease enter a username: ")
makeJSON()
choose()
