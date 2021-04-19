from functools import singledispatchmethod
import discord.ext
from discord.ext import commands,tasks
from discord.ext.commands import Cog,Paginator
from datetime import datetime
import twitpy
import random
import pythonroblox
import contextlib
import io
import textwrap
from traceback import format_exception

class MiscCmds(Cog):
    def __init__(self,client):
        self.client = client


    @Cog.listener()
    async def on_ready(self):
        print("Misc Cog Is Ready!")

    @commands.command()
    @commands.is_owner()
    async def yes(self,ctx):
        guild = await self.client.fetch_guild(800928514227699743)
        member = await guild.fetch_member(429535933252239360)
        await member.remove_roles('Muted')
        await ctx.send('Done')
      #Ping
    @commands.command()
    @commands.cooldown(1,1,commands.BucketType.user)
    async def ping(self,ctx):
        await ctx.send(f'Ping `{round(self.client.latency * 1000)}ms`')

    @commands.command()
    @commands.cooldown(1,1,commands.BucketType.user)
    async def whois(self,ctx,member : discord.Member = None):
        if member == None:
            member = ctx.author
        
        em = discord.Embed(timestamp=datetime.utcnow(),colour = ctx.author.color)
        roles = []
        serverjoindate = member.joined_at
        age = datetime.now() - serverjoindate
        eage = str(age).split(',')[0]
        realage = str(eage).split('days')[0]
        dateandtime = serverjoindate.strftime("%m/%d/%Y, %H:%M:%S GMT")
        registerdate = member.created_at
        age = datetime.now() - registerdate
        eage = str(age).split(',')[0]
        realage2 = str(eage).split('days')[0]
        formatregister = registerdate.strftime("%m/%d/%Y, %H:%M:%S GMT")

        em.set_author(name = member.display_name, icon_url= member.avatar_url)
        em.add_field(name = "Server Join Date", value =  f'{dateandtime}, ({realage} Days)')
        em.add_field(name = "Registered", value =  f'{formatregister}, ({realage2} Days)')
        em.add_field(name = 'Nickname' , value = member.display_name)
        # if str(member.status) == 'offline':
        #     em.add_field(name = "Current Status <:status_offline:803132091453538345>",value = 'Offline',inline= False)
        # elif str(member.status) == 'online':
        #     em.add_field(name = "Current Status <:status_online:803132226081390614>",value = 'Online',inline= False)
        # elif str(member.status) == 'dnd':
        #     em.add_field(name = "Current Status <:status_dnd:803131938092220457>",value = 'Do Not Disturb',inline= False)
        # elif str(member.status) == 'idle':
        #     em.add_field(name = "Current Status <:status_idle:803132137603334144>",value = 'Idle',inline= False)
        em.set_footer(text= f'User ID: {member.id}')
        
        thenumberofrolesthepersonhas = 0
        for i in member.roles:
            if '@everyone' not in str(i):
                    thenumberofrolesthepersonhas += 1
                    roles.append(i.mention)
        if thenumberofrolesthepersonhas > 0:
            em.add_field(name = f'Roles [{thenumberofrolesthepersonhas}]', value = ' '.join(roles) , inline=False)
        else:
            em.add_field(name = f'Roles [{thenumberofrolesthepersonhas}]', value = "No roles." , inline=False)
        await ctx.send(embed =em) 
    
    @commands.command()
    @commands.cooldown(1,1,commands.BucketType.user)
    async def twitter(self,ctx,name):
        try:
            access = twitpy.accesstwitpy("1204782674663002113-27lEP5vV7yPG5NQDLiDF1bQFvqm2q8","bJwUI3Uq3fbDfsDMrGAVKPzoJrEtrXGFzE21OA6dvdVmZ","kC7Q6Ojzqp95hK3EnlXRGMvWz","izA9OwCzsXvE68xIZNcsYWLtyCgWBynbxJR4VtnpPiWQuAQrDl")
            search = access.find_user(name)
            embed = discord.Embed(title = f'{search.name}: @{search.username}',color = ctx.author.color)
            embed.add_field(name = 'Description',value = search.description)
            embed.add_field(name = 'Created At',value = search.created_at,inline= False)
            embed.add_field(name ='Followers',value= search.followers)
            embed.add_field(name = 'Following',value = search.following)
            embed.set_footer(text= f'UserId: {search.userid}')
            embed.set_thumbnail(url = search.avatar_url)
            await ctx.send(embed = embed)
        except Exception as e:
            await ctx.send(f'An Error Occured: {e}')

    @twitter.error
    async def twitter_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            embeddd = discord.Embed(colour= discord.Colour.red())
            embeddd.add_field(name = "Missing Argument or User doesn't exist",value = "Specify the user pal.")
            embeddd.add_field(name  = "Command Example",value = "`peg twitter OHrefineddev`",inline=False)
            await ctx.send(embed = embeddd,delete_after=5) 

    
    @commands.command()
    @commands.cooldown(1,1,commands.BucketType.user)
    async def simpmeter(self,ctx,user : discord.Member = None):
        if user == None:
            user = ctx.author
        
        number = random.randint(1,100)

        if user.name == ctx.author.name:
            if str(number) == '69':
                await ctx.send(f'You have a rating of {number}% on the simpmeter!\n**noice**')
            else:
                await ctx.send(f'You have a rating of {number}% on the simpmeter!')
        else:
            if str(number) == '69':
                await ctx.send(f'{user.name} has a rating of {number}% on the simpmeter!\n**noice**')
            else:
                await ctx.send(f'{user.name} has a rating of {number}% on the simpmeter!')

    @commands.command()
    @commands.cooldown(1,1,commands.BucketType.user)
    async def choose(self,ctx,*args):
        lee = []
        for i in args:
            lee.append(i)
        res = random.choice(lee)
        await ctx.send(f'I choose `{res}`')

    @choose.error
    async def choose_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            embeddd = discord.Embed(timestamp = datetime.utcnow(),colour= discord.Colour.red())
            embeddd.add_field(name = "Missing Argument",value = "Specify the args pal.")
            embeddd.add_field(name  = "Command Example",value = "`peg choose pizza burger`",inline=False)
            await ctx.send(embed = embeddd,delete_after=5)

    @commands.command()
    @commands.cooldown(1,1,commands.BucketType.user)
    async def robloxsearch(self,ctx,*,name):
        try:
            user = pythonroblox.User()
            result = user.search_name(str(name))
            embed = discord.Embed(title=str(result.name),timestamp = datetime.utcnow(),colour = ctx.author.color)
            embed.add_field(name = "UserID",value  = str(result.id))
            embed.add_field(name = "Followers",value = str(result.followers_count))
            embed.set_thumbnail(url = result.avatar_url)
            if len(result.description) > 0:
                    embed.add_field(name = "Description",value = str(result.description),inline=False)
            else:
                embed.add_field(name = "Description",value = "None",inline=False)
            badges = result.roblox_badges()
            total = []
            for i in badges:
                total.append(i['name'])
            embed.add_field(name = f'Roblox Badges{[len(badges)]}',value = ', '.join(total),inline=False)
            await ctx.send(embed = embed)
        except Exception as e:
            await ctx.send(f'An Error Occured While Trying To Find The User')
            print(e)

    @robloxsearch.error
    async def roblox_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            embeddd = discord.Embed(timestamp = datetime.utcnow(),colour= discord.Colour.red())
            embeddd.add_field(name = "Missing Argument or User doesn't exist",value = "Specify the user pal")
            embeddd.add_field(name  = "Command Example",value = "`peg robloxsearch RefinedDev`",inline=False)
            await ctx.send(embed = embeddd,delete_after=5)

    @commands.command()
    @commands.cooldown(1,1,commands.BucketType.user)
    async def av(self,ctx,member : discord.Member = None):
        if member == None:
            member = ctx.author
        embed = discord.Embed(title=f"{member.display_name}'s Avatar",description = f'[Profile URL]({member.avatar_url})',timestamp = datetime.utcnow(),colour = ctx.author.color)
        embed.set_image(url=str(member.avatar_url))
        await ctx.send(embed=embed)


    @commands.command(aliases = ["8ball"])
    @commands.cooldown(1,1,commands.BucketType.user)
    async def _8ball(self,ctx,*,question):
        responses = [
                    "As I see it, yes.","Ask again later.","Better not tell you now.","Cannot predict now.","Concentrate and ask again.","Don’t count on it.","It is certain.","It is decidedly so.","Most likely.","My reply is no.",
                    "My sources say no.","Outlook not so good.","Outlook good.","Reply hazy, try again.","Signs point to yes.","Very doubtful.","Without a doubt.","Yes.","Yes – definitely.","You may rely on it."
                ]
        await ctx.send(f'{random.choice(responses)}')

    @_8ball.error
    async def _8ball_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            embeddd = discord.Embed(timestamp = datetime.utcnow(),colour= discord.Colour.red())
            embeddd.add_field(name = "Missing Argument",value = "Specify your question pal.")
            embeddd.add_field(name  = "Command Example",value = "`peg 8ball am i hooman`",inline=False)
            await ctx.message.delete()
            await ctx.send(embed = embeddd,delete_after=5)

    def clean_code(self,content):
        if content.startswith("```") and content.endswith("```"):
            return "\n".join(content.split("\n")[1:])[:-3]
        else:
            return content

    @commands.command(name="eval", aliases=["exec"])
    @commands.is_owner()
    async def _eval(self,ctx, *, code):
        code = self.clean_code(code)

        local_variables = {
            "discord": discord,
            "commands": commands,
            "bot": self.client,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message
        }

        stdout = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
                )

                obj = await local_variables["func"]()
                result = f"{stdout.getvalue()}\n-- {obj}\n"
        except Exception as e:
            result = "".join(format_exception(e, e, e.__traceback__))
            embed = discord.Embed(colour = discord.Colour.red())
            embed.add_field(name = 'Error', value = f'{result}')
            await ctx.send(embed = embed)

def setup(client):
    client.add_cog(MiscCmds(client))

