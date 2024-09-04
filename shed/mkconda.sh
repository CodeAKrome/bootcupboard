echo "conda activate $1" > .autoenv; echo "conda deactivate" > .autoenv.leave; conda activate $1
