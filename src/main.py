

# Tornado with rpy2

import subprocess

# added code 1 after having error ""OSError: cannot load library 'C:\Program Files\R\R-4.0.3\bin\x64\R.dll': error 0x7e""
import os
os.environ['R_HOME'] = 'C:\\Program Files\\R\\R-4.0.3'
os.environ["PATH"] += os.pathsep + 'C:\\Program Files\\R\\R-4.0.3\\bin\\x64\\'
os.environ["PATH"] += os.pathsep + 'C:\\Program Files\\R\\R-4.0.3\\'

# code 1

import asyncio
import concurrent.futures
import time

import tornado.web
import tornado.platform

import rpy2.robjects as ro
from rpy2.robjects.packages import importr

# R packages and script
importr('fs')
importr('vroom')
importr('dplyr')
importr('jsonlite')
ro.r.source('testf.R')


# ro.r("""source('testf.R')""")


class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello")


class AsyncHandler(tornado.web.RequestHandler):
    async def get(self):

        project = self.get_argument('project', '')
        data = self.get_argument('data', '')
        name = self.get_argument('name', '')
        description = self.get_argument('description', '')

        # pass args to runScript
        await asyncio.get_running_loop().run_in_executor(self.application.executor, self.runScript, project, data, name,
                                                         description)
        self.finish()

    def runScript(self, project, data, name, description):
        ret_value = ro.r.runnerC(project, data, name, description)  # pass args to R function
        if ret_value == 'success':
            self.write("success")
        else:
            self.write("failed")


def make_app():
    handlers = [(r"/hello", HelloHandler),
                (r"/up", AsyncHandler),
                ]
    app = tornado.web.Application(handlers, debug=True)
    app.executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)
    app.counter = 0
    app.listen(8124)


if __name__ == '__main__':
    make_app()
    tornado.ioloop.IOLoop.current().start()
