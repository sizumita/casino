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

        self.is_player_card_tree = False
        self.is_banker_card_tree = False

    def calc(self, cards):
        num = 0
        for x in cards:
            num += x.rank if x.rank < 10 else 0
        if num >= 10:
            num = int(str(num)[-1])
        return num

    async def start(self):
        await self.send('ゲームを開始します...\nまず、参加者の掛け金を確認します。')
        await asyncio.sleep(2)
        embed = discord.Embed(title='参加者一覧')
        banker_users = [f'{key.mention} : {value[1]}nyan' for key, value in self.data['users'].items() if value[0] == 'BANKER']
        player_users = [f'{key.mention} : {value[1]}nyan' for key, value in self.data['users'].items() if value[0] == 'PLAYER']
        tie_users = [f'{key.mention} : {value[1]}nyan' for key, value in self.data['users'].items() if value[0] == 'TIE']
        if not banker_users:
            banker_users = ['なし']
        if not player_users:
            player_users = ['なし']
        if not tie_users:
            tie_users = ['なし']
        embed.add_field(name='BANKER', value='\n'.join(banker_users), inline=False)
        embed.add_field(name='PLAYER', value='\n'.join(player_users), inline=False)
        embed.add_field(name='TIE', value='\n'.join(tie_users), inline=False)
        await self.send(embed=embed)
        await asyncio.sleep(5)
        await self.send('ゲームを開始します！まず、BANKER PLAYER両方とも2枚のカードを引きます。')
        for x in range(2):
            card = self.deck.draw()
            num = card.rank
            if card.rank >= 10:
                num = 0
            self.player_cards.append(card)
            self.player_count += num

            card = self.deck.draw()
            num = card.rank
            if card.rank >= 10:
                num = 0
            self.banker_cards.append(card)
            self.banker_count += num

        if self.banker_count >= 10:
            self.banker_count = int(str(self.banker_count)[-1])
        if self.player_count >= 10:
            self.banker_count = int(str(self.player_count)[-1])
        await asyncio.sleep(3)
        await self.send('では、結果を見てみましょう。5秒後に表示されます...')
        await asyncio.sleep(5)
        banker_card_text = ''.join(f'<:{card.name}:{card.emoji_id()}>' for card in self.banker_cards)
        player_card_text = ''.join(f'<:{card.name}:{card.emoji_id()}>' for card in self.player_cards)
        embed = discord.Embed(title='結果！')
        embed.add_field(name='BANKER', value=banker_card_text, inline=False)
        embed.add_field(name='PLAYER', value=player_card_text, inline=False)
        embed.add_field(name='結果', value=f'BANKER: {self.banker_count}\nPLAYER: {self.player_count}\n', inline=False)
        await self.send(embed=embed)
        if self.banker_count >= 8 or self.player_count >= 8:
            winner = 'TIE'
            if self.banker_count > self.player_count:
                winner = 'BANKER'
            elif self.banker_count < self.player_count:
                winner = 'PLAYER'

            if winner is 'TIE':
                await self.send('両者同じ数字により、タイ(引き分け)!\nタイに掛けた方の報酬が2倍になります。')

            if winner == 'BANKER':
                await self.send('BANKERの勝ち!\nBANKERに掛けた方の報酬が2倍になります。ただし、配当の5%が徴収されます。')

            if winner == 'PLAYER':
                await self.send('PLAYERの勝ち!\nPLAYERに掛けた方の報酬が2倍になります。')

            return winner

        await self.send('どちらも8,9ではないため、3枚目の動作に移ります。')
        await asyncio.sleep(4)
        await self.send('まず、PLAYERから動作を開始します。')
        await asyncio.sleep(4)
        await self.player_three()
        await asyncio.sleep(4)
        await self.send('次に、BANKERが動作します。')
        await asyncio.sleep(4)
        await self.banker_three()
        await asyncio.sleep(4)
        await self.send('最終結果発表！')
        
        winner = 'TIE'
        if self.banker_count > self.player_count:
            winner = 'BANKER'
        elif self.banker_count < self.player_count:
            winner = 'PLAYER'
        
        if winner is 'TIE':
            await self.send('両者同じ数字により、タイ(引き分け)!\nタイに掛けた方の報酬が2倍になります。')

        if winner == 'BANKER':
            await self.send('BANKERの勝ち!\nBANKERに掛けた方の報酬が2倍になります。ただし、配当の5%が徴収されます。')

        if winner == 'PLAYER':
            await self.send('PLAYERの勝ち!\nPLAYERに掛けた方の報酬が2倍になります。')

        return winner

    async def player_three(self):
        if self.player_count <= 5:
            await self.send('PLAYERの合計が5以下であるので、3枚目を引きます。')
            card = self.deck.draw()
            num = card.rank
            if card.rank >= 10:
                num = 0
            self.player_cards.append(card)
            self.player_count += num
            if self.player_count >= 10:
                self.banker_count = int(str(self.player_count)[-1])
            player_card_text = ''.join(f'<:{card.name}:{card.emoji_id}>' for card in self.player_cards)
            embed = discord.Embed(title='結果')
            embed.add_field(name='PLAYER', value=player_card_text, inline=False)
            embed.add_field(name='結果', value=f'PLAYER: {self.player_count}\n', inline=False)
            await self.send(embed=embed)
            self.is_player_card_tree = True
            return
        else:
            await self.send('PLAYERはカードを引きません。')
            return

    async def banker_three(self):
        if self.banker_count <= 2:
            await self.send('BANKERの合計が2以下であるので、3枚目を引きます。')
            await self.banker_draw()
            return
        
        if self.banker_count == 3:
            if not self.is_player_card_tree and self.player_count in [6, 7]:
                await self.send('BANKERはカードを引きます。')
                await self.banker_draw()
                return
            if self.is_player_card_tree and self.player_cards[-1].rank != 8:
                await self.send('BANKERはカードを引きます。')
                await self.banker_draw()
                return
            if self.is_player_card_tree and self.player_cards[-1].rank == 8:
                await self.send('BANKERはカードを引きません。')
                return
            await self.send('BANKERはカードを引きます。')
            await self.banker_draw()
            return
        
        if self.banker_count == 4:
            if not self.is_player_card_tree and self.player_count in [6, 7]:
                await self.send('BANKERはカードを引きます。')
                await self.banker_draw()
                return
            if self.is_player_card_tree and self.player_cards[-1].rank not in [0, 1, 8, 9]:
                await self.send('BANKERはカードを引きます。')
                await self.banker_draw()
                return
            if self.is_player_card_tree and self.player_cards[-1].rank in [0, 1, 8, 9]:
                await self.send('BANKERはカードを引きません。')
                return
            await self.send('BANKERはカードを引きます。')
            await self.banker_draw()
            return
        
        if self.banker_count == 5:
            if not self.is_player_card_tree and self.player_count in [6, 7]:
                await self.send('BANKERはカードを引きます。')
                await self.banker_draw()
                return
            if self.is_player_card_tree and self.player_cards[-1].rank not in [4, 5, 6, 7]:
                await self.send('BANKERはカードを引きます。')
                await self.banker_draw()
                return
            if self.is_player_card_tree and self.player_cards[-1].rank in [4, 5, 6, 7]:
                await self.send('BANKERはカードを引きません。')
                return
            await self.send('BANKERはカードを引きます。')
            await self.banker_draw()
            return

        if self.banker_count == 6:
            if not self.is_player_card_tree and self.player_count in [6, 7]:
                await self.send('BANKERはカードを引きます。')
                await self.banker_draw()
                return
            if self.is_player_card_tree and self.player_cards[-1].rank not in [6, 7]:
                await self.send('BANKERはカードを引きます。')
                await self.banker_draw()
                return
            if self.is_player_card_tree and self.player_cards[-1].rank in [6, 7]:
                await self.send('BANKERはカードを引きません。')
                return
            await self.send('BANKERはカードを引きます。')
            await self.banker_draw()
            return
        await self.send('BANKERはカードを引きません。')
        return

    async def banker_draw(self):
        card = self.deck.draw()
        num = card.rank
        if card.rank >= 10:
            num = 0
        self.banker_cards.append(card)
        self.banker_count += num
        if self.banker_count >= 10:
            self.banker_count = int(str(self.player_count)[-1])
        banker_card_text = ''.join(f'<:{card.name}:{card.emoji_id}>' for card in self.banker_cards)
        embed = discord.Embed(title='結果')
        embed.add_field(name='BANKER', value=banker_card_text, inline=False)
        embed.add_field(name='結果', value=f'BANKER: {self.banker_count}\n', inline=False)
        await self.send(embed=embed)
        return

