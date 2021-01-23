import discord.ext
from discord.ext import commands,tasks
from discord.ext.commands import Cog
from datetime import datetime
import mysql.connector


class HighRank(Cog):
    def __init__(self,client):
        self.client = client

    @Cog.listener()
    async def on_ready(self):
        print("High Rank Cog Is Ready!")

    async def cog_command_error(self,ctx,error):
        if isinstance(error,commands.CommandNotFound):
            pass
        elif isinstance(error,commands.MissingPermissions):
            embed = discord.Embed(colour= discord.Colour.red(),timestamp = datetime.utcnow())
            embed.add_field(name="eyo calmdown",value= "You do not have the required permissions to run this command.")
            await ctx.send(embed= embed,delete_after=5)
        elif isinstance(error,commands.MissingRequiredArgument):
            pass
        elif isinstance(error,commands.MemberNotFound):
            embeddd = discord.Embed(colour= discord.Colour.red())
            embeddd.add_field(name = "eyo calmdown",value = f'Member Not Found.')
            await ctx.send(embed = embeddd,delete_after=5)
        elif isinstance(error,commands.CommandOnCooldown):
            embeddd = discord.Embed(colour= discord.Colour.red())
            embeddd.add_field(name = "eyo calmdown",value = f'This command is on cooldown, try again later after {error.retry_after:,.2f} seconds.')
            await ctx.send(embed = embeddd,delete_after=5)  
        else:
            print(error)

    #ClearChat
    @commands.command(aliases=['clear'])
    @commands.has_permissions(kick_members = True)
    async def purge(self,ctx,amount : int):
        await ctx.channel.purge(limit = amount)

    @purge.error
    async def clear_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            embeddd = discord.Embed(timestamp = datetime.utcnow(),colour= discord.Colour.red())
            embeddd.add_field(name = "Missing Number",value = "Please specify a Integer of how many messages you want to purge.",inline= False)
            embeddd.add_field(name = "Command Example",value = "`?purge 100`",inline= False)
            await ctx.send(embed = embeddd,delete_after=5)

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def announce(self,ctx,channelid,*,text):
        channel = self.client.get_channel(int(channelid))
        if channel != None:
            embed = discord.Embed()
            embed.add_field(name = f'Announcement By {ctx.author.name}',value = text)
            await channel.send(embed = embed)
        else:
            await ctx.send("Channel Not Found.")

    @announce.error
    async def announce_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            embeddd = discord.Embed(timestamp = datetime.utcnow(),colour= discord.Colour.red())
            embeddd.add_field(name = "Missing Text Or ChannelId",value = "Please specify the text and the channelid.",inline= False)
            embeddd.add_field(name = "Command Example",value = "`?announce 4209409582859589 Hello everyone`",inline= False)
            await ctx.send(embed = embeddd,delete_after=5)

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def slowmode(self,ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Slowmode Changed To {seconds}!")

    @slowmode.error
    async def slowmo_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send(f'This channel has a slowmode of {ctx.channel.slowmode_delay} seconds.')

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def warn(self,ctx,user : discord.Member,*,reason = 'Not Specified'):
        db = mysql.connector.connect(
            host = "us-cdbr-east-02.cleardb.com",
            user = "bc4de25d94d683",
            passwd = "0bf00100",
            database = "heroku_1d7c0ca78dfc2ef"
        )

        cursor = db.cursor()
        guildid = ctx.guild.id
        sql = "INSERT INTO logs (userid,reason,guildid,type) VALUES (%s, %s, %s, %s)"
        val = (str(user.id),str(reason),guildid,'Warn')
        cursor.execute(sql,val)
        db.commit()
        await ctx.send(f'{user.mention} was warned: {str(reason)}')
        await user.send(f'You were warned in {ctx.guild.name} reason: {str(reason)}')
        cursor.close()
        db.close()

    @warn.error
    async def warn_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            embeddd = discord.Embed(timestamp = datetime.utcnow(),colour= discord.Colour.red())
            embeddd.add_field(name = "Missing User Or Reason",value = "Specify the user and reason pal.",inline= False)
            embeddd.add_field(name = "Command Example",value = "`?warn 1938194824019 idk cuh`",inline= False)
            await ctx.send(embed = embeddd,delete_after=5)
    
    @commands.command(aliases = ['infraction','warns'])
    @commands.has_permissions(kick_members = True)
    async def inf(self,ctx,user : discord.Member):
        db = mysql.connector.connect(
            host = "us-cdbr-east-02.cleardb.com",
            user = "bc4de25d94d683",
            passwd = "0bf00100",
            database = "heroku_1d7c0ca78dfc2ef"
        )

        cursor = db.cursor()
        cursor.execute('SELECT reason,infid,type FROM logs WHERE userid = ' + str(user.id) + ' AND guildid = ' + str(ctx.guild.id))
        res = cursor.fetchall()
        embed = discord.Embed(title = f'Infractions Of {user.name}',color = ctx.author.color)
        if (len(res) == 0):
            embed.add_field(name = '**No Infractions Found**',value = 'This user has no infractions.')
        else:
            for i in res:
                embed.add_field(name = f'Infraction Id: **{i[1]}**',value = f'Type: {i[2]}\nReason: `{str(i[0])}`',inline = False)
        embed.set_footer(text = 'To revoke a warn use the warn_revoke (infID) command.')
        await ctx.send(embed = embed)
        cursor.close()
        db.close()

    @inf.error
    async def inf_error(self,ctx,error):
        if isinstance(error, commands.MissingRequiredArgument):
            embeddd = discord.Embed(timestamp = datetime.utcnow(),colour= discord.Colour.red())
            embeddd.add_field(name = "Missing User",value = "Specify the user pal.",inline= False)
            embeddd.add_field(name = "Command Example",value = "`?inf 1938194824019 `",inline= False)
            await ctx.send(embed = embeddd,delete_after=5)

    
    @commands.command()
    @commands.cooldown(1,60,commands.BucketType.user)
    @commands.has_permissions(kick_members = True)
    async def revoke_inf(self,ctx,infid):
        db = mysql.connector.connect(
            host = "us-cdbr-east-02.cleardb.com",
            user = "bc4de25d94d683",
            passwd = "0bf00100",
            database = "heroku_1d7c0ca78dfc2ef"
        )

        cursor = db.cursor()
        cursor.execute('SELECT reason FROM logs WHERE infid = ' + str(infid))
        res = cursor.fetchall()
        if (len(res) == 0):
            await ctx.send(f'ERROR 404: Warn with id {infid} not found.')
        else:
            cursor.execute('DELETE FROM logs WHERE infid = ' + str(infid))
            db.commit()
            await ctx.send(f'Warn with id {infid} was revoked.')
        cursor.close()
        db.close()

    @revoke_inf.error
    async def warn_reveke(self,ctx,error):
        if isinstance(error, commands.MissingRequiredArgument):
            embeddd = discord.Embed(colour= discord.Colour.red())
            embeddd.add_field(name = "Missing InfractionID",value = "Specify the infractionID pal.",inline= False)
            embeddd.add_field(name = "Command Example",value = "`?warn_revoke 1`",inline= False)
            embeddd.set_footer(text  = "PS: To get the ID of the infraction run the ?inf (userID) command and get the id of infraction.")
            await ctx.send(embed = embeddd,delete_after=5)

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self,ctx,member : discord.Member = None,*, reason = 'Not Specified'):
        if member == None:
            embeddd = discord.Embed(colour= discord.Colour.red())
            embeddd.add_field(name = "Missing User",value = "Specify the user pal.",inline= False)
            embeddd.add_field(name = "Command Example",value = "`?kick 472985252805298 idk cuh`",inline= False)
            await ctx.send(embed = embeddd,delete_after=5)
            return
        else:
            db = mysql.connector.connect(
                host = "us-cdbr-east-02.cleardb.com",
                user = "bc4de25d94d683",
                passwd = "0bf00100",
                database = "heroku_1d7c0ca78dfc2ef"
            )

            cursor = db.cursor()
            guildid = ctx.guild.id
            sql = "INSERT INTO logs (userid,reason,guildid,type) VALUES (%s, %s, %s, %s)"
            val = (str(member.id),str(reason),guildid,'Kick')
            cursor.execute(sql,val)
            db.commit()
            await member.kick(reason = reason)
            cursor.close() 
            db.close()




def setup(client):
    client.add_cog(HighRank(client))
