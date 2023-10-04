#!env python3
import sys

previous_line = None
output = []

for line in sys.stdin:
    if line.isspace():
        continue
    if previous_line is not None and line.startswith('    '):
        previous_line += line.strip()
    else:
        if previous_line is not None:
            output.append(previous_line)
        previous_line = line.strip()

if previous_line is not None:
    output.append(previous_line)

print('\n'.join(output))
