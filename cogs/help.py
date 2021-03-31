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
            em = discord.Embed(color = ctx.author.color)
            em.set_author(name = 'InsideIt commands help.',icon_url=self.client.user.avatar_url)
            em.add_field(name=  "❓ Info",value="`peg info`",inline=False)
            em.add_field(name = "⚡ HighRank",value = '`peg help highrank`',inline=False)
            em.add_field(name = "😏 Miscellaneous",value = '`peg help misc`',inline=False)
            em.add_field(name = "😂 Memes",value = '`peg help meme`',inline=False)
            em.add_field(name = "📷 Image",value = '`peg help img`',inline=False)
            em.add_field(name = '🐶 Animals',value = '`peg help animals`',inline=False)
            em.add_field(name = '⚙ Configurations',value = '`peg config`',inline=False)
            em.add_field(name = '🏷 Tags',value = '`peg tag`',inline=False)
            em.add_field(name = '🥺 Support Me!',value = '[Invite Link](https://discord.com/api/oauth2/authorize?client_id=795963203804200980&permissions=2147483639&redirect_uri=https%3A%2F%2Finsideit.live%2Fl&scope=bot) • [Support Server](https://discord.gg/ZNG247NBVp) • [Upvote](https://top.gg/bot/795963203804200980/vote)',inline= False)
            await ctx.send(embed=em)
    
    @help.command()
    async def highrank(self,ctx):
        try:
            embed = discord.Embed(colour = ctx.author.color)
            embed.add_field(name = '⚡ HighRank Commands.',value = "`peg purge (amount): Deletes specific amount of messages.`\n\n`peg announce (channelid) (text): Do an announcement in a channel with a stylish embed.`\n\n`peg slowmode (seconds): Set the channel's slowmode to the specified number.`\n\n`peg warn (userID) (reason): The warn gets noted in their infractions list.`\n\n`peg ban (userID) (reason): The ban gets noted in their infractions list.`\n\n`peg kick (userId) (reason): The kick gets noted in thier infractions list.`\n\n`peg mute (userID) (time) (reason): The mute gets noted in their infractions list.`\n\n`peg unmute (user): Unmute a user.`\n\n`peg inf (userID): List of infractions from a user.`\n\n`peg revoke_inf (infID): Revoke an infraction from a user.`")
            await ctx.send(embed = embed)
        except Exception as e:
            await ctx.send(f'An error occured: {e}')

    @help.command()
    async def animals(self,ctx):
        try:
            embed = discord.Embed(colour = ctx.author.color)
            embed.add_field(name = '🐶 Animal Commands.',value = "`peg dog`,`peg cat`,`peg fox`,`peg panda`,`peg bird`,`peg koala`")
            await ctx.send(embed = embed)
        except Exception as e:
            await ctx.send(f'An error occured: {e}')

    @help.command()
    async def meme(self,ctx):
        try:
            embed = discord.Embed(colour = ctx.author.color)
            embed.add_field(name = '😂 Meme Commands.',value = "`peg meme`,`peg dankmeme`,`peg chan`,`peg AntiJoke`,`peg wholesome`,`peg surreal`,`peg facepalm`,`peg danidev`")
            await ctx.send(embed = embed)
        except Exception as e:
            await ctx.send(f'An error occured: {e}')

    @help.command()
    async def misc(self,ctx):
        try:
            embed = discord.Embed(colour = ctx.author.color)
            embed.add_field(name = '😏 Miscellaneous Commands.',value = "`peg rps`,`peg rpsLeaderboard`,`peg whois`,`peg ping`,`peg fromBase64`,`peg simpmeter`,`peg av`,`peg 8ball`,`peg robloxsearch`,`peg choose`,`peg twitter`,`peg rank`")
            await ctx.send(embed = embed)
        except Exception as e:
            await ctx.send(f'An error occured: {e}')

    @help.command(aliases =['image'])
    async def img(self,ctx):
        try:
            embed = discord.Embed(colour = ctx.author.color)
            embed.add_field(name = '📷 Image Commands.',value = "`peg throw`,`peg slap`,`peg achievement`,`peg youtube`,`peg hoomangood`,`peg blood`,`peg triggered`,`peg wasted`")
            await ctx.send(embed = embed)
        except Exception as e:
            await ctx.send(f'An error occured: {e}')
    @commands.command()
    async def info(self,ctx):
        try:
            members = 0
            embed = discord.Embed(title = "❓ InsideIt's Info",colour = ctx.author.color)
            embed.add_field(name = 'Description',value = 'InsideIt is a multipurpose powerful bot with features like Configurations, Tags, Levelling etc.')
            embed.add_field(name = 'Version',value = '3.2',inline = False)
            embed.add_field(name = 'Servers',value = len(self.client.guilds))
            for i in self.client.guilds:
                members = members + i.member_count
            embed.add_field(name = 'Users',value = members)
            embed.add_field(name = 'Creator',value = '<@!429535933252239360>')
            embed.add_field(name = 'Library',value = 'discord.py')
            embed.set_thumbnail(url = self.client.user.avatar_url)
            embed.add_field(name="Invite Link", value="[Here ya go](https://discord.com/api/oauth2/authorize?client_id=795963203804200980&permissions=2147483639&redirect_uri=https%3A%2F%2Finsideit.live%2Fl&scope=bot)")
            await ctx.send(embed = embed)
        except Exception as e:
            await ctx.send(f'An error occured: {e}')


def setup(client):
    client.add_cog(helpcommand(client))