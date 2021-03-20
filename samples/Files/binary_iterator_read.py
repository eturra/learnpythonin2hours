#!/usr/bin/python3

import sys

class intFileIterator():
  """
  Given a file opened for binary reading, iterate until the file is finished, and return n bytes at a time as integer
  """
  def __init__(self, file, n_bytes=4):
    "Get ready to iterate file n_bytes at a time"
    self.file = file
    self.n_bytes = n_bytes
  def __iter__(self):
    "return self, as an iterator"
    return self
  def __next__(self):
    "return the next n_bytes"
    r = self.file.read(self.n_bytes)
    if r == b'':
      raise StopIteration
    else:
      return int.from_bytes(r, sys.byteorder)

f = open('/tmp/abcd', 'rb')

for i in intFileIterator(f, 4):
  sys.stdout.write(str(i) + '\n')

f.close()
