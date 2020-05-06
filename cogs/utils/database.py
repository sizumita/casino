import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import concurrent.futures

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)


class DB:
    def __init__(self, bot):
        self.bot = bot
        self.db = firestore.client()
        self.collection = self.db.collection('users')
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)
        self.documents = {}

    async def get(self, user_id):
        if not self.documents:
            user = self.collection.document(str(user_id))
        else:
            user = self.documents[str(user_id)]
        r = await self.bot.loop.run_in_executor(self.executor, user.get)
        return r.to_dict()

    async def all(self):
        return await self.bot.loop.run_in_executor(self.executor, self.collection.stream)

    async def exists(self, user_id):
        if not self.documents:
            r = await self.get(user_id)
        else:
            r = True if str(user_id) in self.documents.keys else False

        if not r:
            return False

        return True

    async def change_money(self, user_id, money):
        user = self.collection.document(str(user_id))
        await self.bot.loop.run_in_executor(self.executor, user.update, {'money': int((await self.get(user_id))['money'] + money)})

    async def set_money(self, user_id, money):
        user = self.collection.document(str(user_id))
        await self.bot.loop.run_in_executor(self.executor, user.update, {'money': int(money)})
