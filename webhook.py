import asyncio

from aiohttp import web

import service


# TODO: service for loading
# TODO: loading client


async def handler(request):
    try:
        data = await request.text()
        await service.send_info(data)
        service.write_log(data)
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
