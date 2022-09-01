#$ -e sge/stderr
#$ -o sge/stdout
#$ -l h_vmem=50000M
#$ -M hitesh@mpa-garching.mpg.de   # replace <user> with your login name
#$ -m beas                         # send an email at begin, ending, abortion and rescheduling of job

cd /afs/mpa/temp/hitesh/Git/own_package/own_package/athena/

python filament.py
