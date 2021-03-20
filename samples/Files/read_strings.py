#!/usr/bin/python3

import sys
f = open('/tmp/abcd.txt', 'rt')

for line in f:
  sys.stdout.write(line)

f.close()

