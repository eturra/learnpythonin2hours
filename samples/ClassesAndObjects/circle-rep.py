#!/usr/bin/python3

class circle:
  """
  A circle object is created from a radius, default is 1
  """
  pi = 3.141529
  def __init__(self, radius=1):
    "Initialise the circle from the specified radius"
    self.radius = radius
  def diameter(self):
    "Return twice the radius"
    return self.radius * 2
  def area(self):
    "calculate the area of the circle"
    return circle.pi * self.radius **2
  def perimeter(self):
    "calculate the perimeter of the circle"
    return self.diameter() * circle.pi
  def __repr__(self):
    "representation of a circle"
    return '{0}({1})'.format(self.__class__.__name__, self.radius)

c = circle()
print(c)
print(repr(c))
print(str(c))
