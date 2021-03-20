#!/usr/bin/python3

#
# Files opened in binary mode can still use write
# but they expect a bytes-like object.
#
# to_bytes converts integers to bytes.
#
# Use hexdump to examine the contents.
#

import sys

f = open('/tmp/abcd', 'w+b')

for b in range(10):
  f.write(b.to_bytes(4, sys.byteorder))

f.close()
