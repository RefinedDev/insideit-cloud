from discord import message
import discord.ext
from discord.ext import commands,tasks
from discord.ext.commands import Cog
from discord.ext.commands.cooldowns import BucketType
import mysql.connector
import asyncio
import random
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from datetime import datetime
from dateutil.relativedelta import relativedelta

cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred, {
'databaseURL': 'https://insideitdatabase-default-rtdb.firebaseio.com/reactionroles'
})

class config(Cog):
    def __init__(self,client):
        self.client = client

    @Cog.listener()
    async def on_ready(self):
        print("Config Cog Is Ready!")

    @Cog.listener()
    async def on_message(self,message):
        if isinstance(message.channel, discord.channel.DMChannel):
            return

        if message.guild.owner == message.author:
            return    

        if 'discord.gg/' in str.lower(message.content):
            try:
                ref = db.reference('/antilink')
                res = ref.get()
                if f'{message.guild.id}' in res:
                    toggle = res[f'{str(message.guild.id)}']['toggle']
                    if str.lower(toggle) == 'off':
                        return
                    discordmsg = res[f'{str(message.guild.id)}']['discordlink']
                    if str.lower(discordmsg) == 'no':
                        return
                    await message.delete()
                else:
                    return
            except Exception as e:
                print(f'An error occured in no link {e}')
            
        if 'https://' in str.lower(message.content) or 'http://' in str.lower(message.content):
            try:
                ref = db.reference('/antilink')
                res = ref.get() 
                if f'{message.guild.id}' in res:
                    toggle = res[f'{str(message.guild.id)}']['toggle']
                    if str.lower(toggle) == 'off':
                        return
                    othermsg = res[f'{str(message.guild.id)}']['otherlink']
                    if str.lower(othermsg) == 'no':
                        return
                    await message.delete()
                else:
                    return
            except Exception as e:
                print(f'An error occured in no link {e}')

    @Cog.listener()
    async def on_member_join(self,member):
        if member.guild.id == 777895986461671424:
            age = datetime.now() - member.created_at
            eage = str(age).split(',')[0]
            realage = str(eage).split('days')[0]
            ref = db.reference('/minage')
            res = ref.get()
            if f'{member.guild.id}' in res:
                toggle = res[str(member.guild.id)]['toggle']
                if toggle == 'ON':
                    dbage = res[str(member.guild.id)]['age']
                    if int(dbage) > int(realage):
                        await member.send(f"You're account age needs to be over {dbage} days before you can join this server.")
                        await member.kick(reason = f'Account age lower than the specified minimum age amount')

    
    @commands.group()
    @commands.has_permissions(administrator = True)
    async def config(self,ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title = '⚙ Configurations.',description = 'Use `peg config [nameofconfig]` to configure.',color = ctx.author.color)
            embed.add_field(name = 'You can configure the following.',value = '`WelcomeMessage: Messages in a specific channel when a member joins.`\n\n`WelcomeRole: New members recieve the specified role.`\n\n`LeaveMessage: Messages in a specific channel when a member leaves.`\n\n`AntiLink: Prevent links.`\n\n`ReactionRoles: You should know what this does.`\n\n`Minage: Set a minimum age limit for your servers, new members under that age will be kicked (usefull to prvent raids.)`\n\n`Levelling: Enable level system with roles as rewards!`')
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
        ref = db.reference('/antilink')

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
                                        res = ref.get()
                                        if f'{ctx.guild.id}' in res:
                                            await ctx.send('AntiLink is already on!')
                                            return
                                        e = {
                                                'toggle': 'ON',
                                                'discordlink': 'YES',
                                                'otherlink': 'YES'
                                            }
                                        ref.child(f'{ctx.guild.id}').set(e)
                                        await ctx.send(f'AntiLink is now on!')
                                        # val = (guildid,'ON','YES','YES')
                                    elif str.lower(idmsg2.content) == 'no':
                                        res = ref.get()
                                        if f'{ctx.guild.id}' in res:
                                            await ctx.send('AntiLink is already on!')
                                            return
                                        e = {
                                                'toggle': 'ON',
                                                'discordlink': 'YES',
                                                'otherlink': 'NO'
                                            }
                                        ref.child(f'{ctx.guild.id}').set(e)
                                        await ctx.send(f'AntiLink is now on!')
                                        #val = (guildid,'ON','YES','NO')
                            elif str.lower(idmsg.content) == 'no':
                                        await ctx.send('Okay, do you want to prevent ANY other links like youtube or google links? Yes/No')
                                        try:
                                            idmsg2 = await self.client.wait_for('message',timeout = 50.0,check = check)
                                        except asyncio.TimeoutError:
                                            await ctx.send("Din't reply in time noob.")
                                            return
                                        else:
                                            if str.lower(idmsg2.content) == 'yes':
                                                res = ref.get()
                                                if f'{ctx.guild.id}' in res:
                                                    await ctx.send('AntiLink is already on!')
                                                    return
                                                e = {
                                                        'toggle': 'ON',
                                                        'discordlink': 'NO',
                                                        'otherlink': 'YES'
                                                    }
                                                ref.child(f'{ctx.guild.id}').set(e)
                                                await ctx.send(f'AntiLink is now on!')
                                            elif str.lower(idmsg2.content) == 'no':
                                                res = ref.get()
                                                if f'{ctx.guild.id}' in res:
                                                    ref.child(f'{ctx.guild.id}').delete()
                                                await ctx.send(f'All options were chosen as no, so im turning AntiLink off.')
            
                    elif str.lower(msg1.content) == 'off':
                        res = ref.get()
                        if f'{ctx.guild.id}' in res:
                            ref.child(f'{ctx.guild.id}').delete()
                            await ctx.send('AntiLink is now off!')
                        else:
                            await ctx.send('AntiLink is already off!')

            elif str.lower(msg.content) == 'edit':
                    res = ref.get()
                    if not f'{ctx.guild.id}' in res:
                        await ctx.send('AntiLink is currently off, turn it on to edit it.')
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
                                    e = {
                                        'toggle': 'ON',
                                        'discordlink': 'YES',
                                        'otherlink': 'YES'
                                        }
                                    ref.child(f'{ctx.guild.id}').set(e)
                                    await ctx.send(f'Succesfully Edited AntiLink!')
                                elif str.lower(idmsg2.content) == 'no':
                                    e = {
                                        'toggle': 'ON',
                                        'discordlink': 'YES',
                                        'otherlink': 'NO'
                                        }
                                    ref.child(f'{ctx.guild.id}').set(e)
                                    await ctx.send(f'Succesfully Edited AntiLink!')
                                else:
                                    await ctx.send('Invalid Choice')
                        elif str.lower(idmsg.content) == 'no':
                                    await ctx.send('Okay, do you want to prevent ANY other links like youtube or google links? Yes/No')
                                    try:
                                        idmsg2 = await self.client.wait_for('message',timeout = 50.0,check = check)
                                    except asyncio.TimeoutError:
                                        await ctx.send("Din't reply in time noob.")
                                        return
                                    else:
                                        if str.lower(idmsg2.content) == 'no':
                                            res = ref.get()
                                            if f'{ctx.guild.id}' in res:
                                                ref.child(f'{ctx.guild.id}').delete()
                                                await ctx.send('Succesfully Edited AntiLink, AntiLink is now off!')
                                            else:
                                                await ctx.send('AntiLink is already off!')
                                        elif str.lower(idmsg2.content) == 'yes':
                                            e = {
                                                'toggle': 'ON',
                                                'discordlink': 'NO',
                                                'otherlink': 'YES'
                                            }
                                            ref.child(f'{ctx.guild.id}').set(e)
                                            await ctx.send(f'Succesfully Edited AntiLink!')
                                        else:
                                            await ctx.send('Invalid Choice')
            else:
                await ctx.send("Invalid Choice")
    
    @config.command()
    @commands.cooldown(1,60,commands.BucketType.guild)
    @commands.has_permissions(administrator= True)
    async def ReactionRoles(self,ctx):
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
                                emoji2 = str(addmsg4.content).encode(encoding = 'utf_7')
                                emoji = emoji2.decode('utf-8')
                                reactionset = {
                                    'roleid': '{}'.format(role.id),
                                    'emoji': '{}'.format(emoji),
                                    'channelid': '{}'.format(channel.id),
                                    'messageid': '{}'.format(msg.id)
                                }
                                ref = db.reference('/reactionroles')
                                res = ref.get()
                                if f'{str(emoji)}{str(ctx.guild.id)}{str(channel.id)}{str(msg.id)}' in res:
                                    await ctx.send(f'There is already a reactionrole which uses the {addmsg4.content} emoji, use **any** other emoji which is not in the reactionrole with messageid: `{msg.id}` and channelid: `{channel.id}`')
                                    return
                                else:
                                    ref.child(f'{str(emoji)}{str(ctx.guild.id)}{str(channel.id)}{str(msg.id)}').set(reactionset)
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
                            ref = db.reference('/reactionroles')
                            e = ref.get()
                            if f'{str(emoji)}{str(ctx.guild.id)}{str(channel.id)}{str(msg.id)}' in e:
                                ref.child(f'{str(emoji)}{str(ctx.guild.id)}{str(channel.id)}{str(msg.id)}').delete()
                                await ctx.send('Reaction role succesfully removed!')
                            else:
                                await ctx.send('Reaction role was not found.')                  
            else:
                await ctx.send('Invalid choice')
    
    @config.command()
    @commands.cooldown(1,60,commands.BucketType.guild)
    @commands.has_permissions(administrator = True)
    async def Minage(self,ctx):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        await ctx.send('What ya want to configure?\n`toggle`\n`edit`')
        try:
            msg = await self.client.wait_for('message',timeout = 50.0,check = check)
        except asyncio.TimeoutError:
            await ctx.send("Din't reply in time noob.")
            return
        else:
            if str.lower(msg.content) == 'toggle':
                await ctx.send('Would you like to turn Minage `On` Or `Off`?')
                try:
                    msg1 = await self.client.wait_for('message',timeout = 50.0,check = check)
                except asyncio.TimeoutError:
                    await ctx.send("Din't reply in time noob.")
                    return
                else:
                    if str.lower(msg1.content) == 'on':
                        ref = db.reference('/minage')
                        res = ref.get()
                        if not f'{str(ctx.guild.id)}' in res:
                            await ctx.send("What minimumage would you like to set for your server?\n**New members under the specified age will be kicked**\nExample: **7** Make sure there is only a number without context.")
                            try:
                                msg2 = await self.client.wait_for('message',timeout = 50.0,check = check)
                            except asyncio.TimeoutError:
                                await ctx.send("Din't reply in time noob.")
                                return
                            else:
                                lol = {
                                    'toggle': '{}'.format('ON'),
                                    'age': '{}'.format(msg2.content)
                                }
                                ref.child(str(ctx.guild.id)).set(lol)
                                await ctx.send(f"Minage is now on! Users who's account age is under {msg2.content} days will be kicked")
                        else:
                            await ctx.send('Minage is already on!')
                    elif str.lower(msg1.content) == 'off':
                        ref = db.reference('/minage')
                        res = ref.get()
                        if not str(ctx.guild.id) in res:
                            await ctx.send('Minage is already off!')
                        else:
                            toggle = res[str(ctx.guild.id)]['toggle']
                            if toggle == 'OFF':
                                await ctx.send('Minage is already off!')
                            else:
                                ref.child(str(ctx.guild.id)).delete()
                                await ctx.send('Minage is now off!')
            elif str.lower(msg.content) == 'edit':
                ref = db.reference('/minage')
                res = ref.get()
                if not f'{str(ctx.guild.id)}' in res:
                    await ctx.send('Minage is currently off, turn it on before you edit it.')
                    return
                await ctx.send("What minimumage would you like to set for your server?\n**New members under the specified age will be kicked**\nExample: **'7'** :Make sure there is only a number without context.")
                try:
                    msg2 = await self.client.wait_for('message',timeout = 50.0,check = check)
                except asyncio.TimeoutError:
                    await ctx.send("Din't reply in time noob.")
                    return
                else:
                    lol = {
                        'toggle': '{}'.format('ON'),
                        'age': '{}'.format(msg2.content)
                    }
                    ref.child(str(ctx.guild.id)).set(lol)
                    await ctx.send(f"Minage is now on! Users who's account age is under {msg2.content} days will be kicked")
            else:
                await ctx.send("Invalid Choice")
    
    @config.command()
    @commands.has_permissions(administrator = True)
    #@commands.cooldown(1,60,commands.BucketType.guild)
    async def Levelling(self,ctx):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        await ctx.send("What ya want to configure?\n`on`\n`off`\n`addrole`: Give a role to users when they reach a specific level.\n`removerole`: Remove a role that users recieve on specific level.\n\nWill this promote spamming?\nNo, the user can only get a few amounts of XP **per minute** spamming won't help in any way.")
        try:
            msg = await self.client.wait_for('message',timeout = 50.0,check = check)
        except asyncio.TimeoutError:
            await ctx.send("Din't reply in time noob.")
            return
        else:
            if str.lower(msg.content) == 'on':
                ref = db.reference('/level')
                res = ref.get()
                if not f'{str(ctx.guild.id)}' in res:
                    lol = {'blah':'12'}
                    ref.child(str(ctx.guild.id)).child('level').set(lol)
                    await ctx.send('Levelling is now on!')
                else:
                    await ctx.send('Levelling is already on!')
                    return
            elif str.lower(msg.content) == 'off':
                ref = db.reference('/level')
                res = ref.get()
                if f'{str(ctx.guild.id)}' in res:
                    await ctx.send('Are you sure? All the levels that the users have will be deleted, and when re-enabled everyone will restart from level 1. Yes/No')
                    try:
                        msg = await self.client.wait_for('message',timeout = 50.0,check = check)
                    except asyncio.TimeoutError:
                        await ctx.send("Din't reply in time noob.")
                        return
                    else:
                        if str.lower(msg.content) == 'yes':
                            ref.child(str(ctx.guild.id)).delete()
                            await ctx.send('Levelling is now off!')
                        else:
                            await ctx.send('Aborted.')
                else:
                    await ctx.send('Levelling is already off!')
                    return
            elif str.lower(msg.content) == 'addrole':
                #ADDROLE
                ref = db.reference('/level')
                res = ref.get()
                if not f'{str(ctx.guild.id)}' in res:
                    await ctx.send('Levelling is currently off, enable it before adding roles.')
                    return
                res = ref.get()[str(ctx.guild.id)]['level']
                await ctx.send("At what level would you like to give the user the role?\nExample: **5**\nOnly number without context.")
                try:
                    msg = await self.client.wait_for('message',timeout = 50.0,check = check)
                except asyncio.TimeoutError:
                    await ctx.send("Din't reply in time noob.")
                    return
                else:
                    e = int(msg.content)
                    await ctx.send(f'Okay, now write the RoleID that users will recieve when they reach the level `{msg.content}`')
                    try:
                        msg2 = await self.client.wait_for('message',timeout = 50.0,check = check)
                    except asyncio.TimeoutError:
                        await ctx.send("Din't reply in time noob.")
                        return
                    else:
                        role = discord.utils.get(ctx.guild.roles,id = int(msg2.content))
                        if role == None:
                            await ctx.send('Role not found!')
                            return
                        else:
                            if f'{msg2.content}' in res:
                                already = res[str(role.id)]
                                await ctx.send(f'The role `{role.name}` is already being granted by another level `{(already)}`, try some other role or remove the level that grants this role.\nLevel: `{(already)}`')
                                return

                            res[msg2.content] = msg.content
                            ref.child(str(ctx.guild.id)).child('level').set(res)
                            await ctx.send(f'Done, users will recieve the `{role.name}` role when they reach level `{msg.content}`')
            elif str.lower(msg.content) == 'removerole':
                ref = db.reference('/level')
                res = ref.get()
                if not f'{str(ctx.guild.id)}' in res:
                    await ctx.send('Levelling is currently off, enable it before adding roles.')
                    return
                res = ref.get()[str(ctx.guild.id)]['level']
                if len(res) == 1:
                    await ctx.send('This guild has no level roles.')
                    return
        
                embed = discord.Embed(title = 'Remove a level role.',description = 'To remove the level role specify the `ID` from the following options.')
                for i in res:
                    if not 'blah' == str(i):
                        role = discord.utils.get(ctx.guild.roles,id = int(i))
                        if role == None:
                            embed.add_field(name = f'ID: `{i}`',value = f'On level `{res[i]}` users recieve the `None` role.',inline = False)
                        else:
                            embed.add_field(name = f'ID: `{i}`',value = f'On level `{res[i]}` users recieve the `{role.name}` role.',inline = False)
                await ctx.send(embed = embed)
                try:
                    msg2 = await self.client.wait_for('message',timeout = 50.0,check = check)
                except asyncio.TimeoutError:
                    await ctx.send("Din't reply in time noob.")
                    return
                else:
                    role = discord.utils.get(ctx.guild.roles,id = int(msg2.content))
                    ref.child(str(ctx.guild.id)).child('level').child(msg2.content).delete()
                    if role == None:
                        await ctx.send(f'The level `{res[msg2.content]}` which gave users the role `None` has been removed.')
                    else:
                        await ctx.send(f'The level `{res[msg2.content]}` which gave users the role `{role.name}` has been removed.')
    @Cog.listener()
    async def on_message(self,message):
        if message.author.bot:
            return

        if isinstance(message.channel, discord.channel.DMChannel):
            return

        ref = db.reference('/level')
        res = ref.get()
        if not f'{message.guild.id}' in res:
            return

        res2 = res[f'{message.guild.id}']
        if not f'{message.author.id}' in res2:
            newxp = random.randint(20,30)     
            lol = {
                'currentxp': '{}'.format(newxp),
                'xprequired': '{}'.format('200'),
                'lastgather': '{}'.format(datetime.now()),
                'currentlevel': '{}'.format('1'),
                }
            ref.child(str(message.guild.id)).child(str(message.author.id)).set(lol)
            return

        lastgather = res2[str(message.author.id)]['lastgather']
        time = datetime.strptime(lastgather,"%Y-%m-%d %H:%M:%S.%f")
        cooldowntime = time + relativedelta(seconds= 60)
        if datetime.now() >= cooldowntime:
            newxp = random.randint(20,50) 
            lol = {
                'currentxp': '{}'.format(int(res2[str(message.author.id)]['currentxp']) + newxp),
                'xprequired': '{}'.format(res2[str(message.author.id)]['xprequired']),
                'lastgather': '{}'.format(datetime.now()),
                'currentlevel': '{}'.format(res2[str(message.author.id)]['currentlevel']),
                }
            ref.child(str(message.guild.id)).child(str(message.author.id)).set(lol)
            res3 = ref.get()[f'{message.guild.id}']
            if int(res3[str(message.author.id)]['currentxp']) > int(res3[str(message.author.id)]['xprequired']):
                lol = {
                    'currentxp': '{}'.format(res3[str(message.author.id)]['currentxp']),
                    'xprequired': '{}'.format(int(res3[str(message.author.id)]['xprequired']) * 1.2),
                    'lastgather': '{}'.format(res3[str(message.author.id)]['lastgather']),
                    'currentlevel': '{}'.format(int(res3[str(message.author.id)]['currentlevel']) + 1),
                }
                member = await message.guild.fetch_member(int(message.author.id))
                await message.channel.send(f"**{message.author.display_name}#{message.author.discriminator}** Ay, congrats you're now level `{int(res3[str(message.author.id)]['currentlevel']) + 1}`")
                ref.child(str(message.guild.id)).child(str(message.author.id)).set(lol)
                ref3 = res3['level']
                for i in ref3:
                    if not 'blah' == str(i): 
                        if int(ref3[i]) <= (int(res3[str(message.author.id)]['currentlevel']) + 1):
                            role = discord.utils.get(message.guild.roles, id = int(i))
                            if role == None:
                                return
                            await member.add_roles(role)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def rank(self,ctx,member : discord.Member = None):
        if member == None:
            member = ctx.author
        ref = db.reference('/level')
        res = ref.get()
        if not f'{str(ctx.guild.id)}' in res:
            await ctx.send('Levelling is currently off, enable it to use this command.')
            return
        memberlevel = res[str(ctx.guild.id)][str(member.id)]['currentlevel']
        memberxp = res[str(ctx.guild.id)][str(member.id)]['currentxp']
        memberxpreq = res[str(ctx.guild.id)][str(member.id)]['xprequired']
        embed = discord.Embed(title = f"{member.name}'s rank",color = ctx.author.color)
        embed.set_thumbnail(url = member.avatar_url)
        embed.add_field(name = 'Level:',value = f'`{memberlevel}`',inline = False)
        embed.add_field(name = 'XP:',value = f'`{memberxp}`',inline = False)
        percentage = int(memberxp) / int(memberxpreq) * 100
        if round(percentage) >= 10 and round(percentage) < 20:
            embed.add_field(name = 'XP required to rank up:',value = f'`{int(memberxpreq) - int(memberxp)}`\n\n🌕 🌑 🌑 🌑 🌑 🌑 🌑 🌑 🌑 🌑',inline = False)
        elif round(percentage) >= 20 and round(percentage) < 30:
            embed.add_field(name = 'XP required to rank up:',value = f'`{int(memberxpreq) - int(memberxp)}`\n\n🌕 🌕 🌑 🌑 🌑 🌑 🌑 🌑 🌑 🌑',inline = False)
        elif round(percentage) >= 30 and round(percentage) < 40:
            embed.add_field(name = 'XP required to rank up:',value = f'`{int(memberxpreq) - int(memberxp)}`\n\n🌕 🌕 🌕 🌑 🌑 🌑 🌑 🌑 🌑 🌑',inline = False)
        elif round(percentage) >= 40 and round(percentage) < 50:
            embed.add_field(name = 'XP required to rank up:',value = f'`{int(memberxpreq) - int(memberxp)}`\n\n🌕 🌕 🌕 🌕 🌑 🌑 🌑 🌑 🌑 🌑',inline = False)
        elif round(percentage) >= 50 and round(percentage) < 60:
            embed.add_field(name = 'XP required to rank up:',value = f'`{int(memberxpreq) - int(memberxp)}`\n\n🌕 🌕 🌕 🌕 🌕 🌑 🌑 🌑 🌑 🌑',inline = False)
        elif round(percentage) >= 60 and round(percentage) < 70:
            embed.add_field(name = 'XP required to rank up:',value = f'`{int(memberxpreq) - int(memberxp)}`\n\n🌕 🌕 🌕 🌕 🌕 🌕 🌑 🌑 🌑 🌑',inline = False)
        elif round(percentage) >= 70 and round(percentage) < 80:
            embed.add_field(name = 'XP required to rank up:',value = f'`{int(memberxpreq) - int(memberxp)}`\n\n🌕 🌕 🌕 🌕 🌕 🌕 🌕 🌑 🌑 🌑',inline = False)
        elif round(percentage) >= 80 and round(percentage) < 90:
            embed.add_field(name = 'XP required to rank up:',value = f'`{int(memberxpreq) - int(memberxp)}`\n\n🌕 🌕 🌕 🌕 🌕 🌕 🌕 🌕 🌑 🌑',inline = False)
        elif round(percentage) >= 90 and round(percentage) < 100:
            embed.add_field(name = 'XP required to rank up:',value = f'`{int(memberxpreq) - int(memberxp)}`\n\n🌕 🌕 🌕 🌕 🌕 🌕 🌕 🌕 🌕 🌑',inline = False)
        elif round(percentage) >= 100:
            embed.add_field(name = 'XP required to rank up:',value = f'`{int(memberxpreq) - int(memberxp)}`\n\n🌕 🌕 🌕 🌕 🌕 🌕 🌕 🌕 🌕 🌕',inline = False)
        await ctx.send(embed = embed)


    # @commands.command()
    # @commands.cooldown(1,60,commands.BucketType.guild)
    # @commands.has_permissions(administrator = True)
    # async def showconfigs(self,ctx):
    #     try:
    #         dbs = mysql.connector.connect(
    #             host = "us-cdbr-east-02.cleardb.com",
    #             user = "bc4de25d94d683",
    #             passwd = "0bf00100",
    #             database = "heroku_1d7c0ca78dfc2ef"
    #         )

    #         cursor = dbs.cursor()
    #         guildid = str(ctx.guild.id)
    #         cursor.execute("SELECT toggle from welcomeroles WHERE guildid = " + guildid)
    #         res1 = cursor.fetchall()
    #         cursor.execute("SELECT toggle from welcomemsg WHERE guildid = " + guildid)
    #         res2= cursor.fetchall()
    #         cursor.execute("SELECT toggle from leavemsg WHERE guildid = " + guildid)  
    #         res3 = cursor.fetchall()
 
    #         embed = discord.Embed()
    #         if (len(res2) == 0):
    #             embed.add_field(name = 'WelcomeMessage',value = '`OFF`')
    #         else:
    #             embed.add_field(name = 'WelcomeMessage',value = f'`{res2[0][0]}`')

    #         if (len(res1) == 0):
    #             embed.add_field(name = 'WelcomeRole',value = f'`OFF`',inline= False)
    #         else:
    #             embed.add_field(name = 'WelcomeRole',value = f'`{res1[0][0]}`',inline= False)

    #         if (len(res3) == 0):
    #             embed.add_field(name = 'LeaveMessage',value = f'`OFF`',inline= False)
    #         else:
    #             embed.add_field(name = 'LeaveMessage',value = f'`{res3[0][0]}`',inline= False)
    #         ref = db.reference('/antilink')
    #         res = ref.get()

    #         if f'{ctx.guild.id}' in res:
    #             embed.add_field(name = 'AntiLink',value = f'`ON`',inline= False)
    #         else:
    #             embed.add_field(name = 'AntiLink',value = f'`OFF`',inline= False)
    #         await ctx.send(embed = embed)
            
    #         dbs.close()
    #         cursor.close()
    #     except Exception as e:
    #         print(f"An Error Occured In showconfigs {e}")

    @Cog.listener()
    async def on_raw_reaction_add(self,payload):
        try:
            ref = db.reference('/reactionroles')
            staticemoji = str(payload.emoji)
            emoji2 = staticemoji.encode(encoding = 'utf_7')
            emoji = emoji2.decode('utf-8')
            channelid = payload.channel_id
            msgid = payload.message_id
            guildid = payload.guild_id
            member = payload.member
            e = ref.get()
            if f'{str(emoji)}{str(guildid)}{str(channelid)}{str(msgid)}' in e:
                roleid = e[f'{str(emoji)}{str(guildid)}{str(channelid)}{str(msgid)}']['roleid']
                guild = self.client.get_guild(int(guildid))
                if guild != None:
                    role = discord.utils.get(guild.roles, id =  int(roleid))
                    if role != None:
                        if role in member.roles:
                            return

                        await member.add_roles(role)
                        await member.send(f'You have been given the `{role.name}` role!')
                    else:
                        return
                else:
                    return
        except Exception as e:
            print(f'An error occured in reactionrolesadd: {e}')

    @Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        try:
            ref = db.reference('/reactionroles')
            staticemoji = str(payload.emoji)
            emoji2 = staticemoji.encode(encoding = 'utf_7')
            emoji = emoji2.decode('utf-8')
            channelid = payload.channel_id
            msgid = payload.message_id
            guildid = payload.guild_id
            e = ref.get()
            if f'{str(emoji)}{str(guildid)}{str(channelid)}{str(msgid)}' in e:
                roleid = e[f'{str(emoji)}{str(guildid)}{str(channelid)}{str(msgid)}']['roleid']
                guild = self.client.get_guild(int(guildid))
                if guild != None:
                    member = await guild.fetch_member(payload.user_id)
                    role = discord.utils.get(guild.roles, id =  int(roleid))
                    if role and member != None:
                        if not role in member.roles:
                            return

                        await member.remove_roles(role)
                        await member.send(f"You're `{role.name}` role has been removed!")
                    else:
                        return
                else:
                    return
        except Exception as e:
            print(f'An error occured in reactionrolesremove: {e}')


def setup(client):
    client.add_cog(config(client))