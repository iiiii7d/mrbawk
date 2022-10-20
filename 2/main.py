# Mr Bawk - v1.2 (27/3/20) by i____7d

#v1.0 - 24/3/20 - Added repeating function, info page
#v1.0.1 - 26/3/20 - Added help pages, added :parrot: to every dialogue. Commands can now be in lowercase.
#v1.1 - 26/3/20 - Added swearing detection, muting function. Now detects if message has embeds during repeating.
#v1.2 - 27/3/20 - Added lists for members repeated, detected for swearing, or muted. Also added a function to view messages deleted from muting.
#TODO: Multi-server support, changelog?, json file for storage

import discord
import re
import keep_alive

TOKEN = 'asfawfqwfqwfqwfqwf'

client = discord.Client()

toRepeat = []
toDetectSwear = []
toMute = []
mutedmsgs = []

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    
    if message.content.lower().startswith('parrot') and len(message.content.split(" ")) > 1:
        members = message.guild.members
        memberNicks = [o.name.lower() for o in members]
        msgLCase = message.content.lower()
        command = msgLCase.split(" ")
        
        if command[1] == "info":
            await message.channel.send(""":parrot: **Bawk! Hello! I'm Mr Bawk, the Parrot!**\nI was created by i\_\_\_\_7d, my ultimate master!\nThis is v1.2 (27/3/20).
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
**list <repeat/detectswear/muted>** See who is repeated/detected for swearing/muted.""")
        
        elif command[1] == "ping":
          await message.channel.send(":parrot: **Pong!**")

        elif command[1] == "list":
            if msgLCase == "parrot list repeat":
                if len(toRepeat) == 0:
                    await message.channel.send(":parrot: **No players repeated, bawwwwk :(**")
                else:
                    await message.channel.send(":parrot: **Repeated players:** " + ", ".join([a.name for a in toRepeat]))
            elif msgLCase == "parrot list detectswear":
                if len(toDetectSwear) == 0:
                    await message.channel.send(":parrot: **No players detected for swearing, bawwwwk :(**")
                else:
                    await message.channel.send(":parrot: **Players detected for swearing:** " + ", ".join([a.name for a in toDetectSwear]))
            elif msgLCase == "parrot list muted":
                if len(toMute) == 0:
                    await message.channel.send(":parrot: **No players muted, bawwwwk :(**")
                else:
                    await message.channel.send(":parrot: **Muted players:** " + ", ".join([a.name for a in toMute]))

        if "Parrot's Master" in [y.name for y in message.author.roles]:
            if command[1] == "repeat" and len(command) > 2:
                if msgLCase.replace("parrot repeat ", "") in memberNicks:
                    nameIndex = memberNicks.index(msgLCase.replace("parrot repeat ", ""))
                    if members[nameIndex] in toRepeat:
                        await message.channel.send(":parrot: I'm repeating him already, master!")
                    else:
                        toRepeat.append(members[nameIndex])
                        await message.channel.send(":parrot: I'm going to repeat whatever he says, master!")
                else:
                    await message.channel.send(":parrot: There is no one with that name, master!")

            elif command[1] == "stoprepeat" and len(command) > 2:
                toRepeatNicks = [p.name.lower() for p in toRepeat]
                if msgLCase.replace("parrot stoprepeat ", "") in toRepeatNicks:
                    toRepeat.pop(toRepeatNicks.index(msgLCase.replace("parrot stoprepeat ", "")))
                    await message.channel.send(":parrot: I've stopped repeating him, master!")
                else:
                    await message.channel.send(":parrot: I'm not repeating him, master!")

            elif command[1] == "detectswear" and len(command) > 2:
                if msgLCase.replace("parrot detectswear ", "") in memberNicks:
                    nameIndex = memberNicks.index(msgLCase.replace("parrot detectswear ", ""))
                    if members[nameIndex] in toDetectSwear:
                        await message.channel.send(":parrot: I'm detecting him already, master!")
                    else:
                        toDetectSwear.append(members[nameIndex])
                        await message.channel.send(":parrot: I'm going to detect if he swears, master!")
                else:
                    await message.channel.send(":parrot: There is no one with that name, master!")

            elif command[1] == "stopdetectswear" and len(command) > 2:
                toDetectSwearNicks = [p.name.lower() for p in toDetectSwear]
                if msgLCase.replace("parrot stopdetectswear ", "") in toDetectSwearNicks:
                    toDetectSwear.pop(toDetectSwearNicks.index(msgLCase.replace("parrot stopdetectswear ", "")))
                    await message.channel.send(":parrot: I've stopped detecting him, master!")
                else:
                    await message.channel.send(":parrot: I'm not detecting him, master!")

            elif command[1] == "mute" and len(command) > 2:
                if msgLCase.replace("parrot mute ", "") in memberNicks:
                    nameIndex = memberNicks.index(msgLCase.replace("parrot mute ", ""))
                    if members[nameIndex] in toMute:
                        await message.channel.send(":parrot: I'm muting him already, master!")
                    else:
                        toMute.append(members[nameIndex])
                        await message.channel.send(":parrot: I'm going to make noise over what he says, master!")
                else:
                    await message.channel.send(":parrot: There is no one with that name, master!")

            elif command[1] == "unmute" and len(command) > 2:
                toMuteNicks = [p.name.lower() for p in toMute]
                if msgLCase.replace("parrot unmute ", "") in toMuteNicks:
                    toMute.pop(toMuteNicks.index(msgLCase.replace("parrot unmute ", "")))
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
        if message.author in toMute:
            await message.delete()
            await message.channel.send(":parrot: **Bawk bawk bawk bawk bawk bawk! " + message.author.name + " said nothing!**")
            if len(mutedmsgs) != 0:
              await mutedmsgs[0].send(":parrot: **" + message.author.name + ":** " + message.content)
        elif message.author in toRepeat:
            msg = message.content
            while msg.endswith("!") or msg.endswith("?") or msg.endswith(".") or msg.endswith(",") or msg.endswith(";") or msg.endswith(":"):
                msg = msg[:-1]
            msg = re.sub(' +', ' ', msg)
            await message.channel.send(":parrot: **" + msg + "!!!**")
            if len(message.embeds) != 0:
                await message.channel.send(":parrot: ** oi embeds are trash!!!**")

    if message.author in toDetectSwear and any(s in message.content.lower() for s in ["fuck", "shit", "ass", "cunt", "midget", "no u", "no you", "ok boomer", "fk"]):
        await message.channel.send(":parrot: **BAAAAAAAAAAWWWWWWKKKKKKK BAAAAAWWWWWWWKKKKKKK ALERRRRRRT! " + message.author.name + " SWORE! BAAAAAAAAAWWWWWKKKKKK BAAAAAAAAAAAAAAAAAWWWWWWWWWWWWWKKKKKKKKKKKKK!!!!!!!!!! :rotating_light: :rotating_light: :rotating_light:**")
        

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

keep_alive.keep_alive()
client.run(TOKEN)
