from scipy.io import FortranFile
import numpy as np
import sys
import yaml
import os
import shutil
from scipy.io._fortran import FortranFormattingError
config_file = sys.argv[1]
with open(config_file, "r") as f:
     config = yaml.safe_load(f)

if config["MovieOption"]["IMOVIE"] != 0:
     
     fnq = config["InputOutputFiles"][2]
     fnx = config["InputOutputFiles"][1]
     frame = abs(int(config["OptionsAndSpecifications"]["NTSTEP"]/config["MovieOption"]["IMOVIE"]))

     os.makedirs("contour", exist_ok=True)
     shutil.copy(os.path.join("run", fnq), os.path.join("contour", fnq))
     shutil.copy(os.path.join("run", fnx), os.path.join("contour", fnx))
     os.chdir("contour")

     if config["MovieOption"]["IMOVIE"] < 0:
         frame = frame +1

     qfile = FortranFile(fnq,"r")
     for f in range(frame):
         try:
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
         except (EOFError, FortranFormattingError):
             print(f"Reached EOF at frame {f}. Stopping loop.")
             break
         except Exception as e:
         # unexpected errors still raise normally
             raise

     qfile.close()
     os.remove(fnq)
