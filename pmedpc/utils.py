"""
Utility function

By: Beverly Peng
"""
import argparse

def _parse_args(args, **kwargs):
  parser = argparse.ArgumentParser(**kwargs,
                                   formatter_class=argparse.RawDescriptionHelpFormatter)

  # parser.add_argument("filename",
  #                     type=str,
  #                     help="MedPC file to be parsed")
  parser.add_argument('-file', metavar = '-f', 
                      type = str, nargs='?',
                      help = "MedPC file to be parsed")
  # parser.add_argument('-d', '--directory')
  # parser.add_argument('-o', '--stdout')

  return parser.parse_args()
