from discord.ext import commands
import asyncio


class Baccarat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = []
        self.bills = {}

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
        
        if ctx.channel.id in self.games:
            await ctx.send('このチャンネルではすでに開始されています。')
            return

        if ctx.author.id in self.bot.game_que:
            await ctx.send('あなたはすでにゲームを開始/参加しています。')
            return

        self.games.append(ctx.channel.id)
        self.bills[ctx.channel.id] = {'users': {}, 'parent': ctx.author}
        await ctx.send('バカラを開始します。ユーザーを募集します。参加したい人はこのチャンネルにて、`c.bjoin <bid金額>`と入力してください。\n' \
            '親は、募集完了した時に`c.bstart`と入力してください。(親も参加登録する必要があります。)')
    
    @commands.command()
    async def bjoin(self, ctx, bid: int):
        if bid > self.bot.players[ctx.author.id]:
            await ctx.send('指定された金額はあなたの所持金をオーバーしています。')
            return
        if ctx.author.id in self.bot.game_que:
            await ctx.send('あなたはすでにゲームを開始しています。')
            return

        if bid <= 0:
            await ctx.send('0以下の金額は指定できません。')
            return
        
        if ctx.channel.id not in self.bills.keys():
            await ctx.send('このチャンネルではゲームは開始されていません。')
            return

        self.bot.game_que.append(ctx.author.id)
        self.bills[ctx.channel.id]['users'][ctx.author] = bid
        self.bot.players[ctx.author.id] -= bid
        await ctx.send('参加完了しました！')

    @commands.command()
    async def bstart(self, ctx):
        if ctx.channel.id not in self.games:
            await ctx.send('このチャンネルでは開始されていません。')
            return
        
        if self.bills[ctx.channel.id]['parent'].id != ctx.author.id:
            await ctx.send('あなたは親ではありません。')
            return

        await ctx.send('参加締め切りました。')
        await asyncio.sleep(2)

