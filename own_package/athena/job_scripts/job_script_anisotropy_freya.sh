#!/bin/sh
#
#SBATCH -J paran
#SBATCH -o paran."%j".out
#SBATCH -e paran."%j".err
#SBATCH --mail-user hitesh@mpa-garching.mpg.de
#SBATCH --partition=p.test
#SBATCH --mail-type=ALL
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=5000
#SBATCH --time=00:25:00

set -e
SECONDS=0

module purge
# module load anaconda/3/2020.02
module list

# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HDF5_HOME/lib
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$FFTW_HOME/lib
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$I_MPI_ROOT/intel64/lib
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$I_MPI_ROOT/intel64/lib/release/

# pip install -e /ptmp/mpa/hitesh/own_package/

cd /ptmp/mpa/hitesh/own_package/own_package/athena/

# set number of OMP threads *per process*
export OMP_NUM_THREADS=1

num=$1

srun python filament.py $SLURM_CPUS_PER_TASK $num
# srun python filament.py $SLURM_CPUS_PER_TASK 1 &
# wait

# srun --exclusive --cpus-per-task 8 --ntasks 1 python filament.py $SLURM_CPUS_PER_TASK 0 &
# srun --exclusive --cpus-per-task 8 --ntasks 1 python filament.py $SLURM_CPUS_PER_TASK 1 &
# srun --exclusive --cpus-per-task 8 --ntasks 1 python filament.py $SLURM_CPUS_PER_TASK 2 
# srun python filament.py $SLURM_CPUS_PER_TASK 3 &
# srun python filament.py $SLURM_CPUS_PER_TASK 4 &
# srun python filament.py $SLURM_CPUS_PER_TASK 5 

echo "Elapsed: $(($SECONDS / 3600))hrs $((($SECONDS / 60) % 60))min $(($SECONDS % 60))sec"

echo "Boom!"
