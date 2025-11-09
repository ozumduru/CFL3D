from scipy.io import FortranFile
import numpy as np
import sys
import yaml
import os
import shutil
config_file = sys.argv[1]
with open(config_file, "r") as f:
     config = yaml.safe_load(f)

if config["MovieOption"]["IMOVIE"] != 0:
     
     fn = config["InputOutputFiles"][2]
     frame = abs(int(config["OptionsAndSpecifications"]["NTSTEP"]/config["MovieOption"]["IMOVIE"]))

     os.makedirs("contour", exist_ok=True)
     shutil.copy(os.path.join("run", fn), os.path.join("contour", fn))
     os.chdir("contour")

     if config["MovieOption"]["IMOVIE"] < 0:
         frame = frame +1

     qfile = FortranFile(fn,"r")
     for f in range(frame):
         nblk = qfile.read_ints()[0]
         indices = qfile.read_ints()
         properties=[] ; q = []
         for n in range(nblk):
             properties.append(qfile.read_reals(np.float32))
             q.append(qfile.read_reals(np.float32))
     
         qwrite = FortranFile(f"cfl3d_{f}.q", "w")
         qwrite.write_record(nblk)
         qwrite.write_record(indices)

         for i in range(nblk):
             qwrite.write_record(properties[i])
             qwrite.write_record(q[i])
         qwrite.close()
     
     qfile.close()
