from discord.ext import commands


class Baccarat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = []

    async def cog_check(self, ctx):
        if ctx.command == 'register':
            return True

        if ctx.author.id not in self.bot.players.keys():
            await self.bot.take_register(ctx)
            return False

        if not self.bot.is_running:
            await self.bot.say_wait(ctx)
            return False

        return True

    @commands.command(aliases=['bacara'])
    async def baccarat(self, ctx):
        if self.bot.get_money(ctx.author.id):
            await ctx.send('所持金がないプレイヤーは開始できません。')
            return
