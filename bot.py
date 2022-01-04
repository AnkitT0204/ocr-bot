import discord
from discord.ext import commands
import pytesseract
import cv2
import numpy as np
from PIL import Image,ImageOps
import requests
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix='.', description="This is an OCR-bot",help_command=None)


def get_string(img_path,lg,bgdark):
    img = cv2.imread(img_path)
    if(bgdark==1):
        img = cv2.bitwise_not(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    cv2.imwrite("removed_noise.png", img)
    cv2.imwrite(img_path, img)
    pytesseract.pytesseract.tesseract_cmd = "/app/.apt/usr/bin/tesseract"
    result = pytesseract.image_to_string(Image.open(img_path),lang=lg,config='--psm 6')
    return result
    
async def send_reply(ctx,lg,bgdark=0):
    ocr = get_string("img.png",lg,bgdark)
    ocr = "```{}```".format(ocr)
    if(len(ocr.replace(" ",""))>=8):
        await ctx.reply(ocr)
    else:
        author = ctx.message.author
        embed = discord.Embed(
        colour = discord.Colour.red()
        )
        embed.set_author(name="bot couldn't find any TEXT ಥ_ಥ")
        embed.add_field(name="Does your Image have a dark backgrpound? ",value="Try using .dbg command", inline=False)
        embed.add_field(name="Trying different languages?",value="Use the .help command to see correct commands for different languages.", inline=False)
        embed.add_field(name="No OCR after trying multiple times?",value="OCR-bot works best on clear screenshots of texts.", inline=False)
        await ctx.reply("Sorry {}".format(author),embed=embed)
        
#         await ctx.reply(''' 
# bot couldn't find any TEXT ಥ_ಥ.

# (Does your image has a dark background? Try ".dbg" command.)
# (For more language options use ".help")
#                         ''')

@bot.command()
async def ocr(ctx): await send_reply(ctx,lg='eng')

@bot.command()
async def dbg(ctx): await send_reply(ctx,lg='eng',bgdark=1)

@bot.command()
async def jpn(ctx): await send_reply(ctx,lg='jpn')

@bot.command()
async def hin(ctx): await send_reply(ctx,lg='hin')

@bot.command()
async def kor(ctx): await send_reply(ctx,lg='kor')

@bot.command()
async def rus(ctx): await send_reply(ctx,lg='rus')

@bot.command()
async def swe(ctx): await send_reply(ctx,lg='swe')

@bot.command()
async def tel(ctx): await send_reply(ctx,lg='tel')

@bot.command()
async def tam(ctx): await send_reply(ctx,lg='tam')

@bot.command()
async def spa(ctx): await send_reply(ctx,lg='spa')

@bot.command()
async def ger(ctx): await send_reply(ctx,lg='deu')

@bot.command()
async def fra(ctx): await send_reply(ctx,lg='fra')


@bot.command()
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        colour = discord.Colour.orange()
        )
    embed.set_author(name="Help")
    embed.add_field(name="How it works",value="Send an Image with text with one of the following commands:", inline=False)
    embed.add_field(name=".ocr",value="Does OCR in default (English) Language", inline=False)
    embed.add_field(name=".dbg",value="Does OCR for images with text on dark background (usually code screenshots)", inline=False)
    embed.add_field(name=".hin",value="OCR for Hindi")
    embed.add_field(name=".tam",value="OCR for Tamil")
    embed.add_field(name=".tel",value="OCR for Telugu")
    embed.add_field(name=".spa",value="OCR for Spanish")
    embed.add_field(name=".kor",value="OCR for Korean")
    embed.add_field(name=".rus",value="OCR for Russian")
    embed.add_field(name=".swe",value="OCR for Swedish")
    embed.add_field(name=".ger",value="OCR for German")
    embed.add_field(name=".fra",value="OCR for French")
    await ctx.send(author,embed=embed)


# Events
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="bots | .help"))
    print("Lessa GO!! It's bot Time!!!!")

@bot.event
async def on_message(message):
    try:
        url = message.attachments[0].url
        r = requests.get(url)
        filename = "img.png"
        with open(filename, 'wb') as out_file:
            out_file.write(r.content)
        print(url)
    except:
        pass
    await bot.process_commands(message)


    
bot.run(TOKEN)