import discord.ext
from discord.ext import commands,tasks
from discord.ext.commands import Cog
import urllib
import json
import random
import aiohttp
from datetime import datetime

class apiscraping(Cog):
    def __init__(self,client):
        self.client = client
        self.MemesForDankMeme.start()

    @Cog.listener()
    async def on_ready(self):
        print("APIScraping Cog Is Ready!")


    async def cog_command_error(self,ctx,exc):
        if isinstance(exc,commands.CommandOnCooldown):
            embeddd = discord.Embed(colour= discord.Colour.red())
            embeddd.add_field(name = "eyo calmdown",value = f'This command is on cooldown, try again later after {exc.retry_after:,.2f} seconds.')
            await ctx.send(embed = embeddd,delete_after=5)  
        else:
            print(exc)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def meme(self,ctx):
        try:
            # link = "https://www.reddit.com/r/facepalm/new.json?sort=hot,"
            # data = urllib.request.urlopen(link)
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://www.reddit.com/r/memes/new.json?sort=hot,") as data:
                    res = await data.json()
                    choose = res['data']['children'] [random.randint(0, 25)]
                    title = choose['data']['title']
                    standard = 'https://www.reddit.com'
                    lin = choose['data']['permalink']
                    newlink = standard + lin
                    embed = discord.Embed(description= f'[{title}]({newlink})',colour = ctx.author.color)
                    embed.set_image(url= choose['data']['url'] )
                    likes = choose['data']['ups']
                    replies = choose['data']['num_comments']
                    embed.set_footer(text = f'👍 {likes} | 💬 {replies}')
                    await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f'An error occured: {e}',delete_after=10)


    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def dankmeme(self,ctx):
        try:
            # link = "https://www.reddit.com/r/facepalm/new.json?sort=hot,"
            # data = urllib.request.urlopen(link)
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://www.reddit.com/r/dankmemer/new.json?sort=hot,") as data:
                    res = await data.json()
                    choose = res['data']['children'] [random.randint(0, 25)]
                    title = choose['data']['title']
                    standard = 'https://www.reddit.com'
                    lin = choose['data']['permalink']
                    newlink = standard + lin
                    embed = discord.Embed(description= f'[{title}]({newlink})',colour = ctx.author.color)
                    embed.set_image(url= choose['data']['url'] )
                    likes = choose['data']['ups']
                    replies = choose['data']['num_comments']
                    embed.set_footer(text = f'👍 {likes} | 💬 {replies}')
                    await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f'An error occured: {e}',delete_after=10)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def chan(self,ctx):
        try:
            # link = "https://www.reddit.com/r/facepalm/new.json?sort=hot,"
            # data = urllib.request.urlopen(link)
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://www.reddit.com/r/4chan/new.json?sort=hot,") as data:
                    res = await data.json()
                    choose = res['data']['children'] [random.randint(0, 25)]
                    title = choose['data']['title']
                    standard = 'https://www.reddit.com'
                    lin = choose['data']['permalink']
                    newlink = standard + lin
                    embed = discord.Embed(description= f'[{title}]({newlink})',colour = ctx.author.color)
                    embed.set_image(url= choose['data']['url'] )
                    likes = choose['data']['ups']
                    replies = choose['data']['num_comments']
                    embed.set_footer(text = f'👍 {likes} | 💬 {replies}')
                    await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f'An error occured: {e}',delete_after=10)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def AntiJoke(self,ctx):
        try:
            # link = "https://www.reddit.com/r/facepalm/new.json?sort=hot,"
            # data = urllib.request.urlopen(link)
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://www.reddit.com/r/AntiJoke/new.json?sort=hot,") as data:
                    res = await data.json()
                    choose = res['data']['children'] [random.randint(0, 25)]
                    title = choose['data']['title']
                    standard = 'https://www.reddit.com'
                    lin = choose['data']['permalink']
                    newlink = standard + lin
                    embed = discord.Embed(description= f'[{title}]({newlink})',colour = ctx.author.color)
                    embed.set_image(url= choose['data']['url'] )
                    likes = choose['data']['ups']
                    replies = choose['data']['num_comments']
                    embed.set_footer(text = f'👍 {likes} | 💬 {replies}')
                    await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f'An error occured: {e}',delete_after=10)


    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def wholesome(self,ctx):
        try:
            # link = "https://www.reddit.com/r/facepalm/new.json?sort=hot,"
            # data = urllib.request.urlopen(link)
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://www.reddit.com/r/wholesome/new.json?sort=hot,") as data:
                    res = await data.json()
                    choose = res['data']['children'] [random.randint(0, 25)]
                    title = choose['data']['title']
                    standard = 'https://www.reddit.com'
                    lin = choose['data']['permalink']
                    newlink = standard + lin
                    embed = discord.Embed(description= f'[{title}]({newlink})',colour = ctx.author.color)
                    embed.set_image(url= choose['data']['url'] )
                    likes = choose['data']['ups']
                    replies = choose['data']['num_comments']
                    embed.set_footer(text = f'👍 {likes} | 💬 {replies}')
                    await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f'An error occured: {e}',delete_after=10)


    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def surreal(self,ctx):
        try:
            # link = "https://www.reddit.com/r/facepalm/new.json?sort=hot,"
            # data = urllib.request.urlopen(link)
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://www.reddit.com/r/surrealmemes/new.json?sort=hot,") as data:
                    res = await data.json()
                    choose = res['data']['children'] [random.randint(0, 25)]
                    title = choose['data']['title']
                    standard = 'https://www.reddit.com'
                    lin = choose['data']['permalink']
                    newlink = standard + lin
                    embed = discord.Embed(description= f'[{title}]({newlink})',colour = ctx.author.color)
                    embed.set_image(url= choose['data']['url'] )
                    likes = choose['data']['ups']
                    replies = choose['data']['num_comments']
                    embed.set_footer(text = f'👍 {likes} | 💬 {replies}')
                    await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f'An error occured: {e}',delete_after=10)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def facepalm(self,ctx):
        try:
            # link = "https://www.reddit.com/r/facepalm/new.json?sort=hot,"
            # data = urllib.request.urlopen(link)
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://www.reddit.com/r/facepalm/new.json?sort=hot,") as data:
                    res = await data.json()
                    choose = res['data']['children'] [random.randint(0, 25)]
                    title = choose['data']['title']
                    standard = 'https://www.reddit.com'
                    lin = choose['data']['permalink']
                    newlink = standard + lin
                    embed = discord.Embed(description= f'[{title}]({newlink})',colour = ctx.author.color)
                    embed.set_image(url= choose['data']['url'] )
                    likes = choose['data']['ups']
                    replies = choose['data']['num_comments']
                    embed.set_footer(text = f'👍 {likes} | 💬 {replies}')
                    await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f'An error occured: {e}',delete_after=10)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def danidev(self,ctx):
        try:
            # link = "https://www.reddit.com/r/facepalm/new.json?sort=hot,"
            # data = urllib.request.urlopen(link)
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://www.reddit.com/r/DaniDev/new.json?sort=hot,") as data:
                    res = await data.json()
                    choose = res['data']['children'] [random.randint(0, 25)]
                    title = choose['data']['title']
                    standard = 'https://www.reddit.com'
                    lin = choose['data']['permalink']
                    newlink = standard + lin
                    embed = discord.Embed(description= f'[{title}]({newlink})',colour = ctx.author.color)
                    embed.set_image(url= choose['data']['url'] )
                    likes = choose['data']['ups']
                    replies = choose['data']['num_comments']
                    embed.set_footer(text = f'👍 {likes} | 💬 {replies}')
                    await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f'An error occured: {e}',delete_after=10)

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def fortnite(self,ctx):
        try:
            # link = "https://www.reddit.com/r/facepalm/new.json?sort=hot,"
            # data = urllib.request.urlopen(link)
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://www.reddit.com/r/FortNiteBR/new.json?sort=hot,") as data:
                    res = await data.json()
                    choose = res['data']['children'] [random.randint(0, 25)]
                    title = choose['data']['title']
                    standard = 'https://www.reddit.com'
                    lin = choose['data']['permalink']
                    newlink = standard + lin
                    embed = discord.Embed(description= f'[{title}]({newlink})',colour = ctx.author.color)
                    embed.set_image(url= choose['data']['url'] )
                    likes = choose['data']['ups']
                    replies = choose['data']['num_comments']
                    embed.set_footer(text = f'👍 {likes} | 💬 {replies}')
                    await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f'An error occured: {e}',delete_after=10)


    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def discord(self,ctx):
        try:
            # link = "https://www.reddit.com/r/facepalm/new.json?sort=hot,"
            # data = urllib.request.urlopen(link)
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://www.reddit.com/r/discordapp/new.json?sort=hot,") as data:
                    res = await data.json()
                    choose = res['data']['children'] [random.randint(0, 25)]
                    title = choose['data']['title']
                    standard = 'https://www.reddit.com'
                    lin = choose['data']['permalink']
                    newlink = standard + lin
                    embed = discord.Embed(description= f'[{title}]({newlink})',colour = ctx.author.color)
                    embed.set_image(url= choose['data']['url'] )
                    likes = choose['data']['ups']
                    replies = choose['data']['num_comments']
                    embed.set_footer(text = f'👍 {likes} | 💬 {replies}')
                    await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f'An error occured: {e}',delete_after=10)

    @commands.command()
    @commands.cooldown(1,1,commands.BucketType.user)
    async def dog(self,ctx):
        try:
            link = 'https://some-random-api.ml/img/dog'
            post = urllib.request.urlopen(link)
            data = json.load(post)
            thelink = data['link']
            embed = discord.Embed(title = "Here's your dog pic 🐶")
            embed.set_image(url= thelink)
            await ctx.send(embed = embed)
        except Exception as e:
            await ctx.send(f'An error occured {e}',delete_after=10)

    @commands.command()
    @commands.cooldown(1,1,commands.BucketType.user)
    async def cat(self,ctx):
        try:
            link = 'https://some-random-api.ml/img/cat'
            post = urllib.request.urlopen(link)
            data = json.load(post)
            thelink = data['link']
            embed = discord.Embed(title = "Here's your cat pic 😸")
            embed.set_image(url= thelink)
            await ctx.send(embed = embed)
        except Exception as e:
            await ctx.send(f'An error occured {e}',delete_after=10)

    @commands.command()
    @commands.cooldown(1,1,commands.BucketType.user)
    async def panda(self,ctx):
        try:
            link = 'https://some-random-api.ml/img/panda'
            post = urllib.request.urlopen(link)
            data = json.load(post)
            thelink = data['link']
            embed = discord.Embed(title = "Here's your panda pic 🐼")
            embed.set_image(url= thelink)
            await ctx.send(embed = embed)
        except Exception as e:
            await ctx.send(f'An error occured {e}',delete_after=10)


    @commands.command()
    @commands.cooldown(1,1,commands.BucketType.user)
    async def koala(self,ctx):
        try:
            link = 'https://some-random-api.ml/img/koala'
            post = urllib.request.urlopen(link)
            data = json.load(post)
            thelink = data['link']
            embed = discord.Embed(title = "Here's your koala pic 🐨")
            embed.set_image(url= thelink)
            await ctx.send(embed = embed)
        except Exception as e:
            await ctx.send(f'An error occured {e}',delete_after=10)


    @commands.command()
    @commands.cooldown(1,1,commands.BucketType.user)
    async def bird(self,ctx):
        try:
            link = 'https://some-random-api.ml/img/birb'
            post = urllib.request.urlopen(link)
            data = json.load(post)
            thelink = data['link']
            embed = discord.Embed(title = "Here's your bird pic 🐦")
            embed.set_image(url= thelink)
            await ctx.send(embed = embed)
        except Exception as e:
            await ctx.send(f'An error occured {e}',delete_after=10)


    @commands.command()
    @commands.cooldown(1,1,commands.BucketType.user)
    async def fox(self,ctx):
        try:
            link = 'https://some-random-api.ml/img/fox'
            post = urllib.request.urlopen(link)
            data = json.load(post)
            thelink = data['link']
            embed = discord.Embed(title = "Here's your fox pic 🦊")
            embed.set_image(url= thelink)
            await ctx.send(embed = embed)
        except Exception as e:
            await ctx.send(f'An error occured {e}',delete_after=10)

    @commands.command()
    @commands.cooldown(1,1,commands.BucketType.user)
    async def fromBase64(self,ctx,*,code):
        try:
            link = 'https://some-random-api.ml/base64?decode='
            text = code
            total = link + str(text)
            post = urllib.request.urlopen(total)
            data = json.load(post)
            embed = discord.Embed(title = "InsideIt's Base64 Decoder")
            embed.add_field(name = 'Here are the results (might be inaccurate)',value = data['text'])
            await ctx.send(embed = embed)
        except Exception as e:
            await ctx.send(f' An error occured {e}',delete_after = 10)

    @fromBase64.error
    async def lol(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            embeddd = discord.Embed(timestamp = datetime.utcnow(),colour= discord.Colour.red())
            embeddd.add_field(name = "Missing Argument",value = "Specify the text pal.")
            embeddd.add_field(name  = "Command Example",value = "`?fromBase64 bG9s`",inline=False)
            await ctx.send(embed = embeddd,delete_after=5)
    
    @tasks.loop(minutes=5)
    async def MemesForDankMeme(self):
        subreddit = ['memes','dankmeme','danidev']
        subredditt = random.choice(subreddit)
        try:
            for i in self.client.guilds:
                guild = i
                if int(guild.id) == 749855517127737496:
                    channel = guild.get_channel(806741919240945704)
                    async with aiohttp.ClientSession() as cs:
                        async with cs.get(f"https://www.reddit.com/r/{subredditt}/new.json?sort=hot,") as data:
                            res = await data.json()
                            choose = res['data']['children'] [random.randint(0, 25)]
                            title = choose['data']['title']
                            standard = 'https://www.reddit.com'
                            lin = choose['data']['permalink']
                            newlink = standard + lin
                            embed = discord.Embed(description= f'[{title}]({newlink})')
                            embed.set_image(url= choose['data']['url'] )
                            likes = choose['data']['ups']
                            replies = choose['data']['num_comments']
                            embed.set_footer(text = f'👍 {likes} | 💬 {replies}')
                            await channel.send(embed=embed)
        except Exception as e:
            await channel.send(f'An error occured: {e}',delete_after=10)

def setup(client):
    client.add_cog(apiscraping(client))