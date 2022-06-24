import os
import io
import discord
from discord.ext import commands
import json
from pprint import pprint
import requests
import typing
from dotenv import load_dotenv
import PIL
from PIL import Image

# discord bot
bot = commands.Bot(command_prefix="!")

# Opening JSON file with pfps. Add your open file and update it to match the name here
# data = open('backup.json', )

# Folder locations for clean pfps, completed pfps, and outfits

save_img_folder = 'dressed_pfps/'
outfits_folder = 'outfits/beer/'
pfp_folder = 'clean_pfps/'

save_bussin_img_folder = 'bussin/dressed_pfps/'
outfits_bussin_folder = 'outfits/bussin/'

save_dtp_img_folder = 'dtp/dressed_pfps/'
outfits_dtp_folder = 'dtp/outfits/beer/'
pfp_dtp_folder = 'dtp/clean_pfps/'

save_egg_img_folder = 'egg/dressed_pfps/'
outfits_egg_folder = 'egg/outfits/beer/'
pfp_egg_folder = 'egg/clean_pfps/'

save_jersey_img_folder = 'jersey/dressed_pfps/'
outfits_jersey_folder = 'jersey/outfits/beer/'
pfp_jersey_folder = 'jersey/clean_pfps/'


# list of the various outfits you want to offer. these should match the filename on the outfit pngs

outfits = ["background", "clean", "black", "blue", "brown", "gold", "green", "purple", "red", "white"]

# Search for the pfp id in the JSON dictionary and return the image URL associated with that id. You'll need to update the keys to match what's in your JSON delattr


# Downloads the pfp from the image URL and saves it in a directory

def download_image(url, image_file_path):
    r = requests.get(url, timeout=4.0)
    if r.status_code != requests.codes.ok:
        assert False, 'Status code error: {}.'.format(r.status_code)

    with Image.open(io.BytesIO(r.content)) as im:
        im.save(image_file_path)

# Combines the pfp image with a transparent png of the attribute and saves it to an output directory

def get_dressed(fit, pfp_id):
    url = ('https://degenape.nyc3.digitaloceanspaces.com/apes/no-head-traits/' + str(pfp_id) + '.png')
    download_image(url, pfp_folder + str(pfp_id) + '.png')

# This combines the images 

    pfp = Image.open(pfp_folder + str(pfp_id) + '.png')
    outfit = Image.open(outfits_folder + fit + '.png')

    pfp.paste(outfit, (0, 0), mask=outfit)
    pfp.save(save_img_folder + 'dressed' + str(pfp_id) + '.png')

    return
    
def get_bussin(fit, pfp_id):
    url = ('https://degenape.nyc3.digitaloceanspaces.com/apes/no-head-traits/' + str(pfp_id) + '.png')
    download_image(url, pfp_folder + str(pfp_id) + '.png')

# This combines the images 

    pfp = Image.open(pfp_folder + str(pfp_id) + '.png')
    outfit = Image.open(outfits_bussin_folder + fit + '.png')

    pfp.paste(outfit, (0, 0), mask=outfit)
    pfp.save(save_bussin_img_folder + 'dressed' + str(pfp_id) + '.png')

    return

def get_jersey_dressed(pfp_id):
    url = ('https://degenape.nyc3.digitaloceanspaces.com/apes/jersey-1/' + str(pfp_id) + '.png')
    download_image(url, save_jersey_img_folder + str(pfp_id) + '.png')

    return

def get_dtp_dressed(fit, pfp_id):
    
    payload = json.dumps({
        'condition': {
            'project_ids': [
                {
                    'project_id': 'degentrashpandas'
                }
            ],
            'name': {
                'operation': 'EXACT', 
                'value': 'Degen Trash Panda #' + str(pfp_id)
                },
        }
    })
    headers = {
        'Authorization': os.environ['HYPER_TOKEN'],
        'Content-Type': 'application/json'
    }
    r = requests.post('https://beta.api.solanalysis.com/rest/get-market-place-snapshots', headers=headers, data=payload)
    
    url = r.json()['market_place_snapshots'][0]['meta_data_img']

    download_image(url, pfp_dtp_folder + str(pfp_id) + '.png')

# This combines the images 

    pfp = Image.open(pfp_dtp_folder + str(pfp_id) + '.png')
    outfit = Image.open(outfits_dtp_folder + fit + '.png')

    pfp.paste(outfit, (0, 0), mask=outfit)
    pfp.save(save_dtp_img_folder + 'dressed' + str(pfp_id) + '.png')

    return

def get_egg_dressed(fit, pfp_id):
    
    payload = json.dumps({
        'condition': {
            'project_ids': [
                {
                    'project_id': 'degenerateapekindergarten'
                }
            ],
            'name': {
                'operation': 'EXACT', 
                'value': 'Degen Egg #' + str(pfp_id)
                },
        }
    })
    headers = {
        'Authorization': os.environ['HYPER_TOKEN'],
        'Content-Type': 'application/json'
    }
    r = requests.post('https://beta.api.solanalysis.com/rest/get-market-place-snapshots', headers=headers, data=payload)
    
    url = r.json()['market_place_snapshots'][0]['meta_data_img']

    download_image(url, pfp_egg_folder + str(pfp_id) + '.png')

