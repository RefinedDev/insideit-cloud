import discord.ext
from discord.ext import commands,tasks
from discord.ext.commands import Cog
import mysql.connector
import asyncio
import random

botsrpslist = ['r','p','s']

class RockPaperScissors(Cog):
    def __init__(self,client):
        self.client = client

    @Cog.listener()
    async def on_ready(self):
        print("RPS Cog Is Ready!")

    async def cog_command_error(self,ctx,exc):
        if isinstance(exc,commands.CommandOnCooldown):
            embeddd = discord.Embed(colour= discord.Colour.red())
            embeddd.add_field(name = "ERROR",value = f'This command is on cooldown, try again later after {exc.retry_after:,.2f} seconds.')
            await ctx.send(embed = embeddd,delete_after=5)  

    def updateuserstats(self,name,theid):
        db = mysql.connector.connect(
            host = "us-cdbr-east-02.cleardb.com",
            user = "bc4de25d94d683",
            passwd = "0bf00100",
            database = "heroku_1d7c0ca78dfc2ef"
        )

        cursor = db.cursor()
        cursor.execute("SELECT wins from rpsrecords WHERE userid = " + str(theid))
        res = cursor.fetchall()
        if (len(res) == 0):
            sql = "INSERT INTO rpsrecords (name, userid) VALUES (%s, %s)"
            val = (name, theid)
            cursor.execute(sql,val)
            db.commit()
            print(f'New Column For {name} Has Been Created!!')
        else:
            newwin = res[0][0] + 1
            cursor.execute("UPDATE rpsrecords SET wins = " + str(newwin) + " WHERE userid = " + str(theid))   
            db.commit()
            print(f'Updates Wins For {name}!')
        db.close()
        cursor.close()

    @commands.command()
    @commands.cooldown(1,150,commands.BucketType.user)
    async def rps(self,ctx):
        db = mysql.connector.connect(
            host = "us-cdbr-east-02.cleardb.com",
            user = "bc4de25d94d683",
            passwd = "0bf00100",
            database = "heroku_1d7c0ca78dfc2ef"
        )

        cursor = db.cursor()
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        await ctx.send("Hey wanna play Rock Paper Scissors? Yes/No")
        try:
            msg = await self.client.wait_for('message',timeout = 50.0,check = check)
        except asyncio.TimeoutError:
            await ctx.send("Din't reply in time noob.")
            return
        else:
            if msg.content == "Yes" or msg.content == "YES" or msg.content == 'yes':
                await ctx.send("Okay, let's start")
                asyncio.sleep(0.5)
                await ctx.send("Choose something between `(r)` Rock, `(p)` Paper, `(s)` Scissors\nIf you want to quit just say `quit`")

                try:
                    finalmsg = await self.client.wait_for('message',timeout= 50.0, check = check)
                except asyncio.TimeoutError:
                    await ctx.send("Din't reply in time bye.")
                    return
                else:
                    if finalmsg.content == 'r' or finalmsg.content == 'p' or finalmsg.content == 's' or finalmsg.content == 'quit' or finalmsg.content == 'R' or finalmsg.content == 'P' or finalmsg.content == 'S' or finalmsg.content == 'QUIT':
                            plrchoice = str.lower(finalmsg.content)
                            botschoice = random.choice(botsrpslist)

                            if botschoice == 'p' and plrchoice == 'p':
                                await ctx.send("Draw")
                                await ctx.send(f"Your choice - `{plrchoice}`\nBot's Choice - `{botschoice}`")
                            elif botschoice == 's' and plrchoice == 's':
                                await ctx.send("Draw")
                                await ctx.send(f"Your choice - `{plrchoice}`\nBot's Choice - `{botschoice}`")
                            elif botschoice == 'r' and plrchoice == 'r':
                                await ctx.send("Draw")
                                await ctx.send(f"Your choice - `{plrchoice}`\nBot's Choice - `{botschoice}`")

                            elif botschoice == 'r' and plrchoice == 's':
                                await ctx.send("I Won!")
                                await ctx.send(f"Your choice - `{plrchoice}`\nBot's Choice - `{botschoice}`")
                            elif botschoice == 's' and plrchoice == 'p':
                                await ctx.send("I Won!")
                                await ctx.send(f"Your choice - `{plrchoice}`\nBot's Choice - `{botschoice}`")

                            elif botschoice == 'p' and plrchoice == 'r':
                                await ctx.send("I Won!")
                                await ctx.send(f"Your choice - `{plrchoice}`\nBot's Choice - `{botschoice}`")
                            elif botschoice == 'r' and plrchoice == 'p':
                                await ctx.send("You Won!")
                                self.updateuserstats(ctx.author.name,ctx.author.id)
                                await ctx.send(f"Your choice - `{plrchoice}`\nBot's Choice - `{botschoice}`")
                            elif botschoice == 'p' and plrchoice == 's':
                                await ctx.send("You Won!")
                                await ctx.send(f"Your choice - `{plrchoice}`\nBot's Choice - `{botschoice}`")
                                self.updateuserstats(ctx.author.name,ctx.author.id)
                            elif botschoice == 's' and plrchoice == 'r':
                                await ctx.send("You Won!")
                                await ctx.send(f"Your choice - `{plrchoice}`\nBot's Choice - `{botschoice}`")
                                self.updateuserstats(ctx.author.name,ctx.author.id)

                            elif plrchoice == 'quit':
                                await ctx.send("Coward <:uglycat:791151352885149717>")
                                return

                    else:
                        await ctx.send("Invalid Choice")
                        return
            
            elif msg.content == 'No' or msg.content == 'NO' or msg.content == 'no':
                await ctx.send("Bruh why did u call me then >:C bye")
                return
            else:
                await ctx.send("Invalid Choice.")
                return
        db.close()
        cursor.close()

    @commands.command()
    @commands.cooldown(1,150,commands.BucketType.guild)
    async def rpsLeaderboard(self,ctx):
        db = mysql.connector.connect(
            host = "us-cdbr-east-02.cleardb.com",
            user = "bc4de25d94d683",
            passwd = "0bf00100",
            database = "heroku_1d7c0ca78dfc2ef"
        )

        cursor = db.cursor()
        cursor.execute("SELECT * FROM rpsrecords LIMIT 0,10")
        index = cursor.fetchall()
        embed = discord.Embed(title = "Top 10 Highest Global RPS Wins.",color = ctx.author.color)
        for i in index:
            embed.add_field(name = f'**{i[0]}**',value = f'Name: **{i[0]}**\nUserId: **{i[1]}**\nWins: **{i[2]}**',inline = False)

        await ctx.send(embed = embed)
        db.close()
        cursor.close()


def setup(client):
    client.add_cog(RockPaperScissors(client))
    