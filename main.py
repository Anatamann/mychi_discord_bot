
import discord
from discord.ext import commands
import os
#import re
import csv
from datetime import datetime
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=['$','>>'], intents=intents)

#varialbles
My_chi=0
gap=1
c_c=1
goku_id= 529746047413649420
arnab_id= 804723288702058556
#reshov_id= 1207070876302966806
# url= r'^(https?:\/\/[^\s]+\.com\/?)$'

#system var

file_name='chi_data.csv'

#------------------------------------------------------

#system function for chi

def write_chi_data(file_name, i, data):

    with open(file_name, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)

    for j in range(0, len(rows)):
        if j==i:
            rows[j] = data
            break
    
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
#________________________________________________________

def read_chi_data(file_name):
    results = []
    with open(file_name, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            my_chi = float(row[0])
            gap = float(row[1])
            c_c = float(row[2])
            date = row[3]
            if date == 'd':
                date = datetime.now().strftime("%Y-%m-%d")
            results.append((my_chi, gap,c_c,date))
    return results
#__________________________________________________________________
## datefunction 
# def compare_dates(date1_str, date2_str, date_format="%Y-%m-%d"):
#     date1 = datetime.strptime(date1_str, date_format)
#     date2 = datetime.strptime(date2_str, date_format)

#     difference = (date2 - date1).days
#     return difference
#__________________________________________________________________


## chi-level
def chi(id):
    
    if id==goku_id:
        i= 0
    elif id== arnab_id:
        i= 1
    else:
        i= 2
    
    data = read_chi_data(file_name)
    last_date = datetime.fromisoformat(data[0][3])
    today = datetime.now()
    gap = (today - last_date).days
    
    if gap == 0:
        My_chi = data[i][0] + 5
        c_c = data[i][2] + 1
        if c_c % 10 == 0:
            My_chi = data[i][0] + 50
        else:
            My_chi = data[i][0] + 10
    elif gap == 1:
        gap=0
        c_c = data[i][2] + 1
        if c_c % 10 == 0:
            My_chi = data[i][0] + 50
        else:
            My_chi = data[i][0] + 10
    else:
        if gap%3==0:
            My_chi = data[i][0] + 10 - gap
            gap = 0
            c_c = 0
        else:
            My_chi = data[i][0] + 10 - round((gap/3),2) 
            gap = data[i][1] + gap%3
            c_c = 0
                
    data = [My_chi, gap, c_c, today.strftime("%Y-%m-%d")]
    write_chi_data(file_name, i, data)
    return My_chi


#------------------------------------------------------

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    else:
        if (message.content[:2]=='>>'):
            await message.channel.send('We see a project update here, way to go man. Your Chi is being updated...')
            data = chi(message.author.id)
            await message.channel.send(f'Your Chi is now: {data}')
        else:
            if message.content == '$mychi':
                await bot.process_commands(message)
            else:
                if message.content[:1] == '$': 
                    reply=message.content[1:]
                    await message.channel.send(reply+' ;D this was sickly sick.')

# @bot.command()
# async def ping(ctx):
#     '''
#     This text will be shown in the help command
#     '''

#     # Get the latency of the bot
#     latency = round(bot.latency,2)  # Included in the Discord.py library
#     # Send it to the user
#     await ctx.send('latency: '  + str(latency) + ' sec')


@bot.command()
async def mychi(ctx):
    data = read_chi_data(file_name)
    today = datetime.now().strftime("%Y-%m-%d")
    if ctx.author.id == goku_id:
        await ctx.send(f'As of {today} \nYour Chi is: {data[0][0]} \nYour continuity is: {data[0][2]} \nYour gap is: {data[0][1]} \nYour last update was on {data[0][3]}')
    elif ctx.author.id == arnab_id:
        await ctx.send(f'As of {today} \nYour Chi is: {data[1][0]} \nYour continuity is: {data[1][2]} \nYour gap is: {data[1][1]} \nYour last update was on {data[1][3]}')
    else:
        await ctx.send(f'As of {today} \nYour Chi is: {data[2][0]} \nYour continuity is: {data[2][2]} \nYour gap is: {data[2][1]} \nYour last update was on {data[2][3]}')

#________________________________________________________
# Load environment variables from .env file
load_dotenv()

# Get the token from the environment variables
token = os.getenv('TOKEN')

if token is None:
    raise ValueError("No TOKEN found in environment variables")

bot.run(token)