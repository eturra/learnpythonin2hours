#!/usr/bin/python3

f = open('/tmp/abcd.txt', 'wt')
for b in range(10):
  f.write(str(b) + '\n')
f.close()
