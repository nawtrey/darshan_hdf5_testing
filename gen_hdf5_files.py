import os
import argparse

import numpy as np
import h5py


def main(mode, n_bytes):
    # set to 10 ranks for now
    n_ranks = 10

    dir_name = f"test_files_{mode}_{n_bytes}_bytes"
    test_dir_path = os.path.join(os.getcwd(), dir_name)
    if os.path.exists(test_dir_path):
        raise ValueError("Test directory already exists")
    else:
        # just create the test directory since the files
        # are generated at run time
        os.mkdir(test_dir_path)

    if mode == "read":
        bytes_to_write = np.void(bytes(1) * n_bytes)
        # create a file for each rank, each with a 
        # dataset containing `bytes_to_write`
        for i in range(n_ranks):
            fname = f"test_{i}.h5"
            file_path = os.path.join(test_dir_path, fname)
            with h5py.File(file_path, 'w') as f:
                d = f.create_dataset("data", data=bytes_to_write)
            # reopen file to check the contents
            with h5py.File(file_path, 'r') as f:
                bytes_written = f["data"].nbytes
                print(f"\nFile {fname} bytes: {bytes_written}")
                assert bytes_written == n_bytes


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
