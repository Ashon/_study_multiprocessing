
import multiprocessing
import math
import time


SERIAL_CHECK_CUTOFF = 21
CHECK_EVERY = 1000
FLAG_CLEAR = b'0'
FLAG_SET = b'1'


def check_prime_in_range(job):
    # job[0] := number
    # job[1] := tuple (from, to)
    # job[2] := flag value

    if job[0] % 2 == 0:
        return False

    assert job[1][0] % 2 != 0

    check_every = CHECK_EVERY

    for i in range(job[1][0], job[1][1], 2):
        check_every -= 1

        if not check_every:
            if job[2].value == FLAG_SET:
                return False

            check_every = CHECK_EVERY

        if job[0] % i == 0:
            job[2].value = FLAG_SET
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


def check_prime(n, pool, proc_count, value):
    from_num = 3
    to_num = SERIAL_CHECK_CUTOFF

    value.value = FLAG_CLEAR

    if not check_prime_in_range((n, (from_num, to_num), value)):
        return False

    from_num = to_num
    to_num = int(math.sqrt(n)) + 1

    ranges = get_num_ranges_per_proc(from_num, to_num, proc_count)
    ranges = zip(len(ranges) * [n], ranges, len(ranges) * [value])

    assert len(ranges) == proc_count

    results = pool.map(check_prime_in_range, ranges)

    if False in results:
        return False

    return True


def main():
    PROC_COUNT = 4

    manager = multiprocessing.Manager()
    value = manager.Value(b'c', FLAG_CLEAR)

    pool = multiprocessing.Pool(PROC_COUNT)
    big_prime = 100109100129100151

    t1 = time.time()
    c1 = check_prime(big_prime, pool, PROC_COUNT, value)
    d1 = time.time() - t1

    print c1, d1


if __name__ == '__main__':
    main()
