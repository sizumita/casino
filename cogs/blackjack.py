from discord.ext import commands
from cogs.utils.blackjack import BlackJackGame


class Blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

    @commands.command(aliases=['bj'])
    async def blackjack(self, ctx, bid: int):
        """blackjackゲームです。"""
        if bid > self.bot.players[ctx.author.id]:
            await ctx.send('指定された金額はあなたの所持金をオーバーしています。')
            return
        if ctx.author.id in self.bot.game_que:
            await ctx.send('あなたはすでにゲームを開始しています。')
            return

        if bid <= 0:
            await ctx.send('0以下の金額は指定できません。')
            return

        self.bot.players[ctx.author.id] -= bid
        self.bot.game_que.append(ctx.author.id)
        game = BlackJackGame(self.bot, ctx, bid)
        result = await game.start()
        await ctx.send(f'報酬: {result}nyan')
        self.bot.players[ctx.author.id] += result
        self.bot.game_que.remove(ctx.author.id)


def setup(bot):
    return bot.add_cog(Blackjack(bot))
