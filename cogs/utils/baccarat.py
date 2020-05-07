from cogs.utils.tramp import Deck
import discord
import asyncio


class Baccarat:
    def __init__(self, bot, ctx, data):
        self.bot = bot
        self.ctx = ctx
        self.send = ctx.send
        self.parent = ctx.author
        self.data = data

        self.deck = Deck()
        self.deck.shuffle()

        self.player_cards = []
        self.banker_cards = []
        self.player_count = 0
        self.banker_count = 0

    async def start(self):
        await self.send('ゲームを開始します...\nまず、参加者の掛け金を確認します。')
        await asyncio.sleep(2)
        embed = discord.Embed(title='参加者一覧')
        banker_users = [f'{key.mention} : {value[1]}nyan' for key, value in self.data['users'].items() if value[0] == 'BANKER']
        player_users = [f'{key.mention} : {value[1]}nyan' for key, value in self.data['users'].items() if value[0] == 'PLAYER']
        embed.add_field(name='BANKER', value='\n'.join(banker_users))
        embed.add_field(name='PLAYER', value='\n'.join(player_users))
        await self.send(embed=embed)
        await asyncio.sleep(2)
        await self.send('ゲームを開始します！まず、BANKER PLAYER両方とも2枚のカードを引きます。')
        self.banker_cards.append(self.deck.draw())
        self.banker_cards.append(self.deck.draw())
        self.player_cards.append(self.deck.draw())
        self.player_cards.append(self.deck.draw())
        await asyncio.sleep(1)
        await self.send('では、結果を見てみましょう。5秒後に表示されます...')
        await asyncio.sleep(5)

