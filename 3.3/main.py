
# Mr Bawk - v1.3.3 (28/3/20) by i____7d

#v1.0 - 24/3/20 - Added repeating function, info page
#v1.0.1 - 26/3/20 - Added help pages, added :parrot: to every dialogue. Commands can now be in lowercase.
#v1.1 - 26/3/20 - Added swearing detection, muting function. Now detects if message has embeds during repeating.
#v1.2 - 27/3/20 - Added lists for members repeated, detected for swearing, or muted. Also added a function to view messages deleted from muting. Added pinging.
#v1.3 - 28/3/20 - Added changelog. All lists to repeat/detectswear/mute are now in a json file. Multiple server support.
#v1.3.1 - 28/3/20 - in lists, names are no longer all lowercase. All instances of "player" is replaced with "member". :P
#v1.3.2 - 28/3/20 - fixed small bug where members could not be repeated/detected for swearing/muted due to lowercase and stuff
#v1.3.3 - 28/3/20 - fixed small bug where members could start their messages wth "parrot" to countervent mute

#TODO: Mute & Unmute all users, quote things & save to file, etc etc
import discord
import re
import keep_alive
import os
import sys
import json

TOKEN = 'asdfasdfasdfasdfadf'

client = discord.Client()

toRepeat = []
toDetectSwear = []
toMute = []
mutedmsgs = []

def memberlistsRead(key, subkey):
    with open(os.path.join(sys.path[0], "memberlists.json"), "r") as f:
        data = json.load(f)
        f.close()
        return data[key][str(subkey)]

def memberlistsAppend(key, subkey, value):
    with open(os.path.join(sys.path[0], "memberlists.json"), "r+") as f:
        d = json.load(f)
        d[key][str(subkey)].append(value)
        f.seek(0)
        f.truncate()
        json.dump(d, f)
        f.close()

