mv tmp/w3* .
rm tmp/*.png
python ./x_fullpipe_batch.py 'tmp/' $1
