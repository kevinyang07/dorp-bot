import asyncio
from math import ceil
from random import randint
from discord import Embed, Color
import json
import random

banner = [
		"Don't hoard groceries and essentials. Please ensure that people who are in need don't face a shortage because of you!",
		"Be compassionate! Help those in need like the elderly and poor. They are facing a crisis which we can't even imagine!",
		"Be considerate. While buying essentials remember that you need to share with fellow citizens!",
		"Going out to buy essentials? Social Distancing is KEY! Maintain at least 2 metres distance between each other in the line.",
		"Plan ahead! Take a minute and check how much you have at home. Planning let's you buy exactly what you need!",
		"Plan and calculate your essential needs for the next three weeks and get only bare minimum necessities.",
		"Help out the elderly by bringing them their groceries and other essentials.",
		"Help out your workers and domestic workers by not cutting their salaries.",
		"Lockdown means LOCKDOWN! Avoid going out unless absolutely necessary. Stay safe!",
		"Do not panic! Your essential needs will be taken care of. DO NOT HOARD.",
		"Be a true Human being. Show compassion. Be considerate. Help those in need. We will get through this!",
		"If you have any medical queries, reach out to your district administration or doctors!",
		"Wash your hands with soap and water often. Keep the virus at bay.",
		"There is no evidence that hot weather will stop the virus! You can! Stay home, stay safe.",
		"Avoid going out during the lockdown. Help break the chain of spread.",
		"dorp"
	]


def send_banner():
    return random.choice(banner)


class Paginator:
    def __init__(self, data, headers, title, per_page=10, info:str=None):
        self.data = data
        self.title = title
        self.per_page = per_page
        self.headers = headers
        self.total_pages = ceil(len(self.data)/self.per_page)
        self.current_page = 1
        self.message = None
        self.info = info
        self.reactions = ["\U000025c0", "\U000025b6"]

    def get_page_elements(self, page_no):
        return self.data[(page_no-1)*self.per_page:page_no*self.per_page]

    def get_page_content(self, page_no):
        elements = self.get_page_elements(page_no)
        val = [0]*len(self.headers)
        for i in range(len(val)):
            val[i] = max(max([len(element[i]) for element in elements]), len(self.headers[i]))
        content, dashes = "", ""

        for i in range(len(val)):
            content += self.headers[i] + " "*(val[i] - len(self.headers[i])) + " "
            dashes += "-"*val[i] + " "

        content += "\n"+dashes+"\n"

        for i in range(len(elements)):
            for j in range(len(val)):
                content += elements[i][j] + " "*(val[j] - len(elements[i][j])) + " "
            content += "\n"
        return f"```\n{content}```"

    async def paginate(self, ctx, client):
        embed = Embed(title=self.title, description=self.get_page_content(self.current_page),
                      color=Color(randint(0, 0xFFFFFF)))
        embed.set_footer(text="Page %s out of %s\n%s" % (str(self.current_page), str(self.total_pages), send_banner()))
        self.message = await ctx.channel.send(embed=embed)
        if self.total_pages == 1:
            return
        if self.info:
            await ctx.channel.send(self.info)
        await self.message.add_reaction(self.reactions[0])
        await self.message.add_reaction(self.reactions[1])

        def check(reaction, user):
            return reaction.message.id == self.message.id and reaction.emoji in self.reactions and user != client.user

        while True:
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=180, check=check)
                try:
                    await reaction.remove(user)
                except Exception:
                    pass
                if reaction.emoji == self.reactions[0]:
                    self.current_page -= 1
                    if self.current_page == 0:
                        self.current_page = self.total_pages
                    embed.description = self.get_page_content(self.current_page)
                    embed.set_footer(text="Page %s out of %s\n%s" % (str(self.current_page), str(self.total_pages), send_banner()))
                    await self.message.edit(embed=embed)
                else:
                    self.current_page += 1
                    if self.current_page > self.total_pages:
                        self.current_page = 1
                    embed.description = self.get_page_content(self.current_page)
                    embed.set_footer(text="Page %s out of %s\n%s" % (str(self.current_page), str(self.total_pages), send_banner()))
                    await self.message.edit(embed=embed)
            except asyncio.TimeoutError:
                await self.message.clear_reactions()
                break
