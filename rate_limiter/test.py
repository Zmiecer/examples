import time


class DefaultTimer(object):
    def time(self):
        return time.time()

    def wait(self, duration):
        time.sleep(duration)


from rate_limiter import RateLimiter

limiter = RateLimiter(2, 2, timer=DefaultTimer())


def hello():
    time.sleep(2)           # Вот тут менял значение на sleep и смотрел результаты
    print("Hello!")
    return "kek"


def test_call():
    start = time.time()
    for _ in range(6):
        print(limiter.call(hello))
    print("Elapsed %.2f seconds" % (time.time() - start))

# Суть в том, что call(), как я понял, должен отрабатывать последовательно
# Например, прее sleep_time=2, range=6 должно отработать за 12 секунд
# Как я понял, условно call() - это call_many() с max_workers=1
test_call()


def test_call_many():
    start = time.time()
    for _ in limiter.call_many(hello for _ in range(6)):
        pass
    print("Elapsed %.2f seconds" % (time.time() - start))

# А call_many() параллельно
# Например, при sleep_time=2, range=6 должно отработать за 6 секунд
# test_call_many()
