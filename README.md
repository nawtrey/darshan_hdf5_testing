## Darshan HDF5 Testing Scripts
Python scripts used for generating [Darshan](https://www.mcs.anl.gov/research/projects/darshan/) logs with HDF5 data via [`h5py`](https://docs.h5py.org/en/stable/index.html).


### To Run

Create Darshan logs with only `H5F` data:
```bash
mpirun -x DARSHAN_LOGPATH=/path/to/logs/dir -x DARSHAN_DISABLE_SHARED_REDUCTION=1 -x LD_PRELOAD=/path/to/libdarshan.so:/path/to/libhdf5.so -np 3 python h5f_only.py
```


Create Darshan logs with `DXT_POSIX`, `H5F` and `H5D` (write) data:
```bash
python gen_hdf5_files.py write 1
mpirun -x DXT_ENABLE_IO_TRACE=1 -x DARSHAN_LOGPATH=/path/to/logs/dir -x DARSHAN_DISABLE_SHARED_REDUCTION=1 -x LD_PRELOAD=/path/to/libdarshan.so:/path/to/libhdf5.so -np 10 python diagonal_hdf5.py write 1
```

NOTE: Current Darshan instrumentation does not track the `h5py` read calls, so no `H5D` data is generated when executing the "read" mode. See [this issue](https://github.com/darshan-hpc/darshan/issues/690) for details.
