import multiprocessing
import logging
from multiprocessing import Process
from threading import Thread
from time import time


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("factorize")


def factorize(n):

    divisors = [i for i in range(1, n + 1) if n % i == 0]
    logger.info(f"{n} == {divisors}")
    return f"{n} == {divisors}\n"


def cpu_process(numbers):
    processes = []
    for num in numbers:
        process = Process(target=factorize, args=(num,))
        processes.append(process)

    timer = time()
    [process.start() for process in processes]
    [process.join() for process in processes]
    [process.close() for process in processes]
    delta_time = round(time() - timer, 4)
    done_process = [num + 1 for num in numbers]
    print(
        f"Process done by {len(done_process)} processes: {delta_time} seconds")
    print(f"cpu_count: {multiprocessing.cpu_count()}")


def synchro(numbers):
    threads = []
    for num in numbers:
        thread = Thread(target=factorize, args=(num, ))
        threads.append(thread)
    timer = time()
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
    delta_time = round(time() - timer, 4)
    done_threads = [
        num + 1 for num in numbers if not thread.is_alive()
    ]
    print(
        f"Synchro method is done by {len(done_threads)} threads: {delta_time} seconds")


if __name__ == "__main__":

    numbers = [128, 255, 99999, 10651060]

    synchro(numbers)
    cpu_process(numbers)
