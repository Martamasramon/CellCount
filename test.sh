#$ -l tmem=64G,h_vmem=64G
#$ -l h_rt=10:00:00

#$ -S /bin/bash
#$ -j y
#$ -N Test
#$ -V
#$ -wd /cluster/project7/ProsRegNet_CellCount/Cellcount

hostname

date

export PATH=/share/apps/python-3.8.5-shared/bin:$PATH
export LD_LIBRARY_PATH=/share/apps/python-3.8.5-shared/lib:$LD_LIBRARY_PATH

python3 simple_SN.py

dat