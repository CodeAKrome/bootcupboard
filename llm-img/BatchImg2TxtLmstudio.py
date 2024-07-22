import sys
from Lmlib import image2text
""" Read paths/URLs of images and output 2 tab delimited columns with the image followed by description. """

if __name__ == "__main__":
    n = 0
    for l in sys.stdin:
        line = l.strip()
        desc = image2text(line).replace("\n", " ")
        desc = desc.replace('  ',' ')
        print(f"{line}\t{desc}")
        n += 1
        print('.', end='', file=sys.stderr, flush=True)
        if n % 10 == 0:
            print(n, file=sys.stderr)