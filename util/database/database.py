from os import getenv
from pymongo import MongoClient

from util.database.bot import Bot
from util.database.case_numbers import CaseNumber
from util.database.data import Data
from util.database.guilds import Guild
from util.database.users import User

from discord import Embed
from discord.ext import commands

import os
import dotenv
from dotenv import load_dotenv

load_dotenv()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Database:
    """The Database class collects all the functions from each of the
    specific database classes into one to make it easier to use
    """
    def __init__(self):

        # Create the connection to the Omega Psi database and authenticateusername = os.getenv("USERNAME")
        password = os.getenv('dbpassword')
        account_name = os.getenv('dbusername')  # replace this of course
        database_name = os.getenv('dbname')  # and this"""
        self.client = MongoClient(f"mongodb+srv://{account_name}:{password}@cluster0.7dfwi.mongodb.net/{database_name}?retryWrites=true&w=majority")
        self.discordbot = self.client.discordbot
        self.bot = Bot(self.discordbot["bot"])
        self.data = Data(self.discordbot["data"])
        self.case_numbers = CaseNumber(self.discordbot["case_numbers"])
        self.guilds = Guild(self.discordbot["guilds"])
        self.users = User(self.discordbot["users"])


database = Database()
