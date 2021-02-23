import discord
from discord.ext import commands
import asyncio
import requests
import json
from gtts import gTTS
from discord.utils import get
import datetime
from datetime import timedelta
from datetime import date
import matplotlib as mpl
import matplotlib.pyplot as plt
import random as rn
from googlesearch import search
import os
import dotenv 
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('token')

startup_extensions = ['cogs.wolfram', 'cogs.owner', 'cogs.profile', 'cogs.music.music', 'cogs.dad', 'cogs.weather', 'cogs.game.game', 'cogs.emoji',
'cogs.2048', 'cogs.detain', 'cogs.covid.tracker']

client = commands.Bot(command_prefix=".")
client.games = {}

response = ""
#with open("keys.txt", 'r') as file:
    #key = file.readline().replace("\n", "")  # Read API key from keys.txt

@client.event
async def on_ready():
    print('Connected!')
    print('Username: ' + client.user.name)
    game = discord.Activity(
        type=discord.ActivityType.watching, name="over you")
    await client.change_presence(status=discord.Status.idle, activity=game)


@client.event
async def on_message(message):
        if 'ZA WARUDO' in message.content:
            if message.author.guild_permissions.administrator or message.author.id == 712788178742018150:
                memberrole = discord.utils.get(
                    message.guild.roles, id=735959176584364042)
                guardrole = discord.utils.get(
                    message.guild.roles, id=742896707020390421)
                await message.channel.set_permissions(
                    memberrole,
                    read_messages=True,
                    send_messages=False,
                    read_message_history=True)
                await message.channel.set_permissions(
                    guardrole,
                    read_messages=True,
                    send_messages=False,
                    read_message_history=True)
                emoji = '⏰'
                await message.add_reaction(emoji)
                await message.channel.send('1 second has passed')
                await asyncio.sleep(1)
                await message.channel.send('2 seconds have passed')
                await asyncio.sleep(1)
                await message.channel.send('3 seconds have passed')
                await asyncio.sleep(1)
                await message.channel.send('4 seconds have passed')
                await asyncio.sleep(1)
                await message.channel.send('5 seconds have passed')
                await asyncio.sleep(1)
                await message.channel.send('6 seconds have passed')
                await asyncio.sleep(1)
                await message.channel.send('7 seconds have passed')
                await asyncio.sleep(1)
                await message.channel.send('8 seconds have passed')
                await asyncio.sleep(1)
                await message.channel.send('9 seconds have passed')
                await asyncio.sleep(1)
                await message.channel.send('10 seconds have passed')
                await message.channel.send('*TIME NOW WILL RESUME*')
                await message.channel.set_permissions(
                    memberrole,
                    read_messages=True,
                    send_messages=True,
                    read_message_history=True)
                await message.channel.set_permissions(
                    guardrole,
                    read_messages=True,
                    send_messages=True,
                    read_message_history=True)
            else:
                await message.channel.send('**YOU ARE PATHETICALLY WEAK**')
        elif 'tell me a joke' in message.content:
            joke = requests.get(
                'https://icanhazdadjoke.com', headers={
                    "Accept": "text/plain"
                }).text
            await message.channel.send(joke)
        await client.process_commands(message)

@commands.cooldown(rate=1, per=7)
@client.command(hidden=True)
async def shutdown(ctx):
    if await client.is_owner(ctx.message.author):
        await ctx.send("Thus, with a kiss, I die")
        await client.logout()
    else:
        await ctx.send("Death is whoever does Death’s job: me")

@bot.command(name='unban')
async def _unban(ctx):
    user = client.get_user(774295594276618262)
    await ctx.guild.unban(user)
    link = await ctx.channel.create_invite(max_age = 300)
    await user.send(link)
	
