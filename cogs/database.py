"""
朝6時に、botのis_running変数をFalseにし、
全ての動作が終わった上でbotのusers変数をdatabaseに入れる
その後botのusers変数を新しく取得した値で上書き。
最後に、is_runningをTrueにして、他のコマンドが動くようにする。
"""
from discord.ext import commands
import asyncio
import datetime


class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.setup())
        bot.loop.create_task(self.loop())
        self.db = self.bot.db

    async def setup(self):
        await self.bot.wait_until_ready()
        for doc in (await self.db.all()):
            self.bot.players[int(doc.id)] = doc.to_dict()['money']

    async def loop(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            now = datetime.datetime.now()
            if now.hour >= 6:
                target = datetime.datetime(now.year, now.month, now.day, 6, 0, 0, 0) + datetime.timedelta(days=1)
            else:
                target = datetime.datetime(now.year, now.month, now.day, 6, 0, 0, 0)
            await asyncio.sleep(target.timestamp() - now.timestamp())

            await self.update_database()

    async def update_database(self):
        self.bot.is_running = False
        while self.bot.game_que:
            await asyncio.sleep(5)
        for user_id, money in self.bot.players.items():
            await self.db.set_money(user_id, money)

        await setup()
        await asyncio.sleep(10)
        self.bot.is_running = True

    @commands.command()
    @commands.is_owner
    async def save(self, ctx):
        await ctx.send('更新開始')
        await self.update_database()
        await ctx.send('更新終了')



def setup(bot):
    return bot.add_cog(Database(bot))
