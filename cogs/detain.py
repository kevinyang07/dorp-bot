import discord
from discord.ext import commands

class detain(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def detain(self, ctx, member: discord.Member = None):
        overseer = discord.utils.get(ctx.guild.roles, name = "Overseer")
        guard = discord.utils.get(ctx.guild.roles, name = "Guard")
        judge = discord.utils.get(ctx.guild.roles, name = "The Judge")
        staff = discord.utils.get(ctx.guild.roles, name = "Staff")
        if guard in ctx.author.roles or overseer in ctx.author.roles or judge in ctx.author.roles or staff in ctx.author.roles:
            if member == None:
                await ctx.send("Tell me who to put in jail")
            else:
                role = discord.utils.get(ctx.guild.roles, name='Dead Meme')
                role2 = discord.utils.get(ctx.guild.roles, name='Member')
                await member.add_roles(role)
                await member.remove_roles(role2)
                await ctx.send("The user was successfully put in jail")

    @commands.command()
    async def undetain(self, ctx, member: discord.Member = None):
        overseer = discord.utils.get(ctx.guild.roles, name = "Overseer")
        guard = discord.utils.get(ctx.guild.roles, name = "Guard")
        judge = discord.utils.get(ctx.guild.roles, name = "The Judge")
        staff = discord.utils.get(ctx.guild.roles, name = "Staff")
        if guard in ctx.author.roles or overseer in ctx.author.roles or judge in ctx.author.roles or staff in ctx.author.roles:
            if member == None:
                await ctx.send("Tell me who to take out of jail")
            else:
                role = discord.utils.get(ctx.guild.roles, name='Dead Meme')
                role2 = discord.utils.get(ctx.guild.roles, name='Member')
                await member.remove_roles(role)
                await member.add_roles(role2)
                await ctx.send("The user was successfully taken out of jail")
        else:
            await ctx.send("ha you suck")

def setup(bot):
    bot.add_cog(detain(bot))
