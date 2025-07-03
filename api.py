import requests
import json

with open ("config.json") as js:
    config=json.load(js)

api_server=config["API_SERVER"]

def GetPlayerBalance(user):
    response = requests.get(("http://"+api_server+"/api/player/" + user + "/balance"))
    player_data = json.loads(response.text)
    return player_data['balance']

def GetAllItemPrices():
    response = requests.get(("http://"+api_server+"/api/economy/prices"))
    items = json.loads(response.text)
    clean_items = {
        name: {"sell": data["sellPrice"], "buy": data["buyPrice"]}
        for name, data in items.items()
    }
    return clean_items

def GetContributionsLeaderboard():
    response = requests.get(("http://"+api_server+"/api/leaderboard/contributions"))
    players_js = json.loads(response.text)
    players = {
        p["playerName"]: {"rank": int(p["rank"]), "score": int(p["score"])}
        for p in players_js
    }
    return players

def GetMoneyLeaderboard():
    response = requests.get(("http://"+api_server+"/api/leaderboard/money"))
    lb_money = json.loads(response.text)
    players = {
        p["playerName"]: {"rank": int(p["rank"]), "score": int(p["score"])}
        for p in lb_money
    }
    return players

#print(GetPlayerBalance("daiflu"))
#print(GetAllItemPrices()["GUNPOWDER"]["sell"])
#print(GetContributionsLeaderboard()["ohet29"])
#print(GetMoneyLeaderboard()["ohet29"])
