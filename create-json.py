#import libraries
import requests
import json
import os

# Get username and request data
username = input("This program with create a JSON file on your desktop containing the data for a wynncraft player. \nPlease enter a username: ")
requestedData = requests.get('https://api.wynncraft.com/v2/player/'+username+'/stats/').json()

# Check if username exists
if requestedData["data"] == []:
    print(f"Unknown username. '{username}.json' unsuccessfully created. ")
else:
    # Set up dictionary
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

    # Create file on desktop
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    try:
        # File does not already exist, so creating file on desktop
        with open(f"{desktop}\\{username}.json", "x") as f:
            f.write(str(json.dumps(data, indent=4)))
        print(f"'{username}.json' successfully created. ")
    except FileExistsError:
        while True:
            # File already exists
            choice = input(f"The file '{username}.json' already exists. Would you like to overwrite it? [y/n]: ")
            # Overwrite file
            if choice == "y":
                with open(f"{desktop}\\{username}.json", "w") as f:
                    f.write(str(json.dumps(data, indent=4)))
                print(f"'{username}.json' successfully overwritten. ")
                break
            # Don't overwrite file
            elif choice == "n":
                print(f"'{username}.json' unsuccessfully created. ")
                break