@client.command(pass_context=True)
async def poll(ctx, question, arg, *, arg2=30):

    #Function to not display unvoted option in the pie chart
    def spe_autopct(pct):
        return ('%.2f%%' % pct) if pct != 0 else ''

    await ctx.message.delete()
    # Empty list of lists to be filled with the reactions
    reactions = [[] for i in range(0,10)]

    arg2 = int(arg2)

    #Format the args
    choices = arg.split(";")

    #Check if there are enough arguments
    if arg == None or len(choices) < 2:
        await ctx.send("You need at least 2 option to start a poll.")
        return

    #Number emotes. Index corresponds with emote
    emoteRef = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]

    print(arg)

    #Check if there aren't too many args
    if len(choices) > 10:
        await ctx.send("You cannot add more than 10 choices")
        return


    #Create the message
    toPrint = (("{} asked: **{}** \n").format(ctx.author, question))
    print(choices)

    for choice,count in zip(choices, range(len(choices))):
        toPrint += f"{emoteRef[count]}-{choice}, \n"


    toPrint = toPrint[0:len(toPrint)-3]
    embed = discord.Embed(title = "POLL: ", description = toPrint)
    message = await ctx.send(embed = embed)


    #Add the reactions
    for choice,count in zip(choices, range(len(choices))):
        await message.add_reaction(emoteRef[count])
    #Wait for the poll time to end
    await asyncio.sleep(arg2)

    await ctx.send("The poll has expired. Processing results now...")

    cache_msg = get(client.cached_messages, id=message.id)

    reactions = [get(cache_msg.reactions, emoji=emoteRef[i]) for i in range(0,10)]

	#Get the arguments for the pie chart construction
    sizes = []
    for reac in reactions:
        if reac is not None:
            sizes.append(reac.count -1) #-1 needed to not count the bot's reac
        else:
            sizes.append(0)

    voteNb = sum(sizes)
    sizes = sizes[:len(choices)]

	#Create the pie chart
    patches, texts, percent = plt.pie(sizes, shadow=True, startangle=140, autopct=spe_autopct)
    plt.legend(patches, choices, loc="best", title=f"{voteNb} votes")
    plt.axis('equal')
    plt.tight_layout()

	#Randomly generated plot ID to prevent mixing up plots between users
    plotID = str(rn.randrange(1,100000))
    plt.savefig(f"Plot_id{plotID}.png", transparent=True)

	#Send the pie chart
    await ctx.send(file=discord.File(f'Plot_id{plotID}.png'))
    os.remove(f'Plot_id{plotID}.png')

    plt.cla()   # Clear axis
    plt.clf()   # Clear figure
    plt.close()

@client.command(pass_context=True)
async def userstats(ctx, statType = "help",user = None, private = None):

	if private == "private":
		private = True

	if user == "private":
		private = True

	user = ctx.message.author
	print(ctx.message.mentions)
	if len(ctx.message.mentions) > 0:
		print(ctx.message.mentions)
		user = ctx.message.mentions[0]



	async def help(ctx, user, private):
		helpMsg = "Hi there! This message was made to help you use >userstats.\n"
		helpMsg += "Here are the differents types of stats currently implemented:\n"
		helpMsg += '".userstats messages @user" will show stats about user\'s messages.\n'
		helpMsg += '".userstats help" will show this message.\n'
		helpMsg += "You can add the keyword private at the end of your command to receive the results in your DMs\n"
		helpMsg += "_Note: If you don't specify a user, I will assume that you want your own stats._"
		await user.send(helpMsg)

	async def messages(ctx, user, private):

		await ctx.send("Retrieving the messages from " + user.display_name + "...")
		dayMonthList = []
		dateList = []
		channelList = []
		hasAllAccess = True

		if private:
			toSend = ctx.message.author
		else:
			toSend = ctx

		# Goes through every channel to find the user's messages
		for channel in ctx.message.guild.text_channels:

			try:

				# Goes through the messages of this channel
				async for msg in channel.history(limit=10000):
					msgDate = msg.created_at

					now = date.today()
					then = msgDate.date()
					limit = now - timedelta(days = 30)

					# If the message is older than 30 days, our job is done here
					if then < limit:
						break

					# If the message is from the user, then it's the data we want
					elif msg.author == user:
						dateList.append(then)
						channelList.append(msg.channel.name)

			# The bot might not have access to certain channels
			except discord.errors.Forbidden:
				hasAllAccess = False

		# Sorting the dateList
		dateList.sort()

		# TODO: Maybe set() before to avoid another long loop?
		for dates in dateList:
			day = dates.day
			monthName = dates.strftime("%b")
			dayMonth = str(day) + " - " + monthName
			dayMonthList.append(dayMonth)


		# Now that we retrieved the data, we prepare graphs out of it
		dayNb = []
		channelNb = []

		# A list of unique days that still keeps order
		uniqueDayMonth = list(sorted(set(dayMonthList), key=dayMonthList.index))
		uniqueChannel = list(sorted(set(channelList), key=channelList.index))

		# List of messages/month ordered by the unique days list
		for dayMonth in uniqueDayMonth:
			dayNb.append(dayMonthList.count(dayMonth))

		# List of nb of messages/channel ordered by the channel list
		for channel in uniqueChannel:
			channelNb.append(channelList.count(channel))

