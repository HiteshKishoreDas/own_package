#$ -e sge/stderr_filament
#$ -o sge/stdout_filament
#$ -l h_vmem=50000M
#$ -M hitesh@mpa-garching.mpg.de   # replace <user> with your login name
#$ -m beas                         # send an email at begin, ending, abortion and rescheduling of job

#here the module function gets defined
source /usr/common/appl/modules-tcl/init/sh

cd /afs/mpa/temp/hitesh/Git/own_package/own_package/athena/

#module load anaconda3/2020.11
#conda activate /afs/mpa/data/hitesh/envs/athenaenv

# python filament.py

pwd

/afs/mpa/data/hitesh/envs/athenaenv/bin/python cup_render.py
