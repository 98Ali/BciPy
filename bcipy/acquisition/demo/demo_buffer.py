def _main():
    import argparse
    import timeit
    from bcipy.acquisition.util import mock_data
    from bcipy.acquisition import buffer as buffer
    from bcipy.acquisition.record import Record

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--n_records', default=100000, type=int,
                        help='number of records to insert; default is 100000')
    parser.add_argument('-s', '--chunk_size', default=10000, type=int,
                        help="default is 10000")
    parser.add_argument('-c', '--channel_count', default=25, type=int,
                        help="default is 25")

    args = parser.parse_args()
    channels = ["ch" + str(c) for c in range(args.channel_count)]

    print(
        (f"Running with {args.n_records} samples of {args.channel_count} ",
         f"channels each and chunksize {args.chunk_size}"))
    buf = buffer.Buffer(channels=channels, chunksize=args.chunk_size)

    starttime = timeit.default_timer()
    for record_data in mock_data(args.n_records, args.channel_count):
        timestamp = timeit.default_timer()
        buf.append(Record(record_data, timestamp, None))

    endtime = timeit.default_timer()
    totaltime = endtime - starttime

    print("Total records inserted: " + str(len(buf)))
    print("Total time: " + str(totaltime))
    print("Records per second: " + str(args.n_records / totaltime))

    print("First 5 records")
    print(buf.query(start=0, end=6))

    buf.cleanup()


if __name__ == '__main__':
    _main()
