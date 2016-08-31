
import redis
import math
import multiprocessing
import time


SERIAL_CHECK_CUTOFF = 21
CHECK_EVERY = 1000

FLAG_NAME = b'redis_primes_flag'
FLAG_CLEAR = b'0'
FLAG_SET = b'1'


rds = redis.StrictRedis()


def check_prime_in_range(job):
    # job[0] = number
    # job[1] = tuple (from, to)

    if job[0] % 2 == 0:
        return False

    assert job[1][0] != 0

    check_every = CHECK_EVERY

    for i in range(job[1][0], job[1][1], 2):

        check_every -= 1
        if not check_every:

            flag = rds[FLAG_NAME]
            if flag == FLAG_SET:
                return False

            check_every = CHECK_EVERY

        if job[0] % i == 0:
            rds[FLAG_NAME] = FLAG_SET
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


def check_prime(num, pool, proc_count):
    from_num = 3

    # serial check cutoff
    to_num = SERIAL_CHECK_CUTOFF
    rds[FLAG_NAME] = FLAG_CLEAR

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
    PROC_COUNT = 4

    pool = multiprocessing.Pool(PROC_COUNT)
    big_prime = 100109100129100151

    t1 = time.time()
    c1 = check_prime(big_prime, pool, PROC_COUNT)
    d1 = time.time() - t1

    print c1, d1


if __name__ == '__main__':
    main()
