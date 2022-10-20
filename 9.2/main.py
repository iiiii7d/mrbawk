# Mr Bawk - v1.9.2 (9/6/20) by i____7d
VERSION = "v1.9.2 (9/6/20)"

#v1.0 - 24/3/20 - Added repeating function, info page
#v1.0.1 - 26/3/20 - Added help pages, added :parrot: to every dialogue. Commands can now be in lowercase.
#v1.1 - 26/3/20 - Added swearing detection, muting function. Now detects if message has embeds during repeating.
#v1.2 - 27/3/20 - Added lists for members repeated, detected for swearing, or muted. Also added a function to view messages deleted from muting. Added pinging.
#v1.3 - 28/3/20 - Added changelog. All lists to repeat/detectswear/mute are now in a json file. Multiple server support.
#v1.3.1 - 28/3/20 - in lists, names are no longer all lowercase. All instances of "player" is replaced with "member". :P
#v1.3.2 - 28/3/20 - fixed small bug where members could not be repeated/detected for swearing/muted due to lowercase and stuff
#v1.3.3 - 28/3/20 - fixed small bug where members could start their messages wth "parrot" to countervent mute
#v1.4 - 29/3/20 - All regional indicator emojis are now treated as ordinary characters, Employed profanity-check to strengthen swearing detection filter, Invite Link command, 'parrot list muted' is now 'parrot list mute', 'parrot list' now shows all 3 lists instead of nothing. Added settings, so swear alarm and mutelog are both now editable. Parrot masters can now stoprepeat/stopdetectswear/unmute everyone. The role is now "Parrot Master" instead of "Parrot's Master". Initinfo command.
#v1.4.1 - 29/3/20 - Fixed small bug where the swear alarm would stay as default when someone swears
#v1.4.2 - 30/3/20 - Security patch
#v1.5 - 31/3/20 - Added honking, and i____7d is always master, no matter the role. 2 new preferences: nvchannel and dsmba. The version is now a constant variable, so there's no need to change numebrs all around the code. Added quoting. Added newserverannouncing. Mutelog is renamed deletelog.
#v1.5.1 - 1/4/20 - Fixed bug in quoting
#v1.5.2 - 1/4/20 - Fixed bug in quoting
#v1.5.3 - 9/4/20 - Honking is now only for a specific server, due to abuse
#v1.6 - 11/4/20 - When repeating a message with an emebd inside of it, the parrot no longer sends a '!!!' message before sending the 'oi embeds are trash' message. All instances of 'MemberNicks' are replaced with 'MemberNames'. 'parrot quote' is now 'parrot q'. The additional list of swear words is now editable in a preference. Use of .env to store token, so it won't be stuck at the input.
#v1.6.1 - 14/4/20 - Parrot ping now shows latency.
#1.7 - 18/4/20 - Another value to ping. Messup command. Parrot now reacts when pinged. Currency system. Initinfo is removed. Raise command, for testing try/except. Bot now has a custom status.
#1.8 - 20/4/20 - Quotes can only be added if the person is not the person who said the quote. Quotes can now be removed by the person who said it (or me) and can be marked as offensive as well. More efficient announcing system. In memberlists, the id is now stored instead of the name. In addswearwords, one must now end the swear word with ';'. Parrots can now only farm twigs if the user is online. nvchannel is nw annchannel. added parrot myserver.
#1.8.1 - 20/4/20 - Parrots will no longer only collect twigs when the person is online. Reimplemented the pixel limit.
#1.8.2 - 21/4/20 - Bug fix for parrot messup and opening files. New parrot and food.
#1.9 - 22/4/20 - Parrot raise is now removed. Aliases: changelog -> cl; repeat -> re; stoprepeat -> sre; detectswear -> ds; stopdetectswear -> sds,  New additions to parrot c: enc, top, rename. Placefood has a new alias: pf. You can now have multiple bowls, and buy multiple of the same item at once. There is now xp and levelling, and each level gives you a multiplier for attracting parrots. New parrot naming system (random instead of ascending). Achievements. Some new parrots. and foods.
#1.9.1 - 24/4/20 - Drivers for json files. Garbage collection.
#1.9.2 - 9/6/20 - Switched some json files to mongodb. Added uptime, eval, announce command.

import time
initstart = int(round(time.time() * 1000))
import joblib
import discord
import re
import keep_alive
import os
import sys
import json
import random
import requests
import datetime
import asyncio
import math
import numpy
import traceback
import gc
import psutil
from pymongo import MongoClient
from better_profanity import profanity
from threading import Thread
from io import BytesIO
from PIL import Image

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    TOKEN = input("Token: ")

CONSTR = os.getenv("CONSTR")
if not CONSTR:
    CONSTR = input("Constr: ")

mcl = MongoClient(CONSTR)
db = mcl["v110"]

client = discord.Client()
#gc.set_threshold(10, 10, 10)
SwearAlarmDefault = ":parrot: **BAAAAAAAAAAWWWWWWKKKKKKK BAAAAAWWWWWWWKKKKKKK ALERRRRRRT! {author} SWORE! BAAAAAAAAAWWWWWKKKKKK BAAAAAAAAAAAAAAAAAWWWWWWWWWWWWWKKKKKKKKKKKKK!!!!!!!!!! :rotating_light: :rotating_light: :rotating_light:**"
AddSwearWordsDefault = [" no u ", " no you ", " ok boomer ", " swear word ", " stfu ", " fk "]

async def checks(message):
    if not message.guild.id in newServerAnnounceRead():
            newServerAnnounceAppend(message.guild.id)
            try:
                await message.guild.create_role(name="Parrot Master")
                #await message.channel.send(":parrot: **Oh hello! You seem to be the first person to try my commands.**\nIn fact, this is a :warning: **VERY IMPORTANT** :warning: message, at least for admins. If you're not an admin, go get one as soon as possible.\n**If you're an admin: ** Hi! I need some initialisation, do `parrot initinfo`. Thanks :)")
            except:
                await message.channel.send(":parrot: Oops, looks like I don't have permissions to create a role!")

        #request = {"request": "r", "new": None}
        #code = len(memberlistsQueue)
        #memberlistsQueue.append(request)
        #while memberlistsQueue[code] == request:
        #    pass
        #f = memberlistsQueue[code]
        #subkey = str(message.guild.id)
        #if not subkey in f["toRepeat"]:
        #    f["toRepeat"][subkey] = []
        #if not subkey in f["toDetectSwear"]:
        #    f["toDetectSwear"][subkey] = []
        #if not subkey in f["toMute"]:
        #    f["toMute"][subkey] = []
        #memberlistsQueue.append({"request": "w", "new": f})
    if len(list(db["memberlists"].find({"_id" : str(message.guild.id)}))) == 0:
        db["memberlists"].insert_one({"_id": str(message.guild.id), "toRepeat": [], "toDetectSwear": [], "toMute": []})

    #request = {"request": "r", "new": None}
    #code = len(preferencesQueue)
    #preferencesQueue.append(request)
    #while preferencesQueue[code] == request:
    #    pass
    #f = preferencesQueue[code]
    #key = str(message.guild.id)
    #preferencesChange = False
    #if not key in f:
    #    f[key] = {}
    #    preferencesChange = True
    #if not "deletelog" in f[key]:
    #    f[key]["deletelog"] = None
    #    preferencesChange = True
    #if not "swearalarm" in f[key]:
    #    f[key]["swearalarm"] = SwearAlarmDefault
    #    preferencesChange = True
    #if not "annchannel" in f[key]:
    #    f[key]["annchannel"] = None
    #    preferencesChange = True
    #if not "dsmba" in f[key]:
    #    f[key]["dsmba"] = False
    #    preferencesChange = True
    #if not "addswearwords" in f[key]:
    #    f[key]["addswearwords"] = AddSwearWordsDefault
    #    preferencesChange = True
    #if not "currencychannels" in f[key]:
    #    f[key]["currencychannels"] = []
    #    preferencesChange = True
    #if preferencesChange == True:
    #    preferencesQueue.append({"request": "w", "new": f})
    preferencesChange = False
    if len(list(db["preferences"].find({"_id" : str(message.guild.id)}))) == 0:
        db["preferences"].insert_one({"_id": str(message.guild.id), "deletelog": None, "swearalarm": SwearAlarmDefault, "annchannel": None, "dsmba": False, "addswearwords": AddSwearWordsDefault, "currencychannels": []})
        preferencesChange = True

    if message.author.bot == False:
        #request = {"request": "r", "new": None}
        #code = len(currencyQueue)
        #currencyQueue.append(request)
        #while currencyQueue[code] == request:
        #    pass
        #f = currencyQueue[code]
        #key = str(message.author.id)
        #if not key in f:
        #    f[key] = {}
        #if not "balance" in f[key]:
        #    f[key]["balance"] = 50.0
        #if not "bowls" in f[key]:
        #    f[key]["bowls"] = [{"id": 0, "inside": None, "attractsleft": 0}]
        #if not "parrots" in f[key]:
        #    f[key]["parrots"] = []
        #if not "inventory" in f[key]:
        #    f[key]["inventory"] = []
        #if not "lastdaily" in f[key]:
        #    f[key]["lastdaily"] = 0
        #if not "xp" in f[key]:
        #    f[key]["xp"] = 0
        #if not "level" in f[key]:
        #    f[key]["level"] = 0
        #if not "notifs" in f[key]:
        #    f[key]["notifs"] = []
        #if not "ach" in f[key]:
        #    f[key]["ach"] = []
        #currencyQueue.append({"request": "w", "new": f})
        if len(list(db["currency"].find({"_id" : str(message.author.id)}))) == 0:
            db["currency"].insert_one({"_id": str(message.author.id), "balance": 50.0, "bowls": [{"id": 0, "inside": None, "attractsleft": 0}], "parrots": [],"inventory": [], "lastdaily": 0, "xp": 0, "level": 0, "notifs": [], "ach": []})

async def messUp(message):
    messupStart = int(round(time.time() * 1000))
    url = None
    try:
        url = message.attachments[0].url
    except IndexError: 
        url = message.content.replace("parrot messup ", "")
    distorted = None
    for ext in ['.jpg','.png']:
        if url.endswith(ext):
            distorted = await distort(url, message)

            #i = BytesIO(r.content)
    #async with aiohttp.ClientSession() as session:
    #    async with session.get(url) as resp:
    #        if resp.status != 200:
    #            return await message.channel.send('Could not download file...')
    #        i = BytesIO(await resp.read())

    if url == None or distorted == None:
        await message.channel.send(":parrot: Either you did not attach something, or the link is invalid/not an image!")
        return

    diff = (int(round(time.time() * 1000)) - messupStart)

    mention = "<@" + str(message.author.id) + ">"
    await message.channel.send(":parrot: " + mention + " **I took " + msToTime(diff) + " to produce this, aren't you impressed?**" ,file=discord.File(distorted, filename="messy.jpg"))
    if diff >= 7200000:
        ach(message.author, 1)
    return

