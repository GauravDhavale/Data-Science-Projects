import numpy as np
a = np.arange(15).reshape(3,5)
"""import glob, os
glob_dir = os.path.join( "*.txt")
for file_name in glob.glob(glob_dir):
    #This file is corrupt hence ignored
    if os.path.basename(file_name) == "demo_numpy.txt":
        file_path = os.path.join(os.path.basename(file_name))"""
with open("demo_numpy.txt", "w") as txt:
    print(a, file=txt)
    print(a.shape, file=txt)
    print(a.size, file=txt)
    print(a.itemsize, file=txt)
    print(a.ndim, file=txt)
    print(a.dtype, file=txt)
