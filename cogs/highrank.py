import discord.ext
from discord.ext import commands,tasks
from discord.ext.commands import Cog
from datetime import datetime
import mysql.connector
import asyncio
from dateutil.relativedelta import relativedelta
import json

class HighRank(Cog):
    def __init__(self,client):
        self.client = client
    
    @Cog.listener()
    async def on_ready(self):
        print("High Rank Cog Is Ready!")
        self.mute_loop.start()
    
    def get_prefix(self,client,message):
        with open('customperms.json','r') as f:
            perms = json.load(f)
        
        return perms[message.guild.id]

    print(get_prefix)
    #ClearChat
    @commands.command(aliases=['clear'])
    @commands.has_permissions(manage_messages = True)
    async def purge(self,ctx,amount : int = None):
        if amount == None:
            embeddd = discord.Embed(timestamp = datetime.utcnow(),colour= discord.Colour.red())
            embeddd.add_field(name = "Missing Number",value = "Please specify a Integer of how many messages you want to purge.",inline= False)
            embeddd.add_field(name = "Command Example",value = "`peg purge 100`",inline= False)
            await ctx.send(embed = embeddd,delete_after=5)
            return

        await ctx.channel.purge(limit = amount)

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def announce(self,ctx,channelid = None,*,text = None):
        if channelid == None:
            embeddd = discord.Embed(timestamp = datetime.utcnow(),colour= discord.Colour.red())
            embeddd.add_field(name = "Missing ChannelId",value = "Please specify channelid.",inline= False)
            embeddd.add_field(name = "Command Example",value = "`peg announce 4209409582859589 Hello everyone`",inline= False)
            await ctx.send(embed = embeddd,delete_after=5)
            return
        if text == None:
            embeddd = discord.Embed(timestamp = datetime.utcnow(),colour= discord.Colour.red())
            embeddd.add_field(name = "Missing Text",value = "Please specify the text.",inline= False)
            embeddd.add_field(name = "Command Example",value = "`peg announce 4209409582859589 Hello everyone`",inline= False)
            await ctx.send(embed = embeddd,delete_after=5)
            return
        channel = self.client.get_channel(int(channelid))
        if channel != None:
            embed = discord.Embed(color = ctx.author.color)
            embed.add_field(name = f'Announcement By {ctx.author.name}',value = text)
            await channel.send(embed = embed)
        else:
            await ctx.send("Channel Not Found.")



    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def slowmode(self,ctx, seconds: int = None):
        if seconds == None:
            await ctx.send(f'This channel has a slowmode of {ctx.channel.slowmode_delay} seconds.')
            return
        await ctx.channel.edit(slowmode_delay=seconds)
        embed = discord.Embed(color = discord.Colour.green(),description = f'✅ Slowmode changed to {seconds} seconds')
        await ctx.send(embed = embed)

    @commands.command()
    @commands.cooldown(1,30,commands.BucketType.user)
    @commands.has_permissions(kick_members = True)
    async def warn(self,ctx,user : discord.Member = None,*,reason = 'Not Specified'):
        if user == ctx.author:
            await ctx.send('look at this dood tryna warn himself.')
            return
        if user == None:
            embeddd = discord.Embed(timestamp = datetime.utcnow(),colour= discord.Colour.red())
            embeddd.add_field(name = "Missing User Or Reason",value = "Specify the user and reason pal.",inline= False)
            embeddd.add_field(name = "Command Example",value = "`peg warn 1938194824019 idk cuh`",inline= False)
            await ctx.send(embed = embeddd,delete_after=5)
            return

        if user.top_role > ctx.author.top_role:
            embeddd = discord.Embed(timestamp = datetime.utcnow(),colour= discord.Colour.red())
            embeddd.add_field(name = "eyo calmdown",value = "The user has a higher role than you.",inline= False)
            await ctx.send(embed = embeddd,delete_after=5)
            return

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
        embed = discord.Embed(color = discord.Colour.green(),description = f'✅ **{user.name}** was warned | {str(reason)}.')
        await ctx.send(embed = embed)
        embed = discord.Embed(color = discord.Colour.green(),description = f'You were warned in **{ctx.guild.name}** | {str(reason)}.')
        await user.send(embed = embed)
        cursor.close()
        db.close()
    
    
    @commands.command(aliases = ['infraction','modlogs'])
    @commands.cooldown(1,30,commands.BucketType.user)
    @commands.has_permissions(kick_members = True)
    async def inf(self,ctx,user : discord.Member = None):
        if user == None:
            embeddd = discord.Embed(timestamp = datetime.utcnow(),colour= discord.Colour.red())
            embeddd.add_field(name = "Missing User",value = "Specify the user pal.",inline= False)
            embeddd.add_field(name = "Command Example",value = "`peg inf 1938194824019 `",inline= False)
            await ctx.send(embed = embeddd,delete_after=5)
            return

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
        embed.set_footer(text = 'To revoke a warn use the peg revoke_inf (infID) command.')
        await ctx.send(embed = embed)
        cursor.close()
        db.close()

    
    @commands.command()
    @commands.cooldown(1,30,commands.BucketType.user)
    @commands.has_permissions(kick_members = True)
    async def revoke_inf(self,ctx,infid = None):
        if infid == None:
            embeddd = discord.Embed(colour= discord.Colour.red())
            embeddd.add_field(name = "Missing InfractionID",value = "Specify the infractionID pal.",inline= False)
            embeddd.add_field(name = "Command Example",value = "`peg warn_revoke 1`",inline= False)
            embeddd.set_footer(text  = "PS: To get the ID of the infraction run the peg inf (userID) command and get the id of infraction.")
            await ctx.send(embed = embeddd,delete_after=5)
            return

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
            embed = discord.Embed(color = discord.Colour.green(),description = f'✅ Warn with id **{infid}** was revoked.')
            await ctx.send(embed = embed)
        cursor.close()
        db.close()

    @commands.command()
    @commands.cooldown(1,30,commands.BucketType.user)
    @commands.has_permissions(kick_members = True)
    async def kick(self,ctx,member : discord.Member = None,*, reason = 'Not Specified'):
        if member == ctx.author:
            await ctx.send('look at this dood tryna kick himself.')
            return

        if member == None:
            embeddd = discord.Embed(colour= discord.Colour.red())
            embeddd.add_field(name = "Missing User",value = "Specify the user pal.",inline= False)
            embeddd.add_field(name = "Command Example",value = "`peg kick 472985252805298 idk cuh`",inline= False)
            await ctx.send(embed = embeddd,delete_after=5)
            return
        elif member.top_role > ctx.author.top_role:
                embeddd = discord.Embed(timestamp = datetime.utcnow(),colour= discord.Colour.red())
                embeddd.add_field(name = "eyo calmdown",value = "The user has a higher role than you.",inline= False)
                await ctx.send(embed = embeddd,delete_after=5)
                return
        elif member.top_role > ctx.guild.me.top_role:
            embeddd = discord.Embed(timestamp = datetime.utcnow(),colour= discord.Colour.red())
            embeddd.add_field(name = "eyo calmdown",value = "The user has a higher role than me.",inline= False)
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
            embed = discord.Embed(color = discord.Colour.green(),description = f'✅ **{member.name}** was kicked | {str(reason)}.')
            await ctx.send(embed = embed)
            embed = discord.Embed(color = discord.Colour.green(),description = f'You were kicked from **{ctx.guild.name}** | {str(reason)}.')
            await member.send(embed = embed)
            await member.kick(reason = reason)
            cursor.close() 
            db.close()


    @commands.command()
    @commands.cooldown(1,30,commands.BucketType.user)
    @commands.has_permissions(ban_members = True)
    async def ban(self,ctx,member : discord.Member = None,*, reason = 'Not Specified'):
        if member == ctx.author:
            await ctx.send('look at this dood tryna ban himself.')
            return
        if member == None:
            embeddd = discord.Embed(colour= discord.Colour.red())
            embeddd.add_field(name = "Missing User",value = "Specify the user pal.",inline= False)
            embeddd.add_field(name = "Command Example",value = "`peg ban 472985252805298 idk cuh`",inline= False)
            await ctx.send(embed = embeddd,delete_after=5)
            return
        elif member.top_role > ctx.author.top_role:
                embeddd = discord.Embed(timestamp = datetime.utcnow(),colour= discord.Colour.red())
                embeddd.add_field(name = "eyo calmdown",value = "The user has a higher role than you.",inline= False)
                await ctx.send(embed = embeddd,delete_after=5)
                return
        elif member.top_role > ctx.guild.me.top_role:
            embeddd = discord.Embed(timestamp = datetime.utcnow(),colour= discord.Colour.red())
            embeddd.add_field(name = "eyo calmdown",value = "The user has a higher role than me.",inline= False)
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
            val = (str(member.id),str(reason),guildid,'Ban')
            cursor.execute(sql,val)
            db.commit()
            embed = discord.Embed(color = discord.Colour.green(),description = f'✅ **{member.name}** was banned | {str(reason)}.')
            await ctx.send(embed = embed)
            embed = discord.Embed(color = discord.Colour.green(),description = f'You were banned from {ctx.guild.name} | {str(reason)}.')
            await member.send(embed = embed)
            await member.ban(reason = reason)
            cursor.close() 
            db.close()

    def cog_unload(self):
        self.mute_loop.cancel()
        
    @commands.command()
    @commands.cooldown(1,30,commands.BucketType.user)
    @commands.has_permissions(kick_members = True)
    async def mute(self,ctx,user : discord.Member = None,time = None,*,reason = 'Not Specified'):
        if user == ctx.author:
            await ctx.send('look at this dood tryna mute himself.')
            return
        hourandminute = {
            "s": "1",
            "hr": "3600",
            "min": "60",
            "h": "3600",
            "m": "60"
        }
        if user == None:
            embeddd = discord.Embed(colour= discord.Colour.red())
            embeddd.add_field(name = "Missing User",value = "Specify the user pal.",inline= False)
            embeddd.add_field(name = "Command Example",value = "`peg mute 4289358298 10hr idk cuh`",inline= False)
            await ctx.send(embed = embeddd,delete_after=5)
            return

        if time == None:
            embeddd = discord.Embed(colour= discord.Colour.red())
            embeddd.add_field(name = "Missing Duration",value = "Specify the duration pal.",inline= False)
            embeddd.add_field(name = "Command Example",value = "`peg mute 4289358298 10hr idk cuh`",inline= False)
            await ctx.send(embed = embeddd,delete_after=5)
            return


        if user.top_role > ctx.author.top_role:
            embeddd = discord.Embed(timestamp = datetime.utcnow(),colour= discord.Colour.red())
            embeddd.add_field(name = "eyo calmdown",value = "The user has a higher role than you.",inline= False)
            await ctx.send(embed = embeddd,delete_after=5)
            return

        role = discord.utils.get(ctx.guild.roles, name="Muted")

        if not role:
            await ctx.send("Hey bro, there is no role called muted in your server. Create one called. `Muted`")
            return
        
        if role in user.roles:
            await ctx.send('Person is already muted.')
            return

        db = mysql.connector.connect(
                host = "us-cdbr-east-02.cleardb.com",
                user = "bc4de25d94d683",
                passwd = "0bf00100",
                database = "heroku_1d7c0ca78dfc2ef"
        )

        cursor = db.cursor()
        guildid = str(ctx.guild.id)
        newtime = 0
        cursor.execute('SELECT userid FROM mutedata WHERE userid = ' + str(user.id) + ' AND guildid = ' + guildid)
        res = cursor.fetchall()
        if (len(res) == 0):
            for i in hourandminute:
                split = time.split(i)
                if split[0] != time:
                    newtime = int(split[0])
                    newtime = newtime * int(hourandminute[i])
        
            try:
                sql = "INSERT INTO logs (userid,reason,guildid,type) VALUES (%s, %s, %s, %s)"
                val = (str(user.id),str(reason),guildid,'Mute')
                cursor.execute(sql,val)
                db.commit()
                sql = "INSERT INTO mutedata (userid,guildid,time,timemuted) VALUES (%s, %s, %s, %s)"
                val = (str(user.id),guildid,str(newtime), str(datetime.now()))
                cursor.execute(sql,val)
                db.commit()
                await user.add_roles(role)
                embed = discord.Embed(color = discord.Colour.green(),description = f'✅ **{user.name}** was muted | {str(reason)}.')
                await ctx.send(embed = embed)
                embed = discord.Embed(color = discord.Colour.green(),description = f'You were muted in {ctx.guild.name} | {str(reason)}.')
                await user.send(embed = embed)
                if newtime < 300:
                    await asyncio.sleep(newtime)
                    db = mysql.connector.connect(
                        host = "us-cdbr-east-02.cleardb.com",
                        user = "bc4de25d94d683",
                        passwd = "0bf00100",
                        database = "heroku_1d7c0ca78dfc2ef"
                    )
                    cursor = db.cursor()
                    await user.remove_roles(role)
                    cursor.execute('DELETE FROM mutedata WHERE userid = ' + str(user.id))
                    db.commit()
                    print(f'{user.name} has been unmuted.')
                    cursor.close()
                    db.close()
            except Exception as e:
                print(f"An error occured {e}")
        else:
            await ctx.send('My database says that the person is already muted.')
        cursor.close()
        db.close()


    @commands.command()
    @commands.has_permissions(kick_members = True)
    @commands.cooldown(1,30,commands.BucketType.user)
    async def unmute(self,ctx,user : discord.Member = None):            
        if user == None:
            embeddd = discord.Embed(colour= discord.Colour.red())
            embeddd.add_field(name = "Missing User",value = "Specify the user pal.",inline= False)
            embeddd.add_field(name = "Command Example",value = "`peg mute 4289358298 10hr idk cuh`",inline= False)
            await ctx.send(embed = embeddd,delete_after=5)
            return

        if user.top_role > ctx.author.top_role:
            embeddd = discord.Embed(timestamp = datetime.utcnow(),colour= discord.Colour.red())
            embeddd.add_field(name = "eyo calmdown",value = "The user has a higher role than you.",inline= False)
            await ctx.send(embed = embeddd,delete_after=5)
            return

        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            await ctx.send("Hey bro, there is no role called muted in your server. Create one called. `Muted`")
            return
        db = mysql.connector.connect(
                host = "us-cdbr-east-02.cleardb.com",
                user = "bc4de25d94d683",
                passwd = "0bf00100",
                database = "heroku_1d7c0ca78dfc2ef"
        )

        cursor = db.cursor()
        cursor.execute('SELECT userid FROM mutedata WHERE userid = ' + str(user.id) + ' AND guildid = ' + str(ctx.guild.id))
        res = cursor.fetchall()
        if len(res) == 0:
            await ctx.send('Person is not muted bro.')
            return
        else:
            cursor.execute('DELETE FROM mutedata WHERE userid = ' + str(user.id) + " AND guildid = " + str(ctx.guild.id))
            db.commit()
            await user.remove_roles(role)
            embed = discord.Embed(color = discord.Colour.green(),description = f'✅ **{user.name}** was unmuted.')
            await ctx.send(embed = embed)
        cursor.close()
        db.close()

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel : discord.TextChannel=None):
        if channel == None:
            channel = ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        if overwrite.send_messages == False:
            await ctx.send('This channel is already locked!')
            return
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f'`{channel.name}` has been locked.')

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel : discord.TextChannel=None):
        if channel == None:
            channel = ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        if overwrite.send_messages == True:
            await ctx.send('This channel is already unlocked!')
            return
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f'`{channel.name}` has been unlocked.')

    @tasks.loop(minutes = 5)
    async def mute_loop(self):
            db = mysql.connector.connect(
                    host = "us-cdbr-east-02.cleardb.com",
                    user = "bc4de25d94d683",
                    passwd = "0bf00100",
                    database = "heroku_1d7c0ca78dfc2ef"
            )

            cursor = db.cursor()
            try:
                cursor.execute("SELECT * FROM mutedata")
                res = cursor.fetchall()
                currentime = datetime.now()

                if len(res) == 0:
                    pass

                for i in res:
                    time = datetime.strptime(i[3],"%Y-%m-%d %H:%M:%S.%f")
                    unmuteTime = time + relativedelta(seconds= i[1])
                    if currentime >= unmuteTime:
                        guild = self.client.get_guild(int(i[2]))
                        if guild != None:
                            member = guild.get_member(int(i[0]))
                            if member != None:
                                role = discord.utils.get(guild.roles,name = 'Muted')
                                if role != None:
                                    await member.remove_roles(role)
                                    cursor.execute("DELETE FROM mutedata WHERE userid = " + str(i[0]) + " AND guildid = " + str(i[2]))
                                    db.commit()
                                    print(f'Unmuted {member.mention} With Loop!')
            except Exception as e: 
                print(f'AN Error Occured in mute loop {e}')
            cursor.close()
            db.close()
    


def setup(client):
    client.add_cog(HighRank(client))
