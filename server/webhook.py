import asyncio
import functools
from aiohttp import web
import os

print(os.getenv('PYTHONPATH'))

import server.service_notify as service_notify
import server.service_load as service_load
from server.config import read_config

HEADER_TOKEN = read_config()['loader']['token']


# TODO: service for loading
# TODO: loading client

def check_header(func):
    @functools.wraps(func)
    async def wrapped(request: web.Request, *args, **kwargs):
        """Check token in headers."""

        headers = request.headers
        if HEADER_TOKEN == headers.get('TOKEN'):
            response = await func(request, *args, **kwargs)
            return response
        else:
            return web.json_response(
                {'success': False,
                 'reason': 'Bad Token.'}
            )

    return wrapped


@check_header
async def load_ad(request: web.Request):
    """Loader view."""

    data = await request.json()
    try:
        success = service_load.load_to_database(data)
        resp_data = {'success': success}

        if not success:
            resp_data['reason'] = 'Database Error.'
    except service_load.BadParamsError:
        return web.json_response(
            {'success': False,
             'reason': 'Bad params.'},
            status=400
        )

    return web.json_response(resp_data)


@check_header
async def delete_ad(request):
    data = await request.json()
    try:
        success = service_load.delete_ad(data)
        resp_data = {'success': success}
        status = 200
        if not success:
            resp_data['reason'] = 'Database Error.'
            status = 500
    except service_load.BadParamsError:
        return web.json_response(
            {'success': False,
             'reason': 'Bad params.'},
            status=400
        )

    return web.json_response(resp_data, status=status)


async def handler(request):
    """Webhook handler for interacting with API."""

    try:
        data = await request.text()
        await service_notify.send_info(data)
        service_notify.write_log(data)
    except:
        pass
    print('Got request')
    return web.Response(status=200)


async def subscription(request: web.Request):
    return await handler(request)


async def init_app():
    app = web.Application(middlewares=[])
    app.router.add_post('/subscription', handler, name='handler')
    app.router.add_post('/subscription/null', subscription, name='subscription')
    app.router.add_post('/ad', load_ad, name='load')
    app.router.add_delete('/ad', delete_ad, name='delete_ad')
    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        app = loop.run_until_complete(init_app())
        web.run_app(app, host='0.0.0.0', port=8080)
    except Exception as e:
        print('Error create server: %r' % e)
    finally:
        pass
    loop.close()
