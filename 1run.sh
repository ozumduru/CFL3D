#!/bin/bash

iter=20  # "Enter .q file number:" iter
nstep=1000 #"Enter NSTEP:" nstep
file_base_name=aaa # "Enter file base name :" file_base_name
nodirect=0 #"is nodirect avaliable ? 0 is no, 1 is yes :" nodirect  
cfl=1  #" mpi or seq ? 0 is seq, 1 is mpi :" cfl
cores=3 #" core number for mpi :" cores

#read -p " is mesh and input file  transposes ? 0 is no 1 is yes:" tp
#if [ $tp = "0" ]; then
#gridswitchijk
#wait
#mv tempijk.p3dbin $file_base_name.bin
#v6inpswitchijk
#wait
#fi

irest=1
ICname="0"

readarray -t Arr < $file_base_name$ICname.inp

Arr[3]="plot3d_1.q"
Arr[4]="cfl3d_1.out"
Arr[5]="cfl3d.res_1"
Arr[6]="cfl3d.turres_1"

declare -a Arr1=(${Arr[20]})
Arr1[1]=$irest

Arr[20]=${Arr1[*]}

declare -a Arr2=(${Arr[22]})
Arr2[6]=$nstep

Arr[22]=${Arr2[*]}

touch aaa1.inp

printf "%s\n" "${Arr[@]}" > aaa1.inp

for i in $(seq 2 $iter);
do

Arr[3]="plot3d_$i.q"

Arr[4]="cfl3d_$i.out"

Arr[5]="cfl3d.res_$i"

Arr[6]="cfl3d.turres_$i"

touch  "$file_base_name$i.inp"
printf "%s\n" "${Arr[@]}" > "$file_base_name$i.inp"
done

if [ $nodirect = "0" ]; then

if [ $cfl = "0" ]; then
cfl3d_seq < $file_base_name$ICname.inp

for i in $(seq 1 $iter);
do

cfl3d_seq < $file_base_name$i.inp
wait

done
fi

if [ $cfl = "1" ]; then
mpirun -np $cores cfl3d_mpi < $file_base_name$ICname.inp

for i in $(seq 1 $iter);
do

mpirun -np $cores cfl3d_mpi  < $file_base_name$i.inp
wait

done
fi

fi


if [ $nodirect = "1" ]; then

if [ $cfl = "0" ]; then

mv $file_base_name$ICname.inp cfl3d.inp
cfl3d_seq < cfl3d.inp
wait
mv cfl3d.inp $file_base_name$ICname.inp

for i in $(seq 1 $iter);
do
mv $file_base_name$i.inp cfl3d.inp
cfl3d_seq < cfl3d.inp
wait
mv cfl3d.inp $file_base_name$i.inp

done
fi

if [ $cfl = "1" ]; then
mv $file_base_name$ICname.inp cfl3d.inp
mpirun -np $cores cfl3d_mpi < cfl3d.inp
wait
mv cfl3d.inp $file_base_name$ICname.inp

for i in $(seq 1 $iter);
do

mv $file_base_name$i.inp cfl3d.inp
mpirun -np $cores cfl3d_mpi  < cfl3d.inp
wait
mv cfl3d.inp $file_base_name$i.inp

done
fi

fi

