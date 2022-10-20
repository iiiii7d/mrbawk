# Mr Bawk - v1.7 (18/4/20) by i____7d
VERSION = "v1.7 (18/4/20)"

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
#1.7 - - Another value to ping. Messup command. Parrot now reacts when pinged. Currency system. Initinfo is removed. Raise command, for testing try/except. Bot now has a custom status.

import discord
import re
import keep_alive
import os
import sys
import json
import profanity_check
import random
import time
import requests
from io import BytesIO
from PIL import Image
import datetime
import asyncio
import math
import numpy
from threading import Thread
import traceback

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    TOKEN = input("Token: ")

client = discord.Client()

SwearAlarmDefault = ":parrot: **BAAAAAAAAAAWWWWWWKKKKKKK BAAAAAWWWWWWWKKKKKKK ALERRRRRRT! {author} SWORE! BAAAAAAAAAWWWWWKKKKKK BAAAAAAAAAAAAAAAAAWWWWWWWWWWWWWKKKKKKKKKKKKK!!!!!!!!!! :rotating_light: :rotating_light: :rotating_light:**"
AddSwearWordsDefault = [" no u ", " no you ", " ok boomer ", " swear word ", " stfu ", " fk "]

async def messUp(message):
    messupStart = int(round(time.time() * 1000))
    url = None
    try:
        url = message.attachments[0].url
    except IndexError: 
        url = message.content.replace("parrot messup ", "")
    distorted = None
    for ext in ['.jpg','.png','.jpeg']:
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
    #if size > 640000:
    #    #await message.channel.send(":parrot: **Sorry, your image is over 160000 pixels!**")
    #    #return
    #    maxsize = (800, 800)
    #    i = Image.open(BytesIO(r.content))
    #    i.thumbnail(maxsize, Image.ANTIALIAS)
    #    ig = Image.new(i.mode, i.size)
    #    pmap = i.load()
    #    pnew = ig.load()
    #    pvals = []
    #    size = ig.size[0] * ig.size[1]
                

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
            await m.edit(content=":parrot: **Messy! Messy! (" + str(round(t / size * 100)) + "% scrambled, " + msToTime(timeLeft) + " left)**\n**Check back at " + str(etc) + " GMT!**")
    await m.edit(content=":parrot: **Messy! Messy! (COMPLETED)**")
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

def memberlistsRead(key, subkey):
    with open(os.path.join(sys.path[0], "memberlists.json"), "r") as f:
        data = json.load(f)
        f.close()
        return data[str(key)][str(subkey)]

def memberlistsAppend(key, subkey, value):
    with open(os.path.join(sys.path[0], "memberlists.json"), "r+") as f:
        d = json.load(f)
        d[str(key)][str(subkey)].append(value)
        f.seek(0)
        f.truncate()
        json.dump(d, f, indent=4)
        f.close()

def memberlistsPop(key, subkey, index):
    with open(os.path.join(sys.path[0], "memberlists.json"), "r+") as f:
        d = json.load(f)
        d[str(key)][str(subkey)].pop(index)
        f.seek(0)
        f.truncate()
        json.dump(d, f, indent=4)
        f.close()

def preferencesRead(key, subkey):
    with open(os.path.join(sys.path[0], "preferences.json"), "r") as f:
        data = json.load(f)
        f.close()
        return data[str(key)][(subkey)]

def preferencesWrite(key, subkey, value):
    with open(os.path.join(sys.path[0], "preferences.json"), "r+") as f:
        d = json.load(f)
        d[str(key)][str(subkey)] = value
        f.seek(0)
        f.truncate()
        json.dump(d, f, indent=4)
        f.close()

def versionAnnounceRead():
    with open(os.path.join(sys.path[0], "versionannounce.json"), "r") as f:
        data = json.load(f)
        f.close()
        return data["announced"]

def versionAnnounceAppend(value):
    with open(os.path.join(sys.path[0], "versionannounce.json"), "r+") as f:
        d = json.load(f)
        d["announced"].append(value)
        f.seek(0)
        f.truncate()
        json.dump(d, f, indent=4)
        f.close()

def newServerAnnounceRead():
    with open(os.path.join(sys.path[0], "newserverannounce.json"), "r") as f:
        data = json.load(f)
        f.close()
        return data["init"]

def newServerAnnounceAppend(value):
    with open(os.path.join(sys.path[0], "newserverannounce.json"), "r+") as f:
        d = json.load(f)
        d["init"].append(value)
        f.seek(0)
        f.truncate()
        json.dump(d, f, indent=4)
        f.close()

def quotesAdd(member, quote):
    with open(os.path.join(sys.path[0], "quotes.json"), "r+") as f:
        d = json.load(f)
        if not fullnameify(member) in d:
            d[fullnameify(member)] = []
        d[fullnameify(member)].append(quote)
        f.seek(0)
        f.truncate()
        json.dump(d, f, indent=4)
        f.close()