async def distort(url, message):
    r = requests.get(url)
    i = Image.open(BytesIO(r.content))
    ig = Image.new(i.mode, i.size)
    pmap = i.load()
    pnew = ig.load()
    pvals = []
    size = ig.size[0] * ig.size[1]

    await message.channel.send(":parrot: **Please note that this will take a while, so you will be pinged when it's done, bawk!**\n**Number of Pixels: " + str(size) + "**")
    if size > 1000000:
        await message.channel.send(":parrot: **Sorry, your image is going to have to be compressed!**")
        maxsize = (1000, 1000)
        i = Image.open(BytesIO(r.content))
        i.thumbnail(maxsize, Image.ANTIALIAS)
        ig = Image.new(i.mode, i.size)
        pmap = i.load()
        pnew = ig.load()
        pvals = []
        size = ig.size[0] * ig.size[1]
                

    await message.channel.send(":parrot: **Studying! Bawk!**")
    for x in range(ig.size[0]):
        for y in range(ig.size[1]):
            pvals.append(pmap[x, y])

    s = int(round(time.time() * 1000))
    t = 0
    m = await message.channel.send(":parrot: **Messy! Messy! (0 pixels scrambled, ? left)**")
    for x in range(ig.size[0]):
        for y in range(ig.size[1]):
            pnew[x, y] = random.choice(pvals)
            pvals.remove(pnew[x, y])
            await asyncio.sleep(0.001)
            t += 1
            if t == 100:
                timeLeft = round(((int(round(time.time() * 1000)) - s) / t * (size - t)), 2)
                now = datetime.datetime.now()
                etc = (now + datetime.timedelta(milliseconds=timeLeft)).strftime("%H:%M:%S")
                await m.edit(content=":parrot: **Messy! Messy! (" + str(round(t / size * 100)) + "% scrambled, " + msToTime(timeLeft) + " left)**\n**Check back at " + str(etc) + " GMT!**")
            print(t)
        if x % 5 == 0 or x == 0:
            timeLeft = round(((int(round(time.time() * 1000)) - s) / t * (size - t)), 2)
            now = datetime.datetime.now()
            etc = (now + datetime.timedelta(milliseconds=timeLeft)).strftime("%H:%M:%S")
            try:
                await m.edit(content=":parrot: **Messy! Messy! (" + str(round(t / size * 100)) + "% scrambled, " + msToTime(timeLeft) + " left)**\n**Check back at " + str(etc) + " GMT!**")
            except:
                pass
    try:
        await m.edit(content=":parrot: **Messy! Messy! (COMPLETED)**")
    except:
        pass
    i.close()
    b = BytesIO()
    ig.save(b, format='PNG')
    b = b.getvalue()
    return BytesIO(b)

def msToTime(ms):
    s = math.floor(ms / 1000)
    ms = round(ms % 1000, 2)
    m = math.floor(s / 60)
    s = s % 60
    h = math.floor(m / 60)
    m = m % 60
    d = math.floor(h / 24)
    h = h % 24
    res = ""
    if d != 0:
        res = res + str(d) + "d "
    if h != 0:
        res = res + str(h) + "h "
    if m != 0:
        res = res + str(m) + "min "
    if s != 0:
        res = res + str(s) + "s "
    if ms != 0:
        res = res + str(ms) + "ms "
    return res.strip()

def fullnameify(user):
    return user.name + "#" + user.discriminator

def dividefullname(fullname):
    brokendown = fullname.split("#")
    return [brokendown[0], brokendown[1]]

#memberlistsQueue = [] #{"request": "r", "new": None}
def memberlistsRead(category, server):
    return list(db["memberlists"].find({"_id" : str(server)}))[0][str(category)]
    #request = {"request": "r", "new": None}
    #code = len(memberlistsQueue)
    #memberlistsQueue.append(request)
    #while memberlistsQueue[code] == request:
    #    pass
    #data = memberlistsQueue[code]
    #return data[str(key)][str(subkey)]

def memberlistsAppend(category, server, value):
    if len(list(db["memberlists"].find({"_id" : str(server)}))) == 0:
        db["memberlists"].insert_one({"_id": str(server), "toRepeat": [], "toDetectSwear": [], "toMute": []})

    d = list(db["memberlists"].find({"_id" : str(server)}))[0]
    d[str(category)].append(value)
    db["memberlists"].update_one({"_id" : str(server)}, {"$set": d})
    #request = {"request": "r", "new": None}
    #code = len(memberlistsQueue)
    #memberlistsQueue.append(request)
    #while memberlistsQueue[code] == request:
    #    pass
    #data = memberlistsQueue[code]
    #data[str(key)][str(subkey)].append(value)
    #memberlistsQueue.append({"request": "w", "new": data})
    
def memberlistsPop(category, server, index):
    if list(db["memberlists"].find({"_id" : str(server)})) == 0:
        db["memberlists"].insert_one({"_id": str(server), "toRepeat": [], "toDetectSwear": [], "toMute": []})

    d = list(db["memberlists"].find({"_id" : str(server)}))[0]
    d[str(category)].pop(index)
    db["memberlists"].update_one({"_id" : str(server)}, {"$set": d})
    #request = {"request": "r", "new": None}
    #code = len(memberlistsQueue)
    #memberlistsQueue.append(request)
    #while memberlistsQueue[code] == request:
    #    pass
    #data = memberlistsQueue[code]
    #data[str(key)][str(subkey)].pop(index)
    #memberlistsQueue.append({"request": "w", "new": data})

#async def memberlistsDriver():
#    cursor = 0
#    while not client.is_closed():
#        if len(memberlistsQueue) > cursor:
#            #gc.collect()
#            with open(os.path.join(sys.path[0], "memberlists.json"), "r+") as f: 
#                try:
#                    data = json.load(f)
#                    request = memberlistsQueue[cursor]
#                    if request["request"] == "r":
#                        memberlistsQueue[cursor] = data
#                    elif request["request"] == "w": 
#                        f.seek(0)
#                        f.truncate()
#                        json.dump(request["new"], f, indent=4)
#                    cursor += 1
#                except:
#                    print(traceback.format_exc())
#                    cursor += 1
#            f.close()

#preferencesQueue = [] #{"request": "r", "new": None}
def preferencesRead(server, pref):
    return list(db["preferences"].find({"_id" : str(server)}))[0][str(pref)]

def preferencesWrite(server, pref, value):
    if len(list(db["preferences"].find({"_id" : str(server)}))) == 0:
        db["preferences"].insert_one({"_id": str(server)})

    d = list(db["preferences"].find({"_id" : str(server)}))[0]
    d[str(pref)] = value
    db["preferences"].update_one({"_id" : str(server)}, {"$set": d})

#async def preferencesDriver():
#    cursor = 0
#    while not client.is_closed():
#        if len(preferencesQueue) > cursor:
#            #gc.collect()
#            with open(os.path.join(sys.path[0], "preferences.json"), "r+") as f: 
#                try:        
#                    data = json.load(f)
#                    request = preferencesQueue[cursor]
#                    if request["request"] == "r":
#                        preferencesQueue[cursor] = data
#                    elif request["request"] == "w": 
#                        f.seek(0)
#                        f.truncate()
#                        json.dump(request["new"], f, indent=4)
#                    cursor += 1
#                except:
#                    print(traceback.format_exc())
#                    cursor += 1
#            f.close()

def announcementRead(mode):
    with open(os.path.join(sys.path[0], "announcement.json"), "r") as f:
        data = json.load(f)
        f.close()
        if mode == "announced":
            return data["announced"]
        else:
            return data["message"]

def announcementAppend(value):
    with open(os.path.join(sys.path[0], "announcement.json"), "r+") as f:
        d = json.load(f)
        d["announced"].append(value)
        f.seek(0)
        f.truncate()
        json.dump(d, f, indent=4)
        f.close()

def newServerAnnounceRead():
    with open(os.path.join(sys.path[0], "newserverannounce.json"), "r") as f:
        while os.stat("newserverannounce.json").st_size == 0:
            pass
        data = json.load(f)
        f.close()
        return data["init"]

def newServerAnnounceAppend(value):
    with open(os.path.join(sys.path[0], "newserverannounce.json"), "r+") as f:
        while os.stat("newserverannounce.json").st_size == 0:
            pass
        d = json.load(f)
        d["init"].append(value)
        f.seek(0)
        f.truncate()
        json.dump(d, f, indent=4)
        f.close()

#quotesQueue = [] #{"request": "r", "new": None}
def quotesAdd(member, quote):
    if len(list(db["quotes"].find({"_id" : str(fullnameify(member))}))) == 0:
        db["quotes"].insert_one({"_id": str(fullnameify(member)), "quotes": []})

    d = list(db["quotes"].find({"_id" : str(fullnameify(member))}))[0]
    d["quotes"].append(quote)
    db["quotes"].update_one({"_id" : str(fullnameify(member))}, {"$set": d})
#    request = {"request": "r", "new": None}
#    code = len(quotesQueue)
#    quotesQueue.append(request)
#    while quotesQueue[code] == request:
#        pass
#    data = quotesQueue[code]
#    if not fullnameify(member) in data:
#        data[fullnameify(member)] = []
#    data[fullnameify(member)].append(quote)
#    quotesQueue.append({"request": "w", "new": data})

def quotesView(memberfullname):
    data = list(db["quotes"].find({}))
    #request = {"request": "r", "new": None}
    #code = len(quotesQueue)
    #quotesQueue.append(request)
    #while quotesQueue[code] == request:
    #    pass
    #data = quotesQueue[code]
    member = ""
    if memberfullname == "anyone":
        member = random.choice([e["_id"] for e in data])
        memberindex = [e["_id"] for e in data].index(member)
        return [dividefullname(member)[0], data[memberindex]["quotes"]]
    elif memberfullname in [e["_id"] for e in data]:
        member = memberfullname
        memberindex = [e["_id"] for e in data].index(member)
        return [dividefullname(member)[0], data[memberindex]["quotes"]]
    else:
        return "nope"

def quotesRemove(quoteid, offensive, deleter):
    d = list(db["quotes"].find())
    for z in range(0, len(d)):
        for x in range(0, len(d[z]["quotes"])):
            if d[z]["quotes"][x]["id"] == int(quoteid) and (fullnameify(deleter) == z or deleter.id == 644052617500164097):
                if offensive:
                    offensiveAdd(z, d[z]["quotes"][x]["quote"])
                theid = d[z]["quotes"][x]["id"]
                del d[z]["quotes"][x]
                db["quotes"].update_one({"_id" : theid}, {"$set": d[z]})
                #quotesQueue.append({"request": "w", "new": d})
                return "yes"
            elif not (fullnameify(deleter) == z or deleter.id == 644052617500164097):
                return "notyou"
    return "no"

    #request = {"request": "r", "new": None}
    #code = len(quotesQueue)
    #quotesQueue.append(request)
    #while quotesQueue[code] == request:
    #    pass
    #d = quotesQueue[code]
    #for z in d.keys():
    #    for x in range(0, len(d[z])):
    #        if d[z][x]["id"] == int(quoteid) and (fullnameify(deleter) == z or deleter.id == 644052617500164097):
    #            if offensive:
    #                offensiveAdd(z, d[z][x]["quote"])
    #            del d[z][x]
    #            quotesQueue.append({"request": "w", "new": d})
    #            return "yes"
    #        elif not (fullnameify(deleter) == z or deleter.id == 644052617500164097):
    #            return "notyou"
    #return "no"

