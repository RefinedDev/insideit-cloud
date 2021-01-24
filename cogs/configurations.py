import discord.ext
from discord.ext import commands,tasks
from discord.ext.commands import Cog
import random
import mysql.connector
import asyncio
import random

class config(Cog):
    def __init__(self,client):
        self.client = client

    @Cog.listener()
    async def on_ready(self):
        print("Config Cog Is Ready!")
    
    async def cog_command_error(self,ctx,exc):
        if isinstance(exc,commands.CommandOnCooldown):
            embeddd = discord.Embed(colour= discord.Colour.red())
            embeddd.add_field(name = "eyo calmdown",value = f'This command is on cooldown, try again later after {exc.retry_after:,.2f} seconds.')
            await ctx.send(embed = embeddd,delete_after=5)  
        else:
            print(exc)

    @commands.group()
    @commands.has_permissions(administrator = True)
    async def config(self,ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title = '⚙ Configurations.',description = 'Use `?config [nameofconfig]` to configure, you can also use `?showconfigs` to see what configurations are on or off.',color = ctx.author.color)
            embed.add_field(name = 'You can configure the following.',value = '`WelcomeMessage`\n`WelcomeRole`\n`LeaveMessage`\n`ReactionRoles`')
            await ctx.send(embed = embed)


    @config.command()
    @commands.cooldown(1,150,commands.BucketType.guild)
    @commands.has_permissions(administrator= True)
    async def WelcomeMessage(self,ctx):
        db = mysql.connector.connect(
            host = "us-cdbr-east-02.cleardb.com",
            user = "bc4de25d94d683",
            passwd = "0bf00100",
            database = "heroku_1d7c0ca78dfc2ef"
        )

        cursor = db.cursor()
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        await ctx.send('What ya want to configure?\n`toggle`')
        try:
            msg = await self.client.wait_for('message',timeout = 50.0,check = check)
        except asyncio.TimeoutError:
            await ctx.send("Din't reply in time noob.")
            return
        else:
            if msg.content == 'toggle':
                await ctx.send('Would you like to turn Welcome Message `On` Or `Off`?')
                try:
                    msg1 = await self.client.wait_for('message',timeout = 50.0,check = check)
                except asyncio.TimeoutError:
                    await ctx.send("Din't reply in time noob.")
                    return
                else:
                    if str.lower(msg1.content) == 'on':
                        await ctx.send('Write the channel id where welcome msgs should be sent!')
                        try:
                            idmsg = await self.client.wait_for('message',timeout = 50.0,check = check)
                        except asyncio.TimeoutError:
                            await ctx.send("Din't reply in time noob.")
                            return
                        else:
                            guildid = str(ctx.guild.id)
                            channelid = idmsg.content
                            channel = self.client.get_channel(int(channelid))
                            if channel != None:
                                cursor.execute("SELECT toggle,channelid from welcomemsg WHERE guildid = " + guildid)
                                res = cursor.fetchall()
                                if (len(res) == 0):
                                    sql = "INSERT INTO welcomemsg (guildid,toggle) VALUES (%s, %s)"
                                    val = (guildid,'OFF')
                                    cursor.execute(sql,val)
                                    db.commit()
                                    cursor.execute("UPDATE welcomemsg SET toggle = 'ON', channelid = " + channelid + " WHERE guildid = " + guildid)   
                                    db.commit()
                                    await ctx.send(f'Welcome Messages is ON now and will be sent to the `{channel.name}` channel!')
                                elif res[0][0] != 'ON':
                                    cursor.execute("UPDATE welcomemsg SET toggle = 'ON', channelid = " + channelid + " WHERE guildid = " + guildid)  
                                    db.commit()
                                    await ctx.send(f'Welcome Messages is ON now and will be sent to the `{channel.name}` channel!')
                                else:
                                    await ctx.send('This configuration is already turned on!')
                            else:
                                await ctx.send("Channel not found! >:C")
                    elif str.lower(msg1.content) == 'off':
                            guildid = str(ctx.guild.id)
                            channelid = '0'
                            cursor.execute("SELECT toggle from welcomemsg WHERE guildid = " + guildid)
                            res = cursor.fetchall()
                            if (len(res) == 0):
                                sql = "INSERT INTO welcomemsg (guildid,toggle) VALUES (%s, %s)"
                                val = (guildid,'OFF')
                                cursor.execute(sql,val)
                                db.commit()
                                await ctx.send(f'Your server was not in my database and now is created! WelcomeMessages are Off!')
                            elif res[0][0] != 'OFF':
                                cursor.execute("UPDATE welcomemsg SET toggle = 'OFF', channelid = " + channelid + " WHERE guildid = " + guildid)  
                                db.commit()
                                await ctx.send(f'Welcome Messages are now off!')
                            else:
                                await ctx.send('This configuration is already turned off!')
            else:
                await ctx.send("Invalid Choice")
        db.close()
        cursor.close()


    @config.command()
    @commands.cooldown(1,150,commands.BucketType.guild)
    @commands.has_permissions(administrator= True)
    async def LeaveMessage(self,ctx):
        db = mysql.connector.connect(
            host = "us-cdbr-east-02.cleardb.com",
            user = "bc4de25d94d683",
            passwd = "0bf00100",
            database = "heroku_1d7c0ca78dfc2ef"
        )

        cursor = db.cursor()
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        await ctx.send('What ya want to configure?\n`toggle`')
        try:
            msg = await self.client.wait_for('message',timeout = 50.0,check = check)
        except asyncio.TimeoutError:
            await ctx.send("Din't reply in time noob.")
            return
        else:
            if msg.content == 'toggle':
                await ctx.send('Would you like to turn Leave Message `On` Or `Off`?')
                try:
                    msg1 = await self.client.wait_for('message',timeout = 50.0,check = check)
                except asyncio.TimeoutError:
                    await ctx.send("Din't reply in time noob.")
                    return
                else:
                    if str.lower(msg1.content) == 'on':
                        await ctx.send('Write the channel id where Leave msgs should be sent!')
                        try:
                            idmsg = await self.client.wait_for('message',timeout = 50.0,check = check)
                        except asyncio.TimeoutError:
                            await ctx.send("Din't reply in time noob.")
                            return
                        else:
                            guildid = str(ctx.guild.id)
                            channelid = idmsg.content
                            channel = self.client.get_channel(int(channelid))
                            if channel != None:
                                cursor.execute("SELECT toggle,channelid from leavemsg WHERE guildid = " + guildid)
                                res = cursor.fetchall()
                                if (len(res) == 0):
                                    sql = "INSERT INTO leavemsg (guildid,toggle) VALUES (%s, %s)"
                                    val = (guildid,'OFF')
                                    cursor.execute(sql,val)
                                    db.commit()
                                    cursor.execute("UPDATE leavemsg SET toggle = 'ON', channelid = " + channelid + " WHERE guildid = " + guildid)   
                                    db.commit()
                                    await ctx.send(f'Leave Messages is ON now and will be sent to the `{channel.name}` channel!')
                                elif res[0][0] != 'ON':
                                    cursor.execute("UPDATE leavemsg SET toggle = 'ON', channelid = " + channelid + " WHERE guildid = " + guildid)  
                                    db.commit()
                                    await ctx.send(f'Leave Messages is ON now and will be sent to the `{channel.name}` channel!')
                                else:
                                    await ctx.send('This configuration is already turned on!')
                            else:
                                await ctx.send("Channel not found! >:C")
                    elif str.lower(msg1.content) == 'off':
                            guildid = str(ctx.guild.id)
                            channelid = '0'
                            cursor.execute("SELECT toggle from leavemsg WHERE guildid = " + guildid)
                            res = cursor.fetchall()
                            if (len(res) == 0):
                                sql = "INSERT INTO leavemsg (guildid,toggle) VALUES (%s, %s)"
                                val = (guildid,'OFF')
                                cursor.execute(sql,val)
                                db.commit()
                                await ctx.send(f'Your server was not in my database and now is created! LeaveMessages are Off!')
                            elif res[0][0] != 'OFF':
                                cursor.execute("UPDATE leavemsg SET toggle = 'OFF', channelid = " + channelid + " WHERE guildid = " + guildid)  
                                db.commit()
                                await ctx.send(f'Leave Messages are now off!')
                            else:
                                await ctx.send('This configuration is already turned off!')
            else:
                await ctx.send("Invalid Choice")
        db.close()
        cursor.close()

    @config.command()
    @commands.cooldown(1,150,commands.BucketType.guild)
    @commands.has_permissions(administrator= True)
    async def WelcomeRole(self,ctx):
        db = mysql.connector.connect(
            host = "us-cdbr-east-02.cleardb.com",
            user = "bc4de25d94d683",
            passwd = "0bf00100",
            database = "heroku_1d7c0ca78dfc2ef"
        )

        cursor = db.cursor()
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        await ctx.send('What ya want to configure?\n`toggle`')
        try:
            msg = await self.client.wait_for('message',timeout = 50.0,check = check)
        except asyncio.TimeoutError:
            await ctx.send("Din't reply in time noob.")
            return
        else:
            if msg.content == 'toggle':
                await ctx.send('Would you like to turn Welcome Role `On` Or `Off`?')
                try:
                    msg1 = await self.client.wait_for('message',timeout = 50.0,check = check)
                except asyncio.TimeoutError:
                    await ctx.send("Din't reply in time noob.")
                    return
                else:
                    if str.lower(msg1.content) == 'on':
                        await ctx.send('Write the roleID of the role that the new members will recieve when they join!')
                        try:
                            idmsg = await self.client.wait_for('message',timeout = 50.0,check = check)
                        except asyncio.TimeoutError:
                            await ctx.send("Din't reply in time noob.")
                            return
                        else:
                            guildid = str(ctx.guild.id)
                            roleid = idmsg.content
                            role = discord.utils.get(ctx.guild.roles, id=int(roleid))
                            if role != None:
                                cursor.execute("SELECT toggle,roleid from welcomeroles WHERE guildid = " + guildid)
                                res = cursor.fetchall()
                                if (len(res) == 0):
                                    sql = "INSERT INTO welcomeroles (guildid,toggle) VALUES (%s, %s)"
                                    val = (guildid,'OFF')
                                    cursor.execute(sql,val)
                                    db.commit()
                                    cursor.execute("UPDATE welcomeroles SET toggle = 'ON', roleid = " + roleid + " WHERE guildid = " + guildid)   
                                    db.commit()
                                    await ctx.send(f'WelcomeRoles are now on and new members will recieve the `{role.name}` Role!')
                                elif res[0][0] != 'ON':
                                    cursor.execute("UPDATE welcomeroles SET toggle = 'ON', roleid = " + roleid + " WHERE guildid = " + guildid)  
                                    db.commit()
                                    await ctx.send(f'WelcomeRoles are now on and new members will recieve the `{role.name}` Role!')
                                else:
                                    await ctx.send('This configuration is already turned on!')
                            else:
                                await ctx.send("Role not found!")
                    elif str.lower(msg1.content) == 'off':
                            guildid = str(ctx.guild.id)
                            roleid = '0'
                            cursor.execute("SELECT toggle from welcomeroles WHERE guildid = " + guildid)
                            res = cursor.fetchall()
                            if (len(res) == 0):
                                sql = "INSERT INTO welcomeroles (guildid,toggle) VALUES (%s, %s)"
                                val = (guildid,'OFF')
                                cursor.execute(sql,val)
                                db.commit()
                                await ctx.send(f'Your server was not in my database and now is created! WelcomeRole is Off!')
                            elif res[0][0] != 'OFF':
                                cursor.execute("UPDATE welcomeroles SET toggle = 'OFF', roleid = " + roleid + " WHERE guildid = " + guildid)  
                                db.commit()
                                await ctx.send(f'WelcomeRole is now off!')
                            else:
                                await ctx.send('This configuration is already turned off!')
            else:
                await ctx.send("Invalid Choice")
        db.close()
        cursor.close()
    
    @config.command()
    @commands.cooldown(1,150,commands.BucketType.guild)
    @commands.has_permissions(administrator = True)
    async def ReactionRoles(self,ctx):
        messageid = None
        roleid = None
        reaction = None
        db = mysql.connector.connect(
            host = "us-cdbr-east-02.cleardb.com",
            user = "bc4de25d94d683",
            passwd = "0bf00100",
            database = "heroku_1d7c0ca78dfc2ef"
        )

        cursor = db.cursor()
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
                
        await ctx.send('What would ya like to configure?\n`addreaction`\n`deletereaction`')
        try:
            msg = await self.client.wait_for('message',timeout = 50.0,check = check)
        except asyncio.TimeoutError:
            await ctx.send("Din't reply in time noob.")
            return
        else:
            if str.lower(msg.content) == 'addreaction':
                await ctx.send("Write the message's id where you want the reaction role to be done.")
                try:
                    msg2 = await self.client.wait_for('message',timeout = 50.0,check = check)
                except asyncio.TimeoutError:
                    await ctx.send("Din't reply in time noob.")
                    return
                else:
                    messageid = msg2.content
                    channel = await self.client.fetch_message(int(messageid))
                    if channel != None:
                        await ctx.send("Now write the role's id which members will recieve when reacted.")
                        try:
                            msg3 = await self.client.wait_for('message',timeout = 50.0,check = check)
                        except asyncio.TimeoutError:
                            await ctx.send("Din't reply in time noob.")
                            return
                        else:
                            roleid = msg3.content
                            role = discord.utils.get(ctx.guild.roles, id=int(roleid))
                            if role != None:
                                await ctx.send('Now last but not least, write the Reaction Emoji that members will have to react to recieve the role!')
                                try:
                                    msg4 = await self.client.wait_for('message',timeout = 50.0,check = check)
                                except asyncio.TimeoutError:
                                    await ctx.send("Din't reply in time noob.")
                                    return
                                else:
                                    reaction = msg4.content
                                    sql = "INSERT INTO reactionroles (guildid,messageid,roleid,reaction) VALUES (%s, %s, %s, %s)"
                                    val = (str(ctx.guild.id), str(messageid), str(roleid), str(reaction))
                                    cursor.execute(sql,val)
                                    db.commit()
                                    await ctx.send(f'Reaction role added, members will recieve the {role.name} role when reacted to {reaction}!\n**PS: Reaction Roles Are Currently In Maintenance And Will NOT WORK Sorry For The Inconvinience**')
                            else:
                                await ctx.send('Invalid RoleId returning..')
                                return
                    else:
                        await ctx.send('Invalid ChannelId returning..')
                        return
            elif str.lower(msg.content) == 'deletereaction':
                await ctx.send('Hey bro this option is in maintenance check back later!')
                return
        cursor.close()
        db.close()

    @commands.command()
    @commands.cooldown(1,150,commands.BucketType.guild)
    @commands.has_permissions(administrator = True)
    async def showconfigs(self,ctx):
        try:
            db = mysql.connector.connect(
                host = "us-cdbr-east-02.cleardb.com",
                user = "bc4de25d94d683",
                passwd = "0bf00100",
                database = "heroku_1d7c0ca78dfc2ef"
            )

            cursor = db.cursor()
            guildid = str(ctx.guild.id)
            cursor.execute("SELECT toggle from welcomeroles WHERE guildid = " + guildid)
            res1 = cursor.fetchall()
            cursor.execute("SELECT toggle from welcomemsg WHERE guildid = " + guildid)
            res2= cursor.fetchall()
            cursor.execute("SELECT toggle from leavemsg WHERE guildid = " + guildid)  
            res3 = cursor.fetchall()

            embed = discord.Embed()
            if (len(res2) == 0):
                embed.add_field(name = 'WelcomeMessage',value = '`OFF`')
            else:
                embed.add_field(name = 'WelcomeMessage',value = f'`{res2[0][0]}`')

            if (len(res1) == 0):
                embed.add_field(name = 'WelcomeRole',value = f'`OFF`',inline= False)
            else:
                embed.add_field(name = 'WelcomeRole',value = f'`{res1[0][0]}`',inline= False)

            if (len(res3) == 0):
                embed.add_field(name = 'LeaveMessage',value = f'`OFF`',inline= False)
            else:
                embed.add_field(name = 'LeaveMessage',value = f'`{res3[0][0]}`',inline= False)
            await ctx.send(embed = embed)
            db.close()
            cursor.close()
        except Exception as e:
            print(f"An Error Occured In showconfigs {e}")


def setup(client):
    client.add_cog(config(client))