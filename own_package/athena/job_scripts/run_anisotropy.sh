#!/bin/sh

for i in {0..1}; do
	sbatch job_script_anisotropy_freya.sh $i
	echo $i
done
