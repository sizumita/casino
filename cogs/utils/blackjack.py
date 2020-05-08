from cogs.utils.tramp import Deck
import asyncio


class BlackJackGame:
    def __init__(self, bot, ctx, bid):
        self.bot = bot
        self.ctx = ctx
        self.bid = bid
        self.send = ctx.send

        self.deck = Deck()
        self.deck.shuffle()

        self.player_cards = []
        self.bot_cards = []

    def check(self, m):
        return m.author.id == self.ctx.author.id and m.channel.id == self.ctx.channel.id and m.content in ['d', 's', 'h']

    def get_player_sum(self):
        """1はまず11として数えて、それで21を超えていれば1としてカウントします。"""
        sum = 0
        for card in self.player_cards:
            if card.rank == 1:
                sum += 11
                continue
            if card.rank >= 10:
                sum += 10
                continue
            sum += card.rank
        
        if sum <= 21:
            return sum
        
        sum = 0
        for card in self.player_cards:
            if card.rank >= 10:
                sum += 10
                continue
            sum += card.rank

        return sum
    def get_bot_sum(self):
        """1はまず11として数えて、それで21を超えていれば1としてカウントします。"""
        sum = 0
        for card in self.bot_cards:
            if card.rank == 1:
                sum += 11
                continue
            if card.rank >= 10:
                sum += 10
                continue
            sum += card.rank
        
        if sum <= 21:
            return sum
        
        sum = 0
        for card in self.bot_cards:
            if card.rank >= 10:
                sum += 10
                continue
            sum += card.rank

        return sum

    def get_player_card_text(self):
        text = ''
        for card in self.player_cards:
            text += f'<:{card.name}:{card.emoji_id()}>'
        return text

    def get_bot_card_text(self, is_one=False):
        text = ''
        if is_one:
            return f'<:{self.bot_cards[0].name}:{self.bot_cards[0].emoji_id()}>'
        for card in self.bot_cards:
            text += f'<:{card.name}:{card.emoji_id()}>'
        return text

    def is_bot_blackjack(self):
        eleven = False
        over_ten = False
        for card in self.bot_cards:
            if card.rank == 1:
                eleven = True
                continue
            if card.rank >= 10:
                over_ten = True
        return eleven and over_ten

    def is_player_blackjack(self):
        eleven = False
        over_ten = False
        for card in self.player_cards:
            if card.rank == 1:
                eleven = True
                continue
            if card.rank >= 10:
                over_ten = True
        return eleven and over_ten

    async def start(self):
        await self.send('ブラックジャックを開始します。両者カードを引きます。')
        for _ in range(2):
            self.player_cards.append(self.deck.draw())
            self.bot_cards.append(self.deck.draw())
        await asyncio.sleep(5)
        await self.send('あなたのカードを表示します。')
        await self.send(self.get_player_card_text())
        await self.send(f'合計: {self.get_player_sum()}')
        await asyncio.sleep(5)
        await self.send('Botのカードを表示します。')
        await self.send(self.get_bot_card_text(is_one=True))

        if self.is_player_blackjack():
            await self.send('おめでとうございます！！！BlackJackです！賞金は2.5倍になります。')
            return self.bid * 2.5 // 1
        elif self.is_bot_blackjack():
            await self.send('残念ですが、BotがBlackJackになってしまいました...\n')
            return 0
        elif self.is_bot_blackjack() and self.is_player_blackjack():
            await self.send('なんということでしょう、あなたもBotもブラックジャックになりました。引き分けです。')
            return self.bid
        await asyncio.sleep(3)
        await self.send('21になっていないため、ゲームを続けます。')
        await self.draw_card()
        await asyncio.sleep(4)
        if self.get_player_sum() > 21:
            await self.send(f'{self.get_player_sum()}になってしまいました...\nあなたの負けです。')
            return 0
        await self.send('Botがカードを引きます...')
        while self.get_bot_sum() < self.get_player_sum():
            self.bot_cards.append(self.deck.draw())
            await self.send(self.get_bot_card_text())
            await self.send(f'合計: {self.get_bot_sum()}')
            await asyncio.sleep(3)
        await self.send(self.get_bot_card_text())
        await self.send(f'合計: {self.get_bot_sum()}')

        if self.get_bot_sum() > 21:
            await self.send('Botの敗北です...報酬は2倍になります。')
            return self.bid * 2 // 1
        if self.get_bot_sum() == self.get_player_sum():
            await self.send('引き分けです...報酬は1倍です。')
            return self.bid // 1
        if self.get_bot_sum() > self.get_player_sum():
            await self.send('Botの勝利です...報酬はありません。')
            return 0
        await self.send('あなたの勝利です！報酬は2倍になります！')
        return self.bid * 2 // 1

    async def draw_card(self):
        if self.get_player_sum() > 21:
            await self.send('21より大きくなってしまいました...')
            return
        await asyncio.sleep(2)
        if len(self.player_cards) == 2:
            text = 'スタンドしたい場合はs、ダブルしたいときはd、ヒットしたいときはhを入力してください。'
        else:
            text = 'スタンドしたい場合はs、ヒットしたいときはhを入力してください。'
        await self.send(text)
        try:
            message = await self.bot.wait_for('message', check=self.check, timeout=90)
        except asyncio.TimeoutError:
            await self.send('時間切れによりスタンドします...')
            return

        if message.content == 's':
            await self.send('スタンドします...')
            return

        if message.content == 'd' and len(self.player_cards) == 2:
            await self.send('ダブルします...')
            if self.bot.players[self.ctx.author.id] < self.bid:
                await self.send('お金が足りません。')
                await self.draw_card()
            else:
                self.player_cards.append(self.deck.draw())
                await self.send(self.get_player_card_text())
                await self.send(f'合計: {self.get_player_sum()}')
                return        
        if message.content == 'd':
            await self.draw_card()

        await self.send('ヒットします...')
        self.player_cards.append(self.deck.draw())
        await self.send(self.get_player_card_text())
        await self.send(f'合計: {self.get_player_sum()}')
        await self.draw_card()






