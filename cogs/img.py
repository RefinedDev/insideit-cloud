import discord.ext
from discord.ext import commands,tasks
from discord.ext.commands import Cog
import urllib
import json
import random
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO
import requests

class img(Cog):
    def __init__(self,client):
        self.client = client

    @Cog.listener()
    async def on_ready(self):
        print("Image Cog Is Ready!")


    async def cog_command_error(self,ctx,exc):
        if isinstance(exc,commands.CommandOnCooldown):
            embeddd = discord.Embed(colour= discord.Colour.red())
            embeddd.add_field(name = "eyo calmdown",value = f'This command is on cooldown, try again later after {exc.retry_after:,.2f} seconds.')
            await ctx.send(embed = embeddd,delete_after=5) 
        elif isinstance(exc,commands.MemberNotFound):
            embeddd = discord.Embed(colour= discord.Colour.red())
            embeddd.add_field(name = "eyo calmdown",value = f'Member Not Found.')
            await ctx.send(embed = embeddd,delete_after=5) 
        else:
            print(exc)
    
    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def slap(self,ctx,member : discord.Member = None):
        if member == None:
            member = ctx.author

        slap = Image.open("cogs/images/slap.jpg")
        userpfp = member.avatar_url_as(size = 128)
        data = BytesIO(await userpfp.read())
        pfp = Image.open(data)

        pfp = pfp.resize((120,108))
        slap.paste(pfp, (116,29))
        slap.save('cogs/images/profile.jpg')

        hitterpfp = ctx.author.avatar_url_as(size = 128)
        data = BytesIO(await hitterpfp.read())
        pfp = Image.open(data)

        pfp = pfp.resize((134,134))
        slap.paste(pfp, (484,19))
        slap.save('cogs/images/profile.jpg')
        
        await ctx.send(file = discord.File('cogs/images/profile.jpg'))


    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def throw(self,ctx,*,text = 'Worst Dad ever.'):
        abandon = Image.open("cogs/images/abandon.jpg")
        draw = ImageDraw.Draw(abandon)
        font = ImageFont.truetype('cogs/images/ARIAL.TTF',25)
        draw.text((25,417), text, (0,0,0), font= font)

        abandon.save('cogs/images/abandonpic.jpg')
        
        await ctx.send(file = discord.File('cogs/images/abandonpic.jpg'))


    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def youtube(self,ctx,*,text = 'yo calm down jamal'):
        abandon = Image.open("cogs/images/youtube.jpg")
        i = abandon.convert('RGB')
        i.save('cogs/images/youtubepic.jpg')
        draw = ImageDraw.Draw(i)
        font = ImageFont.truetype('cogs/images/ARIAL.TTF',20)
        font2 = ImageFont.truetype('cogs/images/ARIAL.TTF',15)
        draw.text((99,67), text, (0,0,0), font= font)

        draw.text((99,35), ctx.author.name, (0,0,0), font= font2)

        hitterpfp = ctx.author.avatar_url_as(size = 128)
        data = BytesIO(await hitterpfp.read())
        pfp = Image.open(data)

        pfp = pfp.resize((52,54))
        i.paste(pfp, (39,44))
        i.save('cogs/images/youtubepic.jpg')
        
        await ctx.send(file = discord.File('cogs/images/youtubepic.jpg'))



    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def achievement(self,ctx,*,text = 'For free'):
        achiv = Image.open("cogs/images/achivement.jpg")
        i = achiv.convert('RGB')
        i.save('cogs/images/achievementpic.jpg')
        draw = ImageDraw.Draw(i)
        font = ImageFont.truetype('cogs/images/Minecraft.ttf',15)
        draw.text((59,35), text, (255,255,255), font= font)
        
        i.save('cogs/images/achievementpic.jpg')
        
        await ctx.send(file = discord.File('cogs/images/achievementpic.jpg'))

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def hoomangood(self,ctx,*,text = 'idk'):
        abandon = Image.open("cogs/images/humansgood.jpg")
        i = abandon.convert('RGB')
        draw = ImageDraw.Draw(i)
        font = ImageFont.truetype('cogs/images/ARIAL.TTF',15)
        draw.text((238,355), text, (0,0,0), font= font)

        i.save('cogs/images/humansgoodpic.jpg')
        
        await ctx.send(file = discord.File('cogs/images/humansgoodpic.jpg'))

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def blood(self,ctx,*,text = 'THE FUCK YOU SAY TO ME YOU LITTLE SHIT'):
        abandon = Image.open("cogs/images/violence.jpg")
        i = abandon.convert('RGB')
        draw = ImageDraw.Draw(i)
        font = ImageFont.truetype('cogs/images/ARIAL.TTF',15)
        draw.text((205,4), text, (0,0,0), font= font)

        i.save('cogs/images/violencepic.jpg')
        
        await ctx.send(file = discord.File('cogs/images/violencepic.jpg'))

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def trigger(self, ctx,user : discord.Member = None):
        if user == None:
            user = ctx.author
        response = requests.get(f"https://some-random-api.ml/canvas/triggered/?avatar={user.avatar_url_as(size=128)}")
        file = open("triggred.gif", "wb")
        file.write(response.content)
        file.close()
        await ctx.send(file=discord.File('triggred.gif'))

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def wasted(self, ctx,user : discord.Member = None):
        if user == None:
            user = ctx.author
        response = requests.get(f"https://some-random-api.ml/canvas/wasted/?avatar={user.avatar_url_as(size=128)}")
        file = open("wasted.gif", "wb")
        file.write(response.content)
        file.close()
        await ctx.send(file=discord.File('wasted.gif'))

def setup(client):
    client.add_cog(img(client))