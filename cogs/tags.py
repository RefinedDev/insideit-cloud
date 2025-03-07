import discord.ext
from discord.ext import commands,tasks
from discord.ext.commands import Cog
from datetime import datetime
import mysql.connector
import asyncio

class Tags(Cog):
    def __init__(self,client):
        self.client = client
  
    @Cog.listener()
    async def on_ready(self):
        print('Tag cog is ready!')

    @commands.group()
    async def tag(self,ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title = 'TAGS',description = 'Shows a content of tag is it exists.',color = ctx.author.color)
            embed.add_field(name = 'Commands',value = "`peg tag create: Create a tag`\n`peg tag remove (tag): Delete a tag`\n`peg tag edit (tag): Edit a tag's content`\n`peg plstag (tag): Reveal a tag's content aka use it.`\n`peg tag show: Show existing tags in the guild.`")
            await ctx.send(embed = embed)

    @tag.command()
    @commands.cooldown(1,60,commands.BucketType.user)
    @commands.has_permissions(kick_members = True)
    async def create(self,ctx):
        db = mysql.connector.connect(
                host = "us-cdbr-east-02.cleardb.com",
                user = "bc4de25d94d683",
                passwd = "0bf00100",
                database = "heroku_1d7c0ca78dfc2ef"
        )

        cursor = db.cursor()
        dm = await ctx.author.create_dm()
        def check(m):
            return m.author == ctx.author and m.channel == dm

        await ctx.send('Check your DMs')
        await dm.send('Enter the name for your tag.')
        try:
            msg = await self.client.wait_for('message',timeout = 50.0,check = check)
        except asyncio.TimeoutError:
            await ctx.send("Din't reply in time noob.")
            return
        else:
            await dm.send('Enter the content of your tag.')
            try:
                msg2 = await self.client.wait_for('message',timeout = 50.0,check = check)
            except asyncio.TimeoutError:
                await ctx.send("Din't reply in time noob.")
                return
            else:
                try:
                    cursor.execute('SELECT name FROM tags WHERE guildid = ' + str(ctx.guild.id))
                    res = cursor.fetchall()
                    if not (any(str(msg.content) in i for i in res)):
                        sql = "INSERT INTO tags (guildid,name,content) VALUES (%s, %s, %s)"
                        val = (str(ctx.guild.id),str(msg.content),str(msg2.content))
                        cursor.execute(sql,val)
                        db.commit()
                        await dm.send('Tag created!')
                    else:
                        await dm.send('Tag already exists!')
                        return
                except Exception as e:
                    await dm.send(f'An error occured: {e}')
        cursor.close()
        db.close()

    @tag.command()
    @commands.cooldown(1,60,commands.BucketType.user)
    @commands.has_permissions(kick_members = True)
    async def remove(self,ctx,name = None):
        if name == None:
            embeddd = discord.Embed(timestamp = datetime.utcnow(),colour= discord.Colour.red())
            embeddd.add_field(name = "Missing Tag Name",value = "Specify the tag name pal.",inline= False)
            embeddd.add_field(name = "Command Example",value = "`peg tag remove joe `",inline= False)
            await ctx.send(embed = embeddd,delete_after=5)
            return
            
        db = mysql.connector.connect(
                host = "us-cdbr-east-02.cleardb.com",
                user = "bc4de25d94d683",
                passwd = "0bf00100",
                database = "heroku_1d7c0ca78dfc2ef"
        )

        cursor = db.cursor()
        sql = f"SELECT name FROM tags WHERE guildid = {str(ctx.guild.id)} AND name = '{str(name)}'"
        cursor.execute(sql)
        res = cursor.fetchall()
        if len(res) == 0:
            await ctx.send('Tag does not exist')
            cursor.close()
            db.close()
            return
        sql = f"DELETE FROM tags WHERE guildid = {str(ctx.guild.id)} AND name = '{str(name)}'"
        cursor.execute(sql)
        db.commit()
        await ctx.send(f'Tag with name `{name}` is removed!')

        cursor.close()
        db.close()
    
    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def plstag(self,ctx,name = None):
        if name == None:
            embeddd = discord.Embed(timestamp = datetime.utcnow(),colour= discord.Colour.red())
            embeddd.add_field(name = "Missing Tag Name",value = "Specify the tag name pal.",inline= False)
            embeddd.add_field(name = "Command Example",value = "`peg plstag joe `",inline= False)
            await ctx.send(embed = embeddd,delete_after=5)
            return

        db = mysql.connector.connect(
                host = "us-cdbr-east-02.cleardb.com",
                user = "bc4de25d94d683",
                passwd = "0bf00100",
                database = "heroku_1d7c0ca78dfc2ef"
        )

        cursor = db.cursor()
        sql = f"SELECT content FROM tags WHERE guildid = {str(ctx.guild.id)} AND name = '{str(name)}'"
        cursor.execute(sql)
        res = cursor.fetchall()
        if len(res) == 0:
            await ctx.send('No results found.')
            return
        
        await ctx.send(str(res[0][0]))
        cursor.close()
        db.close()
    
    @tag.command()
    @commands.cooldown(1,60,commands.BucketType.user)
    @commands.has_permissions(kick_members = True)
    async def edit(self,ctx,name = None):
        if name == None:
            embeddd = discord.Embed(timestamp = datetime.utcnow(),colour= discord.Colour.red())
            embeddd.add_field(name = "Missing Tag Name",value = "Specify the tag name pal.",inline= False)
            embeddd.add_field(name = "Command Example",value = "`peg tag edit joe `",inline= False)
            await ctx.send(embed = embeddd,delete_after=5)
            return

        db = mysql.connector.connect(
                host = "us-cdbr-east-02.cleardb.com",
                user = "bc4de25d94d683",
                passwd = "0bf00100",
                database = "heroku_1d7c0ca78dfc2ef"
        )

        cursor = db.cursor()
        sql = f"SELECT content FROM tags WHERE guildid = {str(ctx.guild.id)} AND name = '{str(name)}'"
        cursor.execute(sql)
        res = cursor.fetchall()

        if len(res) == 0:
            await ctx.send('Tag does not exist!')
            return

        dm = await ctx.author.create_dm()
        def check(m):
            return m.author == ctx.author and m.channel == dm

        await ctx.send('Check your DMs')
        await dm.send(f'Enter the new content for the tag `{name}`\n\nOld Content -: `{res[0][0]}`')
        try:
            msg = await self.client.wait_for('message',timeout = 50.0,check = check)
        except asyncio.TimeoutError:
            await ctx.send("Din't reply in time noob.")
            return
        else:
            sql = f"UPDATE tags SET content = '{str(msg.content)}' WHERE guildid = {str(ctx.guild.id)} AND name = '{str(name)}'"
            cursor.execute(sql)
            db.commit()
            await dm.send(f"Tag `{name}`'s content has been changed to `{str(msg.content)}`")
        
        cursor.close()
        db.close()

    
    @tag.command()
    @commands.cooldown(1,60,commands.BucketType.guild)
    async def show(self,ctx):
        db = mysql.connector.connect(
                host = "us-cdbr-east-02.cleardb.com",
                user = "bc4de25d94d683",
                passwd = "0bf00100",
                database = "heroku_1d7c0ca78dfc2ef"
        )

        cursor = db.cursor()
        cursor.execute('SELECT name FROM tags WHERE guildid = ' + str(ctx.guild.id))
        res = cursor.fetchall()
        embed = discord.Embed(color = ctx.author.color)
        li = [i for sub in res for i in sub]
        if len(li) == 0:
            embed.add_field(name = 'All the tags of the guild', value = 'No tags in this guild')
        else:
            embed.add_field(name = 'All the tags of the guild', value = '\n'.join(li))
        await ctx.send(embed = embed)


    



def setup(client):
    client.add_cog(Tags(client))