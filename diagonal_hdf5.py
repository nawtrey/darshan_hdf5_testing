import os
import time
import argparse

import numpy as np
from mpi4py import MPI
import h5py


def handle_io(test_dir_path, rank_val, delay_time, n_bytes, mode, flush_file):
    # read/write n_bytes to/from a file from
    # rank rank_val after delay_time seconds
    time.sleep(delay_time)
    filename = f"test_{rank_val}.h5"
    file_path = os.path.join(test_dir_path, filename)

    if mode == "read":
        with h5py.File(file_path, "r") as f:
            data = np.asarray(f.get('data')).tobytes()
    elif mode == "write":
        bytes_to_write = np.void(bytes(1) * n_bytes)
        with h5py.File(file_path, "w") as f:
            f.create_dataset("dataset", data=bytes_to_write)
            if flush_file:
                # only flush half of files
                if rank_val % 2 == 0:
                    f.flush()


def main(mode, n_bytes):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    # set flush status
    flush_files = False

    # each rank should write data
    # at a specific offset time to
    # produce diagonal heatmap IO
    # activity like this:
    #       x
    #     x
    #   x
    # x

    dir_name = f"test_files_{mode}_{n_bytes}_bytes"
    test_dir_path = os.path.join(os.getcwd(), dir_name)

    delay_time = 0.3 + (rank * 0.2)
    for rank_val in range(size):
        if rank == rank_val:
            handle_io(
                test_dir_path=test_dir_path,
                rank_val=rank_val,
                delay_time=delay_time,
                n_bytes=n_bytes,
                mode=mode,
                flush_file=flush_files,
            )    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "run_mode",
        type=str,
        help="Specify run mode (i.e. 'read' or 'write')",
    )
    parser.add_argument(
        "n_bytes",
        type=int,
        help="Specify number of bytes to read/write",
    )
    args = parser.parse_args()
    mode = args.run_mode
    n_bytes = args.n_bytes
    main(mode=mode, n_bytes=n_bytes)
