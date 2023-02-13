for i in {0..5}
do
	python -O clump_size.py $i > log_clump_$i &
done
