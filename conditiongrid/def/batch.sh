#!/bin/bash -login

#SBATCH --time=0-00:12:00
#SBATCH --begin=now

### nodes:ppn - how many nodes & cores per node (ppn) that you require
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=5G
### you can give your job a name for easier identification
#SBATCH -J r-process_python

### specify an array job
### for each int in the array, launch a separate task with specified ${SLURM_ARRAY_TASK_ID}
#SBATCH --array=0-46

### error/output file specifications
#SBATCH -o /mnt/home/agarw132/jina/r_process_outputs/2_%a.txt
#SBATCH -e /mnt/home/agarw132/jina/r_process_outputs/1_%a.txt

### load necessary modules and paths in the command line:
conda activate pranav_jina
module purge

module load GCC/10.3.0
module load OpenMPI/4.1.1
module load gomkl
module load Boost
module load CMake
module load Valgrind/3.17.0
module load SWIG




export PYTHONPATH=~/skynet/install/lib/:$PYTHONPATH


### run script with specific array task id. in my script, this is the variation number
python3 r-process_grid.py ${SLURM_ARRAY_TASK_ID}

### print info on the job
scontrol show job ${SLURM_JOB_ID}