#async def quotesDriver():
#    cursor = 0
#    while not client.is_closed():
#        if len(quotesQueue) > cursor:
#            #gc.collect()
#            with open(os.path.join(sys.path[0], "quotes.json"), "r+") as f: 
#                try:
#                    data = json.load(f)
#                    request = quotesQueue[cursor]
#                    if request["request"] == "r":
#                        quotesQueue[cursor] = data
#                    elif request["request"] == "w": 
#                        f.seek(0)
#                        f.truncate()
#                        json.dump(request["new"], f, indent=4)
#                    cursor += 1
#                except:
#                    print(traceback.format_exc())
#                    cursor += 1
#            f.close()

#offensiveQueue = []
def offensiveAdd(member, offensive):
    if len(list(db["quotesoffensive"].find({"_id" : member}))) == 0:
        db["quotesoffensive"].insert_one({"_id": member, "offensive": []})

    d = list(db["quotesoffensive"].find({"_id" : member}))[0]
    d["offensive"].append(offensive)
    db["quotesoffensive"].update_one({"_id" : member}, {"$set": d})
    #request = {"request": "r", "new": None}
    #code = len(offensiveQueue)
    #offensiveQueue.append(request)
    #while offensiveQueue[code] == request:
    #    pass
    #d = offensiveQueue[code]
    #if not member in d:
    #    d[member] = []
    #d[member].append(offensive)
    #offensiveQueue.append({"request": "w", "new": d})

def offensiveView(memberfullname):
    #request = {"request": "r", "new": None}
    #code = len(offensiveQueue)
    #offensiveQueue.append(request)
    #while offensiveQueue[code] == request:
    #    pass
    #d = offensiveQueue[code]
    try:
        return list(db["quotesoffensive"].find({"_id" : memberfullname}))[0]["offensive"]
    except:
        return []
    #if not memberfullname in d:
    #    return []
    #else:
    #    return d[memberfullname]

#async def offensiveDriver():
#    cursor = 0
#    while not client.is_closed():
#        if len(offensiveQueue) > cursor:
#            #gc.collect()
#            with open(os.path.join(sys.path[0], "quotesoffensive.json"), "r+") as f: 
#                try:
#                    data = json.load(f)
#                    request = offensiveQueue[cursor]
#                    if request["request"] == "r":
#                        offensiveQueue[cursor] = data
#                    elif request["request"] == "w": 
#                        f.seek(0)
#                        f.truncate()
#                        json.dump(request["new"], f, indent=4)
#                    cursor += 1
#                except:
#                    print(traceback.format_exc())
#                    cursor += 1
#            f.close()

def quoteCount():
    with open(os.path.join(sys.path[0], "quotescount.json"), "r") as f:
        while os.stat("quotescount.json").st_size == 0:
            pass
        d = json.load(f)
        f.close()
        return d["count"]

def upQuoteCount():
    with open(os.path.join(sys.path[0], "quotescount.json"), "r+") as f:
        while os.stat("quotescount.json").st_size == 0:
            pass
        d = json.load(f)
        d["count"] += 1
        f.seek(0)
        f.truncate()
        json.dump(d, f, indent=4)
        f.close()

#currencyQueue = []
def currencyRead(key, subkey):
    #request = {"request": "r", "new": None}
    #code = len(currencyQueue)
    #currencyQueue.append(request)
    #while currencyQueue[code] == request:
    #    pass
    #data = currencyQueue[code]
    #return data[str(key)][str(subkey)]
    return list(db["currency"].find({"_id" : str(key)}))[0][str(subkey)]

def currencyWrite(key, subkey, value):
    #request = {"request": "r", "new": None}
    #code = len(currencyQueue)
    #currencyQueue.append(request)
    #while currencyQueue[code] == request:
    #    pass
    #d = currencyQueue[code]
    if len(list(db["currency"].find({"_id" : str(key)}))) == 0:
        db["currency"].insert_one({"_id": str(key)})

    d = list(db["currency"].find({"_id" : str(key)}))[0]
    
    if str(subkey) == "parrots":
        value = sorted(value, key=lambda k: k["name"])
    d[str(subkey)] = value
    db["currency"].update_one({"_id" : str(key)}, {"$set": d})
    #currencyQueue.append({"request": "w", "new": d})

#async def currencyDriver():
#    cursor = 0
#    ready = True
#    prevError = ""
#    while not client.is_closed():
#        #gc.collect()
#        if len(currencyQueue) > cursor:
#            with open(os.path.join(sys.path[0], "currency.json"), "r+") as f: 
#                try:   
#                    data = json.load(f)
#                    request = currencyQueue[cursor]
#                    if request["request"] == "r":
#                        while not ready:
#                            pass
#                        currencyQueue[cursor] = data
#                    elif request["request"] == "w": 
#                        f.seek(0)
#                        f.truncate()
#                        ready = False
#                        json.dump(request["new"], f, indent=4)
#                        ready = True
#                    cursor += 1
#                except:
#                    print(traceback.format_exc())
#                    if traceback.format_exc() == prevError:
#                        shutil.copyfile("b_currency.json", "currency.json")
#                    prevError = traceback.format_exc()
#                    cursor += 1
#            f.close()

def currstatsRead(key):
    with open(os.path.join(sys.path[0], "currstats.json"), "r") as f:
        data = json.load(f)
        f.close()
        return data[str(key)]

def upXPSilent(userid, xpAdd):
    currencyWrite(userid, "xp", currencyRead(userid, "xp") + xpAdd)

async def upXP(message, xpAdd):
    currencyWrite(message.author.id, "xp", currencyRead(message.author.id, "xp") + xpAdd)
    if currencyRead(message.author.id, "xp") >= 100:
        levelsUp = 0
        while currencyRead(message.author.id, "xp") >= 100:
            currencyWrite(message.author.id, "xp", currencyRead(message.author.id, "xp") - 100)
            currencyWrite(message.author.id, "level", currencyRead(message.author.id, "level") + 1)
            levelsUp += 1

        if message.author.nick == None:
            nick = message.author.name
        else:
            nick = message.author.nick
        
        await message.channel.send(":parrot: **Congrats, " + nick + ", you have levelled up from level " + str(currencyRead(message.author.id, "level")-levelsUp) + " to level " + str(currencyRead(message.author.id, "level")) + "!**")

def ach(user, ID):
    oldachs = currencyRead(user.id, "ach")
    if not ID in oldachs:
        oldachs.append(ID)
        currencyWrite(user.id, "ach", oldachs)

