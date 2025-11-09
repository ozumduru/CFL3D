import yaml
import sys
import pandas as pd
import numpy as np
import os
import re
import shutil

def READ_YAML():
     global config,config_file
     config_file = sys.argv[1]
     with open(config_file, "r") as f:
         config = yaml.safe_load(f)

def CFL3D_res():
     fn = config["InputOutputFiles"][4]
     shutil.copy(os.path.join("run", fn), os.path.join("data", fn))
     os.chdir("data")

     with open(fn ,"r") as f:
         lines = f.readlines()

     columns_line = lines[4].split()
     for idx, col in enumerate(columns_line):
         if "log(" in col.lower(): 
             columns = columns_line[idx:]
             break

     data_lines = lines[6:]

     data = []
     for line in data_lines:
         line = line.replace("800 it", "").strip()
         if not line:
             continue
         parts = line.split()
         try:
             float(parts[0])
             parts = parts[1:]
         except:
             pass
         data.append(parts)

     df = pd.DataFrame(data, columns=columns).astype(float)
     df.to_csv(f"{config["InputOutputFiles"][4].replace('.', '_')}.csv", index=False)
     os.chdir("../")
 
def CFL3D_subit_res():
     if config["TimeStepParameters"]["DT"] > 0:
         
         shutil.copy(os.path.join("run", "cfl3d.subit_res"), os.path.join("data", "cfl3d.subit_res"))
         os.chdir("data")

         with open("cfl3d.subit_res", 'r') as f:
             lines = f.readlines()

         columns_line = lines[0].split()

         for idx, col in enumerate(columns_line):
             if "log(" in col.lower():  
                 columns = columns_line[idx:]
                 break       
        
         data_lines = lines[1:]
         data = []
         for line in data_lines:
             line = line.strip()
             if not line:
                 continue
             parts = line.split()
        
             try:
                 float(parts[0])
                 parts = parts[1:]
             except:
                 pass
             data.append(parts)
    
         df = pd.DataFrame(data, columns=columns).astype(float)
         df.to_csv("cfl3d_subit_res.csv", index=False)
         os.chdir("../")

def CFL3D_turres():
     if any(ivisc > 2 for ivisc in list(config["GridForceViscousOptions"].values())[-3:]):
         
         fn = config["InputOutputFiles"][5]
         shutil.copy(os.path.join("run", fn), os.path.join("data", fn))
         os.chdir("data")

         with open(fn ,"r") as f:
             lines = f.readlines()

         columns_line = lines[5].split()
         for idx, col in enumerate(columns_line):
             if "log(" in col.lower(): 
                 columns = columns_line[idx:]
                 break

         data_lines = lines[7:]

         data = []
         for line in data_lines:
             line = line.replace("800 it", "").strip()
             if not line:
                 continue
             parts = line.split()
             try:
                 float(parts[0])
                 parts = parts[1:]
             except:
                 pass
             data.append(parts)

         df = pd.DataFrame(data, columns=columns).astype(float)
         df.to_csv(f"{config["InputOutputFiles"][5].replace('.', '_')}.csv", index=False)
         os.chdir("../")

def CFL3D_subit_turres():
     if config["TimeStepParameters"]["DT"] > 0 and any(ivisc > 2 for ivisc in list(config["GridForceViscousOptions"].values())[-3:]):

         shutil.copy(os.path.join("run", "cfl3d.subit_turres"), os.path.join("data", "cfl3d.subit_turres"))
         os.chdir("data")

         with open("cfl3d.subit_turres", 'r') as f:
             lines = f.readlines()

         columns_line = lines[0].split()

         for idx, col in enumerate(columns_line):
             if "log(" in col.lower():  
                 columns = columns_line[idx:]
                 break       
        
         data_lines = lines[1:]
         data = []
         for line in data_lines:
             line = line.strip()
             if not line:
                 continue
             parts = line.split()
        
             try:
                 float(parts[0])
                 parts = parts[1:]
             except:
                 pass
             data.append(parts)
    
         df = pd.DataFrame(data, columns=columns).astype(float)
         df.to_csv("cfl3d_subit_turres.csv", index=False)
         os.chdir("../")

def CFL3D_prout_pointprobe():
     
     fn = config["InputOutputFiles"][5]
     shutil.copy(os.path.join("run", fn), os.path.join("data", fn))
     os.chdir("data")

     with open(fn ,"r") as f:
         content = f.readlines()

     data_line_pattern = re.compile(r'^\s+\d+\s+\d+\s+\d+')
     filtered_lines = []
     keep_next_data = False
     ijk_count = 0
     for line in content:
         if "I    J    K" in line:
             keep_next_data = True
             ijk_count += 1
         elif keep_next_data and data_line_pattern.match(line):
             filtered_lines.append(line)
         else:
             keep_next_data = False

     new_lines = []

     nprint = config["OptionsAndSpecifications"]["NPRINT"]
     t0 = config["TimeStepParameters"]["DT"]*abs(config["MovieOption"]["IMOVIE"])
     tinc = t0
     nondim = config["Auxiliary"]["nondim"]
     [new_lines.append(filtered_lines[i].strip().split()) for i in range(len(filtered_lines))]
     dataa = np.array(new_lines, dtype=np.float64).reshape((int(np.size(new_lines)/14),14))[:,6:]
     data = pd.DataFrame(np.array(dataa).reshape((int(np.size(dataa)/8),8)))
     time = pd.DataFrame([ t0 + k*tinc for k in range(int(len(data[0])/nprint))],columns=['time']).apply(lambda x: np.float64(x)/nondim)
     time = time.loc[time.index.repeat(nprint)].reset_index(drop=True)
     data = data.rename(columns={ 0:"U/Uinf", 1:"V/Vinf", 2:"W/Winf", 3:"P/Pinf", 4:"T/Tinf", 5:"MACH", 6:"cp", 7:"tur. vis."})
     data = pd.concat([time,data],axis=1)
     
     for i in range(len(config["PrintOutputSpecifications"][5])):
         exportdf = data.iloc[i::nprint].reset_index(drop=True)
         exportdf.to_csv(f"{config["PrintOutputSpecifications"][5][i]}.csv",index=False)

     os.chdir("../")

READ_YAML()

os.makedirs("data", exist_ok=True)

CFL3D_res()
CFL3D_turres()
CFL3D_subit_res()
CFL3D_subit_turres()
CFL3D_prout_pointprobe()