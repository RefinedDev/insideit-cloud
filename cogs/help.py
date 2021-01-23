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
            em.add_field(name = '🥺 Support Me!',value = '[Invite Link](https://discord.com/api/oauth2/authorize?client_id=795963203804200980&permissions=8&scope=bot) • [Support Server](https://discord.gg/ZNG247NBVp)',inline= False)
            await ctx.send(embed=em)
    
    @help.command()
    async def highrank(self,ctx):
        embed = discord.Embed(colour = ctx.author.color)
        await ctx.message.delete()
        embed.add_field(name = '⚡ HighRank Commands.',value = "`?purge (amount): Deletes specific amount of messages from a channel where it was called.`\n\n`?announce (channelid) (text): Do an announcement in the channel specified with the channelid and with a stylish embed.`\n\n`?slowmode (seconds): Set the channel's slowmode to the specified number.`\n\n`?warn (userID) (reason): Warn a user. duh`\n\n`?inf (userID): List of infractions from a user.`\n\n`?revoke_inf (infID): Revoke an infraction from a user.`\n\n`?kick (userId) (reason): The kick gets noted in thier infractions.`\n\n?ban (userID) (reason): The ban gets noted in their infractions.")
        await ctx.send(embed = embed)

    @help.command()
    async def animals(self,ctx):
        embed = discord.Embed(colour = ctx.author.color)
        await ctx.message.delete()
        embed.add_field(name = '🐶 Animal Commands.',value = "`?dog`,`?cat`,`?fox`,`?panda`,`?bird`,`?koala`")
        await ctx.send(embed = embed)
    
    @help.command()
    async def meme(self,ctx):
        embed = discord.Embed(colour = ctx.author.color)
        await ctx.message.delete()
        embed.add_field(name = '😂 Meme Commands.',value = "`?meme`,`?dankmeme`,`?chan`,`?AntiJoke`,`?wholesome`,`?surreal`,`?facepalm`,`?danidev`,`?fortnite`,`?discord`")
        await ctx.send(embed = embed)

    @help.command()
    async def misc(self,ctx):
        embed = discord.Embed(colour = ctx.author.color)
        await ctx.message.delete()
        embed.add_field(name = '😏 Miscellaneous Commands.',value = "`?rps`,`?rpsLeaderboard`,`?whois`,`?ping`,`?fromBase64`,`?simpmeter`,`?av`,`?8ball`,`?robloxsearch`,`?choose`")
        await ctx.send(embed = embed)

    @help.command(aliases =['image'])
    async def img(self,ctx):
        embed = discord.Embed(colour = ctx.author.color)
        await ctx.message.delete()
        embed.add_field(name = '📷 Image Commands.',value = "`?throw`,`?slap`,`?achievement`,`?youtube`,`?hoomangood`,`?blood`")
        await ctx.send(embed = embed)

    @help.command()
    async def info(self,ctx):
        embed = discord.Embed(title = "❓ InsideIt's Info",colour = ctx.author.color)
        embed.add_field(name = 'Description',value = 'InsideIt is a multipurpose powerful bot which has **a lot** of commands and also has configurations, more coming soon!**In BETA Mode**')
        embed.add_field(name = 'Version',value = '2.8',inline = False)
        embed.add_field(name = 'Servers',value = len(self.client.guilds))
        embed.add_field(name = 'Creator',value = '`Refined#0001`')
        embed.set_thumbnail(url = self.client.user.avatar_url)
        embed.add_field(name="Invite The Bot", value="[Link](https://discord.com/api/oauth2/authorize?client_id=795963203804200980&permissions=8&scope=bot)")
        await ctx.send(embed = embed)


def setup(client):
    client.add_cog(helpcommand(client))