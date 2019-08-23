def main():
    """Test script"""
    import numpy as np
    from bcipy.acquisition.record import Record
    import timeit

    n_rows = 1000
    channel_count = 25
    channels = ["ch" + str(c) for c in range(channel_count)]

    pid1 = start(channels, 'buffer1.db')
    pid2 = start(channels, 'buffer2.db')

    starttime = timeit.default_timer()
    for i in range(n_rows):
        data = [np.random.uniform(-1000, 1000) for _ in range(channel_count)]
        if i % 2 == 0:
            append(pid1, Record(data, i, None))
        else:
            append(pid2, Record(data, i, None))

    endtime = timeit.default_timer()
    totaltime = endtime - starttime

    print("Records inserted in buffer 1: {}".format(count(pid1)))
    print("Records inserted in buffer 2: {}".format(count(pid2)))

    print("Total insert time: " + str(totaltime))

    query_n = 5
    data = get_data(pid1, 0, query_n)
    print("Sample records from buffer 1 (query < {}): {}".format(query_n,
                                                                 data))
    stop(pid1)
    stop(pid2)


if __name__ == '__main__':
    import sys
    import multiprocessing as mp
    if sys.version_info >= (3, 0, 0):
        # Only available in Python 3; allows us to test process code as it
        # behaves in Windows environments.
        mp.set_start_method('spawn')
    main()
