# bot.py
from os import getenv
import discord
import sqlite3
from discord.ext import commands
from dotenv import load_dotenv
from tabulate import tabulate
import json
import time
import asyncio
import aiohttp
import random
from pathlib import Path
import sqlite3
from sqlite3 import Error
import pandas as pd


load_dotenv()
token = getenv('DISCORD_TOKEN')

###### Logging



###### Setting up the fandoa table

conn = sqlite3.connect("Discord.db") # or: memory:
cursor = conn.cursor()

try:
    cursor.execute('''CREATE TABLE "test1" (
	"Mid" INT,
	"mandoa" TEXT,
	"pronunciation" TEXT,
	"english" TEXT,
        "server" INT,
        "author" TEXT,
        "roots" TEXT,
        UNIQUE(mandoa,english)   )''')
    
except:
    print('already created')

###### function to call SQL function

def execute_query(query):
    if conn is not None:
        try:            
            output = []
            c = conn.cursor()
            try:
                #print('\nQuery:',query)
                c.execute(query)
            except Exception as e:
                print('e1')
                print(query)
                return e
            info = c.fetchall()
            conn.commit()

            #print('INFO: ',info)

            ke = query.replace(',','').split(' ')
            if 'FROM' in ke:
                id = ke[2:ke.index('FROM')]
            if len(id) > 0:
                for value in info:
                    iv = [v for v in value]
                    output.append(dict(zip(id,iv)))

            else: # COUNT
                #print('INFO debug: ',info)
                output.append(info[0][0])
            if output=="":
                return "No Output / Empty"
            return output
        except Exception as e:
            return e
    else:
        print('conn is none')
    return "Error! the database connection was not created."

#####

bot = commands.Bot(command_prefix = "!") # in the command_prefix line, you can specify any sign, letter, word, word combinations, etc


@bot.event
async def on_ready():
    print("Bot Has been activated") # ready message
    print("Guilds:")
    for guild in bot.guilds: # because. bot for one server, then the loop displays one server
        print(guild.id,' ',guild) # output server id
        serv = guild # no idea why this is
        for member in guild.members: # loop that processes the list of members
            print(member.id,' ',member)
                #print(execute_query())

            
            v = cursor.execute('''SELECT mandoa, english FROM test1 WHERE INSTR(mandoa,"ver")''')
            # where id = {member.id}") # check if a member exists in the database
            #print(v.fetchall())

            if v.fetchone() == None: # If does not exist
                print('does not exist')
                url = 'https://mandoa.org/minimal/?query='
                async with aiohttp.ClientSession() as session:
                      raw_response = await session.get(url)
                      response = await raw_response.text()
                      response = json.loads(response)
                      for r in response:
                          va = list(r.values())
                          va[0] = str(va[0])
                          #print(va)
                          query = execute_query("INSERT INTO test1(Mid,mandoa,pronunciation,english,server,author,roots) VALUES("+ va[0]+',"' +'","'.join(va[1:])+'",'+"'','mandoa.org','')")
                          print(query)
                          
                          conn.commit()
                      #m = execute_query('''INSERT Discord.db test1 response --ignore''')
                      #print(m)

                
                #cursor.execute(f"INSERT INTO users VALUES ({member.id}, '{member.name}', '<@ {member.id}>', 50000, 'S', '[]', 0,0 ) ") # enters all data about the participant in the database
            else: # if exists
                #q = cursor.execute('''SELECT * from test1''')
                #res = q.fetchall()
                #print(res)
                pass

            print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
            conn.commit() # apply changes to the database


######### FANDOA ##

