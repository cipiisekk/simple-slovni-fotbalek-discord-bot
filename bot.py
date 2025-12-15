import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

watched_channel = None
last_user = None
game_running = 0
last_message = None


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name="Cigipisek made me do this"
        )
    )


@bot.command()
# @commands.has_permisions(administrator=True)
async def sf_start(ctx):
    global watched_channel
    global game_running
    global last_message

    if game_running == 1:
        await ctx.send("Jiz kontroluji na jinem kanale")
        return

    if watched_channel == ctx.channel:
        await ctx.send("Na tomto kanale jiz kontroluji..")
        return

    await ctx.send("Hra zacina na slove abeceda")
    last_message = "abeceda"

    watched_channel = ctx.channel
    game_running = 1

    
@bot.event
async def on_message(message):
    global watched_channel
    global last_message
    global last_user
    global game_running

    if message.author.bot:
        return

    if message.channel != watched_channel or game_running == 0:
        await bot.process_commands(message)
        return


    if " " in message.content:
        print(f"{message.author} napsal dve slova, ne jedno - {message.content}")
        await message.delete()
        return
    
    word = message.content.strip()

    if not word.isalpha():
        print(f"{message.author} se snazi napsat specialni znaky - {message.content}")
        await message.delete()
        return

    if last_message is None:
        last_message = message.content
        last_user = message.author
        return
    
    if message.author == last_user:
        print(f"{message.author} se snazi hrat sam")
        await message.delete()
        return
    
    if message.content.lower() == last_message.lower():
        print(f"{message.author} se snazi kopirovat posledni zpravu")
        await message.delete()
        return
    
    if len(message.content) <= 1:
        print(f"{message.author} se snazi napsat jedno pismeno pouze")
        await message.delete()
        return
        
    if message.content[0].lower() != last_message[-1].lower():
        print(f"{message.author} nenapsal spravne slovo - {message.content}")
        await message.delete()
        return

    print(f"{message.channel} Posledni zprava: {last_message} | Nova zprava: {message.content} | Autor: {message.author}")
    last_message = word.lower()
    last_user = message.author


    await bot.process_commands(message)

bot.run(TOKEN)

