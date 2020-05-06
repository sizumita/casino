from discord.ext import commands
from cogs.utils.database import DB


class CasinoBot(commands.Bot):
    def __init__(self):
        super().__init__('c!')
        self.is_running = True
        self.users = {}
        self.game_que = []
        self.db = DB(self)

    async def take_register(self, ctx):
        await ctx.send('あなたはまだゲームに登録していません！登録のために`p!register`コマンドを入力してください。')
