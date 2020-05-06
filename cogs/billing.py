from discord.ext import commands
import discord


class Billing(commands.Cog):
    """
    お金の確認、お金の受け渡し、登録など
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['money', 'balance'])
    async def bal(self, ctx):
        """所持nyanを確認します。"""
        if ctx.author.id not in self.bot.players.keys():
            await self.bot.take_register(ctx)
            return
        await ctx.send(f'あなたの所持nyanは{self.bot.players[ctx.author.id]}nyanです。')

    @commands.command()
    async def pay(self, ctx, to: discord.User, money: int):
        """指定したユーザーにお金を渡します。"""
        if ctx.author.id not in self.bot.players.keys():
            await self.bot.take_register(ctx)
            return

        if to.id not in self.bot.players.keys():
            await ctx.send(f'ユーザー:{to.mention}はゲームに登録していません。')
            return

        if money > self.bot.players[ctx.author.id]:
            await ctx.send('指定されたnyan額はあなたの所持金をオーバーしています。')
            return

    @commands.command()
    async def register(self, ctx):
        """ユーザー登録をします。"""
        if ctx.author.id in self.bot.players.keys():
            await ctx.send('既に登録されています。')
            return
        self.bot.players[ctx.author.id] = 10000
        await ctx.send('登録されました。')


def setup(bot):
    return bot.add_cog(Billing(bot))
