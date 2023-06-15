#!/bin/sh
#
#SBATCH -J parpl
#SBATCH -o parpl."%j".out
#SBATCH -e parpl."%j".err
#SBATCH --mail-user hitesh@mpa-garching.mpg.de
#SBATCH --partition=p.test
#SBATCH --mail-type=ALL
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=40
#SBATCH --time=00:25:00

set -e
SECONDS=0

module purge
module load ffmpeg/4.4
module list

# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HDF5_HOME/lib
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$FFTW_HOME/lib
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$I_MPI_ROOT/intel64/lib
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$I_MPI_ROOT/intel64/lib/release/

pip install -e /ptmp/mpa/hitesh/own_package/

cd /ptmp/mpa/hitesh/own_package/own_package/plot/projection_rust/ 

# set number of OMP threads *per process*
export OMP_NUM_THREADS=1

srun python plot_npy.py $SLURM_CPUS_PER_TASK

echo "Elapsed: $(($SECONDS / 3600))hrs $((($SECONDS / 60) % 60))min $(($SECONDS % 60))sec"

echo "Boom!"
