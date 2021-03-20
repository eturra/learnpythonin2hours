#!/usr/bin/python3

import geometry

c = geometry.circle()
print(c)

#
# In python, everything is an object, and therefore, everything can be assigned to a variable
#
c2 = geometry.circle
c3 = c2()
print(c3)

#
# Import can explicitly merge some of the objects in the module; import * merges everything
#
from geometry import circle
c4 = circle()
print(c4)

