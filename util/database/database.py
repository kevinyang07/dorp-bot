from os import getenv
from pymongo import MongoClient

from util.database.bot import Bot
from util.database.case_numbers import CaseNumber
from util.database.data import Data
from util.database.guilds import Guild
from util.database.users import User

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#2922801a-3c5d-41a8-b4bd-ace46a1a0287

class Database:
    """The Database class collects all the functions from each of the
    specific database classes into one to make it easier to use
    """
    def __init__(self):

        # Create the connection to the Omega Psi database and authenticateusername = os.getenv("USERNAME")
        password = "nyw24bxRvHMhNUQ"
        account_name = "kevinyang07"  # replace this of course
        database_name = "discordbot"  # and this"""
        self.client = MongoClient(f"mongodb+srv://{account_name}:{password}@cluster0.7dfwi.mongodb.net/{database_name}?retryWrites=true&w=majority")
        self.discordbot = self.client.discordbot
        self.bot = Bot(self.discordbot["bot"])
        self.data = Data(self.discordbot["data"])
        self.case_numbers = CaseNumber(self.discordbot["case_numbers"])
        self.guilds = Guild(self.discordbot["guilds"])
        self.users = User(self.discordbot["users"])


database = Database()
