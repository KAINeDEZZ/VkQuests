import asyncio

import tortoise
import aerich

from vk_core.bot import VkBot
import settings


class Core:
    def __init__(self):
        self.bot = VkBot(settings.TOKEN, settings.GROUP_ID, settings.DIALOGS)
        self.loop = asyncio.get_event_loop()

    async def startup(self):
        await self.init_db()
        await self.loop.create_task(self.bot.main_handler())

    @staticmethod
    async def init_db():
        command = aerich.Command(settings.TORTOISE_ORM, app='core')
        await command.init()
        await command.upgrade()

        await tortoise.Tortoise.init(settings.TORTOISE_ORM)

    def run(self):
        tasks = asyncio.wait([self.startup()])

        self.loop.run_until_complete(tasks)
        self.loop.close()


if __name__ == '__main__':
    core = Core()
    core.run()
