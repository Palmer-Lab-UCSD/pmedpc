"""
pmedpc: A tool to extract data from MedPC files and write to csv.

By: Beverly Peng
"""

_epilog = """

Example

Open specified MedPC file, extract relevant data and write
to file <filename>_format.csv

python -m pmedpc <filename>
"""

import sys

import utils

def main():
  args = utils._parse_args(sys.argv[1:],
                          epilog=_epilog,
                          description=__doc__)
  args_1 = sys.argv[1]
  print(args_1)
  


main()