@bot.command(aliases=["f"],pass_context=True,name='fandoa',help='accesses local fandoa file dictionary - NOT an existing google doc',brief='based on mandoa.org dictionary bot; fandoa sqlite3 database',description='to search, use `!fandoa [SEARCHTERM] [LANGUAGE]`; where language is either mandoa or english and term is what you are looking for\n\nUse `!fandoa [SEARCHTERM] [LANGUAGE [s]` (or s) if you are searching for an exact word, instead of words containing the search term. Search works for all single quotation marks')
async def fandoa(ctx, *, arg):
    args = arg.split(' ')
    if len(args) == 1:args.append('mandoa')
    term,language=args[0],args[1].lower()
    term = term.replace('_',' ').replace("'","''")
    if args[1].lower() == 'e':language='english'
    elif args[1].lower() == 'm':language='mandoa'
    
    root = False
    pronun=False
    spec=False
    
    args = [a.lower() for a in args]
    if 'root' in args or 'r' in args: root=True
    if 'pron' in args or 'p' in args: pronun=True
    if 'spec' in args or 's' in args: spec=True

    lang = {'mandoa':0,'english':1}
    
    search1 = term.replace("â€˜","'")
    search2 = search1.replace("`","'")
    term = search2.replace("â€™","'")
    #[j.pop('ID') for j in found]
    
    try:
        query1 = '''SELECT DISTINCT mandoa, english FROM test1 WHERE INSTR('''+language+''',"'''+term+'''")'''
        if root:
            query1 = query1.replace('sh FR','sh, roots FR').replace("INSTR("+language,'INSTR(roots')
        if pronun:
            #print('PRONUN IS TRUE')
            query1 = query1.replace('oa, en','oa, pronunciation, en')
        if spec:
            query1 = query1.replace('INSTR('+language+',"',language+'== "')[:-1]

        #print("query1:", query1)

        found = execute_query(query1)
    except Exception as E:
        print('Error try : ', E)
        await ctx.send('Error: {}'.format(E))
        return
    else:
        if not isinstance(found,list):
            await ctx.send('Error with Search parameters: {}'.format(found),delete_after=15)
            return
        else:
            print('Success!')
            

    if pronun and not len(found) == 0:
        title = term
        desc = '*Searching for the term* `\"'+term+'\"`'
        embed=discord.Embed(title=title, url="https://mandoa.org/minimal", description=desc, color=0x468847)
        embed.set_author(name="mandoa.org", url="https://mandoa.org")#, icon_url="./my_myth.png")
        for j in found:
            v = j['english']
            v2 = "`"+j['pronunciation']+"`"
            v1 = v2+"\n> "+v+"\n--------------\n"
            #print(v1)
            if len(j['mandoa']) > 256:
                v1="**"+j[language]+"**\n\n"+v1
                embed.add_field(name='See Below', value=v1, inline=False)
            else:
                embed.add_field(name=j['mandoa'], value=v1, inline=False)

    elif not len(found) == 0:
        title = term
        desc = '*Searching for the term* `\"'+term+'\"`'
        embed=discord.Embed(title=title, url="https://mandoa.org/minimal", description=desc, color=0x468847)
        embed.set_author(name="mandoa.org", url="https://mandoa.org")#, icon_url="./my_myth.png")
        for j in found:
            #print(j,'\n',type(j),'\n')
            v = j['english']
            v1 = "> "+v+"\n--------------\n"
            if len(j['mandoa']) > 256:
                v1="**"+j[language]+"**\n\n"+v1
                embed.add_field(name='See Below', value=v1, inline=False)
            else:
                embed.add_field(name=j['mandoa'], value=v1, inline=False)

    else: # no results
        title = term
        desc = '*Searching for the term* `\"'+term+'\"`'
        embed=discord.Embed(title=title, url="https://mandoa.org/minimal", description=desc, color=0x468847)
        embed.set_author(name="mandoa.org", url="https://mandoa.org")#, icon_url="./my_myth.png")
        embed.add_field(name=term, value='not found on mandoa.org', inline=False)
        
    conn.commit()
    await ctx.send(embed=embed,delete_after=30)
    await ctx.message.delete()

######## EDIT ###
    
