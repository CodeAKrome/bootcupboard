#!env python3

import argparse
import re


def chunk_file(file_path, chunk_size=512):
    """Chunks a file into smaller pieces of text that are ready for embedding in an LLM.

    Args:
      file_path: The path to the file to be chunked.
      chunk_size: The maximum size of each chunk in tokens.

    Returns:
      A list of strings, where each string is a chunk of text from the file.
    """

    chunks = []
    current_chunk = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                current_chunk.append(line)
            if len(current_chunk) >= chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks


def main():
    """Chunks a file given as a command line argument so it is ready for embedding in an LLM."""

    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="The path to the file to be chunked.")
    parser.add_argument(
        "-c",
        "--chunk-size",
        type=int,
        default=512,
        help="The maximum size of each chunk in tokens.",
    )
    args = parser.parse_args()

    chunks = chunk_file(args.file_path, chunk_size=args.chunk_size)

    for chunk in chunks:
        print(chunk)


if __name__ == "__main__":
    main()