@client.event
async def on_message(message):
    try:
        start = int(round(time.time() * 1000))
        if message.author == client.user:
            return
        
        await client.loop.create_task(checks(message))

        message.content.replace(":regional_indicator_a:", "A").replace(":regional_indicator_b:", "B").replace(":regional_indicator_c:", "C").replace(":regional_indicator_d:", "D").replace(":regional_indicator_e:", "E").replace(":regional_indicator_f:", "F").replace(":regional_indicator_g:", "G").replace(":regional_indicator_h:", "H").replace(":regional_indicator_i:", "I").replace(":regional_indicator_j:", "J").replace(":regional_indicator_k:", "K").replace(":regional_indicator_l:", "L").replace(":regional_indicator_m:", "M").replace(":regional_indicator_n:", "N").replace(":regional_indicator_o:", "O").replace(":regional_indicator_p:", "P").replace(":regional_indicator_q:", "Q").replace(":regional_indicator_r:", "R").replace(":regional_indicator_s:", "S").replace(":regional_indicator_t:", "T").replace(":regional_indicator_u:", "U").replace(":regional_indicator_v:", "V").replace(":regional_indicator_w:", "W").replace(":regional_indicator_x:", "X").replace(":regional_indicator_y:", "Y").replace(":regional_indicator_z:", "Z")

        members = message.guild.members
        memberNames = [o.name.lower() for o in members]
        memberNamesUCase = [o.name for o in members]
        msgLCase = message.content.lower()

        if msgLCase.startswith('parrot') and len(msgLCase.split(" ")) > 1 and msgLCase.split(" ")[1] in ["info", "help", "changelog", "cl", "ping", "list", "repeat", "re", "stoprepeat", "sre", "detectswear", "ds", "stopdetectswear", "sds", "mute", "unmute", "inviteme", "myserver", "s", "honk", "q", "c", "messup", "achievements", "ach", "uptime", "eval", "announce"] and message.author.bot == False:
            command = msgLCase.split(" ")

            memberNicks = []
            for h in members:
                if h.nick == None:
                    memberNicks.append(h.name.lower())
                else:
                    memberNicks.append(h.nick.lower())
            
            if currencyRead(message.author.id, "notifs") != []:
                string = ":parrot: **Since your last used my commands, you attracted: " + "".join([(str(p["qty"]) + " " + p["breed"] + "s, ") for p in currencyRead(message.author.id, "notifs")])
                string = string[:-2] + "**"
                await message.channel.send(string)
                currencyWrite(message.author.id, "notifs", [])

            if command[1] == "info":
                await message.channel.send(""":parrot: **Bawk! Hello! I'm Mr Bawk, the Parrot!**\nI was created by i\_\_\_\_7d, my ultimate master!\nThis is """ + VERSION + """.
If you want to suggest a new feature, just contact i\_\_\_\_7d.
I'm also in """ + str(len(client.guilds)) + """ different servers!
My pfp is from Unsplash.\nThat's all for now, bawk!""")

            elif command[1] == "help":
                if msgLCase == "parrot help master":
                    await message.channel.send(""":parrot: **Master commands - Sometimes masters need help as well!**\nAll my commands start with `parrot`.
Note for parameters: <> means mandatory, [] means optional.
**s ...** Parrot settings and preferences. Type `parrot s` for more info.
**re/repeat <nickname>** Repeats whatever someone says. Very annoying!
**sre/stoprepeat <nickname>** Stops repeating someone. Put '\*' in the <nickname> slot to stop repeating everyone.
**ds/detectswear <nickname>** Detects swearing, and sounds a text alarm when someone does.
**sds/stopdetectswear <nickname>** Stops detecting someone for swearing. Put '\*' in the <nickname> slot to stop detecting everyone.
**mute <nickname>** Talks over what someone says in chat.
**unmute <nickname>** Stops talking over someone. Put '\*' in the <nickname> slot to unmute everyone.""")
                else:
                    await message.channel.send(""":parrot: **You need help? Here ya go!**\nAll my commands start with `parrot`.
Note for parameters: <> means mandatory, [] means optional.
**help [master]** Loads this page. (Append "master" for Parrot Masters' commands, __that can only be used if you have the automatically-created Parrot Master role.__)
**info** View bot info.
**list [repeat(re)/detectswear(ds)/mute]** See who is repeated/detected for swearing/muted. Append nothing for a list of everything.
**ping** Connection test
**uptime** View uptime.
**cl/changelog** View the new additions in this update, and what to look forward in the next update.
**inviteme** Invite me to your server!
**myserver** My support server's link
**q** Quote someone, or view someone else's quotes. Type `parrot q` for more info.
**c** The currency system. Type `parrot c` for more info.
**messup [url]** Scramble images! You either give the URL, or an image attachment.
**ach/achievements** View your achievements.""")
            
            elif command[1] == "ping":
                ms = (message.id >> 22) + 1420070400000
                await message.channel.send(":parrot: **Pong!\n`Time between command reception and reply: " + str(int(round(time.time() * 1000)) - start) + "ms\nClient latency: " + str(round(client.latency * 1000, 5)) + "ms\nBot latency: " + str(int(round(time.time() * 1000)) - ms) + "ms`**")
                
            elif command[1] == "uptime":
                await message.channel.send(":parrot: **I have been alive for " + msToTime(int(round(time.time() * 1000)) - initstart) + ".**")

            elif command[1] == "eval" and message.author.id == 644052617500164097:
                try:
                    await message.channel.send(eval(message.content.replace("parrot eval ", "")))
                except:
                    await message.channel.send("```"+traceback.format_exc()+"```")

            elif command[1] == "announce" and message.author.id == 644052617500164097:
                for guild in client.guilds:
                    if not guild.id in announcementRead("announced"):
                        announcementAppend(guild.id)
                        try:
                            if preferencesRead(guild.id, "annchannel") in [n.name for n in guild.channels] and preferencesRead(guild.id, "annchannel") != None:
                                channel = discord.utils.get(guild.text_channels, name=preferencesRead(guild.id, "annchannel"))
                                if announcementRead("message") == "newversion":
                                    await channel.send(":parrot: **I have updated to " + VERSION + "! Type `parrot changelog` for more info on what has been added.**")
                                elif announcementRead("message") != "":
                                    await channel.send(":parrot: **Announcement from owner:** " + announcementRead("message"))
                        except:
                            pass


            elif command[1] == "changelog" or command[1] == "cl":
                await message.channel.send(""":parrot: **This is what's new in the latest version! Very exciting, bawk!**
**Current version:** """ + VERSION + """
- Parrot raise is now removed.
- Aliases: changelog -> cl; repeat -> re; stoprepeat -> sre; detectswear -> ds; stopdetectswear -> sds
- New additions to parrot c: enc, top, rename. Placefood has a new alias: pf. You can now have multiple bowls, and buy multiple of the same item at once. There is now xp and levelling, and each level gives you a multiplier for attracting parrots. New parrot naming system (random instead of ascending). Some new parrots and foods as well.
- Achievements! I have 5 of them scattered everywhere when you do anything, and they usually come secretly. They give multipliers like levels in the currency system. View you achievents using `parrot ach` or `parrot achievements`.
- Several pesky bug fixes here and there
-(.1) Json file read-writing scripts (aka Drivers in the code), so no file will be corrupted
-(.2) Migrated several JSON files to mongodb
-(.2) Added uptime & eval command

**Next version:** v1.10
- history page
- tips page
- reaction test game
...and many more! If you would like to suggest, contact i\_\_\_\_7d.
*Note that some of these changes, and some bug fixes might go into a '0.?.x' version. These will be counted as part of the '0.x' version, and not separately.*""")

            elif command[1] == "ach" or command[1] == "achievements":
                string = ":parrot: **Bawk! Here's your list of achievements!**\n"
                for a in currencyRead(message.author.id, "ach"):
                    string = string + "**" + currstatsRead("ach")[a]["info"] + "** (" + str(currstatsRead("ach")[a]["multiplier"] * 100) + "% multiplier)\n"
                await message.channel.send(string)
                
            elif command[1] == "list":
                def returnNick(a):
                    for b in members:
                        if b.id == a:
                            if b.nick == None:
                                return b.name
                            else:
                                return b.nick
                    return "(Left)"

                if msgLCase.strip() == "parrot list repeat" or msgLCase.strip() == "parrot list re":
                    if len(memberlistsRead("toRepeat", message.guild.id)) == 0:
                        await message.channel.send(":parrot: **No members repeated, bawwwwk :(**")
                    else:
                        await message.channel.send(":parrot: **Repeated members:** " + ", ".join([returnNick(a) for a in memberlistsRead("toRepeat", message.guild.id)]))
                elif msgLCase.strip() == "parrot list detectswear" or msgLCase.strip() == "parrot list ds":
                    if len(memberlistsRead("toDetectSwear", message.guild.id)) == 0:
                        await message.channel.send(":parrot: **No members detected for swearing, bawwwwk :(**")
                    else:
                        await message.channel.send(":parrot: **Members detected for swearing:** " + ", ".join([returnNick(a) for a in memberlistsRead("toDetectSwear", message.guild.id)]))
                elif msgLCase.strip() == "parrot list mute":
                    if len(memberlistsRead("toMute", message.guild.id)) == 0:
                        await message.channel.send(":parrot: **No members muted, bawwwwk :(**")
                    else:
                        await message.channel.send(":parrot: **Muted members:** " + ", ".join([returnNick(a) for a in memberlistsRead("toMute", message.guild.id)]))
                elif msgLCase.strip() == "parrot list":
                    if len(memberlistsRead("toRepeat", message.guild.id)) == 0:
                        await message.channel.send(":parrot: **Repeated members:** None")
                    else:
                        await message.channel.send(":parrot: **Repeated members:** " + ", ".join([returnNick(a) for a in memberlistsRead("toRepeat", message.guild.id)]))
                    if len(memberlistsRead("toDetectSwear", message.guild.id)) == 0:
                        await message.channel.send(":parrot: **Members detected for swearing:** None")
                    else:
                        await message.channel.send(":parrot: **Members detected for swearing:** " + ", ".join([returnNick(a) for a in memberlistsRead("toDetectSwear", message.guild.id)]))
                    if len(memberlistsRead("toMute", message.guild.id)) == 0:
                        await message.channel.send(":parrot: **Muted members:** None")
                    else:
                        await message.channel.send(":parrot: **Muted members:** " + ", ".join([returnNick(a) for a in memberlistsRead("toMute", message.guild.id)]))

            elif command[1] == "inviteme":
                await message.channel.send(":parrot: **Bawk! Here's my invite link to invite me to another server!**\nLink: https://discordapp.com/api/oauth2/authorize?client_id=691990367569969264&permissions=268478464&scope=bot")

            elif command[1] == "myserver":
                await message.channel.send(":parrot: **Bawk! Here's my support server: https://discord.gg/B4N8nKW**")

            #elif command[1] == "initinfo":
                #await message.channel.send(""":parrot: **Firstly, thank you so much for inviting me into your server! I'm sure i____7d will be glad too!**
                #Here are the steps to initialising me: (Note that this #involves creating and giving roles so its for admins only)
                #1. Create a role called 'Parrot Master' (case sensitive).
                #2. Give yourself and some others the role.
                #That's it, enjoy :)""")

            elif command[1] == "honk" and (message.guild.id == 677954661545803808 or message.author.id == 644052617500164097):
                Os = ""
                if len(command) > 2 and int(msgLCase.replace("parrot honk ", "")) > 0 and int(msgLCase.replace("parrot honk ", "")) < 1981:
                    for o in range(0, int(msgLCase.replace("parrot honk ", ""))):
                        Os = Os + "o"
                else:
                    Os = "o"
                await message.channel.send(":parrot: **H" + Os + "nk!!!**")

            elif command[1] == "q":
                if len(command) > 2 and command[2] == "add":
                    if len(command) > 3 and int(msgLCase.replace("parrot q add ", "")) > 0:
                        try:
                            quote = await message.channel.fetch_message(int(msgLCase.replace("parrot q add ", "")))
                        except:
                            await message.channel.send(":parrot: That message doesn't exist!")
                        else:
                            if quotesView(fullnameify(quote.author)) != "nope" and quote.content in [a["quote"] for a in quotesView(fullnameify(quote.author))[1]]:
                                await message.channel.send(":parrot: That message has already been quoted!")
                            elif quote.author.id == message.author.id and message.author.id != 644052617500164097:
                                await message.channel.send(":parrot: Sorry, you can't quote your own message! Ask another to quote for you.")
                            elif quote.content in offensiveView(fullnameify(quote.author)):
                                await message.channel.send(":parrot: **The sender of this quote has found this offensive.**")
                            else:
                                quotesAdd(quote.author, {"id": quoteCount(), "quote": quote.content})
                                upQuoteCount()
                                await message.channel.send(":parrot: **Message quoted:** _**\"" + quote.content.replace("_", "\_") + "\"** - " + quote.author.name.replace("_", "\_") + "_")
                                await client.get_channel(700946990678409276).send("**Message quoted by " + fullnameify(message.author).replace("_", "\_") + " (ID:" + str(message.author.id) + ") for " + fullnameify(quote.author).replace("_", "\_") + " (ID:" + str(quote.author.id) + "):** " + quote.content + " (ID: " + str(quoteCount()-1) + ")")
                    else:
                        await message.channel.send(""":parrot: **How to quote a message:**
1. Turn on developer mode. This allows you to copy IDs. (To do so, go to Settings > Appearance > Developer Mode.)
2. Click the menu of the message (aka More).
3. Click 'Copy ID'.
4. Do `parrot q add <paste here>`.

**Please also note that racist or sexist quotes are not allowed. i\_\_\_\_7d is actively watching; do not quote racist messages. If you were the one that made the message please delete it (and mark it as `-o`).**""")
                elif len(command) > 2 and command[2] == "view":
                    params = " ".join(message.content.split()[3:]).strip()
                    memberfullname = params.split(" ")[0]
                    index = params.replace(memberfullname, "").strip()
                    if quotesView(memberfullname) == "nope":
                        await message.channel.send(":parrot: No quotes from him!")
                    else:
                        result = quotesView(memberfullname)
                        quotelist = result[1]

                        if result[0] in [g.name for g in message.guild.members]:
                            quotee = result[0]
                        else:
                            quotee = "anonymous"

                        if index == "":
                            l = ""
                            for q in quotelist:
                                l = l + str(quotelist.index(q) + 1) + ". [" + str(q["id"]) + "] \"" + q["quote"] + "\"\n"
                            await message.channel.send(":parrot: **All quotes from " + quotee + ":** ```\n" + l + "```")

                        elif index.strip() == "any":
                            await message.channel.send(":parrot: _**" + random.choice([("[" + str(r["id"]) + "] \"" + r["quote"] + "\"") for r in quotelist]).replace("_", "\_") + "** - " + quotee.replace("_", "\_") + "_")
                        elif int(index) > 0 and int(index) <= len(quotelist):
                            await message.channel.send(":parrot: _**\"" + quotelist[int(index) - 1].replace("_", "\_") + "\"** - " + quotee.replace("_", "\_") + "_")
                elif len(command) > 2 and command[2] == "remove":
                    theid = msgLCase.replace("parrot q remove", "").strip()
                    if len(command) > 4 and command[4] == "-o":
                        offensive = True
                        theid = theid.replace("-o", "").strip()
                    else:
                        offensive = False

                    if not theid.isdigit():
                        await message.channel.send(":parrot: Please provide a valid quote ID.")

                    result = quotesRemove(theid, offensive, message.author)
                    if result == "yes":
                        if offensive:
                            await message.channel.send(":parrot: **Quote deleted and marked as offensive!**")
                        else:
                            await message.channel.send(":parrot: **Quote deleted!**")
                    elif result == "notyou":
                        await message.channel.send(":parrot: **You can't delete others' quotes!**")
                    else:
                        await message.channel.send(":parrot: Please provide a valid quote ID.")

                else:
                    await message.channel.send(""":parrot: **This is my quoting function, welcome!**\nFor this quote function, start with `parrot q`.
**add <Message ID>** Adds a quote to the database. Type `parrot q add` by itself for instructions on how to add a quote. Note that you can only add others' quotes.
**view <person> [index]** View someone's quotes.
- Put 'anyone' in the <person> slot to pick a random person.
- Put 'any' in the [index] slot to pick a random quote from a person.
- Leave [index] empty to get all quotes from someone.
- Do 'anyone any' for a random quote from a random person.
- Note that you have to give the full name (e.g. Foobar#1234) for the <person> slot.
**remove <quote ID> [-o]** Removes a quote. Note that you can only remove your own quote.
- Append `-o` to mark it as offensive, which means that the quote can never be quoted again.""")

            elif command[1] == "messup":
                await messUp(message)

            elif command[1] == "c":
                if len(preferencesRead(message.guild.id, "currencychannels")) != 0 and not message.channel.name in preferencesRead(message.guild.id, "currencychannels"):
                    msg = await message.channel.send(":parrot: Currency commands are not allowed to be used here. Use them in these channels: #" + ", #".join(preferencesRead(message.guild.id, "currencychannels")))
                    await asyncio.sleep(3 + len(preferencesRead(message.guild.id, "currencychannels")))
                    await message.delete()
                    await msg.delete()
                    return
                if len(command) > 2 and command[2] == "daily":
                    if (currencyRead(message.author.id, "lastdaily") + 86400000) < int(round(time.time() * 1000)):
                        currencyWrite(message.author.id, "balance", currencyRead(message.author.id, "balance") + 50)
                        currencyWrite(message.author.id, "lastdaily", int(round(time.time() * 1000)))
                        await upXP(message, 10)
                        await message.channel.send(":parrot: **Here are your daily 50 twigs!**")
                    else:
                        d = msToTime(currencyRead(message.author.id, "lastdaily") + 86400000 - int(round(time.time() * 1000)))
                        t = datetime.datetime.fromtimestamp((currencyRead(message.author.id, "lastdaily") + 86400000)/1000).strftime("%H:%M:%S")
                        await message.channel.send(":parrot: **Sorry, I have not gathered my twigs get, please wait " + d + " until " + t + " GMT!**")
                elif len(command) > 2 and (command[2] == "inv" or command[2] == "inventory"):
                    string = ":parrot: **Your Inventory:**\n"
                    if len(currencyRead(message.author.id, "inventory")) == 0:
                        string = string + "empty!"
                    for v in currencyRead(message.author.id, "inventory"): 
                        string = string + str(v["qty"]) + " " + v["name"] + "s\n"
                    await message.channel.send(string)
                elif len(command) > 2 and (command[2] == "bal" or command[2] == "balance"):
                    await message.channel.send(":parrot: **You currently have " + str(math.floor(float(currencyRead(message.author.id, "balance")))) + " twigs.**\nYou are also at Level " + str(currencyRead(message.author.id, "level")) + " and have " + str(currencyRead(message.author.id, "xp")) + " xp. Bawk!")
                elif len(command) > 2 and command[2] == "parrots":
                    string = ":parrot: **Your Parrots:**\n"
                    if len(currencyRead(message.author.id, "parrots")) == 0:
                        string = string + "none :("
                    else:
                        section = msgLCase.replace("parrot c parrots ", "")
                        if not section.isdigit() or int(section)*10 - len(currencyRead(message.author.id, "parrots")) > 10:
                            section = 1
                        else:
                            section = int(section)
                        st = (section-1)*10
                        if len(currencyRead(message.author.id, "parrots")) < (section*10):
                            en = len(currencyRead(message.author.id, "parrots"))
                        else:
                            en = (section*10)

                        w = st
                        for v in currencyRead(message.author.id, "parrots")[st:en]:
                            string = string + "**" + str(w+1) + ".** " + v["name"] + " (" + v["breed"] + ")\n"
                            w += 1
                        string = string + "**Total parrots: " + str(len(currencyRead(message.author.id, "parrots"))) + "**\n"

                        tpm = 0
                        for u in currencyRead(message.author.id, "parrots"):
                            tpm = round(tpm + currstatsRead("parrots")[[v["name"] for v in currstatsRead("parrots")].index(u["breed"])]["tpm"], 2)
                        string = string + "**All parrots collect " + str(tpm) + " twigs per minute.**\n"
                        string = string + "**(Page " + str(section) + " of " + str(math.ceil(len(currencyRead(message.author.id, "parrots")) / 10)) + ")**"
                    await message.channel.send(string)
                elif len(command) > 2 and command[2] == "bowl":
                    string = ":parrot: **Bawk! Here are your bowls!**\n"
                    for w in currencyRead(message.author.id, "bowls"):
                        if w["inside"] == None:
                            inside = "Empty"
                        else:
                            inside = w["inside"]
                        string = string + "**" + str(currencyRead(message.author.id, "bowls").index(w)+1) + ".** " + inside + "; " + str(w["attractsleft"]) + " attracts left\n"
                    await message.channel.send(string)

                elif len(command) > 2 and (command[2] == "placefood" or command[2] == "pf"):
                    toPlace = msgLCase.replace("parrot c placefood ", "").replace("parrot c pf ", "").strip()
                    bowlIndex = None
                    for q in currencyRead(message.author.id, "bowls"):
                        if q["inside"] == None:
                            bowlIndex = currencyRead(message.author.id, "bowls").index(q)
                            break
                    if bowlIndex == None:
                        await message.channel.send(":parrot: Your bowls are already filled!")
                        return
                    elif toPlace in [p["name"].lower() for p in currencyRead(message.author.id, "inventory")] and currstatsRead("shop")[[c["name"].lower() for c in currstatsRead("shop")].index(toPlace)]["type"] == "food":
                        oldlist = currencyRead(message.author.id, "bowls")
                        oldlist[bowlIndex]["inside"] = toPlace
                        oldlist[bowlIndex]["attractsleft"] = currstatsRead("shop")[[p["name"].lower() for p in currstatsRead("shop")].index(toPlace)]["pax"]
                        currencyWrite(message.author.id, "bowls", oldlist)

                        if currencyRead(message.author.id, "inventory")[[r["name"].lower() for r in currencyRead(message.author.id, "inventory")].index(toPlace)]["qty"] == 1:
                            newInventory = currencyRead(message.author.id, "inventory")
                            del newInventory[[p["name"] for p in currencyRead(message.author.id, "inventory")].index(toPlace)]
                            currencyWrite(message.author.id, "inventory", newInventory)
                        else:
                            newInventory = currencyRead(message.author.id, "inventory")
                            newInventory[[p["name"] for p in currencyRead(message.author.id, "inventory")].index(toPlace)]["qty"] -= 1
                            currencyWrite(message.author.id, "inventory", newInventory)
                        await message.channel.send(":parrot: **You placed some " + toPlace + " into the bowl.**")
                    else:
                        await message.channel.send(":parrot: You either do not have this food item, or the item is inedible!")
                elif len(command) > 2 and command[2] == "shop":
                    val = msgLCase.replace("parrot c shop", "").strip()
                    if val == "" or (not val.isdigit()) or int(val) < 1 or int(val)*4 - len(currstatsRead("shop")) > 4:
                        page = 1
                    else:
                        page = int(val)

                    st = (page-1)*4
                    if len(currstatsRead("shop")) < (page*4):
                        en = len(currstatsRead("shop"))
                    else:
                        en = (page*4)

                    string = ":parrot: **Bawk! Thanks for stopping by the Bawkshop!**\n"
                    for i in currstatsRead("shop")[st:en]:
                        if i["type"] == "food":
                            string = string + "**" + i["name"] + "** - " + str(i["cost"]) + " twigs\n_" + i["lore"] + "_\n- Chance of new parrot every minute: " + str(i["cpm"]) + "\n- No. of parrots it can attract before depleted: " + str(i["pax"]) + "\n"
                        elif i["type"] == "util":
                            string = string + "**" + i["name"] + "** - " + str(i["cost"]) + " twigs\n_" + i["lore"] + "_\n" 
                    string = string + "**(Page " + str(page) + " of " + str(math.ceil(len(currstatsRead("shop")) / 4)) + ")**"
                    await message.channel.send(string)
                elif len(command) > 2 and command[2] == "buy":
                    params = msgLCase.replace("parrot c buy", "").strip()
                    if len(params.split(" ")) < 2 or not params.split(" ")[0].isdigit():
                        await message.channel.send(":parrot: Please include the quanity of items you're going to buy and the item itself!")
                        return
                    toBuy = " ".join(params.split(" ")[1:])
                    qty = int(params.split(" ")[0])
                    if qty < 1:
                        await message.channel.send(":parrot: Positive integers only!")
                        return
                    if toBuy in [p["name"].lower() for p in currstatsRead("shop")]:
                        toBuyStat = currstatsRead("shop")[[p["name"].lower() for p in currstatsRead("shop")].index(toBuy)]
                        if toBuyStat["cost"]*qty > currencyRead(message.author.id, "balance"):
                            await message.channel.send(":parrot: **Sorry, you don't have enough twigs for the " + toBuy + "!**")
                        else:
                            currencyWrite(message.author.id, "balance", currencyRead(message.author.id, "balance") - toBuyStat["cost"]*qty)
                            if toBuyStat["type"] == "food":
                                if toBuy in [r["name"].lower() for r in currencyRead(message.author.id, "inventory")]:
                                    newInventory = currencyRead(message.author.id, "inventory")
                                    newInventory[[p["name"] for p in currencyRead(message.author.id, "inventory")].index(toBuy)]["qty"] += qty
                                    currencyWrite(message.author.id, "inventory", newInventory)
                                else:
                                    newInventory = currencyRead(message.author.id, "inventory")
                                    newInventory.append({"name": toBuy, "qty": qty})
                                    currencyWrite(message.author.id, "inventory", newInventory)
                            elif toBuyStat["name"] == "Bowl":
                                oldbowls = currencyRead(message.author.id, "bowls")
                                for blah in range(0, qty):
                                    oldbowls.append({"id": len(oldbowls), "inside": None, "attractsleft": 0})
                                currencyWrite(message.author.id, "bowls", oldbowls)
                            await message.channel.send(":parrot: **" + str(qty) + " " + toBuy + " bought for " + str(toBuyStat["cost"]*qty) + " twigs!**")
                            if len(currencyRead(message.author.id, "bowls")) > 1:
                                ach(message.author, 3)
                            await upXP(message, 10*qty)
                    else:
                        await message.channel.send(":parrot: That item doesn't exist!")
                elif len(command) > 2 and command[2] == "rename":
                    if not len(command) > 4 or command[3].isdigit() == False:
                        await message.channel.send(":parrot: Please include the index of your parrot (a number) and the new name!")
                        return
                    number = int(command[3])
                    newname = " ".join(message.content.split(" ")[4:])
                    if number >= len(currencyRead(message.author.id, "parrots")):
                        await message.channel.send(":parrot: Your index is out of range; you do not have that much parrots!")
                        return
                    oldlist = currencyRead(message.author.id, "parrots")
                    oldlist[number-1]["name"] = newname
                    currencyWrite(message.author.id, "parrots", oldlist)
                    await message.channel.send(":parrot: **Successfully renamed your parrot to " + newname + "!**")
                elif len(command) > 2 and command[2] == "enc":
                    if msgLCase == "parrot c enc":
                        await message.channel.send("**Parrot breeds:** " + ", ".join([j["name"] for j in currstatsRead("parrots")]))
                        return

                    breed = message.content.replace("parrot c enc ", "")
                    if not breed in [j["name"].lower() for j in currstatsRead("parrots")]:
                        await message.channel.send(":parrot: Sorry, there is no such breed!")
                    else:
                        for k in range(0, len(currstatsRead("parrots"))):
                            if breed == currstatsRead("parrots")[k]["name"].lower():
                                encEntry = currstatsRead("parrots")[k]
                                break

                        await message.channel.send("**Page on " + encEntry["name"] + ":**\nRate of twigs collected per minute: " + str(encEntry["tpm"]) + "\nChance of this breed being attracted: " + str(encEntry["chance"] * 100) + "%")

                elif len(command) > 2 and command[2] == "top":
                    if len(command) > 3 and command[3] == "twigs":
                        sortAs = "balance"
                        sortMsg = "twigs"
                    elif len(command) > 3 and command[3] == "parrots":
                        sortAs = "parrots"
                        sortMsg = "no. of parrots"
                    elif len(command) > 3 and command[3] == "xp":
                        sortAs = "xp"
                        sortMsg = "total xp gained"
                    else:
                        sortAs = "score"
                        sortMsg = "all factors"
                    #request = {"request": "r", "new": None}
                    #code = len(currencyQueue)
                    #currencyQueue.append(request)
                    #while currencyQueue[code] == request:
                    #    pass
                    #data = currencyQueue[code]
                    data = list(db["currency"].find({}))
                    servermemberids = [r.id for r in members]
                    toSort = []
                    for m in servermemberids:
                        try:
                            toSort.append(data[str(m)])
                            toSort[len(toSort)-1]["fullname"] = fullnameify(client.get_user(m))
                            toSort[len(toSort)-1]["xp"] = toSort[len(toSort)-1]["xp"] + 100*toSort[len(toSort)-1]["level"]
                            toSort[len(toSort)-1]["score"] = round((toSort[len(toSort)-1]["balance"] + len(toSort[len(toSort)-1]["parrots"]) + toSort[len(toSort)-1]["level"]) / 10, 2)
                            toSort[len(toSort)-1]["parrots"] = len(toSort[len(toSort)-1]["parrots"])
                        except KeyError:
                            pass
                    toSort = sorted(toSort, key=lambda k: k[sortAs], reverse=True)
                    longestFullname = 0
                    longestBal = 0
                    longestParrotLength = 0
                    longestXP = 0
                    longestScore = 0
                    for m in toSort:
                        if len(m["fullname"]) > longestFullname:
                            longestFullname = len(m["fullname"])
                        if len(str(m["balance"])) > longestBal:
                            longestBal = len(str(m["balance"]))
                        if len(str(m["parrots"])) > longestParrotLength:
                            longestParrotLength = len(str(m["parrots"]))
                        if len(str(m["xp"])) > longestXP:
                            longestXP = len(str(m["xp"]))
                        if len(str(m["score"])) > longestScore:
                            longestScore = len(str(m["score"]))

                    def spaces(headerword, longestentrylen, spacechar):
                        headerword = str(headerword)
                        if len(headerword) >= longestentrylen:
                            return str(headerword)
                        else:
                            spaceamt = longestentrylen - len(headerword)
                            space = ""
                            for o in range(0, spaceamt):
                                space = space + spacechar
                            return str(headerword + space)

                    def spacescontent(contentword, header, spacechar):
                        contentword = str(contentword)
                        spaceamt = len(header) - len(contentword)
                        space = ""
                        for o in range(0, spaceamt):
                            space = space + spacechar
                        return str(contentword + space)
                    
                    nameHeader = spaces("Name", longestFullname, "-")
                    balHeader = spaces("Balance", longestBal, "-")
                    parrotlengthHeader = spaces("Parrots", longestParrotLength, "-")
                    xpHeader = spaces("Total XP", longestXP, "-")
                    scoreHeader = spaces("Score", longestScore, "-")

                    string = ":parrot: **Viewing the top 15 in the server based on: " + sortMsg + "**\n```" + nameHeader + "|" + balHeader + "|" + parrotlengthHeader + "|" + xpHeader + "|" + scoreHeader + "\n"
                    f = 0
                    for t in toSort:
                        string = string + spacescontent(t["fullname"], nameHeader, " ") + "|" + spacescontent(t["balance"], balHeader, " ") + "|" + spacescontent(t["parrots"], parrotlengthHeader, " ") + "|" + spacescontent(t["xp"], xpHeader, " ") + "|" + spacescontent(t["score"], scoreHeader, " ") + "\n"
                        f += 1
                        if f == 15:
                            break
                    string = string + "```"
                    await message.channel.send(string)


                elif len(command) > 2 and command[2] == "how":
                    await message.channel.send(""":parrot: **Hi! Here is how to use this currency system!**
When you first start, you get 50 twigs. You go to the shop (`parrot c shop`) and buy some food (`parrot c buy`). You then place some food in your bowl (`parrot c placefood`) to attract parrots. Every minute, there is a chance that you will get a new parrot.
To view your parrots, type `parrot c parrots`. You can rename one of them using `parrot c rename <index> <new name>`.
Some actions give you xp. They are usually the action commands instead of the viewing commands. Each 100xp is converted into levels. Each level gives you a multiplier of 5%.
Achievements also give multipliers. They depend on how hard it takes to get the achievement. Multipliers affect the chance of getting a new parrot every minute, and the rate of twigs per minute.
This currency system is still under development, so comment to i\_\_\_\_7d if it is either too slow or fast for you!
Also note that I am NOT a parrot expert, so the parrot stats might not correspond to real-world context. :P""")
                else:
                    await message.channel.send(""":parrot: **Bawk! Here's the help page for the currency system!**\nFor this currency function, start with `parrot c`.
**shop [page]** Shop for items, especially foods
**buy <qty> <item>** Buy items from the shop.
**pf/placefood <item>** Put food into the bowl.
**inv/inventory** View your inventory.
**bowl** View what's inside your bowls.
**parrots [page]** View your parrots.
**bal/balance** View your balance.
**daily** Claim your daily twigs.
**enc [breed]** View the encyclopaedia of parrots.
**top [twigs/parrots/xp]** Views the top 15 players on this server, based on amount of twigs, parrots, or xp. Append nothing to rank players based on all three factors combined.
**rename <index> <new name>** Rename one of your parrots.
**how** View the tutorial for this system.""")

            if "Parrot Master" in [y.name for y in message.author.roles] or message.author.id == 644052617500164097:
                if (command[1] == "repeat" or command[1] == "re") and len(command) > 2:
                    if msgLCase.replace("parrot repeat ", "").replace("parrot re ", "") in memberNicks:
                        memberID = None
                        for e in range(0, len(members)):
                            if memberNicks[e] == msgLCase.replace("parrot repeat ", "").replace("parrot re ", ""):
                                memberID = members[e].id
                                break

                        if memberID in memberlistsRead("toRepeat", message.guild.id):
                            await message.channel.send(":parrot: I'm repeating him already, master!")
                        else:
                            memberlistsAppend("toRepeat", message.guild.id, memberID)
                            await message.channel.send(":parrot: I'm going to repeat whatever he says, master!")
                    else:
                        await message.channel.send(":parrot: There is no one with that name, master!")

                elif (command[1] == "stoprepeat" or command[1] == "sre") and len(command) > 2:
                    if msgLCase.replace("parrot stoprepeat ", "").replace("parrot sre ", "") == "*":
                        for blah in memberlistsRead("toRepeat", message.guild.id):
                            memberlistsPop("toRepeat", message.guild.id, 0)
                        await message.channel.send(":parrot: I've stopped repeating everyone, master!")
                    else:
                        toRepeatIDs = memberlistsRead("toRepeat", message.guild.id)

                        memberID = None
                        for e in range(0, len(members)):
                            if memberNicks[e] == msgLCase.replace("parrot stoprepeat ", "").replace("parrot sre ", ""):
                                memberID = members[e].id
                                break
                        
                        if memberID in toRepeatIDs:
                            memberlistsPop("toRepeat", message.guild.id,toRepeatIDs.index(memberID))
                            await message.channel.send(":parrot: I've stopped repeating him, master!")
                        else:
                            await message.channel.send(":parrot: I'm not repeating him, master!")

                elif (command[1] == "detectswear" or command[1] == "ds") and len(command) > 2:
                    if msgLCase.replace("parrot detectswear ", "").replace("parrot ds ", "") in memberNicks:
                        memberID = None
                        for e in range(0, len(members)):
                            if memberNicks[e] == msgLCase.replace("parrot detectswear ", "").replace("parrot ds ", ""):
                                memberID = members[e].id
                                break
                        
                        if memberID in memberlistsRead("toDetectSwear", message.guild.id):
                            await message.channel.send(":parrot: I'm detecting him already, master!")
                        else:
                            memberlistsAppend("toDetectSwear", message.guild.id, memberID)
                            await message.channel.send(":parrot: I'm going to detect if he swears, master!")
                    else:
                        await message.channel.send(":parrot: There is no one with that name, master!")

                elif (command[1] == "stopdetectswear" or command[1] == "sds") and len(command) > 2:
                    if msgLCase.replace("parrot stopdetectswear ", "").replace("parrot sds ", "") == "*":
                        for blah in memberlistsRead("toDetectSwear", message.guild.id):
                            memberlistsPop("toDetectSwear", message.guild.id, 0)
                        await message.channel.send(":parrot: I've stopped detecting everyone, master!")
                    else:
                        toDetectSwearIDs = memberlistsRead("toDetectSwear", message.guild.id)

                        memberID = None
                        for e in range(0, len(members)):
                            if memberNicks[e] == msgLCase.replace("parrot stopdetectswear ", "").replace("parrot sds ", ""):
                                memberID = members[e].id
                                break
                        
                        if memberID in toDetectSwearIDs:
                            memberlistsPop("toDetectSwear", message.guild.id,toDetectSwearIDs.index(memberID))
                            await message.channel.send(":parrot: I've stopped detecting him, master!")
                        else:
                            await message.channel.send(":parrot: I'm not detecting him, master!")

                elif command[1] == "mute" and len(command) > 2:
                    if msgLCase.replace("parrot mute ", "") in memberNicks:
                        memberID = None
                        for e in range(0, len(members)):
                            if memberNicks[e] == msgLCase.replace("parrot mute ", ""):
                                memberID = members[e].id
                                break
                        
                        if memberID in memberlistsRead("toMute", message.guild.id):
                            await message.channel.send(":parrot: I'm muting him already, master!")
                        else:
                            memberlistsAppend("toMute", message.guild.id, memberID)
                            await message.channel.send(":parrot: I'm going to make noise over what he says, master!")
                    else:
                        await message.channel.send(":parrot: There is no one with that name, master!")

                elif command[1] == "unmute" and len(command) > 2:
                    if msgLCase.replace("parrot unmute ", "") == "*":
                        for blah in memberlistsRead("toMute", message.guild.id):
                            memberlistsPop("toMute", message.guild.id, 0)
                        await message.channel.send(":parrot: I've stopped muting everyone, master!")
                    else:
                        toMuteIDs = memberlistsRead("toMute", message.guild.id)

                        memberID = None
                        for e in range(0, len(members)):
                            if memberNicks[e] == msgLCase.replace("parrot unmute ", ""):
                                memberID = members[e].id
                                break
                        
                        if memberID in toMuteIDs:
                            memberlistsPop("toMute", message.guild.id,toMuteIDs.index(memberID))
                            await message.channel.send(":parrot: I've stopped muting him, master!")
                        else:
                            await message.channel.send(":parrot: I'm not muting him, master!")
                
                #elif command[1] == "vcbawk":
                #    voiceChannel = message.author.voice.channel
                #    if voiceChannel == None:
                #        if discord.utils.get(message.guild.voice_channels, name=message.content.replace("parrot vcbawk ", "")):
                #            voiceChannel = message.content.replace("parrot vcbawk ", "")
                #        else:
                #            await message.channel.send("That channel does not exist!")
                #            return
                #    if voiceChannel == None:
                #        await message.channel.send("You are not in a channel!")
                #        return
                #    else:
                #        try:
                #            await voiceChannel.connect()
                #        except:
                #            pass 
                #        source = await discord.FFmpegPCMAudio.from_probe("bawking.m4a")
                #        await voiceChannel.play(source)
                #        while voiceChannel.is_playing():
                #            await asyncio.sleep(1)
                #        await voiceChannel.stop()
                #        await voiceChannel.disconnect()

                elif command[1] == "s":
                    if len(command) > 2 and command[2] == "v":
                        if msgLCase == "parrot s v deletelog":
                            if preferencesRead(message.guild.id, "deletelog") != None:
                                await message.channel.send(":parrot: Current channel set for deletelog: #" + str(preferencesRead(message.guild.id, "deletelog")))
                            else:
                                await message.channel.send(":parrot: Current channel set for deletelog: None")
                        elif msgLCase == "parrot s v swearalarm":
                            await message.channel.send(":parrot: Current swear alarm message: " + preferencesRead(message.guild.id, "swearalarm"))
                        elif msgLCase == "parrot s v annchannel":
                            if preferencesRead(message.guild.id, "annchannel") != None:
                                await message.channel.send(":parrot: Current channel set for announcing new versions: #" + str(preferencesRead(message.guild.id, "annchannel")))
                            else:
                                await message.channel.send(":parrot: Current channel set for announcing new versions: None")
                        elif msgLCase == "parrot s v dsmba":
                            await message.channel.send(":parrot: Delete message containing swear word before sounding swear alarm: " + str(preferencesRead(message.guild.id, "dsmba")))
                        elif msgLCase == "parrot s v addswearwords":
                            await message.channel.send(":parrot: Additional swear words: " + ", ".join("'"+w+"'" for w in preferencesRead(message.guild.id, "addswearwords")))
                        elif msgLCase == "parrot s v currencychannels":
                            if len(preferencesRead(message.guild.id, "currencychannels")) == 0:
                                await message.channel.send(":parrot: Channels where `parrot c` can be used: Every")
                            else:
                                await message.channel.send(":parrot: Channels where `parrot c` can be used: " + ", ".join("#"+w for w in preferencesRead(message.guild.id, "currencychannels")))
                        else:
                            #deletelog
                            if preferencesRead(message.guild.id, "deletelog") != None:
                                await message.channel.send(":parrot: Current channel set for deletelog: #" + str(preferencesRead(message.guild.id, "deletelog")))
                            else:
                                await message.channel.send(":parrot: Current channel set for deletelog: None")
                            #swearalarm
                            if len(preferencesRead(message.guild.id, "swearalarm")) > 20:
                                SATruncated = str(preferencesRead(message.guild.id, "swearalarm"))[0:20] + "..."
                            else:
                                SATruncated = str(preferencesRead(message.guild.id, "swearalarm"))
                            await message.channel.send(":parrot: Current swear alarm message: " + SATruncated)
                            #annchannel
                            if preferencesRead(message.guild.id, "annchannel") != None:
                                await message.channel.send(":parrot: Current channel set for announcing new versions: #" + str(preferencesRead(message.guild.id, "annchannel")))
                            else:
                                await message.channel.send(":parrot: Current channel set for announcing new versions: None")
                            #dsmba
                            await message.channel.send(":parrot: Delete message containing swear word before sounding swear alarm: " + str(preferencesRead(message.guild.id, "dsmba")))
                            #addswearwords
                            await message.channel.send(":parrot: Additional swear words: " + ", ".join("'"+w+"'" for w in preferencesRead(message.guild.id, "addswearwords")))
                            #currencychannels
                            if len(preferencesRead(message.guild.id, "currencychannels")) == 0:
                                await message.channel.send(":parrot: Channels where `parrot c` can be used: Every")
                            else:
                                await message.channel.send(":parrot: Channels where `parrot c` can be used: " + ", ".join("#"+w for w in preferencesRead(message.guild.id, "currencychannels")))

                    elif len(command) > 2 and command[2] == "deletelog":
                        channelName = msgLCase.replace("parrot s deletelog ", "")
                        if channelName in [n.name for n in message.guild.channels]:
                            preferencesWrite(message.guild.id, "deletelog", channelName)
                            await message.channel.send(":parrot: Channel for deleted messages has been set to #" + channelName + "!")
                        else:
                            await message.channel.send(":parrot: There is no such channel '#" + channelName + "'!")
                    elif len(command) > 2 and command[2] == "deletelogreset":
                        preferencesWrite(message.guild.id, "deletelog", None)
                        await message.channel.send(":parrot: Channel for deleted messages reset! There is now no channel for deleted messages to go to.")
                    elif len(command) > 2 and command[2] == "swearalarm":
                        alarm = message.content[20:].strip()
                        if not alarm.startswith(":parrot:"):
                            alarm = ":parrot: " + alarm
                        preferencesWrite(message.guild.id, "swearalarm", alarm)
                        await message.channel.send(":parrot: The new swear alarm message has been set to: " + alarm)
                    elif len(command) > 2 and command[2] == "swearalarmreset":
                        preferencesWrite(message.guild.id, "swearalarm", SwearAlarmDefault)
                        await message.channel.send(":parrot: The swear alarm message is reverted to its default: " + SwearAlarmDefault)
                    elif len(command) > 2 and command[2] == "annchannel":
                        channelName = msgLCase.replace("parrot s annchannel ", "")
                        if channelName in [n.name for n in message.guild.channels]:
                            preferencesWrite(message.guild.id, "annchannel", channelName)
                            await message.channel.send(":parrot: Channel for new version announcements messages has been set to #" + channelName + "!")
                        else:
                            await message.channel.send(":parrot: There is no such channel '#" + channelName + "'!")
                    elif len(command) > 2 and command[2] == "annchannelreset":
                        preferencesWrite(message.guild.id, "annchannel", None)
                        await message.channel.send(":parrot: Channel for new version announcements reset! There is now no channel for announcements to go to.")
                    elif len(command) > 2 and command[2] == "dsmba":
                        if msgLCase.replace("parrot s dsmba ", "") == "true":
                            preferencesWrite(message.guild.id, "dsmba", True)
                            await message.channel.send(":parrot: I will now delete the message with the swear word in it when sounding a swear alarm!")
                        elif msgLCase.replace("parrot s dsmba ", "") == "false":
                            preferencesWrite(message.guild.id, "dsmba", False)
                            await message.channel.send(":parrot: I will no longer delete the message with the swear word in it when sounding a swear alarm!")
                    elif len(command) > 2 and command[2] == "addswearwords":
                        if msgLCase.startswith("parrot s addswearwords add:"):
                            addword = re.search(':(.*);', msgLCase)
                            if addword == None:
                                await message.channel.send(":parrot: Remember to put ':' before and ';' after your swear word.")
                                return
                            else:
                                addword = addword.group(1)
                            if not addword in preferencesRead(message.guild.id, "addswearwords"):
                                oldlist = preferencesRead(message.guild.id, "addswearwords")
                                oldlist.append(addword)
                                preferencesWrite(message.guild.id, "addswearwords", oldlist)
                                await message.channel.send(":parrot: Added '" + addword + "' to the list of additional swear words!")
                            else:
                                await message.channel.send(":parrot: That word/phrase has already been added!")
                        elif msgLCase.startswith("parrot s addswearwords remove:"):
                            removeword = re.search(':(.*);', msgLCase)
                            if removeword == None:
                                await message.channel.send(":parrot: Remember to put ':' before and ';' after your swear word.")
                                return
                            else:
                                removeword = removeword.group(1)
                            if removeword in preferencesRead(message.guild.id, "addswearwords"):
                                oldlist = preferencesRead(message.guild.id, "addswearwords")
                                oldlist.remove(removeword)
                                preferencesWrite(message.guild.id, "addswearwords", oldlist)
                                await message.channel.send(":parrot: Removed '" + removeword + "' from the list of additional swear words!")
                            else:
                                await message.channel.send(":parrot: That word/phrase is not in the list!")
                        elif msgLCase.startswith("parrot s addswearwords reset"):
                            preferencesWrite(message.guild.id, "addswearwords", AddSwearWordsDefault)
                            await message.channel.send(":parrot: Reset the list of additional swear words!")

                    elif len(command) > 2 and command[2] == "currencychannels":
                        if len(command) > 3 and command[3] == "add":
                            addchannel = msgLCase.replace("parrot s currencychannels add ", "")
                            if not addchannel in [n.name for n in message.guild.channels]:
                                await message.channel.send(":parrot: There is no such channel '#" + addchannel + "'!")
                                return
                            if not addchannel in preferencesRead(message.guild.id, "currencychannels"):
                                oldlist = preferencesRead(message.guild.id, "currencychannels")
                                oldlist.append(addchannel)
                                preferencesWrite(message.guild.id, "currencychannels", oldlist)
                                await message.channel.send(":parrot: Added #" + addchannel + " to the list of channels where `parrot c` can be used!")
                            else:
                                await message.channel.send(":parrot: That channel has already been added!")
                        elif msgLCase.startswith("parrot s currencychannels remove:"):
                            removechannel = msgLCase.replace("parrot s currencychannels remove:", "")
                            if not removechannel in [n.name for n in message.guild.channels]:
                                await message.channel.send(":parrot: There is no such channel '#" + removechannel + "'!")
                                return
                            if removechannel in preferencesRead(message.guild.id, "currencychannels"):
                                oldlist = preferencesRead(message.guild.id, "currencychannels")
                                oldlist.remove(removechannel)
                                preferencesWrite(message.guild.id, "currencychannels", oldlist)
                                await message.channel.send(":parrot: Removed #" + removechannel + " from the list of channels where `parrot c` can be used!")
                            else:
                                await message.channel.send(":parrot: That channel is not in the list!")
                        elif msgLCase.startswith("parrot s currencychannels reset"):
                            preferencesWrite(message.guild.id, "currencychannels", [])
                            await message.channel.send(":parrot: Reset, now `parrot c` can be used in any channel!")

                    else:
                        await message.channel.send(""":parrot: **Bawk! This is the settings help page!**
For changing settings, use 'parrot s <preference> <option>'.
_If you are editing a <message> and want to state the author of the message it is replying to, use '{author}'._
**v [preference]** Views all preference values.
**deletelog <channel>** Sets the channel where deleted messages from muting are sent to.
**- deletelogreset** Resets the channel for deletelogging to no channel.
**swearalarm <message>** Sets the swear alarm.
**- swearalarmreset** Resets the swear alarm.
**annchannel <channel>** (short for announcementschannel) Sets the channel where announcements will be made.
**- annchannelreset** Resets the channel for version announcing to no channel.
**dsmba <true/false>** (short for deleteswearmsgbeforealarm) When someone swears while they are being detected, choose whether to delete the message with the swear word inside of it or not before sounding the alarm. Note that deleted messages will go to deletelog.
**addswearwords...** Edits the list of additional swear words to detect.
**- ...add:<word>;** Adds a word or phrase to the list.
**- ...remove:<word>;** Removes a word or phrase from the list.
**- ...reset;** Resets the list to its default.
- Always remember to put the colon and semicolon in `add` and `remove`. This prevents loss of spacebars.
- If you want to detect for a swear word in any word, don't put spaces. Put a space after the colon for a prefix swear; and before the semicolon for a suffix swear. Put both spaces for an exact swear word.
**currencychannels...** Edits the list of channels where `parrot c` can be used.
**- ...add <channel>** Adds a channel to the list.
**- ...remove <channel>** Removes a channel from the list.
**- ...reset** Resets the list to its default.""")
        
        else:
            if message.author.id in memberlistsRead("toMute", message.guild.id):
                try:
                    await message.delete()
                except:
                    pass
                await message.channel.send(":parrot: **Bawk bawk bawk bawk bawk bawk! " + message.author.name + " said nothing!**")
                if preferencesRead(message.guild.id, "deletelog") in [n.name for n in message.guild.channels] and preferencesRead(message.guild.id, "deletelog") != None:
                    await discord.utils.get(message.guild.text_channels, name=preferencesRead(message.guild.id, "deletelog")).send(":parrot: **" + message.author.name + ":** " + message.content)
            elif message.author.id in memberlistsRead("toRepeat", message.guild.id):
                msg = message.content
                while msg.endswith("!") or msg.endswith("?") or msg.endswith(".") or msg.endswith(",") or msg.endswith(";") or msg.endswith(":"):
                    msg = msg[:-1]
                msg = re.sub(' +', ' ', msg)
                if len(message.embeds) != 0:
                    await message.channel.send(":parrot: ** oi embeds are trash!!!**")
                else:
                    await message.channel.send(":parrot: **" + msg + "!!!**")

        if message.author.id in memberlistsRead("toDetectSwear", message.guild.id) and (profanity.contains_profanity(message.content.lower()) == True or any(s in ' '+message.content.lower()+' ' for s in AddSwearWordsDefault)):
            if preferencesRead(message.guild.id, "dsmba") == True:
                await message.delete()
                if preferencesRead(message.guild.id, "deletelog") in [n.name for n in message.guild.channels] and preferencesRead(message.guild.id, "deletelog") != None:
                    await discord.utils.get(message.guild.text_channels, name=preferencesRead(message.guild.id, "deletelog")).send(":parrot: **" + message.author.name + " (swearing):** " + message.content)
            if message.author.nick == None:
                nick = message.author.name
            else:
                nick = message.author.nick
            await message.channel.send(preferencesRead(message.guild.id, "swearalarm").replace("{author}", nick))
        if "<@!"+str(client.user.id)+">" in message.content:
            await message.channel.send(":parrot: **Oi why did you ping me!**")
    except:
        if not "discord.errors.Forbidden: 403 Forbidden (error code: 50001): Missing Access" in traceback.format_exc() and not "discord.errors.Forbidden: 403 Forbidden (error code: 50013): Missing Permissions" in traceback.format_exc() and message.content.startswith("parrot"):
            try:
                await message.channel.send(":parrot: **Oops, something went wrong. A report has been automatically sent to i\_\_\_\_7d already (if it's a bug), so there's no need to report manually!**")
                await message.channel.send("```" + traceback.format_exc() + "```")
                ach(message.author, 0)
            except:
                pass
            if not "Hi, this isn't a bug; this is the try/except test" in traceback.format_exc():
                try:
                    await client.get_channel(700946990678409276).send("Bug from " + VERSION + ": ```" + traceback.format_exc() + "```")
                except:
                    pass