@bot.command(aliases=["fe"],pass_context=True,name='fandoa_edit',help='edit local fandoa sqlite3 database',brief='update local fandoa database',description='use `!fandoa_edit [FANDOA_WORD] [COLUMN] [new_phrase]`. If this changes in the future, any additional keys will be documented here.\n\n.Also, if you want to replace a specific phrase, please use `_` instead of da space.\n\nWARNING: This function is case sensitive\n\nExample: !fe jat roots jatne jatne;_jate')
#@commands.has_role('admin')
async def fandoa_edit(ctx, *, arg):
    args = arg.split(' ')
    term,column=args[0],args[1]
    #args = [a.lower() for a in args]

    new_term = args[2]
    new_term = new_term.replace('_',' ')

    term = term.replace('_',' ')
    
    search1 = term.replace("â€˜","'")
    search2 = search1.replace("`","'")
    term = search2.replace("â€™","'")
    #term = term.replace("'","''")

    lang = {'mandoa':0,'english':1}

    try:
        find = execute_query('''SELECT DISTINCT mandoa, english FROM test1 WHERE INSTR( mandoa,"'''+term+'''")''')
        #print('find:',find)
        if isinstance(find,list):
            memb = '{}'.format(ctx.message.author)
            gld = '{}'.format(ctx.guild)
            gld = gld.replace("'","''")
            memb = memb.replace("'","''")

            #print('''UPDATE test1 SET '''+column+''' = "'''+new_term+'''", server = "'''+gld+'''", author = "'''+memb+'''" WHERE INSTR(mandoa, "'''+term+'''")''')
            out = execute_query('''UPDATE test1 SET '''+column+''' = "'''+new_term+'''", server = "'''+gld+'''", author = "'''+memb+'''" WHERE INSTR(mandoa, "'''+term+'''")''')
            print('out :',out)
    except Exception as E:
        print(E)
       # print('try select exception')
        await ctx.send('Error0: {}'.format(E))
        return
    else:
        print('updated successfully!')

      
    conn.commit()
    await ctx.send('You edited the entry for {} in fandoa!.'.format(term),delete_after=30)
    
    try:
        if column != 'mandoa' and column != 'english':
            query1 = '''SELECT DISTINCT mandoa, english,'''+column+''' FROM test1 WHERE mandoa == "'''+term+'"'
        else:
            if column == 'mandoa':term = new_term
            query1 = '''SELECT DISTINCT mandoa, english FROM test1 WHERE mandoa == "'''+term+'"'
        found = execute_query(query1)
    except Exception as E:
        print('Error try : ', E)
        await ctx.send('Error: {}'.format(E))
        return
    else:
        if not isinstance(found,list):
            await ctx.send('Error with Search parameters: {}'.format(found),delete_after=30)
            return
        else:
            print('Success!')
            

    desc = '*Edited the term* `\"'+term+'\"`'
    embed=discord.Embed(title=term, url="https://mandoa.org/minimal", description=desc, color=0x468847)
    embed.set_author(name="mandoa.org", url="https://mandoa.org")#
    for j in found:
        v = j['english']
        if column == 'pronunciation':v2 = "`"+j['pronunciation']+"`"
        else:v2 = ""
        v1 = v2+"\n> "+v+"\n--------------\n"
        if len(j['mandoa']) > 256:
            v1="**"+j['mandoa']+"**\n\n"+v1
            embed.add_field(name='See Below', value=v1, inline=False)
        else:
            embed.add_field(name=j['mandoa'], value=v1, inline=False)

    await ctx.message.delete()
    await ctx.send(embed=embed, delete_after=30) 

######### ADD ##
    
