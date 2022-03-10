from mpi4py import MPI
import h5py


def main(rank_val):
    fname = f"test_h5f_only_{rank_val}.h5"
    with h5py.File(fname, "w") as f:
        print(f"{fname} opened")


if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # open 3 unique files but don't create any
    # datasets so only `H5F` data is created
    for rank_val in range(size):
        if rank == rank_val:
            main(rank_val=rank_val)
