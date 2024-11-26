import json
import tornado.ioloop
import tornado.websocket
import tornado.web
import threading
import asyncio
import requests
import os

WTD_DELAY = 15

SERVER_URL = "http://pt:8008"


def output(message):
    print(message)


def get_count_from_server(session_key):
    url = SERVER_URL + "/unread_notification/" + session_key + "/"
    output("checking {0}".format(session_key))
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            output("get_count_from_server error {0}".format(response.status_code))
            return {}
    except Exception as err:
        output("get_count_from_server exception {0}".format(err))
        return {}


def wtd_worker(handler, loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(check_counts(handler))


async def check_counts(handler):
    while True:
        if handler.is_open:
            new_data = get_count_from_server(handler.session_key)
            handler.write_message(json.dumps(new_data))
            await asyncio.sleep(WTD_DELAY)
        else:
            output("handler.is_open False")
            break


class BaseHandler(tornado.web.RequestHandler):
    is_open = False
    session_key = ""

    def check_origin(self, origin):
        return True


class WebSocketHandler(BaseHandler, tornado.websocket.WebSocketHandler):
    def allow_draft76(self):
        return True

    def open(self, session_key):
        self.is_open = True
        self.session_key = session_key
        loop = asyncio.new_event_loop()
        p = threading.Thread(target=wtd_worker, args=(self, loop,))
        p.start()

    def on_message(self, message):
        self.write_message(f"Alınan mesaj: {message}")

    def on_close(self):
        self.is_open = False
        output("WebSocket bağlantısı kapandı.")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/ws/([^/]+)/", WebSocketHandler),
        ]
        setting = dict(
            xsrf_cookies=True,
            debug=True,
            content_type="application/json",
        )
        super(Application, self).__init__(handlers, **setting)


if __name__ == "__main__":
    TORNADO_PORT = 1337
    output("Tornado server is running at wss://127.0.0.1:{0}".format(TORNADO_PORT))
    app = Application()
    app.listen(TORNADO_PORT)
    tornado.ioloop.IOLoop.current().start()
