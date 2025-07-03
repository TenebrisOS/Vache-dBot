import requests
import json

with open ("config.json") as js:
    config=json.load(js)

api_server=config["API_SERVER"]

def GetPlayerBalance():
    pass
def GetAllItemPrices():
    pass
def GetContributionsLeaderboard():
    pass
def GetMoneyLeaderboard():
    pass