@bot.command(aliases=["fa"],pass_context=True,name='fandoa_add',help='add entry to fandoa sqlite3 database',brief='add to local fandoa dictionary',description='use `!fandoa_add [FANDOA_WORD] [Definition] [ROOT(S)] [Pronunciation]. Roots is needed - list the word(s) that are used to make your new word. If there are more than one root in your new word, please use an underscore instead of a space.If your word *has* no roots, please use a dash instead. Pronunciation is optional, but is the fourth string.\n\n.Also, if you want to add a specific phrase, please use `_` instead of a space.\n\nWARNING: This function is case sensitive\n\nExample: `!fa jat correct;_valid_from_Jango_the_Muse jatne JAT`')
#@commands.has_role('admin')
async def fandoa_add(ctx, *, arg):#search: str, language: str, root: bool):
    args = arg.split(' ')
    term,definition=args[0],args[1]
    roots = args[2]
    pronun = ''
    if len(args) > 3:
        pronun = args[3]

    term = term.replace('_',' ')
    definition = definition.replace('_',' ')
    roots = roots.replace('_',' ')
    
    search1 = term.replace("â€˜","'")
    search2 = search1.replace("`","'")
    term = search2.replace("â€™","'")

    lang = {'mandoa':0,'english':1}

    try:
        vn = execute_query("SELECT COUNT(*) FROM test1")
        #print(vn[0])

        memb = '{}'.format(ctx.message.author)
        gld = '{}'.format(ctx.guild)
        memb = memb.replace("'","''")
        gld = gld.replace("'","''")

        out = execute_query("INSERT INTO test1(Mid,mandoa,pronunciation,english,server,author,roots) VALUES("+str(vn[0]+1)+',"'+term+'","'+pronun +'","'+definition+'","'+gld+'","'+memb+'","'+roots+'")')
        
        #print(out)
    except Exception as E:
        #print(E)
        await ctx.send('Error: {}'.format(E),delete_after=15)
        return
    else:
        out = execute_query('SELECT distinct mandoa english FROM test1  WHERE INSTR(mandoa,"'+term+'")')
        #print(out)
    
    conn.commit()

    await ctx.send('You added the new entry for {} to: fandoa!.'.format(term),delete_after=30)

    
    try:
        query1 = '''SELECT DISTINCT * FROM test1 WHERE mandoa == "'''+term+'"'
        found = execute_query(query1)
    except Exception as E:
        await ctx.send('Error: {}'.format(E))
        return
    else:
        if not isinstance(found,list):
            await ctx.send('Error with Search parameters: {}'.format(found),delete_after=30)
            return
        else:
            print('Success!')
            

    desc = '*Added the term* `\"'+term+'\"`'
    embed=discord.Embed(title=term, url="https://mandoa.org/minimal", description=desc, color=0x468847)
    embed.set_author(name="mandoa.org", url="https://mandoa.org")#
    for j in found:
        v = j['english']
        v2 = "`"+j['pronunciation']+"`"
        v1 = v2+"\n> "+v+"\n--------------\n"
        if len(j['mandoa']) > 256:
            v1="**"+j[language]+"**\n\n"+v1
            embed.add_field(name='See Below', value=v1, inline=False)
        else:
            embed.add_field(name=j['mandoa'], value=v1, inline=False)

    await ctx.message.delete()
    await ctx.send(embed=embed, delete_after=30)    
    
    
######### DELETE ##
    
@bot.command(aliases=["fd"],pass_context=True,name='fandoa_delete',help='remove entry from local fandoa sqlite3 database',brief='remove from local fandoa dictionary',description='use `!fandoa_delete [FANDOA_WORD] or !fd [FANDOA_WORD] to remove the word [FANDOA_WORD] from the database')
#@commands.has_role('admin')
async def fandoa_delete(ctx, *, arg):#search: str, language: str, root: bool):
    args = arg.split(' ')
    term=args[0]
    term = term.replace('_',' ')
    
    search1 = term.replace("â€˜","'")
    search2 = search1.replace("`","'")
    term = search2.replace("â€™","'")

    try:
        out = execute_query('DELETE FROM test1 WHERE mandoa = "'+term+'"')
    except Exception as E:
        await ctx.send('Error: {}'.format(E),delete_after=30)
        return
    
    conn.commit()

    await ctx.send('You removed the entry for {} from: fandoa!.'.format(term),delete_after=30)
    await ctx.message.delete()
    
######### MANDO ##

