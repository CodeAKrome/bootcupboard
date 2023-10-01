#!/usr/bin/env python3

import sys
from pyarrow.json import read_json
from pyarrow.parquet import write_table

write_table(read_json(sys.argv[1]), sys.argv[2])
