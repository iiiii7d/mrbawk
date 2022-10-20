## Introduction

**Your guild is mundane.** The channels are quieter than usual. All you need is **a pet.**  
This is what Mr Bawk is for: to provide entertainment like how a parrot would, with being able to repeat someone, detect someone for swearing, or to talk over someone (in chat), plus a currency system, a quoting function, being able to mess up images, a reaction game, and more!  
Founded on 24 March by i____7d#5755, this parrot aims to provide fun for all.

## Changelog

### Latest version: v1.11 (2/10/20)

* `parrot c bowls` now shows your bowls in pages... for those who have too many of them
* Item prices & achievements now follow an exponential rate depending on no. of parrots & levels respectively, preventing inflation
* Swearing counter! Note that swears will be detected only if swearing detection is on.

## Initialisation Guide

When you first invite Mr Bawk into the server, a new role is automatically created called "Parrot Master". Give this role to yourself and some others so that they can use the master commands of Mr Bawk.  
You are also recommended to look at the server preferences (parrot s), when you are a Parrot Master. You are highly recommended to set a specific channel for announcements (in annchannel) as that is where updates for version updating or other messages from me will be posted to. Feel free to look at the other options.

## Command list

All my commands start with `parrot`. Note for parameters: <> means mandatory, [] means optional.  

### General commands (parrot help)

#### All commands here start with `parrot`.

*   **help [master]:** The help page. Append [master] for Parrot Master commands.
*   **info:** View bot info.
*   **list [repeat/detectswear/mute]:** See who is repeated/detected for swearing/muted. Append nothing for a list of everything.
*   **sc/swearcount [nick]:** View your or others' swear count
*   **ping:** Connection test.
*   **uptime:** View uptime.
*   **cl/changelog:** View the new additions in this update, and what to look forward in the next update.
*   **inviteme:** Invite me to your server!
*   **myserver:** Get the invite link for my support server
*   **vote:** Vote for me!
*   **q:** Quote someone, or view someone else's quotes. Type `parrot q` for more info.
*   **c:** The currency system. Type `parrot c` for more info.
*   **r:** The reaction test game. Type `parrot r` for more info.
*   **messup [url]:** Scramble images! You either give the URL, or an image attachment.
*   **ach/achievements:** View your achievements.
*   **gif:** View parrot gifs &lt;3

### Master commands (parrot help master)

#### All commands here start with `parrot`.

*   **s:** Parrot settings and preferences. Type `parrot s` for more info.
*   **re/repeat <nickname>:**Repeats whatever someone says.
*   **sre/stoprepeat <nickname>:** Stops repeating someone. Put '*' in the <nickname> slot to stop repeating everyone.
*   **ds/detectswear <nickname>:** Detects swearing, and sounds a text alarm when someone does.
*   **sds/stopdetectswear <nickname>:** Stops detecting someone for swearing. Put '*' in the <nickname> slot to stop detecting everyone.
*   **mute <nickname>:** Talks over what someone says in chat.
*   **unmute <nickname>:** Stops talking over someone. Put '*' in the <nickname> slot to unmute everyone.

### Preferences commands (parrot s)

#### All commands here start with `parrot s`.

*   **v [preference]:** Views all preference values, or a specific one.
*   **deletelog <channel>:** Sets the channel where deleted messages from muting are sent to. [Default: None]
    *   **deletelogreset:** Resets the channel for deletelogging to no channel.
*   **swearalarm <message>:** Sets the swear alarm, if you think the default is too spammy. Use "{author}" to put in the swearer's nickname. [Default: (Too long)]
    *   **swearalarmreset:** Resets the swear alarm.
*   **annchannel <channel>:** (short for announcements channel) Sets the channel where announcements about new versions will be made. [Default: None]
    *   **annchannelreset:** Resets the channel for version announcing to no channel.
*   **dsmba <true/false>:** (short for deleteswearmsgbeforealarm) When someone swears while they are being detected, choose whether to delete the message with the swear word inside of it or not before sounding the alarm. Note that deleted messages will go to deletelog. [Default: False]
*   **addswearwords...:** Edits the list of additional swear words to detect. [Default: (Too long)]
    *   **...add:<word>; :** Adds a word or phrase to the list.
    *   **...remove:<word>; :** Removes a word or phrase from the list.
    *   **...reset:** Resets the list to its default.
    *   Always remember to put the colon and semicolon in `add` and `remove`. This prevents loss of spacebars.
    *   If you want to detect for a swear word in any word, don't put spaces. Put a space after the colon for a prefix swear; and before the semicolon for a suffix swear. Put both spaces for an exact swear word.
*   **currencychannels...:** Edits the list of channels where `parrot c` can be used. [Default: None (Every channel)]
    *   **...add:<channel>:** Adds a channel to the list.
    *   **...remove:<channel>:** Removes a channel from the list.
    *   **...reset:** Resets the list to its default.

### Quoting commands (parrot q)

#### All commands here start with `parrot q`.

*   **add <message ID>:** Adds a quote to the database. Type `parrot q add` by itself for instructions on how to add a quote.
*   **view <person> [index]:** View someone's quotes.
    *   Put `anyone` in the <person> slot to pick a random person.
    *   Put `any` in the [index] slot to pick a random quote from a person.
    *   Leave [index] empty to get all quotes from someone.
    *   Do `anyone any` for a random quote from a random person.
    *   Note that you have to give the full name (e.g. Foobar#1234) for the <person> slot.
*   **remove <quote ID> [-o]:** Removes a quote. Note that you can only remove your own quote.
    *   Append `-o` to mark it as offensive, which means that the quote can never be quoted again.

### Currency commands (parrot c)

#### All commands here start with `parrot c`.

*   **shop [page]:** Shop for items, especially foods.
*   **buy <qty> <item>:** Buy items from the shop.
*   **pf/placefood <item> [-a]:** Put food into the bowl. Append -a to fill as much empty bowls as there are.
*   **inv/inventory:** View your inventory.
*   **bowls [page]:** View what's inside your bowl.
*   **parrots [page]:** View your parrots.
*   **bal/balance:** View your balance.
*   **daily:** Claim your daily twigs.
*   **enc [breed]:** View the encyclopaedia of parrots.
*   **top [twigs/parrots/xp]:** Views the top 15 players on this server, based on amount of twigs, parrots, or xp. Append nothing to rank players based on all three factors combined.
*   **rename <index> <new name>:** Rename one of your parrots.
*   **how:** View the tutorial for this system.

### Reaction game commands (parrot r)

#### All commands here start with `parrot r`.

#### Optional parameters are denoted between angle brackets ({}). For example, {-a[];} would be written in the command as -aVALUE;.

*   **start {-t[];} {-w[];} :** Starts a game. Append -t to set the threshold for the game to end, and -w to set the number of seconds to wait before the game starts.
*   **join:** Join an ongoing game.
*   **leave:** Leave an ongoing game.
*   **stop:** Stop an ongoing game. This command is for Parrot Masters only.

## More about this bot

If a bug occurs within the code, a report would be sent to i____7d, in the support server.
If you detect anything that is wrong with the bot, but no error message is produced, go and tell i____7d (in the support server).  

Nevertheless, have fun with my bot :)

## Gallery

![](https://i.imgur.com/J1JoEiQ.png "source: imgur.com")  
![](https://i.imgur.com/kfe7YoR.png "source: imgur.com")  
![](https://i.imgur.com/kFPvfhi.png "source: imgur.com")  
![](https://i.imgur.com/cL5tkd3.png "source: imgur.com")  
![](https://i.imgur.com/AxAQWUY.png "source: imgur.com")