def memberlistsPop(key, subkey, index):
    with open(os.path.join(sys.path[0], "memberlists.json"), "r+") as f:
        d = json.load(f)
        d[key][str(subkey)].pop(index)
        f.seek(0)
        f.truncate()
        json.dump(d, f)
        f.close()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    with open(os.path.join(sys.path[0], "memberlists.json"), "r+") as e:
        f = json.load(e)
        subkey = str(message.guild.id)
        if not str(message.guild.id) in f["toRepeat"]:
            f["toRepeat"][subkey] = []
            f["toDetectSwear"][subkey] = []
            f["toMute"][subkey] = []
            e.seek(0)
            e.truncate()
            json.dump(f, e)
        e.close()
    
    if message.content.lower().startswith('parrot') and len(message.content.split(" ")) > 1 and any(s in ' '+message.content.lower()+' ' for s in [" info ", " help ", " changelog ", " ping ", " list ", " repeat ", " stoprepeat ", " detectswear ", " stopdetectswear ", " mute ", " unmute ", " mutelog ", " mutelogreset "]):
        members = message.guild.members
        memberNicks = [o.name.lower() for o in members]
        memberNicksUCase = [o.name for o in members]
        msgLCase = message.content.lower()
        command = msgLCase.split(" ")
        
        if command[1] == "info":
            await message.channel.send(""":parrot: **Bawk! Hello! I'm Mr Bawk, the Parrot!**\nI was created by i\_\_\_\_7d, my ultimate master!\nThis is v1.3.3 (28/3/20).
If you want to suggest a new feature, just contact i\_\_\_\_7d.
My pfp is from Unsplash.\nThat's all for now, bawk!""")

        elif command[1] == "help":
            if msgLCase == "parrot help master":
                await message.channel.send(""":parrot: **Master commands - Sometimes masters need help as well!**\nAll my commands start with `parrot`.
Note for parameters: <> means mandatory, [] means optional.
**repeat <name>** Repeats whatever someone says. Very annoying!
**stoprepeat <name>** Stops repeating someone.
**detectswear <name>** Detects swearing, and sounds a text alarm when someone does.
**stopdetectswear <name>** Stops detecting someone for swearing.
**mute <name>** Talks over what someone says.
**unmute <name>** Stops talking over someone.
**mutelog <channel>** Sets the channel where deleted messages from muting are sent to.
**mutelogreset** Resets the channel for mutelogging.""")
            else:
                await message.channel.send(""":parrot: **You need help? Here ya go!**\nAll my commands start with `parrot`.
Note for parameters: <> means mandatory, [] means optional.
**help [master]** Loads this page. (Append "master" for Parrot's Masters' commands.)
**info** View bot info.
**list <repeat/detectswear/muted>** See who is repeated/detected for swearing/muted.
**ping** Connection test
**changelog** View the new additions in this update, and what to look forward in the next update.""")
        
        elif command[1] == "ping":
            await message.channel.send(":parrot: **Pong!**")

        elif command[1] == "changelog":
            await message.channel.send(""":parrot: **This is what's new in the latest version! Very exciting, bawk!**
**Current version:** v1.3.3 (28/3/20)
- Added changelogs
- Multi-server support
- The lists of repeated, detected-for-swearing, and muted members are now all in a json file, so that when updating, the masters do not need to do a mass adding back :D
-(.1) In lists, names are no longer all lowercase. All instances of "player" is replaced with "member". :P

**Next version:** v.1.4 (possibly 30/3/20)
- For masters, repeat/detect for swearing/mute or unrepeat/undetect for swearing/unmute all members
- make the parrot quote something
- invite link command
- make swearing alarm editable
...and many more! If you would like to suggest, contact i____7d.
*Note that some of these changes might go into a '0.?.x' version. These will be counted as part of the '0.x' version, and not separately.*""")

        elif command[1] == "list":
            if msgLCase == "parrot list repeat":
                if len(memberlistsRead("toRepeat", message.guild.id)) == 0:
                    await message.channel.send(":parrot: **No members repeated, bawwwwk :(**")
                else:
                    await message.channel.send(":parrot: **Repeated members:** " + ", ".join([a for a in memberlistsRead("toRepeat", message.guild.id)]))
            elif msgLCase == "parrot list detectswear":
                if len(memberlistsRead("toDetectSwear", message.guild.id)) == 0:
                    await message.channel.send(":parrot: **No members detected for swearing, bawwwwk :(**")
                else:
                    await message.channel.send(":parrot: **members detected for swearing:** " + ", ".join([a for a in memberlistsRead("toDetectSwear", message.guild.id)]))
            elif msgLCase == "parrot list muted":
                if len(memberlistsRead("toMute", message.guild.id)) == 0:
                    await message.channel.send(":parrot: **No members muted, bawwwwk :(**")
                else:
                    await message.channel.send(":parrot: **Muted members:** " + ", ".join([a for a in memberlistsRead("toMute", message.guild.id)]))

        if "Parrot's Master" in [y.name for y in message.author.roles]:
            if command[1] == "repeat" and len(command) > 2:
                if msgLCase.replace("parrot repeat ", "") in memberNicks:
                    nameIndex = memberNicks.index(msgLCase.replace("parrot repeat ", ""))
                    if memberNicks[nameIndex] in memberlistsRead("toRepeat", message.guild.id):
                        await message.channel.send(":parrot: I'm repeating him already, master!")
                    else:
                        memberlistsAppend("toRepeat", message.guild.id, memberNicksUCase[nameIndex])
                        await message.channel.send(":parrot: I'm going to repeat whatever he says, master!")
                else:
                    await message.channel.send(":parrot: There is no one with that name, master!")

            elif command[1] == "stoprepeat" and len(command) > 2:
                toRepeatNicks = [p.lower() for p in memberlistsRead("toRepeat", message.guild.id)]
                if msgLCase.replace("parrot stoprepeat ", "") in toRepeatNicks:
                    memberlistsPop("toRepeat", message.guild.id, toRepeatNicks.index(msgLCase.replace("parrot stoprepeat ", "")))
                    await message.channel.send(":parrot: I've stopped repeating him, master!")
                else:
                    await message.channel.send(":parrot: I'm not repeating him, master!")

            elif command[1] == "detectswear" and len(command) > 2:
                if msgLCase.replace("parrot detectswear ", "") in memberNicks:
                    nameIndex = memberNicks.index(msgLCase.replace("parrot detectswear ", ""))
                    if memberNicks[nameIndex] in memberlistsRead("toDetectSwear", message.guild.id):
                        await message.channel.send(":parrot: I'm detecting him already, master!")
                    else:
                        memberlistsAppend("toDetectSwear", message.guild.id, memberNicksUCase[nameIndex])
                        await message.channel.send(":parrot: I'm going to detect if he swears, master!")
                else:
                    await message.channel.send(":parrot: There is no one with that name, master!")

            elif command[1] == "stopdetectswear" and len(command) > 2:
                toDetectSwearNicks = [p.lower() for p in memberlistsRead("toDetectSwear", message.guild.id)]
                if msgLCase.replace("parrot stopdetectswear ", "") in toDetectSwearNicks:
                    memberlistsPop("toDetectSwear", message.guild.id, toDetectSwearNicks.index(msgLCase.replace("parrot stopdetectswear ", "")))
                    await message.channel.send(":parrot: I've stopped detecting him, master!")
                else:
                    await message.channel.send(":parrot: I'm not detecting him, master!")

            elif command[1] == "mute" and len(command) > 2:
                if msgLCase.replace("parrot mute ", "") in memberNicks:
                    nameIndex = memberNicks.index(msgLCase.replace("parrot mute ", ""))
                    if memberNicks[nameIndex] in memberlistsRead("toMute", message.guild.id):
                        await message.channel.send(":parrot: I'm muting him already, master!")
                    else:
                        memberlistsAppend("toMute", message.guild.id, memberNicksUCase[nameIndex])
                        await message.channel.send(":parrot: I'm going to make noise over what he says, master!")
                else:
                    await message.channel.send(":parrot: There is no one with that name, master!")

            elif command[1] == "unmute" and len(command) > 2:
                toMuteNicks = [p.lower() for p in memberlistsRead("toMute", message.guild.id)]
                if msgLCase.replace("parrot unmute ", "") in toMuteNicks:
                    memberlistsPop("toMute", message.guild.id, toMuteNicks.index(msgLCase.replace("parrot unmute ", "")))
                    await message.channel.send(":parrot: I've stopped muting him, master!")
                else:
                    await message.channel.send(":parrot: I'm not muting him, master!")

            elif command[1] == "mutelog":
                channelName = msgLCase.replace("parrot mutelog ", "")
                if channelName in [n.name for n in message.guild.channels]:
                    if len(mutedmsgs) == 0:
                      mutedmsgs.append(discord.utils.get(message.guild.text_channels, name=channelName))
                    mutedmsgs[0] = discord.utils.get(message.guild.text_channels, name=channelName)
                    await message.channel.send(":parrot: Channel for deleted messages has been set to #" + channelName + "!")
                else:
                    await message.channel.send(":parrot: There is no such channel '#" + channelName + "'!")
            elif command[1] == "mutelogreset":
              mutedmsgs.clear()
              await message.channel.send(":parrot: Channel for deleted messages reset! There is now no channel for deleted messages to go to.")

    
    else:
        if message.author.name in memberlistsRead("toMute", message.guild.id):
            await message.delete()
            await message.channel.send(":parrot: **Bawk bawk bawk bawk bawk bawk! " + message.author.name + " said nothing!**")
            if len(mutedmsgs) != 0:
              await mutedmsgs[0].send(":parrot: **" + message.author.name + ":** " + message.content)
        elif message.author.name in memberlistsRead("toRepeat", message.guild.id):
            msg = message.content
            while msg.endswith("!") or msg.endswith("?") or msg.endswith(".") or msg.endswith(",") or msg.endswith(";") or msg.endswith(":"):
                msg = msg[:-1]
            msg = re.sub(' +', ' ', msg)
            await message.channel.send(":parrot: **" + msg + "!!!**")
            if len(message.embeds) != 0:
                await message.channel.send(":parrot: ** oi embeds are trash!!!**")

    if message.author.name in memberlistsRead("toDetectSwear", message.guild.id) and any(s in message.content.lower() for s in ["fuck", "shit", "ass", "cunt", "midget", " no u ", " no you ", " ok boomer ", " fk "]):
        await message.channel.send(":parrot: **BAAAAAAAAAAWWWWWWKKKKKKK BAAAAAWWWWWWWKKKKKKK ALERRRRRRT! " + message.author.name + " SWORE! BAAAAAAAAAWWWWWKKKKKK BAAAAAAAAAAAAAAAAAWWWWWWWWWWWWWKKKKKKKKKKKKK!!!!!!!!!! :rotating_light: :rotating_light: :rotating_light:**")
        

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

keep_alive.keep_alive()
client.run(TOKEN)
