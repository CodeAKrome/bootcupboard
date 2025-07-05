# Brief instructions
## Install
### Make virtual environment
```sh
conda create -n filmstrip python=3.10
conda activate filmstrip
pip install -r requirements.txt
```
## Split by sentence
```sh
cat textfile.txt | ./sentences.py > textfile_sent.txt
```
or
```sh
cat textfile.txt | ./sent.pl > textfile_sent.txt
```
## Make movie
```sh
MkFilmstrip.sh textfile_sent.txt outfile.mp4
```

---

textfile.txt should have one sentence per line.
sent.pl is a simple splitter.
sentences.py uses flair to split sentences more accurately.

