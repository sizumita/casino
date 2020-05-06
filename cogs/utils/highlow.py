from cogs.utils.tramp import Deck
import discord
import asyncio
magnifications = {
    1: [0, 1.1],
    2: [2.2, 1.2],
    3: [2.1, 1.3],
    4: [2.0, 1.4],
    5: [1.9, 1.5],
    6: [1.8, 1.6],
    7: [1.7, 1.7],
    8: [1.6, 1.8],
    9: [1.5, 1.9],
    10: [1.4, 2.0],
    11: [1.3, 2.1],
    12: [1.2, 2.2],
    13: [1.1, 0]
}


class HighAndLow:
    def __init__(self, bot, ctx, bid):
        self.bot = bot
        self.ctx = ctx
        self.deck = Deck()
        self.bid = bid

    def check(self, m):
        return m.author.id == self.ctx.author.id and m.channel.id == self.ctx.channel.id and m.content in ['h', 'l', 'e']

    async def play(self) -> int:
        self.deck.shuffle()
        embed = discord.Embed()
        while not self.bot.is_closed():
            card = self.deck.draw()
            embed = discord.Embed(title='High And Law', 
            description='次に出るカードが表示されたカードよりも大きいと思った場合は**h**、\n' \
                        '小さいと思った場合は**l**、\n' \
                        '終了したい場合はeと打ち込んでください。')
            embed.add_field(name='Highを選んだときの倍率', value=f'{magnifications[card.rank][1]}倍')
            embed.add_field(name='Lowを選んだときの倍率', value=f'{magnifications[card.rank][0]}倍')
            embed.add_field(name='現在の掛け金', value=f'{self.bid}nyan')
            file = discord.File(card.path(), filename="image.png")
            embed.set_image(url="attachment://image.png")
            await self.ctx.send(embed=embed)
            try:
                message = await self.bot.wait_for('message', check=self.check, timeout=60)
            except asyncio.TimeoutError:
                await self.ctx.send('60秒間入力がなかったため、ゲームを終了しました。現在の金額を返却します。')
                return self.bid

            if message.content == 'e':
                await self.ctx.send(f'ゲームを終了します。最終金額: {self.bid}nyan')
                return self.bid
            
            next = self.deck.next()

            if (card.rank == 0 and message.content == 'l') or (card.rank == 13 and message.content == 'h'):
                embed = discord.Embed(title='エラー', description='それは選べませんね...次のカードから再スタートします。')
                file = discord.File(next.path(), filename="image.png")
                embed.set_image(url="attachment://image.png")

                await self.ctx.send(embed=embed)
                await asyncio.sleep(2)
                continue

            if next.rank == card.rank:
                embed = discord.Embed(title='引き分け！', description='次のカードは同じ数字だったようです...\n2秒後に次のゲームへ移行します...')
                file = discord.File(next.path(), filename="image.png")
                embed.set_image(url="attachment://image.png")

                await self.ctx.send(embed=embed)
                await asyncio.sleep(2)
                continue

            if message.content == 'h':
                if next.rank > card.rank:
                    embed = discord.Embed(title='勝ち！', description='おめでとうございます！あなたは見事引き当てました！\n2秒後に次のゲームへ移行します...')
                    self.bid = self.bid * magnifications[card.rank][1] // 1
                    embed.add_field(name='結果', value=f'掛け金は{magnifications[card.rank][1]}倍の {self.bid}nyanになりました！')
                    file = discord.File(next.path(), filename="image.png")
                    embed.set_image(url="attachment://image.png")

                    await self.ctx.send(embed=embed)
                    await asyncio.sleep(2)
                    continue
                else:
                    return await self.lose()
            
            else:
                if next.rank < card.rank:
                    embed = discord.Embed(title='勝ち！', description='おめでとうございます！あなたは見事引き当てました！\n2秒後に次のゲームへ移行します...')
                    self.bid = self.bid * magnifications[card.rank][0] // 1
                    embed.add_field(name='結果', value=f'掛け金は{magnifications[card.rank][0]}倍の {self.bid}nyanになりました！')
                    file = discord.File(next.path(), filename="image.png")
                    embed.set_image(url="attachment://image.png")

                    await self.ctx.send(embed=embed)
                    await asyncio.sleep(2)
                    continue
                else:
                    return await self.lose()

    async def lose(self, next):
        embed = discord.Embed(title='負け...', description='あなたは外しました...掛け金を全て失います。')
        file = discord.File(next.path(), filename="image.png")
        embed.set_image(url="attachment://image.png")

        await self.ctx.send(embed=embed)
        await asyncio.sleep(2)
        return 0
