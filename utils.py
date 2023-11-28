"""
Utility function

By: Beverly Peng
"""
import argparse

def _parse_args(args, **kwargs):
  parser = argparse.ArgumentParser(**kwargs,
                                   formatter_class=argparse.RawDescriptionHelpFormatter)

  parser.add_argument("filename",
                      type=str,
                      help="MedPC file to be parsed.")

  return parser.parse_args()
