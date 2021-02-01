import discord.ext
from discord.ext import commands,tasks
from discord.ext.commands import Cog

class helpcommand(Cog):
    def __init__(self,client):
        self.client = client
        self.client.remove_command('help')
        
    @Cog.listener()
    async def on_ready(self):
        print("Help cog is ready")
    
    @commands.group()
    async def help(self,ctx):
        if ctx.invoked_subcommand is None:
            em = discord.Embed(title = 'InsideIt Commands Help',color = ctx.author.color)
            em.add_field(name=  "❓ Info",value="`?help info`")
            em.add_field(name = "⚡ HighRank",value = '`?help highrank`')
            em.add_field(name = "😏 Miscellaneous",value = '`?help misc`')
            em.add_field(name = "😂 Memes",value = '`?help meme`')
            em.add_field(name = "📷 Image",value = '`?help img`')
            em.add_field(name = '🐶 Animals',value = '`?help animals`')
            em.add_field(name = '⚙ Configurations',value = '`?config`')
            em.add_field(name = '🥺 Support Me!',value = '[Invite Link](https://discord.com/api/oauth2/authorize?client_id=795963203804200980&permissions=2147483639&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fl&scope=bot) • [Support Server](https://discord.gg/ZNG247NBVp)',inline= False)
            await ctx.send(embed=em)
    
    @help.command()
    async def highrank(self,ctx):
        try:
            embed = discord.Embed(colour = ctx.author.color)
            await ctx.message.delete()
            embed.add_field(name = '⚡ HighRank Commands.',value = "`?purge (amount): Deletes specific amount of messages.`\n\n`?announce (channelid) (text): Do an announcement in a channel with a stylish embed.`\n\n`?slowmode (seconds): Set the channel's slowmode to the specified number.`\n\n`?warn (userID) (reason): The warn gets noted in their infractions list.`\n\n`?ban (userID) (reason): The ban gets noted in their infractions list.`\n\n`?kick (userId) (reason): The kick gets noted in thier infractions list.`\n\n`?mute (userID) (time) (reason): The mute gets noted in their infractions list.`\n\n`?unmute (user): Unmute a user.`\n\n`?inf (userID): List of infractions from a user.`\n\n`?revoke_inf (infID): Revoke an infraction from a user.`")
            await ctx.send(embed = embed)
        except Exception as e:
            if str(e) == '403 Forbidden (error code: 50013): Missing Permissions':
                await ctx.send("I do not have enough permissions to send the message, something is stopping me! Please give me administrator permissions no i won't harm your server.")
            else:
                await ctx.send(f'An error occured: {e}')

    @help.command()
    async def animals(self,ctx):
        try:
            embed = discord.Embed(colour = ctx.author.color)
            await ctx.message.delete()
            embed.add_field(name = '🐶 Animal Commands.',value = "`?dog`,`?cat`,`?fox`,`?panda`,`?bird`,`?koala`")
            await ctx.send(embed = embed)
        except Exception as e:
            if str(e) == '403 Forbidden (error code: 50013): Missing Permissions':
                await ctx.send("I do not have enough permissions to send the message, something is stopping me! Please give me administrator permissions no i won't harm your server.")
            else:
                await ctx.send(f'An error occured: {e}')

    @help.command()
    async def meme(self,ctx):
        try:
            embed = discord.Embed(colour = ctx.author.color)
            await ctx.message.delete()
            embed.add_field(name = '😂 Meme Commands.',value = "`?meme`,`?dankmeme`,`?chan`,`?AntiJoke`,`?wholesome`,`?surreal`,`?facepalm`,`?danidev`,`?fortnite`,`?discord`")
            await ctx.send(embed = embed)
        except Exception as e:
            if str(e) == '403 Forbidden (error code: 50013): Missing Permissions':
                await ctx.send("I do not have enough permissions to send the message, something is stopping me! Please give me administrator permissions no i won't harm your server.")
            else:
                await ctx.send(f'An error occured: {e}')

    @help.command()
    async def misc(self,ctx):
        try:
            embed = discord.Embed(colour = ctx.author.color)
            await ctx.message.delete()
            embed.add_field(name = '😏 Miscellaneous Commands.',value = "`?rps`,`?rpsLeaderboard`,`?whois`,`?ping`,`?fromBase64`,`?simpmeter`,`?av`,`?8ball`,`?robloxsearch`,`?choose`,`?twitter`")
            await ctx.send(embed = embed)
        except Exception as e:
            if str(e) == '403 Forbidden (error code: 50013): Missing Permissions':
                await ctx.send("I do not have enough permissions to send the message, something is stopping me! Please give me administrator permissions no i won't harm your server.")
            else:
                await ctx.send(f'An error occured: {e}')

    @help.command(aliases =['image'])
    async def img(self,ctx):
        try:
            embed = discord.Embed(colour = ctx.author.color)
            await ctx.message.delete()
            embed.add_field(name = '📷 Image Commands.',value = "`?throw`,`?slap`,`?achievement`,`?youtube`,`?hoomangood`,`?blood`,`?triggered`,`?wasted`")
            await ctx.send(embed = embed)
        except Exception as e:
            if str(e) == '403 Forbidden (error code: 50013): Missing Permissions':
                await ctx.send("I do not have enough permissions to send the message, something is stopping me! Please give me administrator permissions no i won't harm your server.")
            else:
                await ctx.send(f'An error occured: {e}')
    @help.command()
    async def info(self,ctx):
        try:
            embed = discord.Embed(title = "❓ InsideIt's Info",colour = ctx.author.color)
            embed.add_field(name = 'Description',value = 'InsideIt is a multipurpose powerful bot which has **a lot** of commands and also has configurations, more coming soon!**In BETA Mode**')
            embed.add_field(name = 'Version',value = '2.8',inline = False)
            embed.add_field(name = 'Servers',value = len(self.client.guilds))
            embed.add_field(name = 'Creator',value = '`Refined#0001`')
            embed.set_thumbnail(url = self.client.user.avatar_url)
            embed.add_field(name="Invite The Bot", value="[Link](https://discord.com/api/oauth2/authorize?client_id=795963203804200980&permissions=2147483639&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fl&scope=bot)")
            await ctx.send(embed = embed)
        except Exception as e:
            if str(e) == '403 Forbidden (error code: 50013): Missing Permissions':
                await ctx.send("I do not have enough permissions to send the message, something is stopping me! Please give me administrator permissions no i won't harm your server.")
            else:
                await ctx.send(f'An error occured: {e}')


def setup(client):
    client.add_cog(helpcommand(client))