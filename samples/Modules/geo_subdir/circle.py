#!/usr/bin/python3

class circle:
  """
  A circle object is created from a radius, default is 1
  """
  def __init__(self, radius=1):
    "Initialise the circle from the specified radius"
    self.radius = radius
  @staticmethod
  def pi():
    "Decent approximation of a circle"
    return 355/113
  @classmethod
  def strpi(cls):
    "Format pi to look nice"
    return "{cls}'s π = {pi:6f}".format(cls=cls.__name__, pi=cls.pi())
  def diameter(self):
    "Return twice the radius"
    return self.radius * 2
  def area(self):
    "calculate the area of the circle"
    return circle.pi() * self.radius **2
  def perimeter(self):
    "calculate the perimeter of the circle"
    return self.diameter() * circle.pi()
  def __repr__(self):
    "representation of a circle"
    return '{0}({1})'.format(self.__class__.__name__, self.radius)
  def __str__(self):
    "Pretty representation of a circle"
    return 'circle with radius: {r:.6f}, diameter(d:.6f) area: {a:.6f}, perimeter: {p:.6f}'.format(r=self.radius, d=self.diameter(), a=self.area(), p=self.perimeter())
