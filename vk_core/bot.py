import vk_api
from vk_api.bot_longpoll import VkBotEventType

from database import User, StageEnd
from .log import log
from .vk_aiolongpol import AIOLongpoll


class VkBot:
    def __init__(self, token, group_id, dialogs):
        self.vk = vk_api.VkApi(token=token)
        self.api = self.vk.get_api()

        self.longpoll = AIOLongpoll(self.vk, group_id)
        self.dialogs = dialogs

    async def main_handler(self):
        while True:
            try:
                for event in await self.longpoll.check():
                    if event.type == VkBotEventType.MESSAGE_NEW and event.message and event.message['text'][0] == '/':
                        user = await self.load_user(event.message['peer_id'])
                        await self.handle_command(user, event.message['text'][1:])

            except Exception as ex:
                log('main_handler', ex)

    async def load_user(self, user_id):
        user = await User.filter(id=user_id)

        if user:
            user = user[0]
        else:
            user = await User.create(id=user_id)

        return user

    async def handle_command(self, user, message):
        stage = self.dialogs[user.stage] if len(self.dialogs) > user.stage + 1 else\
            {'keys': [message], 'answer': {'message': 'Вы уже прошли квест'}}

        if message not in stage['keys']:
            self.api.messages.send(peer_id=user.id, random_id=0, message='Неверная команда')
            return

        await StageEnd.create(stage=user.stage, user=user)
        user.stage += 1
        await user.save()

        if user.stage == len(self.dialogs):
            await self.last_stage(user)
        else:
            self.api.messages.send(peer_id=user.id, random_id=0, **stage['answer'])

    async def last_stage(self, user):
        if not await StageEnd.filter(stage=len(self.dialogs)).exists():
            self.api.messages.send(peer_id=user.id, random_id=0, message='\n'.join([
                '1-ым: Поздравляем вы первые завершили наш отбор!',
                'Благодарим вас за участие и вам полагается главный приз.',
                'Приходите за ним. 56.842513, 60.655354',
                '',
                'До новых встреч?)'
            ]))

        else:
            self.api.messages.send(peer_id=user.id, random_id=0, message='\n'.join([
                'Поздравляем, вы завершили наш отбор. Благодарим вас за участие.',
                'Другая команда оказалась быстрее вас, но вам также полагает приз.',
                'Приходите за ним. 56.842513, 60.655354',
                '',
                'До новых встреч?)'
            ]))
