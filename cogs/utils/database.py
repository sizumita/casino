import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import asyncio
import concurrent.futures

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


collection = db.collection('users')

doc = collection.document('212513828641046529')

doc.set({'money': 10000})


class DB:
    def __init__(self, bot):
        self.bot = bot
        self.db = firestore.client()
        self.collection = db.collection('users')
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)

    async def get(self, user_id):
        user = self.collection.document(str(user_id))
        return await self.bot.loop.run_in_executor(self.executor, user.get)

    async def change_money(self, user_id, money):
        user = self.collection.document(str(user_id))
        await self.bot.loop.run_in_executor(self.executor, user.set, {'money': (await self.get(user_id)) + money})

    async def set_money(self, user_id, money):
        user = self.collection.document(str(user_id))
        await self.bot.loop.run_in_executor(self.executor, user.set, {'money': money})
