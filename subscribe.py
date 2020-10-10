#!./venv/bin/python
# /Users/nekotopec/dev/vadim_notifier/venv/bin/python
# Subscription task

import asyncio
import json
import logging
import sys

import aiohttp

from config import read_config

API_TOKEN = read_config()['xsi_token']['api_key']
logging.basicConfig(filename='sub_log.txt',
                    filemode='a',
                    format=(u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s'
                            u' [%(asctime)s]  %(message)s'),
                    level=logging.INFO)


async def unsubscribe(session: aiohttp.ClientSession, sub_id: str) -> None:
    headers = {
        'X-MPBX-API-AUTH-TOKEN': API_TOKEN,
    }
    url = ('https://cloudpbx.beeline.ru/apis/portal/subscription?'
           f'subscriptionId={sub_id}')
    async with session.delete(url, headers=headers):
        pass


async def subscribe(session: aiohttp.ClientSession) -> str:
    headers = {
        'X-MPBX-API-AUTH-TOKEN': API_TOKEN,
        'Content-Type': 'application/json'
    }
    data = {"pattern": "9658136992@ip.beeline.ru",
            "expires": 3600,
            "subscriptionType": "BASIC_CALL",
            "url": f"http://{ip}/subscription"}
    url = 'https://cloudpbx.beeline.ru/apis/portal/subscription'
    async with session.put(url=url,
                           headers=headers,
                           data=json.dumps(data)
                           ) as response:
        data = await response.json()
        return data['subscriptionId']


async def check_sub(sub_id, session: aiohttp.ClientSession) -> bool:
    headers = {
        'X-MPBX-API-AUTH-TOKEN': API_TOKEN,
    }
    url = (f'https://cloudpbx.beeline.ru/apis/portal/subscription?'
           f'subscriptionId={sub_id}')
    async with session.get(url, headers=headers) as response:
        data = await response.json()
        error = data.get('errorCode')
        if error is not None:
            if error == 'GetSubscriptionInfoError':
                print(error)
                logging.error('GetSubscriptionInfoError')
                return False
            else:
                logging.error(f'{error} P.S.(БИЛАЙН)')
                return False
        return True


async def task():
    sub_id = None
    while True:
        async with aiohttp.ClientSession() as session:
            if sub_id is not None:
                await unsubscribe(session=session, sub_id=sub_id)
            sub_id = await subscribe(session)
            print(sub_id)
            mark = await check_sub(sub_id, session=session)
            if mark:
                await asyncio.sleep(3400)
            await asyncio.sleep(10)


if __name__ == '__main__':
    ip = sys.argv[1]
    loop = asyncio.get_event_loop()
    task_ = loop.create_task(task())
    future = asyncio.wait([task_])
    loop.run_until_complete(future)
