# Mr Bawk - v1.4.2 (30/3/20) by i____7d

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


import discord
import re
import keep_alive
import os
import sys
import json
import profanity_check

TOKEN = ''
#TOKEN = input("Token: ")

client = discord.Client()

mutedmsgs = []
SwearAlarmDefault = ":parrot: **BAAAAAAAAAAWWWWWWKKKKKKK BAAAAAWWWWWWWKKKKKKK ALERRRRRRT! {author} SWORE! BAAAAAAAAAWWWWWKKKKKK BAAAAAAAAAAAAAAAAAWWWWWWWWWWWWWKKKKKKKKKKKKK!!!!!!!!!! :rotating_light: :rotating_light: :rotating_light:**"

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
        return data[str(key)][str(subkey)]

def preferencesWrite(key, subkey, value):
    with open(os.path.join(sys.path[0], "preferences.json"), "r+") as f:
        d = json.load(f)
        d[str(key)][str(subkey)] = value
        f.seek(0)
        f.truncate()
        json.dump(d, f)
        f.close()

@client.event
async def on_message(message):
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
            f[key]["mutelog"] = None
            f[key]["swearalarm"] = SwearAlarmDefault
            e.seek(0)
            e.truncate()
            json.dump(f, e)
        e.close()
    
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
    memberNicks = [o.name.lower() for o in members]
    memberNicksUCase = [o.name for o in members]
    msgLCase = message.content.lower()

    if msgLCase.startswith('parrot') and len(msgLCase.split(" ")) > 1 and any(s in msgLCase.split(" ")[1] for s in ["info", "help", "changelog", "ping", "list", "repeat", "stoprepeat", "detectswear", "stopdetectswear", "mute", "unmute", "inviteme", "s", "initinfo"]):
        command = msgLCase.split(" ")
        
        if command[1] == "info":
            await message.channel.send(""":parrot: **Bawk! Hello! I'm Mr Bawk, the Parrot!**\nI was created by i\_\_\_\_7d, my ultimate master!\nThis is v1.4.2 (30/3/20).
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
**initinfo** **Info on configuring the bot when you first invite it. (VERY IMPORTANT!!!)** """)
        
        elif command[1] == "ping":
            await message.channel.send(":parrot: **Pong!**")

        elif command[1] == "changelog":
            await message.channel.send(""":parrot: **This is what's new in the latest version! Very exciting, bawk!**
**Current version:** v1.4.2 (30/3/20)
- All regional indicator emojis are now treated as ordinary characters.
- Employed profanity-check to strengthen swearing detection filter.
- Invite Link command
- 'parrot list muted' is now 'parrot list mute'. This is for consistency purpouses.
- 'parrot list' now shows all 3 lists instead of nothing.
- 'parrot s' for Parrot Masters. Now, the swear alarm and the mutelogging command are editable.
-- Last time, the mutelogging had a bug where all servers' muted messages go into a channel in only one server, and not the channel in the respective servers. This has been fixed through a json file :D
- Parrot masters can now stoprepeat/stopdetectswear/unmute everyone.
- The role is now 'Parrot Master' instead of 'Parrot's Master'.
- Initialising Information, for when you first invite the bot.

**Next version:** v1.5 (???)
- make the parrot quote something
- a currency system maybe?
- announcement when theres a new update
- an overhaul of member lists where both the name and the tag are stored instead of just the name
- history page
- tips page
...and many more! If you would like to suggest, contact i____7d.
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
            await message.channel.send(":parrot: **Bawk! Here's my invite link to invite me to another server!**\nLink: https://discordapp.com/api/oauth2/authorize?client_id=691990367569969264&permissions=0&scope=bot")

        elif command[1] == "initinfo":
            await message.channel.send(""":parrot: **Firstly, thank you so much for inviting me into your server! I'm sure i____7d will be glad too!**
Here are the steps to initialising me: (Note that this involves creating and giving roles so its for admins only)
1. Create a role called 'Parrot Master' (case sensitive).
2. Give yourself and some others the role.
That's it, enjoy :)""")

        if "Parrot Master" in [y.name for y in message.author.roles]:
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
                    if msgLCase == "parrot s v mutelog":
                        if preferencesRead(message.guild.id, "mutelog") != None:
                            await message.channel.send(":parrot: Current channel set for mutelog: #" + str(preferencesRead(message.guild.id, "mutelog")))
                        else:
                            await message.channel.send(":parrot: Current channel set for mutelog: None")
                    elif msgLCase == "parrot s v swearalarm":
                        await message.channel.send(":parrot: Current swear alarm message: " + preferencesRead(message.guild.id, "swearalarm"))
                    elif msgLCase.strip() == "parrot s v":
                        await message.channel.send(":parrot: Current channel set for mutelog: #" + str(preferencesRead(message.guild.id, "mutelog")))
                        if len(preferencesRead(message.guild.id, "swearalarm")) > 20:
                            SATruncated = str(preferencesRead(message.guild.id, "swearalarm"))[0:20] + "..."
                        else:
                            SATruncated = str(preferencesRead(message.guild.id, "swearalarm"))
                        await message.channel.send(":parrot: Current swear alarm message: " + SATruncated)

                if len(command) > 2 and command[2] == "mutelog":
                    channelName = msgLCase.replace("parrot s mutelog ", "")
                    if channelName in [n.name for n in message.guild.channels]:
                        if len(mutedmsgs) == 0:
                            mutedmsgs.append(discord.utils.get(message.guild.text_channels, name=channelName))
                        mutedmsgs[0] = discord.utils.get(message.guild.text_channels, name=channelName)

                        preferencesWrite(message.guild.id, "mutelog", channelName)

                        await message.channel.send(":parrot: Channel for deleted messages has been set to #" + channelName + "!")
                    else:
                        await message.channel.send(":parrot: There is no such channel '#" + channelName + "'!")
                elif len(command) > 2 and command[2] == "mutelogreset":
                    preferencesWrite(message.guild.id, "mutelog", None)
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
                elif msgLCase.strip() == "parrot s":
                    await message.channel.send(""":parrot: **Bawk! This is the settings help page!**
For changing settings, use 'parrot s <preference> <option>'.
_If you are editing a <message> and want to state the author of the message it is replying to, use '{author}'._
**v [preference]** Views all preference values.
**mutelog <channel>** Sets the channel where deleted messages from muting are sent to.
**- mutelogreset** Resets the channel for mutelogging.
**swearalarm <message>** Sets the swear alarm.
**- swearalarmreset** Resets the swear alarm.""")
    
    else:
        if message.author.name in memberlistsRead("toMute", message.guild.id):
            await message.delete()
            await message.channel.send(":parrot: **Bawk bawk bawk bawk bawk bawk! " + message.author.name + " said nothing!**")
            if preferencesRead(message.guild.id, "mutelog") in [n.name for n in message.guild.channels] and preferencesRead(message.guild.id, "mutelog") != None:
              await discord.utils.get(message.guild.text_channels, name=preferencesRead(message.guild.id, "mutelog")).send(":parrot: **" + message.author.name + ":** " + message.content)
        elif message.author.name in memberlistsRead("toRepeat", message.guild.id):
            msg = message.content
            while msg.endswith("!") or msg.endswith("?") or msg.endswith(".") or msg.endswith(",") or msg.endswith(";") or msg.endswith(":"):
                msg = msg[:-1]
            msg = re.sub(' +', ' ', msg)
            await message.channel.send(":parrot: **" + msg + "!!!**")
            if len(message.embeds) != 0:
                await message.channel.send(":parrot: ** oi embeds are trash!!!**")

    if message.author.name in memberlistsRead("toDetectSwear", message.guild.id) and (profanity_check.predict([message.content.lower()])[0] == 1 or any(s in ' '+message.content.lower()+' ' for s in ["midget", " no u ", " no you ", "piss", " ok boomer ", " swear word ", " stfu ", " fk "])):
        await message.channel.send(preferencesRead(message.guild.id, "swearalarm").replace("{author}", message.author.name))
        

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

keep_alive.keep_alive()
client.run(TOKEN)
