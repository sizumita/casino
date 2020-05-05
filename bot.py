from discord.ext import commands


class CasinoBot(commands.Bot):
    def __init__(self):
        super().__init__('c!')
