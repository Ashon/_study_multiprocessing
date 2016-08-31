import math
import multiprocessing
import time


FLAG_ALL_DONE = b"WORK_FINISHED"
FLAG_WORKER_FINISHED_PROCESSING = b"WORKER_FINISHED_PROCESSING"


# check prime function
def is_prime(num):

    if num % 2 == 0:
        return False

    for i in range(3, int(math.sqrt(num)) + 1, 2):
        if num % i == 0:
            return False

    return True


# define worker
def check_prime_worker(possible_primes_queue, definite_primes_queue):
    # print("start worker")
    # worker_id = int(random.random() * 10000)

    while True:

        # get recent message(or number) from queue
        n = possible_primes_queue.get()

        # print("worker-%s: %s" % (worker_id, n))

        # if all finished stop this worker
        if n == FLAG_ALL_DONE:
            definite_primes_queue.put(FLAG_WORKER_FINISHED_PROCESSING)
            # print("quit worker")
            break

        # else, find prime then put to queue.
        else:
            if is_prime(n):
                definite_primes_queue.put(n)


def main():

    primes = []

    NBR_PROCESSES = 4

    manager = multiprocessing.Manager()

    possible_primes_queue = manager.Queue()
    definite_primes_queue = manager.Queue()

    # process pool
    pool = multiprocessing.Pool(NBR_PROCESSES)
    processes = []

    for _ in range(NBR_PROCESSES):

        p = multiprocessing.Process(
            target=check_prime_worker,
            args=(possible_primes_queue, definite_primes_queue)
        )

        processes.append(p)
        p.start()

    t1 = time.time()

    number_range = range(100000000, 101000000)
    # initialize possible prime queue
    for possible_prime in number_range:
        possible_primes_queue.put(possible_prime)

    # add poison pills to stop the remote workers
    for n in range(NBR_PROCESSES):
        possible_primes_queue.put(FLAG_ALL_DONE)

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

    print "Took:", time.time() - t1
    print len(primes), primes[:10], primes[-10:]


if __name__ == '__main__':
    main()
