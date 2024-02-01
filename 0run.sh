#!/bin/bash

gridswitchijk  <<EOF
aa.bin
0
EOF

mv tempijk.p3dbin aaa.bin

v6inpswitchijk  <<EOF
aa.inp
aaa0.inp
aaa.bin
0
EOF

readarray -t Arr < aaa0.inp

Arr[2]="plot3d.xyz"
Arr[3]="plot3d_0.q"
Arr[4]="cfl3d_0.out"
Arr[5]="cfl3d.res_0"
Arr[6]="cfl3d.turres_0"
Arr[7]="cfl3d.blomax"
Arr[8]="cfl3d.out15"
Arr[9]="cfl3d.prout"
Arr[10]="cfl3d.out20"
Arr[11]="ovrlp.bin"
Arr[12]="patch.bin"
Arr[13]="restart.bin"

touch  "aaa0.inp"
printf "%s\n" "${Arr[@]}" > "aaa0.inp"

echo "aaa0.inp is ready"
