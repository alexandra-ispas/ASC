#!/bin/bash

make
./tema2_neopt input 
./compare out1 /export/asc/tema2/out1 0.001
./compare out2 /export/asc/tema2/out2 0.001
./compare out3 /export/asc/tema2/out3 0.001

./tema2_blas input 
./compare out1 /export/asc/tema2/out1 0.001
./compare out2 /export/asc/tema2/out2 0.001
./compare out3 /export/asc/tema2/out3 0.001

./tema2_opt_m input 
./compare out1 /export/asc/tema2/out1 0.001
./compare out2 /export/asc/tema2/out2 0.001
./compare out3 /export/asc/tema2/out3 0.001

make clean