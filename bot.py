from discord.ext import commands
from cogs.utils.database import DB


class CasinoBot(commands.Bot):
    def __init__(self):
        super().__init__('c!')
        self.is_running = True
        self.players = {}
        self.game_que = []
        self.db = DB(self)

    async def on_command_error(self, context, exception):
        if isinstance(exception, commands.CheckFailure):
            return

        if isinstance(exception, commands.MissingRequiredArgument):
            await context.send('引数が足りません。')
            return

        await super().on_command_error(context, exception)

    async def take_register(self, ctx):
        await ctx.send('あなたはまだゲームに登録していません！登録のために`p!register`コマンドを入力してください。')
