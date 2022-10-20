# Mr Bawk - v1.6.1 (14/4/20) by i____7d
VERSION = "v1.6.1 (14/4/20)"

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

import discord
import re
import keep_alive
import os
import sys
import json
import profanity_check
import random
import time

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    TOKEN = input("Token: ")

client = discord.Client()

SwearAlarmDefault = ":parrot: **BAAAAAAAAAAWWWWWWKKKKKKK BAAAAAWWWWWWWKKKKKKK ALERRRRRRT! {author} SWORE! BAAAAAAAAAWWWWWKKKKKK BAAAAAAAAAAAAAAAAAWWWWWWWWWWWWWKKKKKKKKKKKKK!!!!!!!!!! :rotating_light: :rotating_light: :rotating_light:**"
AddSwearWordsDefault = [" no u ", " no you ", " ok boomer ", " swear word ", " stfu ", " fk "]

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
        json.dump(d, f)
        f.close()

def memberlistsPop(key, subkey, index):
    with open(os.path.join(sys.path[0], "memberlists.json"), "r+") as f:
        d = json.load(f)
        d[str(key)][str(subkey)].pop(index)
        f.seek(0)
        f.truncate()
        json.dump(d, f)
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
        json.dump(d, f)
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
        json.dump(d, f)
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
        json.dump(d, f)
        f.close()

def quotesAdd(member, quote):
    with open(os.path.join(sys.path[0], "quotes.json"), "r+") as f:
        d = json.load(f)
        if not fullnameify(member) in d:
            d[fullnameify(member)] = []
        d[fullnameify(member)].append(quote)
        f.seek(0)
        f.truncate()
        json.dump(d, f)
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

@client.event
async def on_message(message):
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
            json.dump(f, e)
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
        json.dump(f, e)
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

    if msgLCase.startswith('parrot') and len(msgLCase.split(" ")) > 1 and any(s in msgLCase.split(" ")[1] for s in ["info", "help", "changelog", "ping", "list", "repeat", "stoprepeat", "detectswear", "stopdetectswear", "mute", "unmute", "inviteme", "s", "initinfo", "honk", "q"]):
        command = msgLCase.split(" ")
        
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
**help [master]** Loads this page. (Append "master" for Parrot Masters' commands.)
**info** View bot info.
**list [repeat/detectswear/mute]** See who is repeated/detected for swearing/muted. Append nothing for a list of everything.
**ping** Connection test
**changelog** View the new additions in this update, and what to look forward in the next update.
**inviteme** Invite me to your server!
**q** Quote someone, or view someone else's quotes. Type `parrot q` for more info.
**initinfo** Info on configuring the bot when you first invite it. **(VERY IMPORTANT!!!)** """)
        
        elif command[1] == "ping":
            await message.channel.send(":parrot: **Pong!\n`Time between command and reply: " + str(int(round(time.time() * 1000)) - start) + "ms; Bot latency: " + str(round(client.latency, 5)) + "ms`**")

        elif command[1] == "changelog":
            await message.channel.send(""":parrot: **This is what's new in the latest version! Very exciting, bawk!**
**Current version:** """ + VERSION + """
- When repeating a message with an emebd inside of it, the parrot no longer sends a '!!!' message before sending the 'oi embeds are trash' message.
- 'parrot quote' is now 'parrot q'.
- The additional list of swear words is now editable in a preference.
- The bot should not suddenly shut down now. I used an .env file.
-(.1) Pinging now shows latency.

**Next version:** v1.7
- a currency system
- possibly an overhaul of member lists where both the name and the tag are stored instead of just the name (this'll probably be an independent update together)
- Mailing
- history page
- tips page
- earrape
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
            await message.channel.send(":parrot: **Bawk! Here's my invite link to invite me to another server!**\nLink: https://discordapp.com/api/oauth2/authorize?client_id=691990367569969264&permissions=8192&scope=bot")

        elif command[1] == "initinfo":
            await message.channel.send(""":parrot: **Firstly, thank you so much for inviting me into your server! I'm sure i____7d will be glad too!**
Here are the steps to initialising me: (Note that this involves creating and giving roles so its for admins only)
1. Create a role called 'Parrot Master' (case sensitive).
2. Give yourself and some others the role.
That's it, enjoy :)""")

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
                    if msgLCase.replace("parrot stoprepeat ", "") in    toRepeatNicks:
                        memberlistsPop("toRepeat", message.guild.id,toRepeatNicks.index(msgLCase.replace("parrot stoprepeat ", "")))
                        await message.channel.send(":parrot: I've stopped repeating him, master!")
                    else:
                        await message.channel.send(":parrot: I'm not repeating  him, master!")

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

        if not message.guild.id in newServerAnnounceRead():
            newServerAnnounceAppend(message.guild.id)
            await message.channel.send(":parrot: **Oh hello! You seem to be the first person to try my commands.**\nIn fact, this is a :warning: **VERY IMPORTANT** :warning: message, at least for admins. If you're not an admin, go get one as soon as possible.\n**If you're an admin: ** Hi! I need some initialisation, do `parrot initinfo`. Thanks :)")
    
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
        

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

keep_alive.keep_alive()
client.run(TOKEN)