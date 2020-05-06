from discord.ext import commands


class Billing(commands.Cog):
    """
    お金の確認など
    """

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    return bot.add_cog(Billing(bot))
