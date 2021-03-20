#!/usr/bin/python3
#
# Class and instance can be reference, e.g. `circle.pi` to get pi. We could also have used `self.pi`, `self.__class__`, or `type(self).pi`
#
class circle:
  """
  A circle object is created from a radius, default is 1
  """
  pi = 3.141529
  def __init__(self, radius=1):
    "Initialise the circle from the specified radius"
    circle.radius = radius
  def diameter(self):
    "Return twice the radius"
    return self.radius * 2
  def area(self):
    "calculate the area of the circle"
    return circle.pi * self.radius **2
  def perimeter(self):
    "calculate the perimeter of the circle"
    return self.diameter() * self.__class__.pi
#
# Set the radius to 7
c = circle(7)

#
# Print info about the circle

print('Area', c.area())
print('Diameter', c.diameter())
print('Perimeter', c.perimeter())
