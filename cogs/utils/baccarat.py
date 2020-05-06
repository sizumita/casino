from cogs.utils.tramp import Deck
import discord


class Baccarat:
    def __init__(self, bot, ctx):
        self.bot = bot
        self.ctx = ctx
        self.send = ctx.send
        self.parent = ctx.author

    async def start(self):
        await self.send('ゲームを開始します...')


