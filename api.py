import requests
import json

with open ("config.json") as js:
    config=json.load(js)

api_server=config["API_SERVER"]
api_key=config["API_KEY"]

def GetPlayerBalance(user):
    return 0
def GetAllItemPrices():
    pass
def GetContributionsLeaderboard():
    pass
def GetMoneyLeaderboard():
    pass