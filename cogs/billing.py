from discord.ext import commands
import discord


class Billing(commands.Cog):
    """
    お金の確認、お金の受け渡し、登録など
    """
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not self.bot.is_running:
            await self.bot.say_wait(ctx)
            return False

        return True

    @commands.command(aliases=['money', 'balance'])
    async def bal(self, ctx, user: discord.User=None):
        """所持nyanを確認します。"""
        if user:
            if user.id not in self.bot.players.keys():
                await ctx.send(f'ユーザー:{user.mention}はゲームに登録していません。')
                return
            target = user
        else:
            target = ctx.author
        if ctx.author.id not in self.bot.players.keys():
            await self.bot.take_register(ctx)
            return
        await ctx.send(f'{target.mention}の所持nyanは{self.bot.players[target.id]}nyanです。')

    @commands.command()
    async def pay(self, ctx, to: discord.User, money: int):
        """指定したユーザーにお金を渡します。"""
        if ctx.author.id not in self.bot.players.keys():
            await self.bot.take_register(ctx)
            return

        if to.id not in self.bot.players.keys():
            await ctx.send(f'ユーザー:{to.mention}はゲームに登録していません。')
            return

        if money > self.bot.players[ctx.author.id] and ctx.author.id != 212513828641046529:
            await ctx.send('指定されたnyan額はあなたの所持金をオーバーしています。')
            return

        if money <= 0:
            await ctx.send('0以下の金額は指定できません。')
            return

        if ctx.author.id != 212513828641046529:
            self.bot.players[ctx.author.id] -= money
        self.bot.players[to.id] += money
        await ctx.send(f'{to.mention}さんに{money}nyanを送りました。')

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
