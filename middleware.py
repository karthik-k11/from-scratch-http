import time
from logger import log_info


class MiddlewareManager:

    def __init__(self):
        self.middlewares = []

    def add(self, middleware_func):
        self.middlewares.append(middleware_func)

    def run_before(self, request):
        for m in self.middlewares:
            m(request)


##Example middleware
def logging_middleware(request):
   log_info(f"[MIDDLEWARE] {request.method} {request.path}")


def timing_middleware(request):
    request.start_time = time.time()