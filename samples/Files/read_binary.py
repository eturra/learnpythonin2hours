#!/usr/bin/python3

#
# Need to check if the `read` returns an empty value, 
# to indicate that the end no file was reached.
#
# After that, we need to convert from binary back to
# strings so that we can print out the integers which
# were stored there by the write_integers.py script
#

import sys
f = open('/tmp/abcd', 'rb')

tmp = None

while tmp != b'':
  tmp = f.read(4)
  if tmp != b'':
    sys.stdout.write(str(int.from_bytes(tmp, sys.byteorder)) + '\n')

f.close()
