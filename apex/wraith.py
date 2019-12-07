import aiohttp
import asyncio

class Wraith:

    def __init__(self, bot):
        self.url = "https://public-api.tracker.gg/apex/v1/standard/profile/"
        self._session = aiohttp.ClientSession()
        self.api = None
        self.bot = bot

    async def __unload(self):
        self._session.detach()

    async def _get_api_key(self):
        if not self.api:
            api = await self.bot.get_shared_api_tokens('apex')
            self.api = api.get('key')
            return self.api
        else:
            return self.api

    async def api_key(self):
        if not self.api:
            return await self._get_api_key()
        else:
            return self.api

    
    async def get(self, url):
        async with self._session.get(url, headers={"TRN-Api-Key": await self.api_key()}) as response:
            return await response.json()

    async def get_infos(self, platform, username):
        platform = platform.replace("pc", "5")
        platform = platform.replace("xbox", "2")
        req = await self.get(self.url + platform + "/" + username)
        res = []
        for i in req['data']['children']:
            tmp = {}
            charinfo = i['metadata']
            tmp['legend'] = charinfo['legend_name']
            tmp['icon_url'] = charinfo['icon']
            stats = []
            for j in i['stats']:
                infos = j['metadata']
                stats.append({'name': infos['key'], 'value': j['displayValue']})
            tmp['stats'] = stats
            res.append(tmp)
        return res
