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
            embed = discord.Embed(title = '⚙ Configurations.',description = 'Use `peg config [nameofconfig]` to configure, you can also use `peg showconfigs` to see what configurations are on or off.',color = ctx.author.color)
            embed.add_field(name = 'You can configure the following.',value = '`WelcomeMessage`\n`WelcomeRole`\n`LeaveMessage`\n`AntiLink`')
            await ctx.send(embed = embed)


    @config.command()
    @commands.cooldown(1,60,commands.BucketType.guild)
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
                                    sql = "INSERT INTO welcomemsg (guildid,toggle,channelid) VALUES (%s, %s, %s)"
                                    val = (guildid,'ON',channelid)
                                    cursor.execute(sql,val)
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
    @commands.cooldown(1,60,commands.BucketType.guild)
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
                                    sql = "INSERT INTO leavemsg (guildid,toggle,channelid) VALUES (%s, %s, %s)"
                                    val = (guildid,'ON',channelid)
                                    cursor.execute(sql,val)
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
    @commands.cooldown(1,60,commands.BucketType.guild)
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
                                    sql = "INSERT INTO welcomeroles (guildid,toggle,roleid) VALUES (%s, %s, %s)"
                                    val = (guildid,'ON',roleid)
                                    cursor.execute(sql,val)
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
    @commands.cooldown(1,60,commands.BucketType.guild)
    @commands.has_permissions(administrator= True)
    async def AntiLink(self,ctx):
        db = mysql.connector.connect(
            host = "us-cdbr-east-02.cleardb.com",
            user = "bc4de25d94d683",
            passwd = "0bf00100",
            database = "heroku_1d7c0ca78dfc2ef"
        )

        cursor = db.cursor()
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        await ctx.send('What ya want to configure?\n`toggle`\n`edit`')
        try:
            msg = await self.client.wait_for('message',timeout = 50.0,check = check)
        except asyncio.TimeoutError:
            await ctx.send("Din't reply in time noob.")
            return
        else:
            if msg.content == 'toggle':
                await ctx.send('Would you like to turn AntiLink `On` Or `Off`?')
                try:
                    msg1 = await self.client.wait_for('message',timeout = 50.0,check = check)
                except asyncio.TimeoutError:
                    await ctx.send("Din't reply in time noob.")
                    return
                else:
                    if str.lower(msg1.content) == 'on':
                        await ctx.send('Do you want to prevent discord invite links? Yes/No')
                        try:
                            idmsg = await self.client.wait_for('message',timeout = 50.0,check = check)
                        except asyncio.TimeoutError:
                            await ctx.send("Din't reply in time noob.")
                            return
                        else:
                            if str.lower(idmsg.content) == 'yes':
                                await ctx.send('Okay, do you want to prevent ANY other links like youtube or google links? Yes/No')
                                try:
                                    idmsg2 = await self.client.wait_for('message',timeout = 50.0,check = check)
                                except asyncio.TimeoutError:
                                    await ctx.send("Din't reply in time noob.")
                                    return
                                else:
                                    if str.lower(idmsg2.content) == 'yes':
                                        guildid = str(ctx.guild.id)
                                        cursor.execute("SELECT toggle from antilink WHERE guildid = " + guildid)
                                        res = cursor.fetchall()
                                        if (len(res) == 0):
                                            sql = "INSERT INTO antilink (guildid,toggle,discordlink,otherlink) VALUES (%s, %s, %s, %s)"
                                            val = (guildid,'ON','YES','YES')
                                            cursor.execute(sql,val)
                                            db.commit()
                                            await ctx.send(f'AntiLink is now on!')
                                        elif res[0][0] != 'ON':
                                            cursor.execute("UPDATE antilink SET toggle = 'ON', discordlink = 'YES', otherlink = 'YES' WHERE guildid = " + guildid)  
                                            db.commit()
                                            await ctx.send(f'AntiLink is now on!')
                                        else:
                                            await ctx.send('This configuration is already turned on!')
                                    elif str.lower(idmsg2.content) == 'no':
                                        guildid = str(ctx.guild.id)
                                        cursor.execute("SELECT toggle from antilink WHERE guildid = " + guildid)
                                        res = cursor.fetchall()
                                        if (len(res) == 0):
                                            sql = "INSERT INTO antilink (guildid,toggle,discordlink,otherlink) VALUES (%s, %s, %s, %s)"
                                            val = (guildid,'ON','YES','NO')
                                            cursor.execute(sql,val)
                                            db.commit()
                                            await ctx.send(f'AntiLink is now on!')
                                        elif res[0][0] != 'ON':
                                            cursor.execute("UPDATE antilink SET toggle = 'ON', discordlink = 'YES', otherlink = 'NO' WHERE guildid = " + guildid)  
                                            db.commit()
                                            await ctx.send(f'AntiLink is now on!')
                                        else:
                                            await ctx.send('This configuration is already turned on!')
                            elif str.lower(idmsg.content) == 'no':
                                        await ctx.send('Okay, do you want to prevent ANY other links like youtube or google links? Yes/No')
                                        try:
                                            idmsg2 = await self.client.wait_for('message',timeout = 50.0,check = check)
                                        except asyncio.TimeoutError:
                                            await ctx.send("Din't reply in time noob.")
                                            return
                                        else:
                                            if str.lower(idmsg2.content) == 'yes':
                                                guildid = str(ctx.guild.id)
                                                cursor.execute("SELECT toggle,discordlink,otherlink from antilink WHERE guildid = " + guildid)
                                                res = cursor.fetchall()
                                                if (len(res) == 0):
                                                    sql = "INSERT INTO antilink (guildid,toggle,discordlink,otherlink) VALUES (%s, %s, %s, %s)"
                                                    val = (guildid,'ON','NO','YES')
                                                    cursor.execute(sql,val)
                                                    db.commit()
                                                    await ctx.send(f'AntiLink is now on!')
                                                elif res[0][0] != 'ON':
                                                    cursor.execute("UPDATE antilink SET toggle = 'ON', discordlink = 'NO', otherlink = 'YES' WHERE guildid = " + guildid)  
                                                    db.commit()
                                                    await ctx.send(f'AntiLink is now on!')
                                                else:
                                                    await ctx.send('This configuration is already turned on!')
                                            elif str.lower(idmsg2.content) == 'no':
                                                guildid = str(ctx.guild.id)
                                                cursor.execute("SELECT toggle from antilink WHERE guildid = " + guildid)
                                                res = cursor.fetchall()
                                                if (len(res) == 0):
                                                    sql = "INSERT INTO antilink (guildid,toggle,discordlink,otherlink) VALUES (%s, %s, %s, %s)"
                                                    val = (guildid,'OFF','NO','NO')
                                                    cursor.execute(sql,val)
                                                    db.commit()
                                                    await ctx.send("Both of the options were chosen as No so i'm not turning AntiLink on.")
                                                    return
                                                elif res[0][0] != 'ON':
                                                    await ctx.send("Both of the options were chosen as No so i'm not turning AntiLink on.")
                                                    return
                                                else:
                                                    await ctx.send('This configuration is already turned on!')
            
                    elif str.lower(msg1.content) == 'off':
                            guildid = str(ctx.guild.id)
                            cursor.execute("SELECT toggle from antilink WHERE guildid = " + guildid)
                            res = cursor.fetchall()
                            if (len(res) == 0):
                                sql = "INSERT INTO antilink (guildid,toggle) VALUES (%s, %s)"
                                val = (guildid,'OFF')
                                cursor.execute(sql,val)
                                db.commit()
                                await ctx.send(f'Your server was not in my database and now is created! AntiLink is Off!')
                            elif res[0][0] != 'OFF':
                                cursor.execute("UPDATE antilink SET toggle = 'OFF' WHERE guildid = " + guildid)  
                                db.commit()
                                await ctx.send(f'AntiLink is now off!')
                            else:
                                await ctx.send('This configuration is already turned off!')
                    else:
                        await ctx.send('Invalid Choice.')

            elif str.lower(msg.content) == 'edit':
                        cursor.execute('SELECT toggle FROM antilink WHERE guildid = ' + str(ctx.guild.id))
                        res = cursor.fetchall()

                        if len(res) == 0:
                            await ctx.send('AntiLink is currently off so you cannot edit it!')
                            return
                        
                        if res[0][0] == 'OFF':
                            await ctx.send('AntiLink is currently off so you cannot edit it!')
                            return
                        
                        await ctx.send('Do you want to prevent discord invite links? Yes/No')
                        try:
                            idmsg = await self.client.wait_for('message',timeout = 50.0,check = check)
                        except asyncio.TimeoutError:
                            await ctx.send("Din't reply in time noob.")
                            return
                        else:
                            if str.lower(idmsg.content) == 'yes':
                                await ctx.send('Okay, do you want to prevent ANY other links like youtube or google links? Yes/No')
                                try:
                                    idmsg2 = await self.client.wait_for('message',timeout = 50.0,check = check)
                                except asyncio.TimeoutError:
                                    await ctx.send("Din't reply in time noob.")
                                    return
                                else:
                                    if str.lower(idmsg2.content) == 'yes':
                                        guildid = str(ctx.guild.id)
                                        cursor.execute("UPDATE antilink SET toggle = 'ON', discordlink = 'YES', otherlink = 'YES' WHERE guildid = " + guildid)  
                                        db.commit()
                                        await ctx.send(f'Succesfully Edited AntiLink!')
                                    elif str.lower(idmsg2.content) == 'no':
                                        guildid = str(ctx.guild.id)
                                        cursor.execute("UPDATE antilink SET toggle = 'ON', discordlink = 'YES', otherlink = 'NO' WHERE guildid = " + guildid)  
                                        db.commit()
                                        await ctx.send(f'Succesfully Edited AntiLink!')
                            elif str.lower(idmsg.content) == 'no':
                                        await ctx.send('Okay, do you want to prevent ANY other links like youtube or google links? Yes/No')
                                        try:
                                            idmsg2 = await self.client.wait_for('message',timeout = 50.0,check = check)
                                        except asyncio.TimeoutError:
                                            await ctx.send("Din't reply in time noob.")
                                            return
                                        else:
                                            if str.lower(idmsg2.content) == 'yes':
                                                guildid = str(ctx.guild.id)
                                                cursor.execute("UPDATE antilink SET toggle = 'ON', discordlink = 'NO', otherlink = 'YES' WHERE guildid = " + guildid)  
                                                db.commit()
                                                await ctx.send(f'Succesfully Edited AntiLink!')
                                            elif str.lower(idmsg2.content) == 'no':
                                                guildid = str(ctx.guild.id)
                                                cursor.execute("UPDATE antilink SET toggle = 'OFF', discordlink = 'NO', otherlink = 'NO' WHERE guildid = " + guildid)
                                                db.commit()
                                                await ctx.send('Succesfully Edited AntiLink, AntiLink is now off!')
            else:
                await ctx.send("Invalid Choice")
        db.close()
        cursor.close()
    
    @config.command()
    #@commands.cooldown(1,60,commands.BucketType.guild)
    @commands.has_permissions(administrator= True)
    async def ReactionRoles(self,ctx):
        db = mysql.connector.connect(
            host = "us-cdbr-east-02.cleardb.com",
            user = "bc4de25d94d683",
            passwd = "0bf00100",
            database = "heroku_1d7c0ca78dfc2ef"
        )

        cursor = db.cursor()
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        await ctx.send('What ya want to configure?\n`add`\n`remove`')
        try:
            msg = await self.client.wait_for('message',timeout = 50.0,check = check)
        except asyncio.TimeoutError:
            await ctx.send("Din't reply in time noob.")
            return
        else:
            if str.lower(msg.content) == 'add':
                await ctx.send('Okay, write the channel id where the reaction role will be.')
                try:
                    addmsg = await self.client.wait_for('message',timeout = 50.0,check = check)
                except asyncio.TimeoutError:
                    await ctx.send("Din't reply in time noob.")
                    return
                else:
                    channel = ctx.guild.get_channel(int(addmsg.content))
                    if channel == None:
                        await ctx.send('Channel not found.')
                        return
                    await ctx.send('Okay, now write the message id of the reaction role.')
                    try:
                        addmsg2 = await self.client.wait_for('message',timeout = 50.0,check = check)
                    except asyncio.TimeoutError:
                        await ctx.send("Din't reply in time noob.")
                        return
                    else:
                        msg = await channel.fetch_message(int(addmsg2.content))
                        if msg == None:
                            await ctx.send('Message not found!')
                            return
                        await ctx.send('Okay, now write the roleid that users will recieve when reacted.')
                        try:
                            addmsg3 = await self.client.wait_for('message',timeout = 50.0,check = check)
                        except asyncio.TimeoutError:
                            await ctx.send("Din't reply in time noob.")
                            return
                        else:
                            role = discord.utils.get(ctx.guild.roles,id = int(addmsg3.content))
                            if role == None:
                                await ctx.send('Role not found!')
                                return
                            await ctx.send('Okay, last but not least write the  emoji without any context like\n😀')
                            try:
                                addmsg4 = await self.client.wait_for('message',timeout = 50.0,check = check)
                            except asyncio.TimeoutError:
                                await ctx.send("Din't reply in time noob.")
                                return
                            else: 
                                emoji = str(addmsg4.content).encode(encoding = 'utf_7')
                                sql = "INSERT INTO reactionroles (guildid,channelid,messageid,roleid,emoji) VALUES (%s, %s,%s,%s,%s)"
                                val = (str(ctx.guild.id),channel.id,msg.id,role.id,emoji)
                                cursor.execute(sql,val)
                                db.commit()
                                await ctx.send(f'Reaction role created, users will recieve the `{role.name}` role when reacting to {addmsg4.content}')
            elif str.lower(msg.content) == 'remove':
                await ctx.send('Okay, write the channel id where the reaction role is.')
                try:
                    denymsg = await self.client.wait_for('message',timeout = 50.0,check = check)
                except asyncio.TimeoutError:
                    await ctx.send("Din't reply in time noob.")
                    return
                else:
                    channel = ctx.guild.get_channel(int(denymsg.content))
                    if channel == None:
                        await ctx.send('Channel not found.')
                        return
                    await ctx.send('Okay, now write the message id where the reaction role is.')
                    try:
                        denymsg2 = await self.client.wait_for('message',timeout = 50.0,check = check)
                    except asyncio.TimeoutError:
                        await ctx.send("Din't reply in time noob.")
                        return
                    else:
                        msge = await channel.fetch_message(int(denymsg2.content))
                        if msge == None:
                            await ctx.send('Message not found!')
                            return
                        await ctx.send('Okay, last but not least write the emoji of the reaction role that you want to remove without context.')
                        try:
                            denymsg3 = await self.client.wait_for('message',timeout = 50.0,check = check)
                        except asyncio.TimeoutError:
                            await ctx.send("Din't reply in time noob.")
                            return
                        else:
                            staticemoji = denymsg3.content
                            emoji2 = staticemoji.encode(encoding = 'utf_7')
                            emoji = emoji2.decode('utf-8')
                            cursor.execute(f"SELECT roleid FROM reactionroles WHERE guildid = {str(ctx.guild.id)} AND channelid = {str(channel.id)} AND emoji = '{emoji}' AND messageid = {msge.id}")
                            res = cursor.fetchall()
                            if len(res) == 0:
                                await ctx.send(f'Could not find the reaction role with emoji {staticemoji}')
                            else:
                                print(emoji)
                                role = discord.utils.get(ctx.guild.roles,id = res[0][0])
                                cursor.execute(f"DELETE FROM reactionroles guildid = {str(ctx.guild.id)} AND channelid = {str(channel.id)} AND emoji = '{emoji}' AND messageid = {msge.id}")
                                await ctx.send(f'Reaction role which gave users the {role.name} role has been removed!')
                            
            else:
                await ctx.send('Invalid choice')
        
        db.close()
        cursor.close()

    @commands.command()
    @commands.cooldown(1,60,commands.BucketType.guild)
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
            cursor.execute("SELECT toggle,discordlink,otherlink from antilink WHERE guildid = " + guildid)  
            res4 = cursor.fetchall()

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
            
            if (len(res4) == 0):
                embed.add_field(name = 'AntiLink',value = f'`OFF`',inline= False)
            elif res4[0][0] == 'OFF':
                 embed.add_field(name = 'AntiLink',value = f'`OFF`',inline= False)
            else:
                embed.add_field(name = 'AntiLink',value = f'`{res4[0][0]}`\n`NODiscordLink: {res4[0][1]}`\n`NOOtherLinks: {res4[0][2]}`',inline= False)
            await ctx.send(embed = embed)
            db.close()
            cursor.close()
        except Exception as e:
            print(f"An Error Occured In showconfigs {e}")


def setup(client):
    client.add_cog(config(client))