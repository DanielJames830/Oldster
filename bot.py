import os
import random

from aiohttp import streamer

import twitch


#subprocess.check_call([sys.executable, '-m','pip', 'install', '-r', 'requirements.txt', '--user'])

from discord.ext import tasks, commands
from dotenv import load_dotenv 

load_dotenv() 
TOKEN = os.getenv('DISCORD_TOKEN') 

client = commands.Bot(command_prefix='$')

message_channel = None


#______________________________EVENTS_______________________________________

#Called when the bot has successfully launched
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')




# Called everytime a user sends a message in the server

@client.event
async def on_message(message):
    responses = open('responses.txt', 'r').readlines()
    keywords = open('keywords.txt', 'r').readlines()
    if message.author == client.user:
        return
    
    for keyword in keywords:
        if keyword.strip() in message.content:
            messageToSend = random.randint(0, len(responses) - 1)
            await message.channel.send(responses[messageToSend].strip())
            break
    
    await client.process_commands(message)
        
        
        
#______________________________COMMANDS_____________________________________
@client.command()
async def add(ctx, response=None):

    if not ctx.message.author.guild_permissions.administrator:
        await ctx.send(f'You must be an administator to use this command!')
        return

    if response == None:
        await ctx.send(f'Please specify a phrase to add.')
        return
    
    response = ctx.message.content.replace("$add ", '')

    responses = open('responses.txt', 'a')
    responses.write(f"{response}\n")
    responses.close()
    await ctx.send(f'Successfully added "{response}" to my vocabulary! :smiling_imp:')

@client.command()
async def remove(ctx):
    if not ctx.message.author.guild_permissions.administrator:
        await ctx.send(f'You must be an administator to use this command!')
        return
    


    responses = open('responses.txt', 'r')
    lines = responses.readlines()
    responses.close()

    output = ''

    for index, line in enumerate(lines):
        line = f"[{index + 1}] " + line
        output += line

    await ctx.send(f"Which phrase would you like to remove?\n```{output}```")

    msg = await client.wait_for('message', timeout=400)
    toRemove = int(msg.content)

    
    
    responses = open("responses.txt", "w")
    for index, line in enumerate(lines):
        if index != toRemove - 1:
            responses.write(line)
    
    await ctx.send(f"Removed phrase #{toRemove}")

@client.command()
async def get_channel(ctx, *, given_name=None):
    for channel in ctx.guild.channels:
        if channel.name == given_name:
            wanted_channel_id = channel.id

    await ctx.send(wanted_channel_id)


sendNotification = True
twitchStreamer = 'philza' 
@tasks.loop(seconds=5)
async def isLive():
    
    global sendNotification
    channel = client.get_channel(954926869407469598)
    if not twitch.isLive(twitchStreamer):
        sendNotification = True 
        return

    if sendNotification:
        await channel.send(f'@everyone {twitchStreamer} is live!! Come hang out! \nhttps://twitch.tv/{twitchStreamer}')
        sendNotification = False
    
@isLive.before_loop
async def before():
    await client.wait_until_ready()

isLive.start()
client.run(TOKEN) 
