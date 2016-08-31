import math
import time
import multiprocessing


def is_prime(num):

    if num % 2 == 0:
        return False

    for i in xrange(3, int(math.sqrt(num)) + 1, 2):
        if num % i == 0:
            return False

    return True


def check_prime_in_range(job):
    # job[0] = number
    # job[1] = tuple (from, to)
    if job[0] % 2 == 0:
        return False

    assert job[1][0] != 0

    for i in range(job[1][0], job[1][1], 2):
        if job[0] % i == 0:
            return False

    return True


def get_num_ranges_per_proc(from_num, to_num, proc_count):

    range_per_proc = (to_num - from_num) / proc_count

    return [
        (
            int(from_num + (range_per_proc * proc_idx)),
            int(from_num + (range_per_proc * (proc_idx + 1)))
        ) for proc_idx in range(proc_count)
    ]


def is_prime_with_pool(num, pool, proc_count):
    from_num = 3
    to_num = int(math.sqrt(num)) + 1

    ranges = get_num_ranges_per_proc(from_num, to_num, proc_count)
    ranges = zip(len(ranges) * [num], ranges)

    assert len(ranges) == proc_count

    results = pool.map(check_prime_in_range, ranges)

    if False in results:
        return False

    return True


def check_prime(num, pool, proc_count):
    from_num = 3

    # serial check cutoff
    to_num = 21

    if not check_prime_in_range((num, (from_num, to_num))):
        return False

    from_num = to_num
    to_num = int(math.sqrt(num)) + 1

    ranges = get_num_ranges_per_proc(from_num, to_num, proc_count)
    ranges = zip(len(ranges) * [num], ranges)

    assert len(ranges) == proc_count

    results = pool.map(check_prime_in_range, ranges)

    if False in results:
        return False

    return True


def main():

    proc_count = 4
    pool = multiprocessing.Pool(proc_count)

    small_prime = 17
    big_prime = 100109100129100151

    # Serial Solution - big prime
    t1 = time.time()
    c1 = is_prime_with_pool(big_prime, pool, proc_count)
    d1 = time.time() - t1

    # Naive Pool Solution - big prime
    t2 = time.time()
    c2 = is_prime(big_prime)
    d2 = time.time() - t2

    # Serial Solution - small prime
    t3 = time.time()
    c3 = is_prime_with_pool(small_prime, pool, proc_count)
    d3 = time.time() - t3

    # Naive Pool Solution - small prime
    t4 = time.time()
    c4 = is_prime(small_prime)
    d4 = time.time() - t4

    # Less Naive Pool Solution - big prime
    t5 = time.time()
    c5 = check_prime(big_prime, pool, proc_count)
    d5 = time.time() - t5

    t6 = time.time()
    c6 = check_prime(small_prime, pool, proc_count)
    d6 = time.time() - t6

    # print(c1, c2)
    # print(d1, d2)

    print "check big prime"
    print c1, c2
    print d1, d2, d1 < d2

    print "check small prime"
    print c3, c4
    print d3, d4, d3 < d4

    print "less naive pool"
    print c5, c6
    print d5, d6


if __name__ == '__main__':
    main()
