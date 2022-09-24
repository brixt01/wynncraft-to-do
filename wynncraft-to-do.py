#import libraries
import requests
import json

#get the data
username = "brixt01"
data = requests.get('https://api.wynncraft.com/v2/player/'+username+'/stats/').json()

print(json.dumps(data, indent=4))
