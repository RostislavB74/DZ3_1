import collections
import itertools
import logging
from multiprocessing import Process, RLock as PoolLock, Pool
from threading import Thread, RLock as TRlock
from time import time


def calc_product(iterable):
    acc = 1
    for i in iterable:
        acc *= i
    return acc


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("factorize1")
logger = logging.getLogger("factorize")


def factorize(n, filename, lock):

    divisors = [i for i in range(1, n + 1) if n % i == 0]
    logger.info(f"{n} == {divisors}")
    with lock:
        with open(filename, "a") as f:
            f.write(f"{n} == {divisors}\n")


def factorize1(n):
    divisors = [i for i in range(1, n + 1) if n % i == 0]
    logger.info(f"{n} == {divisors}")


def synchronous_version(numbers):
    th_filename = "th_factorize.txt"
    th_lock = TRlock()
    threads = []
    for num in numbers:
        thread = Thread(target=factorize, args=(num, th_filename, th_lock))
        threads.append(thread)

    timer = time()
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
    elapsed_time = round(time() - timer, 4)  # Обчислюємо час, що пройшов
    done_threads = [
        num + 1 for num in numbers if not thread.is_alive()
    ]  # Знаходимо завершені потоки
    print(f"Done by {len(done_threads)} threads: {elapsed_time} seconds")


def get_all_divisors(n):
    primes = factorize1(n)
    primes_counted = collections.Counter(primes)
    divisors_exponentiated = [
        [div ** i for i in range(count + 1)]
        for div, count in primes_counted.items()
    ]
    for prime_exp_combination in itertools.product(*divisors_exponentiated):
        yield calc_product(prime_exp_combination)


if __name__ == "__main__":

    numbers = [128, 255, 99999, 10651060]
    # Синхронна версія, треди
    synchronous_version(numbers)

    # Процеси
    # processs_version(numbers)

    # 1 процес
    # one_process_version(numbers)

    # Пул - треди в оболонці процесів
    # pool_version(numbers)

    print(list(get_all_divisors(128)))  # 8!
    print(list(get_all_divisors(255)))
    print(list(get_all_divisors(99999)))
    print(list(get_all_divisors(106511060)))
