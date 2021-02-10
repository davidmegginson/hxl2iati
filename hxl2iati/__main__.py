import sys
from hxl2iati.convert import convert


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} <url_or_filename>".format(sys.argv[0]), file=sys.stderr)
        sys.exit(2)
    convert(sys.argv[1], sys.stdout, True)
