import discord
from discord.ext import commands, tasks
import json
import random
import asyncio

# alap
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='ec!', intents=intents)


# itt betoltjuk a cuccot
try:
    with open('users.json', 'r') as file:
        users = json.load(file)
except FileNotFoundError:
    users = {}

# a faljt ment itt
async def save_users():
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)

# le menti a fajlt nem megy xd
@bot.event
async def on_disconnect():
    await save_users()

@bot.event
async def on_shutdown():
    await save_users()

@bot.event
async def on_close():
    await save_users()

@bot.event
async def on_error():
    await save_users()

# az adatij
eco_data = {}

# munkak idk pl varga
jobs = ['Programozó', 'Gyári munkás', 'Eladó', 'Pincér', 'Szállítmányozó', "YouTuber", "Énekes", "Varga", "Szabó", "Játék Developer"]

# ahol lehet hasznalni a bot helye
business_channel_id = channel_id # a csatorna id-je

@tasks.loop(seconds=5)
async def update_status():
    await bot.change_presence(activity=discord.Game(name='RP Rendszer Bot vagyok :)'))

# parancsaink
@bot.command(name='munka', help='Végezzen egy munkát a pénzkereséshez!')
async def work(ctx):
    if ctx.channel.id != business_channel_id:
        await ctx.send('Ezt a parancsot csak az üzleti csatornán használhatja!')
        return

    user_id = str(ctx.author.id)
    if user_id not in eco_data:
        eco_data[user_id] = {'money': 0}

    job = random.choice(jobs)
    earnings = random.randint(50, 200)
    eco_data[user_id]['money'] += earnings

    await ctx.send(f'{ctx.author.mention} sikeresen elvégezte a "{job}" munkát és {earnings}$-t kereshetett!')

@bot.command(name='egyenleg', help='Ellenőrizze az egyenlegét!')
async def balance(ctx):
    user_id = str(ctx.author.id)
    if user_id not in eco_data:
        await ctx.send('Nem található egyenleg az Ön számára.')
        return

    money = eco_data[user_id]['money']
    await ctx.send(f'{ctx.author.mention} jelenleg {money}$-al rendelkezik.')

# Bank parancsok
@bot.group(name='bank', help='Bank műveletek', invoke_without_command=True)
async def bank(ctx):
    await ctx.send('Használat: !bank <betét/kivét/egyenleg>')

@bank.command(name='betét', help='Befizetés a bankszámlára!')
async def deposit(ctx, amount: int):
    if amount <= 0:
        await ctx.send('Az összegnek pozitívnak kell lennie!')
        return

    user_id = str(ctx.author.id)
    if user_id not in eco_data:
        await ctx.send('Nem található egyenleg az Ön számára.')
        return

    eco_data[user_id]['money'] += amount  # Korábban hiányzott a betétel összegének hozzáadása
    await ctx.send(f'{ctx.author.mention} sikeresen betételte {amount}$-t a bankszámlájára.')

@bank.command(name='kivét', help='Pénzkivétel a bankszámláról!')
async def withdraw(ctx, amount: int):
    if amount <= 0:
        await ctx.send('Az összegnek pozitívnak kell lennie!')
        return

    user_id = str(ctx.author.id)
    if user_id not in eco_data:
        await ctx.send('Nem található egyenleg az Ön számára.')
        return

    if eco_data[user_id]['money'] < amount:
        await ctx.send('Nincs elegendő pénze a kivételhez!')
        return

    eco_data[user_id]['money'] -= amount
    await ctx.send(f'{ctx.author.mention} sikeresen kivette {amount}$-t a bankszámlájáról.')

@bank.command(name='egyenleg', help='Ellenőrizze a bankszámláját!')
async def bank_balance(ctx):
    user_id = str(ctx.author.id)
    if user_id not in eco_data:
        await ctx.send('Nem található egyenleg az Ön számára.')
        return

    money = eco_data[user_id]['money']
    await ctx.send(f'{ctx.author.mention} jelenleg {money}$-al rendelkezik a bankszámláján.')

# itt kifog irni valamit
@bot.event
async def on_ready():
    print(f'{bot.user.name} online!')
    update_status.start()  # a botnak az allapotja

@bot.command(name='chelp', help='Core Help')
async def custom_help(ctx):
    # embed-et csinal
    embed = discord.Embed(title="CoreHelp", description="Help", color=0x00ff00)

    # az embed parancs resze
    embed.add_field(name="!bank <egyenleg/kivétel/betét>", value="Bankolsz", inline=False)
    embed.add_field(name="!munka", value="Egy munkát végzel el", inline=False)

    # embed help kuldes
    await ctx.send(embed=embed)









#discord bot inditasa
bot.run(' Rakd be a tokened ')
