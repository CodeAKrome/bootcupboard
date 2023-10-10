import re
import sys


def middle(beg, end):
    spew = False
    for line in sys.stdin:
        if re.match(beg, line):
            spew = True
        if spew:
            print(line.strip())
        if re.match(end, line):
            break


if __name__ == "__main__":
    middle(sys.argv[1], sys.argv[2])