# This combines the images 

    pfp = Image.open(pfp_egg_folder + str(pfp_id) + '.png')
    outfit = Image.open(outfits_egg_folder + fit + '.png')

    pfp.paste(outfit, (0, 0), mask=outfit)
    pfp.save(save_egg_img_folder + 'dressed' + str(pfp_id) + '.png')

    return

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# !beerme command executes the get_dressed function and returns the resulting image. It accepts a value between 1 and 10000. Update this to use the command name you want and the values to fit the range of your project

@bot.command(name="beerme", brief='Add a beer helmet to your pfp', description='This command will let you apply new fits to your pfp')
async def beerme(ctx, pfp_id: int, fit: typing.Optional[str] = "clean"):
    try:
      if fit.lower() in outfits:
        if 0 <= pfp_id <= 10000:
            get_dressed(fit, str(pfp_id))
            await ctx.channel.send(file=discord.File(save_img_folder + 'dressed' + str(pfp_id) +'.png'))
      else: 
        await ctx.send('Please enter a valid fit. Check !fits for options')
    except:
        await ctx.send('Please enter a valid number between 1 and 10000.')

@bot.command(name="beerme-ape", brief='Add a beer helmet to your pfp', description='This command will let you apply new fits to your pfp')
async def beerme_ape(ctx, pfp_id: int, fit: typing.Optional[str] = "clean"):
    try:
      if fit.lower() in outfits:
        if 0 <= pfp_id <= 10000:
            get_dressed(fit, str(pfp_id))
            await ctx.channel.send(file=discord.File(save_img_folder + 'dressed' + str(pfp_id) +'.png'))
      else: 
        await ctx.send('Please enter a valid fit. Check !fits for options')
    except:
        await ctx.send('Please enter a valid number between 1 and 10000.')

@bot.command(name="seven", brief='Add a jersey to your pfp', description='This command will let you apply new fits to your pfp')
async def seven(ctx, pfp_id: int):
    try:
        if 0 <= pfp_id <= 10000:
            get_jersey_dressed(str(pfp_id))
            await ctx.channel.send(file=discord.File(save_jersey_img_folder + str(pfp_id) +'.png'))
    except:
        await ctx.send('Please enter a valid number between 1 and 10000.')

@bot.command(name="beerme-panda", brief='Add a beer helmet to your trashy Panda', description='This command will let you add a beer helmet to your DTP')
async def beer_panda(ctx, pfp_id: int, fit: typing.Optional[str] = "clean"):
    try:
      if fit.lower() in outfits:
        if 0 <= pfp_id <= 20000:
            get_dtp_dressed(fit, str(pfp_id))
            await ctx.channel.send(file=discord.File(save_dtp_img_folder + 'dressed' + str(pfp_id) +'.png'))
      else: 
        await ctx.send('Please enter a valid fit. Check !fits for options')
    except:
        await ctx.send('Please enter a valid number between 1 and 20000.')

@bot.command(name="beer-panda", brief='Add a beer helmet to your trashy Panda', description='This command will let you add a beer helmet to your DTP')
async def beer_panda(ctx, pfp_id: int, fit: typing.Optional[str] = "clean"):
    try:
      if fit.lower() in outfits:
        if 0 <= pfp_id <= 20000:
            get_dtp_dressed(fit, str(pfp_id))
            await ctx.channel.send(file=discord.File(save_dtp_img_folder + 'dressed' + str(pfp_id) +'.png'))
      else: 
        await ctx.send('Please enter a valid fit. Check !fits for options')
    except:
        await ctx.send('Please enter a valid number between 1 and 20000.')

@bot.command(name="beerme-egg", brief='Add a beer helmet to your lovely Egg', description='This command will let you add a beer helmet to your DEGG')
async def beer_egg(ctx, pfp_id: int, fit: typing.Optional[str] = "clean"):
    try:
      if fit.lower() in outfits:
        if 0 <= pfp_id <= 2500:
            get_egg_dressed(fit, str(pfp_id))
            await ctx.channel.send(file=discord.File(save_egg_img_folder + 'dressed' + str(pfp_id) +'.png'))
      else: 
        await ctx.send('Please enter a valid fit. Check !fits for options')
    except:
        await ctx.send('Please enter a valid number between 1 and 2500.')

@bot.command(name="bussin", brief='You bussin fr fr no cap', description='This command will let you be much cooler than you are')
async def bussin_ape(ctx, pfp_id: int, fit: typing.Optional[str] = "black"):
    try:
      if fit.lower() in outfits:
        if 0 <= pfp_id <= 10000:
            get_bussin(fit, str(pfp_id))
            await ctx.channel.send(file=discord.File(save_bussin_img_folder + 'dressed' + str(pfp_id) +'.png'))
      else: 
        await ctx.send('Please enter a valid fit. Check !fits for options')
    except:
        await ctx.send('Please enter a valid number between 1 and 10000.')

# Lists the different "fits" available. This just returns the outfits list on new lines 

@bot.command(brief='List avaiable fits', description='This command will list the different outfits available to you')
async def fits(ctx):
    await ctx.send('**List of Fits (please choose from one of the below)**\n\n'+ "\n".join(outfits))

# Lets user know when they enter an invalid command
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound): # or discord.ext.commands.errors.CommandNotFound as you wrote
        await ctx.send("Unknown command, please check !help for a list of available commands")

load_dotenv()

bot.run(os.environ['DISCORD_TOKEN'])

