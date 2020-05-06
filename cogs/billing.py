from discord.ext import commands
import discord


class Billing(commands.Cog):
    """
    お金の確認、お金の受け渡し、登録など
    """
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if ctx.author.id not in self.bot.users.keys():
            return False

    @commands.command(aliases=['money', 'balance'])
    async def bal(self, ctx):
        """所持金を確認します。"""

    @commands.command()
    async def pay(self, ctx, to: discord.User, money: int):
        """指定したユーザーにお金を渡します。"""
        if to.id not in self.bot.users.keys():
            await ctx.send(f'ユーザー:{to.mention}はゲームに登録していません。')
            return

        if money > self.bot.users[ctx.author.id]:
            await ctx.send('指定された金額はあなたの所持金をオーバーしています。')
            return

    @commands.command()
    async def register(self, ctx):
        """ユーザー登録をします。"""
        if ctx.author.id in self.bot.users.keys():
            await ctx.send('既に登録されています。')
            return
        self.bot.users[ctx.author.id] = 10000
        await ctx.send('登録されました。')


def setup(bot):
    return bot.add_cog(Billing(bot))
