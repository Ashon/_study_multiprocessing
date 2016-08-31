
import multiprocessing
import threading
import time

from use_ipc import FLAG_ALL_DONE
from use_ipc import FLAG_WORKER_FINISHED_PROCESSING
from use_ipc import check_prime_worker


# function for feed new jobs asynchronously
def feed_new_jobs(number_range, possible_primes_queue, nbr_poison_pills):
    for possible_prime in number_range:
        possible_primes_queue.put(possible_prime)

    # add poison pills to stop the remote workers
    for n in range(nbr_poison_pills):
        possible_primes_queue.put(FLAG_ALL_DONE)


def main():
    primes = []

    NBR_PROCESSES = 4

    manager = multiprocessing.Manager()

    possible_primes_queue = manager.Queue()
    definite_primes_queue = manager.Queue()

    number_range = range(100000000, 101000000)

    # process pool
    multiprocessing.Pool(NBR_PROCESSES)

    processes = []

    for _ in range(NBR_PROCESSES):

        p = multiprocessing.Process(
            target=check_prime_worker,
            args=(possible_primes_queue, definite_primes_queue))

        processes.append(p)
        p.start()

    t1 = time.time()

    thread = threading.Thread(
        target=feed_new_jobs,
        args=(number_range, possible_primes_queue, NBR_PROCESSES))

    thread.start()


    processors_indicating_they_have_finished = 0

    while True:

        # block while waiting for results
        new_result = definite_primes_queue.get()

        if new_result == FLAG_WORKER_FINISHED_PROCESSING:
            processors_indicating_they_have_finished += 1
            if processors_indicating_they_have_finished == NBR_PROCESSES:
                break
        else:
            primes.append(new_result)

    # check all worker is killed
    assert processors_indicating_they_have_finished == NBR_PROCESSES

    print("Took:", time.time() - t1)
    print(len(primes), primes[:10], primes[-10:])


if __name__ == '__main__':
    main()