def quotesView(memberfullname):
    with open(os.path.join(sys.path[0], "quotes.json"), "r") as f:
        d = json.load(f)
        member = ""
        if memberfullname == "anyone":
            member = random.choice(list(d))
            f.close()
            return [dividefullname(member)[0], d[member]]
        elif memberfullname in d:
            member = memberfullname
            f.close()
            return [dividefullname(member)[0], d[member]]
        else:
            f.close()
            return "nope"

def currencyRead(key, subkey):
    with open(os.path.join(sys.path[0], "currency.json"), "r") as f:
        data = json.load(f)
        f.close()
        return data[str(key)][str(subkey)]

def currencyWrite(key, subkey, value):
    with open(os.path.join(sys.path[0], "currency.json"), "r+") as f:
        d = json.load(f)
        d[str(key)][str(subkey)] = value
        f.seek(0)
        f.truncate()
        json.dump(d, f, indent=4)
        f.close()

def currstatsRead(key):
    with open(os.path.join(sys.path[0], "currstats.json"), "r") as f:
        data = json.load(f)
        f.close()
        return data[str(key)]

@client.event
async def on_message(message):
    try:
        start = int(round(time.time() * 1000))
        if message.author == client.user:
            return

        with open(os.path.join(sys.path[0], "memberlists.json"), "r+") as e:
            f = json.load(e)
            subkey = str(message.guild.id)
            if not subkey in f["toRepeat"]:
                f["toRepeat"][subkey] = []
            if not subkey in f["toDetectSwear"]:
                f["toDetectSwear"][subkey] = []
            if not subkey in f["toMute"]:
                f["toMute"][subkey] = []
                e.seek(0)
                e.truncate()
                json.dump(f, e, indent=4)
            e.close()

        with open(os.path.join(sys.path[0], "preferences.json"), "r+") as e:
            f = json.load(e)
            key = str(message.guild.id)
            if not key in f:
                f[key] = {}
            if not "deletelog" in f[key]:
                f[key]["deletelog"] = None
            if not "swearalarm" in f[key]:
                f[key]["swearalarm"] = SwearAlarmDefault
            if not "nvchannel" in f[key]:
                f[key]["nvchannel"] = None
            if not "dsmba" in f[key]:
                f[key]["dsmba"] = False
            if not "addswearwords" in f[key]:
                f[key]["addswearwords"] = AddSwearWordsDefault
            e.seek(0)
            e.truncate()
            json.dump(f, e, indent=4)
            e.close()

        if message.author.bot == False:
            with open(os.path.join(sys.path[0], "currency.json"), "r+") as e:
                f = json.load(e)
                key = str(message.author.id)
                if not key in f:
                    f[key] = {}
                if not "balance" in f[key]:
                    f[key]["balance"] = 50
                if not "bowl" in f[key]:
                    f[key]["bowl"] = None
                if not "parrots" in f[key]:
                    f[key]["parrots"] = []
                if not "inventory" in f[key]:
                    f[key]["inventory"] = []
                if not "lastdaily" in f[key]:
                    f[key]["lastdaily"] = 0
                if not "attractsleft" in f[key]:
                    f[key]["attractsleft"] = 0
                e.seek(0)
                e.truncate()
                json.dump(f, e, indent=4)
                e.close()

        if not message.guild.id in versionAnnounceRead():
            versionAnnounceAppend(message.guild.id)
            if preferencesRead(message.guild.id, "nvchannel") in [n.name for n in message.guild.channels] and preferencesRead(message.guild.id, "nvchannel") != None:
                channel = discord.utils.get(message.guild.text_channels, name=preferencesRead(message.guild.id, "nvchannel"))
                await channel.send(":parrot: **I have updated to " + VERSION + "! Type `parrot changelog` for more info on what has been added.**")
        
        message.content.replace(":regional_indicator_a:", "A")
        message.content.replace(":regional_indicator_b:", "B")
        message.content.replace(":regional_indicator_c:", "C")
        message.content.replace(":regional_indicator_d:", "D")
        message.content.replace(":regional_indicator_e:", "E")
        message.content.replace(":regional_indicator_f:", "F")
        message.content.replace(":regional_indicator_g:", "G")
        message.content.replace(":regional_indicator_h:", "H")
        message.content.replace(":regional_indicator_i:", "I")
        message.content.replace(":regional_indicator_j:", "J")
        message.content.replace(":regional_indicator_k:", "K")
        message.content.replace(":regional_indicator_l:", "L")
        message.content.replace(":regional_indicator_m:", "M")
        message.content.replace(":regional_indicator_n:", "N")
        message.content.replace(":regional_indicator_o:", "O")
        message.content.replace(":regional_indicator_p:", "P")
        message.content.replace(":regional_indicator_q:", "Q")
        message.content.replace(":regional_indicator_r:", "R")
        message.content.replace(":regional_indicator_s:", "S")
        message.content.replace(":regional_indicator_t:", "T")
        message.content.replace(":regional_indicator_u:", "U")
        message.content.replace(":regional_indicator_v:", "V")
        message.content.replace(":regional_indicator_w:", "W")
        message.content.replace(":regional_indicator_x:", "X")
        message.content.replace(":regional_indicator_y:", "Y")
        message.content.replace(":regional_indicator_z:", "Z")

        members = message.guild.members
        memberNames = [o.name.lower() for o in members]
        memberNamesUCase = [o.name for o in members]
        msgLCase = message.content.lower()

        if msgLCase.startswith('parrot') and len(msgLCase.split(" ")) > 1 and any(s in msgLCase.split(" ")[1] for s in ["info", "help", "changelog", "ping", "list", "repeat", "stoprepeat", "detectswear", "stopdetectswear", "mute", "unmute", "inviteme", "s", "honk", "q", "vcbawk", "c", "messup"]) and message.author.bot == False:
            command = msgLCase.split(" ")
            
            if not message.guild.id in newServerAnnounceRead():
                newServerAnnounceAppend(message.guild.id)
                await message.guild.create_role(name="Parrot Master")
                #await message.channel.send(":parrot: **Oh hello! You seem to be the first person to try my commands.**\nIn fact, this is a :warning: **VERY IMPORTANT** :warning: message, at least for admins. If you're not an admin, go get one as soon as possible.\n**If you're an admin: ** Hi! I need some initialisation, do `parrot initinfo`. Thanks :)")

            if command[1] == "info":
                await message.channel.send(""":parrot: **Bawk! Hello! I'm Mr Bawk, the Parrot!**\nI was created by i\_\_\_\_7d, my ultimate master!\nThis is """ + VERSION + """.
If you want to suggest a new feature, just contact i\_\_\_\_7d.
My pfp is from Unsplash.\nThat's all for now, bawk!""")

            elif command[1] == "help":
                if msgLCase == "parrot help master":
                    await message.channel.send(""":parrot: **Master commands - Sometimes masters need help as well!**\nAll my commands start with `parrot`.
Note for parameters: <> means mandatory, [] means optional.
**s ...** Parrot settings and preferences. Type `parrot s` for more info.
**repeat <name>** Repeats whatever someone says. Very annoying!
**stoprepeat <name>** Stops repeating someone. Put '\*' in the <name> slot to stop repeating everyone.
**detectswear <name>** Detects swearing, and sounds a text alarm when someone does.
**stopdetectswear <name>** Stops detecting someone for swearing. Put '\*' in the <name> slot to stop detecting everyone.
**mute <name>** Talks over what someone says in chat.
**unmute <name>** Stops talking over someone. Put '\*' in the <name> slot to unmute everyone.""")
                else:
                    await message.channel.send(""":parrot: **You need help? Here ya go!**\nAll my commands start with `parrot`.
Note for parameters: <> means mandatory, [] means optional.
**help [master]** Loads this page. (Append "master" for Parrot Masters' commands, __that can only be used if you have the automatically-created Parrot Master role.__)
**info** View bot info.
**list [repeat/detectswear/mute]** See who is repeated/detected for swearing/muted. Append nothing for a list of everything.
**ping** Connection test
**raise** Exception handling test
**changelog** View the new additions in this update, and what to look forward in the next update.
**inviteme** Invite me to your server!
**q** Quote someone, or view someone else's quotes. Type `parrot quote` for more info.
**c** The currency system. Type `parrot c` for more info.
**messup [url]** Scramble images! You either give the URL, or an image attachment.""")
            
            elif command[1] == "ping":
                ms = (message.id >> 22) + 1420070400000
                await message.channel.send(":parrot: **Pong!\n`Time between command reception and reply: " + str(int(round(time.time() * 1000)) - start) + "ms\nClient latency: " + str(round(client.latency * 1000, 5)) + "ms\nBot latency: " + str(int(round(time.time() * 1000)) - ms) + "ms`**")

            elif command[1] == "raise":
                raise NameError("Hi, this isn't a bug; this is the try/except test")

            elif command[1] == "changelog":
                await message.channel.send(""":parrot: **This is what's new in the latest version! Very exciting, bawk!**
**Current version:** """ + VERSION + """
- initinfo is now removed. The Parrot Master role is now created automatically. RIP Initinfo
- The parrot can now scramble images!
-- For low resolution images, scrambling can happen in a matter of minutes. For more high resolution ones, it can take hours. (The other time, it took 12 hours.) In the future, when it gets very laggy I might make a queue.
- A currency system! (a set-down-food-and-attract-animals one.)
- The parrot now reacts when mentioned.
- A new command: parrot raise, if you want to test the exception handling.
- The bot now has a custom status!

**Next version:** v1.8
- an overhaul of member lists where the ID is stored instead of just the name (this'll probably be an independent update together)
- More additions to the currency system
- that only other people can quote you and must not contain any swear words, and that only you can remove it (and you can flag it as -o if you find it offensive)
- history page
- tips page
- an announcing system that is more systematic
...and many more! If you would like to suggest, contact i\_\_\_\_7d.
*Note that some of these changes, and some bug fixes might go into a '0.?.x' version. These will be counted as part of the '0.x' version, and not separately.*""")

            elif command[1] == "list":
                if msgLCase.strip() == "parrot list repeat":
                    if len(memberlistsRead("toRepeat", message.guild.id)) == 0:
                        await message.channel.send(":parrot: **No members repeated, bawwwwk :(**")
                    else:
                        await message.channel.send(":parrot: **Repeated members:** " + ", ".join([a for a in memberlistsRead("toRepeat", message.guild.id)]))
                elif msgLCase.strip() == "parrot list detectswear":
                    if len(memberlistsRead("toDetectSwear", message.guild.id)) == 0:
                        await message.channel.send(":parrot: **No members detected for swearing, bawwwwk :(**")
                    else:
                        await message.channel.send(":parrot: **Members detected for swearing:** " + ", ".join([a for a in memberlistsRead("toDetectSwear", message.guild.id)]))
                elif msgLCase.strip() == "parrot list mute":
                    if len(memberlistsRead("toMute", message.guild.id)) == 0:
                        await message.channel.send(":parrot: **No members muted, bawwwwk :(**")
                    else:
                        await message.channel.send(":parrot: **Muted members:** " + ", ".join([a for a in memberlistsRead("toMute", message.guild.id)]))
                elif msgLCase.strip() == "parrot list":
                    if len(memberlistsRead("toRepeat", message.guild.id)) == 0:
                        await message.channel.send(":parrot: **Repeated members:** None")
                    else:
                        await message.channel.send(":parrot: **Repeated members:** " + ", ".join([a for a in memberlistsRead("toRepeat", message.guild.id)]))
                    if len(memberlistsRead("toDetectSwear", message.guild.id)) == 0:
                        await message.channel.send(":parrot: **Members detected for swearing:** None")
                    else:
                        await message.channel.send(":parrot: **Members detected for swearing:** " + ", ".join([a for a in memberlistsRead("toDetectSwear", message.guild.id)]))
                    if len(memberlistsRead("toMute", message.guild.id)) == 0:
                        await message.channel.send(":parrot: **Muted members:** None")
                    else:
                        await message.channel.send(":parrot: **Muted members:** " + ", ".join([a for a in memberlistsRead("toMute", message.guild.id)]))

            elif command[1] == "inviteme":
                await message.channel.send(":parrot: **Bawk! Here's my invite link to invite me to another server!**\nLink: https://discordapp.com/api/oauth2/authorize?client_id=691990367569969264&permissions=268478464&scope=bot")

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
                            if quote.content in quotesView(fullnameify(quote.author))[1]:
                                await message.channel.send(":parrot: That message has already been quoted!")
                            else:
                                quotesAdd(quote.author, quote.content)
                                await message.channel.send(":parrot: **Message quoted:** _**\"" + quote.content.replace("_", "\_") + "\"** - " + quote.author.name.replace("_", "\_") + "_")
                    elif msgLCase.strip() == "parrot q add":
                        await message.channel.send(""":parrot: **How to quote a message:**
1. Turn on developer mode. This allows you to copy IDs. (To do so, go to Settings > Appearance > Developer Mode.)
2. Click the menu of the message (aka More).
3. Click 'Copy ID'.
4. Do `parrot quote <paste here>`.""")
                elif len(command) > 2 and command[2] == "view":
                    params = " ".join(message.content.split()[3:]).strip()
                    memberfullname = params.split(" ")[0]
                    index = params.replace(memberfullname, "").strip()
                    if quotesView(memberfullname) == "nope":
                        await message.channel.send(":parrot: No quotes from him!")
                    else:
                        result = quotesView(memberfullname)
                        quotee = result[0]
                        quotelist = result[1]
                        if index == "":
                            l = ""
                            for q in quotelist:
                                l = l + str(quotelist.index(q) + 1) + ". \"" + q + "\"\n"
                            await message.channel.send(":parrot: **All quotes from " + quotee + ":** ```\n" + l + "```")

                        elif index.strip() == "any":
                            await message.channel.send(":parrot: _**\"" + random.choice(quotelist).replace("_", "\_") + "\"** - " + quotee.replace("_", "\_") + "_")
                        elif int(index) > 0 and int(index) <= len(quotelist):
                            await message.channel.send(":parrot: _**\"" + quotelist[int(index) - 1].replace("_", "\_") + "\"** - " + quotee.replace("_", "\_") + "_")
                elif msgLCase.strip() == "parrot q":
                    await message.channel.send(""":parrot: **This is my quoting function, welcome!**\nFor this quote function, start with `parrot quote`.
**add <ID>** Adds a quote to the database. Type `parrot quote add` by itself for instructions on how to add a quote.
**view <person> [index]** View someone's quotes.
- Put 'anyone' in the <person> slot to pick a random person.
- Put 'any' in the [index] slot to pick a random quote from a person.
- Leave [index] empty to get all quotes from someone.
- Do 'anyone any' for a random quote from a random person.
- Note that you have to give the full name (e.g. Foobar#1234) for the <person> slot.""")

            elif command[1] == "messup":
                await messUp(message)
                
            elif command[1] == "c":
                if len(command) > 2 and command[2] == "daily":
                    if (currencyRead(message.author.id, "lastdaily") + 86400000) < int(round(time.time() * 1000)):
                        currencyWrite(message.author.id, "balance", currencyRead(message.author.id, "balance") + 50)
                        currencyWrite(message.author.id, "lastdaily", int(round(time.time() * 1000)))
                        await message.channel.send(":parrot: **Here are your daily 50 twigs!**")
                    else:
                        d = msToTime(currencyRead(message.author.id, "lastdaily") + 86400000 - int(round(time.time() * 1000)))
                        t = datetime.datetime.fromtimestamp((currencyRead(message.author.id, "lastdaily") + 86400000)/1000).strftime("%H:%M:%S")
                        await message.channel.send(":parrot: **Sorry, I have not gathered my twigs get, please wait " + d + " until " + t + " GMT!**")
                elif len(command) > 2 and command[2] == "inv" or len(command) > 2 and command[2] == "inventory":
                    string = ":parrot: **Your Inventory:**\n"
                    if len(currencyRead(message.author.id, "inventory")) == 0:
                        string = string + "empty!"
                    for v in currencyRead(message.author.id, "inventory"): 
                        string = string + str(v["qty"]) + " " + v["name"] + "s\n"
                    await message.channel.send(string)
                elif len(command) > 2 and command[2] == "bal" or len(command) > 2 and command[2] == "balance":
                    await message.channel.send(":parrot: **You currently have " + str(currencyRead(message.author.id, "balance")) + " twigs. Bawk!**")
                elif len(command) > 2 and command[2] == "parrots":
                    string = ":parrot: **Your Parrots:**\n"
                    if len(currencyRead(message.author.id, "parrots")) == 0:
                        string = string + "none :("

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
                        string = string + "**" + str(w) + ".** " + v["name"] + " (" + v["breed"] + ")\n"
                        w += 1
                    await message.channel.send(string)
                elif len(command) > 2 and command[2] == "bowl":
                    if currencyRead(message.author.id, "bowl") == None:
                        await message.channel.send(":parrot: **There is nothing in your bowl currently.**")
                    else:
                        await message.channel.send(":parrot: **There is some " + currencyRead(message.author.id, "bowl") + " in your bowl.**")

                elif len(command) > 2 and command[2] == "placefood":
                    toPlace = msgLCase.replace("parrot c placefood ", "").strip()
                    if currencyRead(message.author.id, "bowl") != None:
                        await message.channel.send(":parrot: Your bowl is already filled!")
                    elif toPlace in [p["name"].lower() for p in currencyRead(message.author.id, "inventory")]:
                        currencyWrite(message.author.id, "bowl", toPlace)
                        if currencyRead(message.author.id, "inventory")[[r["name"].lower() for r in currencyRead(message.author.id, "inventory")].index(toPlace)]["qty"] == 1:
                            newInventory = currencyRead(message.author.id, "inventory")
                            del newInventory[[p["name"] for p in currencyRead(message.author.id, "inventory")].index(toPlace)]
                            currencyWrite(message.author.id, "inventory", newInventory)
                        else:
                            newInventory = currencyRead(message.author.id, "inventory")
                            newInventory[[p["name"] for p in currencyRead(message.author.id, "inventory")].index(toPlace)]["qty"] -= 1
                            currencyWrite(message.author.id, "inventory", newInventory)
                        currencyWrite(message.author.id, "attractsleft", currstatsRead("shop")[[p["name"].lower() for p in currstatsRead("shop")].index(toPlace)]["pax"])
                        await message.channel.send(":parrot: **You placed some " + toPlace + " into the bowl.**")
                    else:
                        await message.channel.send(":parrot: You do not have this food item!")
                elif len(command) > 2 and command[2] == "shop":
                    string = ":parrot: **Bawk! Thanks for stopping by the Bawkshop!**\n"
                    for i in currstatsRead("shop"):
                        string = string + "**" + str(i["name"]) + "** - " + str(i["cost"]) + " twigs\n_" + i["lore"] + "_\n- Chance of new parrot every minute: " + str(i["cpm"]) + "\n- No. of parrots it can attract before depleted: " + str(i["pax"]) + "\n"
                    await message.channel.send(string)
                elif len(command) > 2 and command[2] == "buy":
                    toBuy = msgLCase.replace("parrot c buy ", "").strip()
                    if toBuy in [p["name"].lower() for p in currstatsRead("shop")]:
                        toBuyStat = currstatsRead("shop")[[p["name"].lower() for p in currstatsRead("shop")].index(toBuy)]
                        if toBuyStat["cost"] > currencyRead(message.author.id, "balance"):
                            await message.channel.send(":parrot: **Sorry, you don't have enough twigs for the " + toBuy + "!**")
                        else:
                            currencyWrite(message.author.id, "balance", currencyRead(message.author.id, "balance") - toBuyStat["cost"])
                            if toBuy in [r["name"].lower() for r in currencyRead(message.author.id, "inventory")]:
                                newInventory = currencyRead(message.author.id, "inventory")
                                newInventory[[p["name"] for p in currencyRead(message.author.id, "inventory")].index(toBuy)]["qty"] += 1
                                currencyWrite(message.author.id, "inventory", newInventory)
                            else:
                                newInventory = currencyRead(message.author.id, "inventory")
                                newInventory.append({"name": toBuy, "qty": 1})
                                currencyWrite(message.author.id, "inventory", newInventory)
                            await message.channel.send(":parrot: **1 " + toBuy + " bought for " + str(toBuyStat["cost"]) + " twigs!**")
                    else:
                        await message.channel.send(":parrot: That item doesn't exist!")
                elif len(command) > 2 and command[2] == "how":
                    await message.channel.send(""":parrot: **Hi! Here is how to use this currency system!**
When you first start, you get 50 twigs. You go to the shop and buy some food. You then place some food in your bowl to attract parrots. Every minute, there is a chance that you will get a new parrot.
Currently, all parrots are cockatiels; more breeds will come in the future versions. Every minute, each parrot picks up a certain number of twigs for you. As for cockatiels, each would pick up 1 twig per minute.
This is currently very simplistic and this currency system is still under development, so comment to i\_\_\_\_7d if it is either too slow or fast for you!""")
                elif msgLCase.strip() == "parrot c":
                    await message.channel.send(""":parrot: **Bawk! Here's the help page for the currency system!**\nFor this currency function, start with `parrot c`.
**shop** Shop for items, especially foods
**buy** Buy items from the shop.
**placefood** Put food into the bowl.
**inv/inventory** View your inventory.
**bowl** View what's inside your bowl.
**parrots** View your parrots.
**bal/balance** View your balance.
**daily** Claim your daily twigs.
**how** View the tutorial for this system.""")
                        


            if "Parrot Master" in [y.name for y in message.author.roles] or message.author.id == 644052617500164097:
                if command[1] == "repeat" and len(command) > 2:
                    if msgLCase.replace("parrot repeat ", "") in memberNames:
                        nameIndex = memberNames.index(msgLCase.replace("parrot repeat ", ""))
                        if memberNames[nameIndex] in memberlistsRead("toRepeat", message.guild.id):
                            await message.channel.send(":parrot: I'm repeating him already, master!")
                        else:
                            memberlistsAppend("toRepeat", message.guild.id, memberNamesUCase[nameIndex])
                            await message.channel.send(":parrot: I'm going to repeat whatever he says, master!")
                    else:
                        await message.channel.send(":parrot: There is no one with that name, master!")

                elif command[1] == "stoprepeat" and len(command) > 2:
                    if msgLCase.replace("parrot stoprepeat ", "") == "*":
                        for blah in memberlistsRead("toRepeat", message.guild.id):
                            memberlistsPop("toRepeat", message.guild.id, 0)
                        await message.channel.send(":parrot: I've stopped repeating everyone, master!")
                    else:
                        toRepeatNicks = [p.lower() for p in memberlistsRead("toRepeat", message.guild.id)]
                        if msgLCase.replace("parrot stoprepeat ", "") in toRepeatNicks:
                            memberlistsPop("toRepeat", message.guild.id,toRepeatNicks.index(msgLCase.replace("parrot stoprepeat ", "")))
                            await message.channel.send(":parrot: I've stopped repeating him, master!")
                        else:
                            await message.channel.send(":parrot: I'm not repeating him, master!")

                elif command[1] == "detectswear" and len(command) > 2:
                    if msgLCase.replace("parrot detectswear ", "") in memberNames:
                        nameIndex = memberNames.index(msgLCase.replace("parrot detectswear ", ""))
                        if memberNames[nameIndex] in memberlistsRead("toDetectSwear", message.guild.id):
                            await message.channel.send(":parrot: I'm detecting him already, master!")
                        else:
                            memberlistsAppend("toDetectSwear", message.guild.id, memberNamesUCase[nameIndex])
                            await message.channel.send(":parrot: I'm going to detect if he swears, master!")
                    else:
                        await message.channel.send(":parrot: There is no one with that name, master!")

                elif command[1] == "stopdetectswear" and len(command) > 2:
                    if msgLCase.replace("parrot stopdetectswear ", "") == "*":
                        for blah in memberlistsRead("toDetectSwear", message.guild.id):
                            memberlistsPop("toDetectSwear", message.guild.id, 0)
                        await message.channel.send(":parrot: I've stopped detecting everyone, master!")
                    else:
                        toDetectSwearNicks = [p.lower() for p in memberlistsRead("toDetectSwear", message.guild.id)]
                        if msgLCase.replace("parrot stopdetectswear ", "") in toDetectSwearNicks:
                            memberlistsPop("toDetectSwear", message.guild.id, toDetectSwearNicks.index(msgLCase.replace("parrot stopdetectswear ", "")))
                            await message.channel.send(":parrot: I've stopped detecting him, master!")
                        else:
                            await message.channel.send(":parrot: I'm not detecting him, master!")

                elif command[1] == "mute" and len(command) > 2:
                    if msgLCase.replace("parrot mute ", "") in memberNames:
                        nameIndex = memberNames.index(msgLCase.replace("parrot mute ", ""))
                        if memberNames[nameIndex] in memberlistsRead("toMute", message.guild.id):
                            await message.channel.send(":parrot: I'm muting him already, master!")
                        else:
                            memberlistsAppend("toMute", message.guild.id, memberNamesUCase[nameIndex])
                            await message.channel.send(":parrot: I'm going to make noise over what he says, master!")
                    else:
                        await message.channel.send(":parrot: There is no one with that name, master!")

                elif command[1] == "unmute" and len(command) > 2:
                    if msgLCase.replace("parrot unmute ", "") == "*":
                        for blah in memberlistsRead("toMute", message.guild.id):
                            memberlistsPop("toMute", message.guild.id, 0)
                        await message.channel.send(":parrot: I've stopped muting everyone, master!")
                    else:
                        toMuteNicks = [p.lower() for p in memberlistsRead("toMute", message.guild.id)]
                        if msgLCase.replace("parrot unmute ", "") in toMuteNicks:
                            memberlistsPop("toMute", message.guild.id, toMuteNicks.index(msgLCase.replace("parrot unmute ", "")))
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
                        elif msgLCase == "parrot s v nvchannel":
                            if preferencesRead(message.guild.id, "nvchannel") != None:
                                await message.channel.send(":parrot: Current channel set for announcing new versions: #" + str(preferencesRead(message.guild.id, "nvchannel")))
                            else:
                                await message.channel.send(":parrot: Current channel set for announcing new versions: None")
                        elif msgLCase == "parrot s v dsmba":
                            await message.channel.send(":parrot: Delete message containing swear word before sounding swear alarm: " + str(preferencesRead(message.guild.id, "dsmba")))
                        elif msgLCase == "parrot s v addswearwords":
                            await message.channel.send(":parrot: Additional swear words: " + ", ".join("'"+w+"'" for w in preferencesRead(message.guild.id, "addswearwords")))
                        elif msgLCase.strip() == "parrot s v":
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
                            #nvchannel
                            if preferencesRead(message.guild.id, "nvchannel") != None:
                                await message.channel.send(":parrot: Current channel set for announcing new versions: #" + str(preferencesRead(message.guild.id, "nvchannel")))
                            else:
                                await message.channel.send(":parrot: Current channel set for announcing new versions: None")
                            #dsmba
                            await message.channel.send(":parrot: Delete message containing swear word before sounding swear alarm: " + str(preferencesRead(message.guild.id, "dsmba")))
                            #addswearwords
                            await message.channel.send(":parrot: Additional swear words: " + ", ".join("'"+w+"'" for w in preferencesRead(message.guild.id, "addswearwords")))

                    if len(command) > 2 and command[2] == "deletelog":
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
                    elif len(command) > 2 and command[2] == "nvchannel":
                        channelName = msgLCase.replace("parrot s nvchannel ", "")
                        if channelName in [n.name for n in message.guild.channels]:
                            preferencesWrite(message.guild.id, "nvchannel", channelName)
                            await message.channel.send(":parrot: Channel for new version announcements messages has been set to #" + channelName + "!")
                        else:
                            await message.channel.send(":parrot: There is no such channel '#" + channelName + "'!")
                    elif len(command) > 2 and command[2] == "nvchannelreset":
                        preferencesWrite(message.guild.id, "nvchannel", None)
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
                            addword = msgLCase.replace("parrot s addswearwords add:", "")
                            if not addword in preferencesRead(message.guild.id, "addswearwords"):
                                oldlist = preferencesRead(message.guild.id, "addswearwords")
                                oldlist.append(addword)
                                preferencesWrite(message.guild.id, "addswearwords", oldlist)
                                await message.channel.send(":parrot: Added '" + addword + "' to the list of additional swear words!")
                            else:
                                await message.channel.send(":parrot: That word/phrase has already been added!")
                        elif msgLCase.startswith("parrot s addswearwords remove:"):
                            removeword = msgLCase.replace("parrot s addswearwords remove:", "")
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

                    elif msgLCase.strip() == "parrot s":
                        await message.channel.send(""":parrot: **Bawk! This is the settings help page!**
For changing settings, use 'parrot s <preference> <option>'.
_If you are editing a <message> and want to state the author of the message it is replying to, use '{author}'._
**v [preference]** Views all preference values.
**deletelog <channel>** Sets the channel where deleted messages from muting are sent to.
**- deletelogreset** Resets the channel for deletelogging to no channel.
**swearalarm <message>** Sets the swear alarm.
**- swearalarmreset** Resets the swear alarm.
**nvchannel <channel>** (short for newversionchannel) Sets the channel where announcements about new versions will be made.
**- nvchannelreset** Resets the channel for version announcing to no channel.
**dsmba <true/false>** (short for deleteswearmsgbeforealarm) When someone swears while they are being detected, choose whether to delete the message with the swear word inside of it or not before sounding the alarm. Note that deleted messages will go to deletelog.
**addswearwords...** Edits the list of additional swear words to detect.
**- ...add:<word>** Adds a word or phrase to the list.
**- ...remove:<word>** Removes a word or phrase from the list.
**- ...reset** Resets the list to its default.""")
        
        else:
            if message.author.name in memberlistsRead("toMute", message.guild.id):
                await message.delete()
                await message.channel.send(":parrot: **Bawk bawk bawk bawk bawk bawk! " + message.author.name + " said nothing!**")
                if preferencesRead(message.guild.id, "deletelog") in [n.name for n in message.guild.channels] and preferencesRead(message.guild.id, "deletelog") != None:
                    await discord.utils.get(message.guild.text_channels, name=preferencesRead(message.guild.id, "deletelog")).send(":parrot: **" + message.author.name + ":** " + message.content)
            elif message.author.name in memberlistsRead("toRepeat", message.guild.id):
                msg = message.content
                while msg.endswith("!") or msg.endswith("?") or msg.endswith(".") or msg.endswith(",") or msg.endswith(";") or msg.endswith(":"):
                    msg = msg[:-1]
                msg = re.sub(' +', ' ', msg)
                if len(message.embeds) != 0:
                    await message.channel.send(":parrot: ** oi embeds are trash!!!**")
                else:
                    await message.channel.send(":parrot: **" + msg + "!!!**")


        if message.author.name in memberlistsRead("toDetectSwear", message.guild.id) and (profanity_check.predict([message.content.lower()])[0] == 1 or any(s in ' '+message.content.lower()+' ' for s in AddSwearWordsDefault)):
            if preferencesRead(message.guild.id, "dsmba") == True:
                await message.delete()
                if preferencesRead(message.guild.id, "deletelog") in [n.name for n in message.guild.channels] and preferencesRead(message.guild.id, "deletelog") != None:
                    await discord.utils.get(message.guild.text_channels, name=preferencesRead(message.guild.id, "deletelog")).send(":parrot: **" + message.author.name + " (swearing):** " + message.content)
            await message.channel.send(preferencesRead(message.guild.id, "swearalarm").replace("{author}", message.author.name))
        if str(client.user.mention) in message.content:
            await message.channel.send(":parrot: **Oi why did you ping me!**")
    except:
        await message.channel.send(":parrot: **Oops, something went wrong. A report has been automatically sent to i\_\_\_\_7d already (if it's a bug), so there's no need to report manually!**")
        await message.channel.send("```" + traceback.format_exc() + "```")
        if not "Hi, this isn't a bug; this is the try/except test" in traceback.format_exc():
            await client.get_channel(700946990678409276).send("Bug from " + VERSION + ": ```" + traceback.format_exc() + "```")