def background():
    #await client.wait_until_ready()
    while not client.is_closed():
        #gc.collect()
        print("Before: " + str(gc.get_count()))
        gc.collect()
        print("After: " + str(gc.get_count()))
        process = psutil.Process(os.getpid())
        print(process.memory_info().rss/1000000)
        time.sleep(30)
        print("Before: " + str(gc.get_count()))
        gc.collect()
        print("After: " + str(gc.get_count()))
        process = psutil.Process(os.getpid())
        print(process.memory_info().rss/1000000)
        time.sleep(30)
        try: 
            #request = {"request": "r", "new": None}
            #code = len(currencyQueue)
            #currencyQueue.append(request)
            #while currencyQueue[code] == request:
            #    pass
            #users = currencyQueue[code]
            users = list(db["currency"].find({}))
            for u in range(0, len(users)):
                multiplier = 1 + 0.05*users[u]["level"] + sum([currstatsRead("ach")[z]["multiplier"] for z in users[u]["ach"]])

                for s in users[u]["parrots"]:
                    new = currstatsRead("parrots")[[t["name"] for t in currstatsRead("parrots")].index(s["breed"])]["tpm"]
                    new = new * multiplier
                    users[u]["balance"] = round(users[u]["balance"] + new, 1)

                for t in users[u]["bowls"]:
                    if t["inside"] != None:
                        foodStat = currstatsRead("shop")[[e["name"].lower() for e in currstatsRead("shop")].index(t["inside"])]
                        if random.random() <= foodStat["cpm"]*multiplier:
                            breed = numpy.random.choice([g["name"] for g in currstatsRead("parrots")], p=[h["chance"] for h in currstatsRead("parrots")])
                            users[u]["parrots"].append({"name": "Parrot #" + str(random.randint(0, 9999)), "breed": breed})
                            upXPSilent(users[u]["_id"], round(1 - currstatsRead("parrots")[[a["name"] for a in currstatsRead("parrots")].index(breed)]["chance"] * 10))

                            if breed in [w["breed"] for w in users[u]["notifs"]]:
                                users[u]["notifs"][[w["breed"] for w in users[u]["notifs"]].index(breed)]["qty"] += 1
                            else:
                                users[u]["notifs"].append({"breed": breed, "qty": 1})

                            if users[u]["bowls"][users[u]["bowls"].index(t)]["attractsleft"] == 1:
                                users[u]["bowls"][users[u]["bowls"].index(t)]["attractsleft"] = 0
                                users[u]["bowls"][users[u]["bowls"].index(t)]["inside"] = None
                            else:
                                users[u]["bowls"][users[u]["bowls"].index(t)]["attractsleft"] -= 1
                            users[u]["parrots"] = sorted(users[u]["parrots"], key=lambda k: k["name"])
                            try:
                                if len(users[u]["parrots"]) >= 50:
                                    ach(client.get_user(int(users[u])), 2)
                                if breed == "Caique":
                                    ach(client.get_user(int(users[u])), 3)
                            except:
                                pass
                #currencyQueue.append({"request": "w", "new": users})
                db["currency"].update_one({"_id": users[u]["_id"]}, {"$set": users[u]})
        except:
            print(traceback.format_exc())

#def garbage():
    #time.sleep(15)
    #while not client.is_closed():
        #pass
        #with open(os.path.join(sys.path[0], #"currency.json"), "r+") as f:
        #    with open("b_currency.json", "r+") as g:
        #        try:
        #            if len(json.loads(f)) >= len(json.loads(g)):
        #                shutil.copyfile("currency.json", "b_currency.json")
        #        except:
        #            shutil.copyfile("b_currency.json", "currency.json")
        #    f.close()
        #    g.close() 
        #print("Before: " + str(gc.get_count()))
        #gc.collect()
        #print("After: " + str(gc.get_count()))
        #process = psutil.Process(os.getpid())
        #print(process.memory_info().rss/1000000)
        #time.sleep(30)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for 'parrot help'"))
    print("Logged in as " + str(client.user.name) + " (" + str(client.user.id) + ")")
    print("Setup in " + str((int(round(time.time() * 1000)) - initstart)/1000) + "s")
    print('------')

keep_alive.keep_alive()
#gc.collect()
print(psutil.Process(os.getpid()).memory_info().rss/1000000)
Thread(target=background).start()
print("Background script started")
time.sleep(1)
print("Starting...")
client.run(TOKEN)