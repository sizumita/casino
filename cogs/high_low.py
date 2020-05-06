from discord.ext import commands
from cogs.utils.highlow import HighAndLow


class HighLow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['hal', 'hl'])
    async def high_and_low(self, ctx, bid):
        if bid > self.bot.users[ctx.author.id]:
            await ctx.send('指定された金額はあなたの所持金をオーバーしています。')
            return
        if ctx.author.id in self.bot.game_que:
            await ctx.send('あなたはすでにゲームを開始しています。')
            return
        self.bot.users[ctx.author.id] -= bid
        self.bot.game_que.append(ctx.author.id)

        game = HighAndLow(self.bot, ctx, bid)
        result = await game.play()
        
        self.bot.users[ctx.author.id] += bid
        self.bot.game_que.remove(ctx.author.id)


def setup(bot):
    return bot.add_cog(HighLow(bot))