# 		print("dayMonthList = "+ str(dayMonthList))
# 		print("dayNb = "+str(dayNb))
# 		print("uniqueDayMonth = "+ str(uniqueDayMonth))

		# Creates the msg/day graph
		mpl.rcParams.update({'font.size': 14})
		fig = plt.figure(figsize = [12,7])
		plt.style.use("dark_background")

		# Creates the messages/day plot
		ax = fig.add_subplot(211)
		ax.set_facecolor("#36393E")
		ax.bar(uniqueDayMonth,dayNb, color = "#7289DA")
		ax.set_title("messages/day from "+user.display_name+" in the last 30 days")

		# Final touches
		plt.xticks(rotation=45)
		plt.tight_layout()

		# Creates the messages/channel plot
		ax2 = fig.add_subplot(212)
		ax2.set_facecolor("#36393E")
		ax2.bar(uniqueChannel,channelNb, color = "#7289DA")
		ax2.set_title("messages/channel from "+user.display_name+" in the last 30 days")

		# Final touches
		plt.xticks(rotation=35)
		plt.tight_layout()

		#Randomly generated plot ID to prevent mixing up plots between users
		plotID = str(rn.randrange(1,10000000))
		plt.savefig(f"Plot_id{plotID}.png", transparent=False, facecolor="#36393E", edgecolor='none')

		# Set the font size back to default
		mpl.rcParams.update({'font.size': 12})

		#Send the plot
		if private:
			await ctx.send("The data has been processed! Check your DMs!   (private stats)")

		await toSend.send("Here are the stats for "+ user.mention +" 's messages:   (Click to enhance)")
		await toSend.send(file=discord.File(f'Plot_id{plotID}.png'))
		os.remove(f'Plot_id{plotID}.png')

		plt.cla()   # Clear axis
		plt.clf()   # Clear figure
		plt.close()

	await eval(f"{statType}(ctx,user,{private})")

@client.command()
async def mute(ctx, *, member: discord.Member):
    try:
        if ctx.author.voice:  # check if the user is in a voice channel
            if ctx.author.guild_permissions.mute_members:  # check if the user has mute members permission
                try:  # try to mute if the client has permissions
                    await member.edit(mute=True)
                    await ctx.send('muted')
                except discord.errors.Forbidden:
                    await ctx.channel.send(  # the client doesn't have the permission to mute
                        f"I don't have the `Mute Members` permission. Make sure I have the permission in my role "
                        f"**and** in your current voice channel `{ctx.author.voice.channel}`")
            else:
                await ctx.channel.send("You don't have the `Mute Members` permission")
        else:
            await ctx.send("You must join a voice channel first")
    except Exception as e:
        await ctx.channel.send(f"Something went wrong ({e}).")

@client.command()
async def unmute(ctx, *, member: discord.Member):
    try:
        if ctx.author.voice:  # check if the user is in a voice channel
            if ctx.author.guild_permissions.mute_members:  # check if the user has mute members permission
                try:  # try to mute if the client has permissions
                    await member.edit(mute=False)
                    await ctx.send('unmuted')
                except discord.errors.Forbidden:
                    await ctx.channel.send(  # the client doesn't have the permission to mute
                        f"I don't have the `Mute Members` permission. Make sure I have the permission in my role "
                        f"**and** in your current voice channel `{ctx.author.voice.channel}`")
            else:
                await ctx.channel.send("You don't have the `Mute Members` permission")
        else:
            await ctx.send("You must join a voice channel first")
    except Exception as e:
        await ctx.channel.send(f"Something went wrong ({e}).")

@client.command()
async def deafen(ctx, *, member: discord.Member):
    try:
        if ctx.author.voice:  # check if the user is in a voice channel
            if ctx.author.guild_permissions.deafen_members:  # check if the user has mute members permission
                try:  # try to mute if the client has permissions
                    await member.edit(deafen=True)
                    await ctx.send('deafened')
                except discord.errors.Forbidden:
                    await ctx.channel.send(  # the client doesn't have the permission to mute
                        f"I don't have the `Deafen Members` permission. Make sure I have the permission in my role "
                        f"**and** in your current voice channel `{ctx.author.voice.channel}`")
            else:
                await ctx.channel.send("You don't have the `Deafen Members` permission")
        else:
            await ctx.send("You must join a voice channel first")
    except Exception as e:
        await ctx.channel.send(f"Something went wrong ({e}).")

@client.command()
async def undeafen(ctx, *, member: discord.Member):
    try:
        if ctx.author.voice:  # check if the user is in a voice channel
            if ctx.author.guild_permissions.deafen_members:  # check if the user has mute members permission
                try:  # try to mute if the client has permissions
                    await member.edit(deafen=False)
                    await ctx.send('undeafened')
                except discord.errors.Forbidden:
                    await ctx.channel.send(  # the client doesn't have the permission to mute
                        f"I don't have the `Deafen Members` permission. Make sure I have the permission in my role "
                        f"**and** in your current voice channel `{ctx.author.voice.channel}`")
            else:
                await ctx.channel.send("You don't have the `Deafen Members` permission")
        else:
            await ctx.send("You must join a voice channel first")
    except Exception as e:
        await ctx.channel.send(f"Something went wrong ({e}).")


if __name__ == "__main__":
        for extension in startup_extensions:
            try:
                client.load_extension(extension)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))
        client.run(token)
