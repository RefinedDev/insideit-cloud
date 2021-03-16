import discord.ext
from discord.ext import commands,tasks
import os 
from datetime import datetime
import mysql.connector
import asyncio
import random

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='peg ',intents = intents)

# token = "Nzk1OTYzMjAzODA0MjAwOTgw.X_RAgA.aciIvaEGbyz8jEGII1iwMNZ9ugE"

@client.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.CommandNotFound):
        pass
    elif isinstance(error,commands.MissingPermissions):
        embed = discord.Embed(colour= discord.Colour.red(),timestamp = datetime.utcnow())
        embed.add_field(name="eyo calmdown",value= "You do not have the required permissions to run this command.")
        await ctx.send(embed= embed,delete_after=5)
    elif isinstance(error,commands.MissingRequiredArgument):
        pass
    else:
        print(error)


@client.event
async def on_ready():
    print("Bot is online!")
    await  client.change_presence(activity =discord.Activity(type= discord.ActivityType.listening,name= f'peg help in {len(client.guilds)} servers'))

@client.event
async def on_guild_join(guild):
    await  client.change_presence(activity =discord.Activity(type= discord.ActivityType.listening,name= f'peg help in {len(client.guilds)} servers'))

@client.event
async def on_guild_remove(guild):
    try:
        await  client.change_presence(activity =discord.Activity(type= discord.ActivityType.listening,name= f'peg help in {len(client.guilds)} servers'))
    except Exception as e:
        print(f'An Error Occured in on_guild_remove {e}')


def memberjoin(member):
    sentences = [
    f'**{member.name}#{member.discriminator}** has joined the server, we have {len(member.guild.members)} now!',
    f'**{member.name}#{member.discriminator}** fell from the sky we have {len(member.guild.members)} now!',f'{member.mention} showed up!',
    f'**{member.name}#{member.discriminator}** somehow became visible we have {len(member.guild.members)} now!',
    f'Welcome **{member.name}#{member.discriminator}** enjoy your stay! :D',
    f'Nice to meet you **{member.name}#{member.discriminator}**! We have {len(member.guild.members)} now!',
    f'Welcome **{member.name}#{member.discriminator}**, we hope you brought some snacks!'
    ]
    value = random.choice(sentences)
    return value

@client.event
async def on_member_join(member):
    try:
        db = mysql.connector.connect(
            host = "us-cdbr-east-02.cleardb.com",
            user = "bc4de25d94d683",
            passwd = "0bf00100",
            database = "heroku_1d7c0ca78dfc2ef"
        )
        cursor = db.cursor()
        guildid = str(member.guild.id)

        cursor.execute('SELECT * FROM mutedata WHERE userid = ' + str(member.id) + ' AND guildid = ' + str(member.guild.id))
        res = cursor.fetchall()
        if len(res) == 0:
            pass
        else:
            role = discord.utils.get(member.guild.roles,name = 'Muted')
            if role != None:
                await member.add_roles(role)

        cursor.execute("SELECT toggle,channelid from welcomemsg WHERE guildid = " + guildid)
        res = cursor.fetchall()

        if (len(res) == 0):
            return
        elif res[0][0] == 'OFF':
            cursor.execute("SELECT toggle,roleid from welcomeroles WHERE guildid = " + guildid)
            res = cursor.fetchall()

            if (len(res) == 0):
                return
            elif res[0][0] == 'OFF':
                return
            else:
                roleid = res[0][1]
                role = discord.utils.get(member.guild.roles, id= roleid)
                if role != None:
                    await member.add_roles(role)
                else:
                    pass
        else:
            channelid = res[0][1]
            channel = client.get_channel(int(channelid))
            if channel != None:
                msg = memberjoin(member)
                await channel.send(msg)
            else:
                pass
        cursor.execute("SELECT toggle,roleid from welcomeroles WHERE guildid = " + guildid)
        res = cursor.fetchall()

        if (len(res) == 0):
            return
        elif res[0][0] == 'OFF':
            return
        else:
            roleid = res[0][1]
            role = discord.utils.get(member.guild.roles, id= roleid)
            if role != None:
                await member.add_roles(role)
            else:
                pass
        cursor.close()
        db.close()
    except Exception as e:
        print(f"An error occured on_member_join {e}")

def memberleave(member):
    sentences = [
    f'**{member.name}#{member.discriminator}** decided to head out.',
    f'**{member.name}#{member.discriminator}** withered away.',
    f'**{member.name}#{member.discriminator}** disappeared.',
    f'Cya **{member.name}#{member.discriminator}** it was a good time.',
    f'We lost **{member.name}#{member.discriminator}**, we have {len(member.guild.members)} left.'
    ]
    value = random.choice(sentences)
    return value

@client.command()
async def getserver(ctx):
    if ctx.author.id == 429535933252239360:
        activeservers = client.guilds
        for guild in activeservers:
            await ctx.send(f"{guild.name} {guild.id} {guild.owner_id}")
        return

    await ctx.send(f"You don't have permissions to use that!")

@client.command()
async def leaveserver(ctx, id: int):
    if ctx.author.id == 429535933252239360:
        guild = client.get_guild(id)
        await guild.leave()
        await ctx.send(f"Left that server successfully")
        return

    await ctx.send(f"You don't have permissions to use that!")

@client.event
async def on_member_remove(member):
    try:
        db = mysql.connector.connect(
            host = "us-cdbr-east-02.cleardb.com",
            user = "bc4de25d94d683",
            passwd = "0bf00100",
            database = "heroku_1d7c0ca78dfc2ef"
        )
        cursor = db.cursor()
        guildid = str(member.guild.id)
        cursor.execute("SELECT toggle,channelid from leavemsg WHERE guildid = " + guildid)
        res = cursor.fetchall()

        if (len(res) == 0):
            return
        elif res[0][0] == 'OFF':
            return
        else:
            channelid = res[0][1]
            channel = client.get_channel(int(channelid))
            if channel != None:
                msg = memberleave(member)
                await channel.send(msg)
            else:
                pass
        cursor.close()
        db.close()
    except Exception as e:
        print(f"An error occured on_member_remove {e}")

@client.listen('on_message')
async def botping(message):
    if isinstance(message.channel, discord.channel.DMChannel):
        return
    if message.content == '<@!795963203804200980>':
        try:
            await message.channel.send('My prefix is `peg`')
        except Exception as e:
            print(f'Error in botping: {e}')


cogslist = ['cogs.misc','cogs.help','cogs.APIscrape','cogs.RPS','cogs.configurations','cogs.highrank','cogs.img','cogs.tags']

if __name__ == '__main__':
    for i in cogslist:
        client.load_extension(i)


client.run(os.environ['Token'])