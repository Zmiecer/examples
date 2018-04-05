import time

from bisect import bisect_left
from multiprocessing.dummy import Pool


class DefaultTimer(object):
    def time(self):
        return time.time()

    def wait(self, duration):
        time.sleep(duration)


class RateLimiter(object):
    def __init__(self, rate_limit, max_workers, timer=DefaultTimer()):
        self.rate_limit = rate_limit
        if self.rate_limit > 1:
            self.tick_time = 1
        else:
            self.tick_time = 1. / rate_limit
            self.rate_limit = 1
        self.max_workers = max_workers
        self.timer = timer

        self.queue = []

    def cut_queue(self):
        tick_bound = bisect_left(self.queue,
                                 self.timer.time() - self.tick_time)
        self.queue = self.queue[tick_bound:]

    def wait_for_tick(self):
        if len(self.queue) >= self.rate_limit:
            wait_time = self.queue[0] + self.tick_time - self.timer.time()
            if wait_time > 0:
                self.timer.wait(wait_time)

    def call(self, task):
        self.cut_queue()
        self.wait_for_tick()
        self.queue.append(self.timer.time())
        result = task()
        return result

    def call_many(self, tasks):
        tasks = [task for task in tasks]
        result_list = [None] * len(tasks)

        def run_task(task_number, task):
            result = task()
            return task_number, result

        def log_result(answer):
            task_number, result = answer
            result_list[task_number] = result

        pool = Pool(self.max_workers)
        for task_number, task in enumerate(tasks):
            self.cut_queue()
            self.wait_for_tick()
            pool.apply_async(run_task, args=(task_number, task),
                             callback=log_result)
            self.queue.append(self.timer.time())
        pool.close()
        pool.join()
        return result_list
