
import random
import re

import discord
from discord.ext import commands


class Dad(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def hi_im_dad(self, msg):
        content = msg.content.lower()
        if len(content) > 4 and any(punct == content[-1] for punct in ('.', '?', '!', ',')):
            content = content[:-1]
        ims = ('im ', "i'm ", 'i am ')
        for im in ims:
            if content.startswith(im):
                if 'dad' in content or 'father' in content:
                    await msg.channel.send("no i am")
                else:
                    await msg.channel.send(f"Hi {content[len(im):]}, I'm dad")

    @commands.Cog.listener()
    async def on_message(self, msg):
        await self.hi_im_dad(msg)

def setup(bot):
    bot.add_cog(Dad(bot))
