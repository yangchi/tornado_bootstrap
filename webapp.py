#!/usr/bin/env python3


import logging
import os
import tornado.ioloop
import tornado.web
import tornado.auth
import tornado.options
import tornado.httpserver
import tornado.gen
from tornado.options import define, options
import base64
import uuid

web_logger = logging.getLogger('realtime')
web_logger.setLevel(logging.DEBUG)
web_logfile = logging.FileHandler('realtime.log')
web_logger.addHandler(web_logfile)

define("port", default=8081, help="run on the given port", type=int)
tornado.options.parse_command_line()


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("index.html")


class LoginHandler(BaseHandler):
    def get(self):
        web_logger.info("LogingHandler:get() func")
        self.cheat()
        self.render("login.html")

    def post(self):
        #handle user input
        web_logger.info("LogingHandler:post() func")
        self.set_secure_cookie("user", self.get_argument("username"))
        self.redirect("/")

    def cheat(self):
        web_logger.info("LogingHandler:cheat() func")
        self.set_secure_cookie("user", "cheating")
        #self.redirect("/")


class MyApp(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/login", LoginHandler),
        ]
        setting = {
            "cookie_secret": base64.b64encode(uuid.uuid4().bytes +
                                              uuid.uuid4().bytes),
            "xsrf_cookies": True,
            "template_path": os.path.join(os.path.dirname(__file__),
                                          "templates"),
            "login_url": "/login",
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
        }
        tornado.web.Application.__init__(self, handlers,
                                         debug=True,
                                         **setting)

if __name__ == '__main__':
    app = MyApp()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
