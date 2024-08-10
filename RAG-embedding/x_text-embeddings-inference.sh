model=BAAI/bge-large-en-v1.5
volume=$PWD/data # share a volume with the Docker container to avoid downloading weights every run

docker run -p 8080:80 -v $volume:/data --pull always ghcr.io/huggingface/text-embeddings-inference:1.5 --model-id $model