@bot.command(aliases=["m"],pass_context=True,name='mandoa',help='searches mandoa.org for words',brief='mandoa.org dictionary bot',description='to search, use `!mandoa [SEARCHTERM] [LANGUAGE]` ; where language is either mandoa or english and term is what you are looking for\n\nUse `!mandoa [SEARCHTERM] [LANGUAGE] [-S]` if you are searching for an exact word, instead of words containing the search term\n\nUse `!mandoa [SEARCHTERM] [LANGUAGE] [-P]` if you want to have the pronunciation shown as well.')
async def mandoa(ctx, *, arg):
    args = arg.split(' ')
    if len(args) == 1:args.append('mandoa')
    search,language=args[0],args[1].lower()
    
    if args[1].lower() == 'e':language='english'
    elif args[1].lower() == 'm':language='mandoa'
    
    spec=False
    pronun=False
    
    args = [a.lower() for a in args]
    if 'spec' in args or 's' in args: spec=True
    if 'pron' in args or 'p' in args: pronun=True

    lang = {'mandoa':0,'english':1}
        
    url = 'https://mandoa.org/minimal/?query='
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)

        search1 = search.replace("â€˜","'")
        search2 = search1.replace("`","'")
        search = search2.replace("â€™","'")
        if not spec:found = [element for element in response if search in element[language]]
        else:found = [element for element in response if element[language]==search]
        [j.pop('ID') for j in found]

        if pronun and not len(found) == 0:
            title = search
            desc = '*Searching for the term* `\"'+search+'\"`'
            embed=discord.Embed(title=title, url="https://mandoa.org/minimal", description=desc, color=0x468847)
            embed.set_author(name="mandoa.org", url="https://mandoa.org")
            for j in found:
                v = j['english']
                v2 = "`"+j['pronunciation']+"`"
                v1 = v2+"\n> "+v+"\n--------------\n"
                if len(j['mandoa']) > 256:
                    v1="**"+j[language]+"**\n\n"+v1
                    embed.add_field(name='See Below', value=v1, inline=False)
                else:
                    embed.add_field(name=j['mandoa'], value=v1, inline=False)

        elif not len(found) == 0:
            title = search
            desc = '*Searching for the term* `\"'+search+'\"`'
            embed=discord.Embed(title=title, url="https://mandoa.org/minimal", description=desc, color=0x468847)
            embed.set_author(name="mandoa.org", url="https://mandoa.org")
            for j in found:
                v = j['english']
                v1 = "> "+v+"\n--------------\n"
                if len(j['mandoa']) > 256:
                    v1="**"+j[language]+"**\n\n"+v1
                    embed.add_field(name='See Below', value=v1, inline=False)
                else:
                    embed.add_field(name=j['mandoa'], value=v1, inline=False)

        else: # no results
            title = search
            desc = '*Searching for the term* `\"'+search+'\"`'
            embed=discord.Embed(title=title, url="https://mandoa.org/minimal", description=desc, color=0x468847)
            embed.set_author(name="mandoa.org", url="https://mandoa.org")#, icon_url="./my_myth.png")
            embed.add_field(name=search, value='not found on mandoa.org', inline=False)

    conn.commit()
    await ctx.send(embed=embed,delete_after=30)
    await ctx.message.delete()

######

@bot.command(pass_context=True)
async def ping(ctx):
    '''Returns pong when called'''
    author = ctx.message.author.name
    #print(ctx.message)
    server = ctx.message.guild.name
    await ctx.send('Pong for {} from {}!'.format(author, server))

############
        
# Close the bot
@bot.command(aliases=["quit"])
@commands.has_permissions(administrator=True)
async def close(ctx):

    conn.commit()
    conn.close()
    await ctx.message.delete()
    await bot.close()
    print("Bot Closed")  # This is optional, but it is there to tell you


#########
        
if __name__ == '__main__':
    try:
        bot.run(token)
    except Exception as e:
        print('Could Not Start Bot')
        print(e)
    finally:
        print('Closing Session')
        #conn.commit()
        #bot.close()
