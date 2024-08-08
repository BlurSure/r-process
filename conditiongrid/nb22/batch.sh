#!/bin/bash -login

#SBATCH --time=0-00:06:00
#SBATCH --begin=now

### nodes:ppn - how many nodes & cores per node (ppn) that you require
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=5G
### you can give your job a name for easier identification
#SBATCH -J r-process_python

### specify an array job
### for each int in the array, launch a separate task with specified ${SLURM_ARRAY_TASK_ID}
#SBATCH --array=0-986

### error/output file specifications
#SBATCH -o /evtdata/jina1/Skynet_Ashley/slurmlogs/1_%a.txt
#SBATCH -e /evtdata/jina1/Skynet_Ashley/slurmlogs/1_%a.txt

### load necessary modules and paths in the command line:
module load /mnt/misc/sw/x86_64/Debian/10/.modulefiles/geant4/10.07.00-angular
module load cmake/3.13.4
module load anaconda/python3.7
module load pythia8/gnu/8.210
module load intel/13.1.1.163
module load PrgEnv-intel
module load gcc/4.9.2
export LD_LIBRARY_PATH=/projects/jina/jina_ashley/installs/CMake-hdf5-1.12.1/build/HDF5-1.12.1-Linux/HDF_Group/HDF5/1.12.1/lib:/projects/jina/jina_ashley/installs/lib:$LD_LIBRARY_PATH
export CMAKE_PREFIX_PATH=/projects/jina/jina_ashley/installs/CMake-hdf5-1.12.1/build/HDF5-1.12.1-Linux/HDF_Group/HDF5/1.12.1/share/cmake:/projects/jina/jina_ashley/installs/share:$CMAKE_PREFIX_PATH
export PKG_CONFIG_PATH=/projects/jina/jina_ashley/installs/lib/pkgconfig:$PKG_CONFIG_PATH
export PYTHONPATH=/projects/jina/jina_bianca/Skynet/skynet_install/lib:$PYTHONPATH
export HDF5_DIR=/projects/jina/jina_ashley/installs/CMake-hdf5-1.12.1/build/HDF5-1.12.1-Linux/HDF_Group/HDF5/1.12.1
### run script with specific array task id. in my script, this is the variation number
python r-process_grid.py ${SLURM_ARRAY_TASK_ID}

### print info on the job
scontrol show job ${SLURM_JOB_ID}
