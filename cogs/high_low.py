from discord.ext import commands
from cogs.utils.highlow import HighAndLow


class HighLow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['hal', 'hl'])
    async def high_and_low(self, ctx, bid):
        game = HighAndLow(self.bot, ctx, bid)
        result = await game.play()


def setup(bot):
    return bot.add_cog(HighLow(bot))
