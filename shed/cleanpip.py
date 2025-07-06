#!/usr/bin/env python

import sys
import subprocess


keep =["Package", "pip", "setuptools", "wheel", "build","conda","xattr","xmod","python","pyobjc"]


for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        kill = False
        for keeper in keep:
            if keeper in line:
                kill = True
                break
        if kill:
            print(f"keep {line}")
        else:
            #print(f"kill {line}")
            cmd = f"pip uninstall {line} -y"
            print(cmd)
            subprocess.run(cmd, shell=True, check=True)
    except Exception as e:
        print(f"{e}\n{line}", file=sys.stderr)