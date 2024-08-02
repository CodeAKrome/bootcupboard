rm -f video/*
rm -f audio/*
cat $1 | python ADLightning.py
cat $1 | ./jenny.py
./ZipVideoAudio.py -o $2
