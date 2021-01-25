import discord.ext
from discord.ext import commands,tasks
from discord.ext.commands import Cog
from datetime import datetime
import twitpy
import random
import pythonroblox
import ast

class MiscCmds(Cog):
    def __init__(self,client):
        self.client = client


    @Cog.listener()
    async def on_ready(self):
        print("SomeCommands Cog Is Ready!")

    async def cog_command_error(self,ctx,error):
        if isinstance(error,commands.CommandNotFound):
            pass
        elif isinstance(error,commands.MissingPermissions):
            embed = discord.Embed(colour= discord.Colour.red(),timestamp = datetime.utcnow())
            embed.add_field(name="eyo calmdown",value= "You do not have the required permissions to run this command.")
            await ctx.send(embed= embed,delete_after=5)
        elif isinstance(error,commands.MissingRequiredArgument):
            pass
        elif isinstance(error,commands.CommandOnCooldown):
            embeddd = discord.Embed(colour= discord.Colour.red())
            embeddd.add_field(name = "eyo calmdown",value = f'This command is on cooldown, try again later after {error.retry_after:,.2f} seconds.')
            await ctx.send(embed = embeddd,delete_after=5)  
        else:
            print(error)
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
        dateandtime = serverjoindate.strftime("%m/%d/%Y, %H:%M:%S GMT")
        registerdate = member.created_at
        formatregister = registerdate.strftime("%m/%d/%Y, %H:%M:%S GMT")

        em.set_author(name = member.display_name, icon_url= member.avatar_url)
        em.add_field(name = "Server Join Date", value =  dateandtime)
        em.add_field(name = "Registered", value =  formatregister)
        if str(member.status) == 'offline':
            em.add_field(name = "Current Status",value = '<:status_offline:596576752013279242> Offline',inline= False)
        elif str(member.status) == 'online':
            em.add_field(name = "Current Status",value = '<:status_online:596576749790429200> Online',inline= False)
        elif str(member.status) == 'dnd':
            em.add_field(name = "Current Status",value = '<:status_dnd:596576774364856321> Do Not Disturb',inline= False)
        elif str(member.status) == 'idle':
            em.add_field(name = "Current Status",value = '<:status_idle:596576773488115722> Idle',inline= False)
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
            embeddd.add_field(name  = "Command Example",value = "`?twitter OHrefineddev`",inline=False)
            await ctx.send(embed = embeddd,delete_after=5) 

    
    @commands.command()
    @commands.cooldown(1,1,commands.BucketType.user)
    async def simpmeter(self,ctx,user : discord.Member = None):
        if user == None:
            user = ctx.author
        
        number = random.randint(1,100)

        if user.name == ctx.author.name:
            await ctx.send(f'You have a rating of {number}% on the simpmeter!')
        else:
            await ctx.send(f'{user.name} has a rating of {number}% on the simpmeter!')

    @commands.command()
    @commands.cooldown(1,1,commands.BucketType.user)
    async def choose(self,ctx,choice1,choice2):
        choice = random.randint(1,2)
        if choice == 1:
            await ctx.send(f'I choose `{choice1}`')
        if choice == 2:
            await ctx.send(f'I choose `{choice2}`')

    @choose.error
    async def choose_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            embeddd = discord.Embed(timestamp = datetime.utcnow(),colour= discord.Colour.red())
            embeddd.add_field(name = "Missing Argument",value = "Specify the args pal.")
            embeddd.add_field(name  = "Command Example",value = "`?choose pizza burger`",inline=False)
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
            embeddd.add_field(name  = "Command Example",value = "`?robloxsearch RefinedDev`",inline=False)
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
            embeddd.add_field(name  = "Command Example",value = "`?8ball am i hooman`",inline=False)
            await ctx.message.delete()
            await ctx.send(embed = embeddd,delete_after=5)

    def insert_returns(self,body):
        # insert return stmt if the last expression is a expression statement
        if isinstance(body[-1], ast.Expr):
            body[-1] = ast.Return(body[-1].value)
            ast.fix_missing_locations(body[-1])

        # for if statements, we insert returns into the body and the orelse
        if isinstance(body[-1], ast.If):
            self.insert_returns(body[-1].body)
            self.insert_returns(body[-1].orelse)

        # for with blocks, again we insert returns into the body
        if isinstance(body[-1], ast.With):
            self.insert_returns(body[-1].body)

        # for with blocks, again we insert returns into the body
        if isinstance(body[-1], ast.AsyncWith):
            self.insert_returns(body[-1].body)


    @commands.command()
    async def eval_fn(self,ctx, *, cmd):
        if ctx.author.id == 429535933252239360:
            try:
                fn_name = "_eval_expr"

                cmd = cmd.strip("` ")

                # add a layer of indentation
                cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

                # wrap in async def body
                body = f"async def {fn_name}():\n{cmd}"

                parsed = ast.parse(body)
                body = parsed.body[0].body

                self.insert_returns(body)

                env = {
                    'bot': ctx.bot,
                    'discord': discord,
                    'commands': commands,
                    'ctx': ctx,
                    '__import__': __import__
                }
                exec(compile(parsed, filename="<ast>", mode="exec"), env)

                (await eval(f"{fn_name}()", env))
            except:
                pass

def setup(client):
    client.add_cog(MiscCmds(client))

