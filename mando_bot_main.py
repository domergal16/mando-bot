# bot.py
import os
import random
from dotenv import load_dotenv
import aiohttp
import json
import discord

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


# 2
# Change only the no_category default string
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

bot = commands.Bot(command_prefix='!',description='Mandalorian Dictionary Bot',help_command=help_command)

@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    #print(f'{bot.user.name} has connected to Discord!')

######

@bot.command(name='fandoa',help='accesses local fandoa file dictionary - NOT an existing google doc',brief=' basesd on mandoa.org dictionary bot',description='to search, use `!fandoa SEARCHTERM LANGUAGE` ; where language is either mandoa or english and term is what you are looking for\n\nUse `!fandoa SEARCHTERM LANGUAGE ROOT` (or -r) if you are searching for an exact word, instead of words containing the search term. Search works for all single quotation marks')
async def fandoa(ctx, *, arg):#search: str, language: str, root: bool):
    args = arg.split(' ')
    search,language=args[0],args[1].lower()
    root = False
    args = [a.lower() for a in args]
    if '-r' in args or 'root' in args:root = True

    #print(args.lower())

    with open('./fandoa.json') as f:
        response=json.load(f)

    search1 = search.replace("‘","'")
    search2 = search1.replace("`","'")
    search = search2.replace("’","'")
    if not root:found = [element for element in response if search in element[language]]
    else:found = [element for element in response if element[language]==search]
    [j.pop('ID') for j in found]
    title = search
    desc = '*Searching for the term* `\"'+search+'\"`'
    embed=discord.Embed(title=title, url="https://mandoa.org/minimal", description=desc, color=0x1a441c)
    embed.set_author(name="Local Fando'a dictionary")#, icon_url="./my_myth.png")
    for j in found:
        v = j['english']
        v1 = "`"+v+"`\n--------------\n"
        if len(j['mandoa']) > 256:
            v1="**"+j[language]+"**\n\n"+v1
            embed.add_field(name='See Below', value=v1, inline=False)
        else:
            embed.add_field(name=j['mandoa'], value=v1, inline=False)
    await ctx.send(embed=embed)

########

@bot.command(name='fandoa_edit',help='edit local fandoa file dictionary - NOT an existing google doc',brief=' update local fandoa dictionary',description='to search, use `!mandoa MANDOA_WORD LANGUAGE -REP Original_word New_word` ; where language is either the mandoa or english definition you wish to update and mandoa_word is the specific word you want to edit. -REP signals that you want to replace a part of the definition or term, and New_word is what you will be replacing the original with.\n\n `!mandoa MANDOA_WORD LANGUAGE TERM` is used when you want to replace the entire definition or term.\n\n The `fandoa.json` file will be updated.')
async def fandoa_edit(ctx, *, arg):#search: str, language: str, root: bool):
    args = arg.split(' ')
    search,language=args[0],args[1].lower()
    replace=False
    args = [a.lower() for a in args]

    if '-rep' in args or 'replace' in args:
        replace=True
        rep_og = args[-2]
        rep_new = args[-1]

    search1 = search.replace("‘","'")
    search2 = search1.replace("`","'")
    search = search2.replace("’","'")

    with open('./fandoa.json') as f:
        response=json.load(f)
        for j in response:
            if search == j['mandoa'] and replace:
                j[language].replace(rep_og,rep_new)
                break
            elif search == j['mandoa']:
                j[language]=args[-1]
                break

    os.remove('./fandoa.json')
    with open('./fandoa.json','w') as f:
        json.dump(response,f)

    found = [element for element in response if element['mandoa']==search]

    await ctx.send('You updated the {} entry for {}.'.format(language, search))

#########    
    
@bot.command(name='mandoa',help='searches mandoa.org for words',brief='mandoa.org dictionary bot',description='to search, use `!mandoa SEARCHTERM LANGUAGE` ; where language is either mandoa or english and term is what you are looking for\n\nUse `!mandoa SEARCHTERM LANGUAGE ROOT` if you are searching for an exact word, instead of words containing the search term')
async def mandoa(ctx, *, arg):#search: str, language: str, root: bool):
    args = arg.split(' ')
    search,language=args[0],args[1].lower()
    root = ''
    if len(args) > 2:
        root = args[2]
        
    url = 'https://mandoa.org/minimal/?query='
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        print('language: ',language)
        print('search: ',search)
        if "‘" in search:print("‘ found")
        if "`" in search:print("` found")
        if "’" in search:print("’ found")

        #l2 = ['mandoa','english']

        search1 = search.replace("‘","'")
        search2 = search1.replace("`","'")
        search = search2.replace("’","'")
        if not len(root) > 0:found = [element for element in response if search in element[language]]
        else:found = [element for element in response if element[language]==search]
        [j.pop('ID') for j in found]
        title = search
        desc = '*Searching for the term* `\"'+search+'\"`'
        embed=discord.Embed(title=title, url="https://mandoa.org/minimal", description=desc, color=0x1a441c)
        embed.set_author(name="mandoa.org", url="https://mandoa.org")#, icon_url="./my_myth.png")
        for j in found:
            v = j['english']
            v1 = "`"+v+"`\n--------------\n"
            if len(j['mandoa']) > 256:
                v1="**"+j[language]+"**\n\n"+v1
                embed.add_field(name='See Below', value=v1, inline=False)
            else:
                embed.add_field(name=j['mandoa'], value=v1, inline=False)
    await ctx.send(embed=embed)


# Close the bot
@bot.command(aliases=["quit"])
@commands.has_permissions(administrator=True)
async def close(ctx):
    await client.close()
    print("Bot Closed")  # This is optional, but it is there to tell you.

    
bot.run(TOKEN)
