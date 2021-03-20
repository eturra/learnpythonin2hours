#!/usr/bin/python3

import sys

def intFileIterator(file, n_bytes=4):
  """
  Given a file opened for binary reading, iterate until the file is finished, and return n bytes at a time as integer
  """
  tmp = None
  while tmp != b'':
    tmp = f.read(n_bytes)
    if tmp != b'':
      yield int.from_bytes(tmp, sys.byteorder)

f = open('/tmp/abcd', 'rb')

for i in intFileIterator(f, 4):
  sys.stdout.write(str(i) + '\n')

f.close()

