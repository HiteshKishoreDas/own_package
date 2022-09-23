#$ -e sge/stderr_image
#$ -o sge/stdout_image
#$ -l h_vmem=5000M
#$ -M hitesh@mpa-garching.mpg.de   # replace <user> with your login name
#$ -m beas                         # send an email at begin, ending, abortion and rescheduling of job

#here the module function gets defined
source /usr/common/appl/modules-tcl/init/sh

cd /afs/mpa/temp/hitesh/Git/own_package/own_package/athena/

#module load anaconda3/2020.11
#conda activate /afs/mpa/data/hitesh/envs/athenaenv

# python filament.py

pwd

python cup_render.py

#convert rho_smooth_MHD_gist_rainbow.png MPA_hoch_E_green.png rho_smooth_HD_gist_rainbow.png +append mug_strip_image_less_ram.png
