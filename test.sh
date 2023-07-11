#$ -l tmem=80G,h_vmem=80G
#$ -l h_rt=2:00:00

#$ -S /bin/bash
#$ -j y
#$ -N Sub-Images
#$ -V
#$ -wd /home/mmasramo/CellCount

hostname

date

export PATH=/share/apps/python-3.8.5-shared/bin:$PATH
export LD_LIBRARY_PATH=/share/apps/python-3.8.5-shared/lib:$LD_LIBRARY_PATH

python3 pipeline.py

date