def background():
    try:
        #await client.wait_until_ready()
        while not client.is_closed():
            time.sleep(60)
            with open(os.path.join(sys.path[0], "currency.json"), "r") as f:
                users = json.load(f)
                f.close()
            for u in users.keys():
                for s in users[u]["parrots"]:
                    new = currstatsRead("parrots")[[t["name"] for t in currstatsRead("parrots")].index(s["breed"])]["tpm"]
                    currencyWrite(u, "balance", currencyRead(u, "balance") + new)

                if users[u]["bowl"] != None:
                    foodStat = currstatsRead("shop")[[e["name"].lower() for e in currstatsRead("shop")].index(users[u]["bowl"])]
                    if random.random() <= foodStat["cpm"]:
                        with open(os.path.join(sys.path[0], "currency.json"), "r+") as f:
                            d = json.load(f)
                            breed = numpy.random.choice([g["name"] for g in currstatsRead("parrots")], p=[h["chance"] for h in currstatsRead("parrots")])
                            d[u]["parrots"].append({"name": "Parrot #" + str(len(users[u]["parrots"])), "breed": breed})
                            if d[u]["attractsleft"] == 1:
                                d[u]["attractsleft"] = 0
                                d[u]["bowl"] = None
                            else:
                                d[u]["attractsleft"] -= 1
                            f.seek(0)
                            f.truncate()
                            json.dump(d, f, indent=4)
                            f.close()
    except:
        print(traceback.format_exc())

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for 'parrot help'"))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

Thread(target=background).start()
keep_alive.keep_alive()
client.run(TOKEN)