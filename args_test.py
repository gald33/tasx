import argparse

parser = argparse.ArgumentParser(add_help=True)

parser.add_argument('-a', default=False)
parser.add_argument('-b', dest="b")
parser.add_argument('-c', dest="c", type=int)

print parser.parse_args()