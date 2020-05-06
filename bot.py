from discord.ext import commands
from cogs.utils.database import DB


class CasinoBot(commands.Bot):
    def __init__(self):
        super().__init__('c!')
        self.is_running = True
        self.users = {}
        self.db = DB(self)
