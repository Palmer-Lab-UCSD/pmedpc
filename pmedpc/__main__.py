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

from . import utils

def main():
  args = utils._parse_args(sys.arv[1:],
                          epilog=_epilog,
                          description=__doc__)

  raise NotImplementedError
  return 0


main()
