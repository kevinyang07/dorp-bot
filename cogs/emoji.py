import discord
from discord.ext import commands
from discord.utils import get

class EmojiConverter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def emojistuff(self, msg):
      content = msg.content.split()
      emoji_found = False
      for emoji in self.bot.emojis:
        for i in range(len(content)):
          if content[i].lower() == emoji.name.lower():
            emoji_found = True
            content[i] = str(emoji)
      content = " ".join(content)
      if emoji_found:
        await msg.delete()
        await msg.channel.send("{} said: {}".format(msg.author.mention, content))

    @commands.Cog.listener()
    async def on_message(self, msg):
        if not msg.author.bot:
            await self.emojistuff(msg)

    @commands.command()
    async def emojis(self, ctx):
        argument = ", ".join([ emoji.name for emoji in self.bot.emojis ])
        await ctx.send(argument)

def setup(bot):
    bot.add_cog(EmojiConverter(bot))
