from discord.ext import commands
from cogs.utils.database import DB
import traceback


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

        if isinstance(exception, commands.CommandNotFound):
            return

        # orig_error = getattr(exception, "original", exception)
        # error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
        # error_msg = "```py\n" + error_msg[1500:] + "\n```"
        # await context.send(error_msg)
        await super().on_command_error(context, exception)

    async def take_register(self, ctx):
        await ctx.send('あなたはまだゲームに登録していません！登録のために`c!register`コマンドを入力してください。')

    async def say_wait(self, ctx):
        await ctx.send('現在botは稼働していません。しばらくお待ちください。')
