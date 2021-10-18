import aiohttp

from vk_api.bot_longpoll import VkBotLongPoll


class AIOLongpoll(VkBotLongPoll):
    def __init__(self, vk, group_id):
        super().__init__(vk, group_id)
        self.async_session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(self.wait + 10))

    async def check(self):
        values = {
            'act': 'a_check',
            'key': self.key,
            'ts': self.ts,
            'wait': self.wait,
        }

        request = self.url + '?'
        for key in values:
            request += f'{key}={values[key]}&'

        response = await self.async_session.get(request)
        response = await response.json()

        if 'failed' not in response:
            self.ts = response['ts']
            return [
                self._parse_event(raw_event)
                for raw_event in response['updates']
            ]

        elif response['failed'] == 1:
            self.ts = response['ts']

        elif response['failed'] == 2:
            self.update_longpoll_server(update_ts=False)

        elif response['failed'] == 3:
            self.update_longpoll_server()

        return []

    async def shutdown(self):
        await self.async_session.close()
