from flask import Flask, request
from threading import Thread
import os
from pymongo import MongoClient

def currencyRead(bot, key, subkey):
    if bot == True:
        return {"_id": str(key), "balance": 50.0, "bowls": [{"id": 0, "inside": None, "attractsleft": 0}], "parrots": [],"inventory": [], "lastdaily": 0, "xp": 0, "level": 0, "notifs": [], "ach": [], "reactiongames": 0, "swears": 0}[str(subkey)]
    else:
        if len(list(db["currency"].find({"_id" : str(key)}).hint("_id_").limit(1))) == 0:
            return {"_id": str(key), "balance": 50.0, "bowls": [{"id": 0, "inside": None, "attractsleft": 0}], "parrots": [],"inventory": [], "lastdaily": 0, "xp": 0, "level": 0, "notifs": [], "ach": [], "reactiongames": 0, "swears": 0}[str(subkey)]
        else:
            doc = list(db["currency"].find({"_id" : str(key)}))[0]
            if not "swears" in doc.keys():
                doc["swears"] = 0
                db["currency"].update_one({"_id": str(key)}, {"$set": doc})
        return list(db["currency"].find({"_id" : str(key)}).hint("_id_").limit(1))[0][str(subkey)]

def currencyWrite(bot, key, subkey, value):
    if bot == False:
        if len(list(db["currency"].find({"_id" : str(key)}).hint("_id_").limit(1))) == 0:
            db["currency"].insert_one({"_id": str(key), "balance": 50.0, "bowls": [{"id": 0, "inside": None, "attractsleft": 0}], "parrots": [],"inventory": [], "lastdaily": 0, "xp": 0, "level": 0, "notifs": [], "ach": [], "reactiongames": 0, "swears": 0})
        else:
            doc = list(db["currency"].find({"_id" : str(key)}).hint("_id_").limit(1))[0]
            if not "swears" in doc.keys():
                doc["swears"] = 0
                db["currency"].update_one({"_id": str(key)}, {"$set": doc})
    d = list(db["currency"].find({"_id" : str(key)}).hint("_id_").limit(1))[0]
    
    if str(subkey) == "parrots":
        value = sorted(value, key=lambda k: k["name"])
    d[str(subkey)] = value
    db["currency"].update_one({"_id" : str(key)}, {"$set": d})

CONSTR = os.getenv("CONSTR")
if not CONSTR:
    CONSTR = input("Constr: ")
TOPGG = os.getenv("TOPGG")
if not TOPGG:
    TOPGG = input("Topgg: ")
DBL = os.getenv("DBL")
if not DBL:
    DBL = input("DBL: ")

app = Flask('')
mcl = MongoClient(CONSTR)
db = mcl["v192"]

@app.route('/', methods=['GET'])
def main():
    return "Your bot is alive!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

@app.route('/', methods=['POST', 'OPTIONS'])
def result():
    if request.headers["Authorization"] == "i am hangre i et hotdog (dbl)":
        currencyWrite(False, request.json["id"], "balance",   currencyRead(False, request.json["id"], "balance") + 50)
        print("vote (dbl)")
        return "received"
    elif request.headers["Authorization"] == "i am hangre i et hotdog (bfd)":
        currencyWrite(False, request.json["user"], "balance",   currencyRead(False, request.json["user"], "balance") + 50)
        print("vote (bfd)")
        return "received"


