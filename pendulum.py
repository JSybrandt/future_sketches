#!/usr/bin/env python3
# 2020-03-01

from fire import Fire
from PIL import Image, ImageDraw
import cv2
import math
from dataclasses import dataclass
from copy import copy
from point import Point

GRAVITY=9.8


@dataclass
class Bob:
  mass:float
  length:float
  rotation:float  #relative to vertical down


class Pendulum(object):
  def __init__(
      self,
      inner:Bob,
      outer:Bob,
      pivot:Point,
  ):
    self.inner = copy(inner)
    self.outer = copy(outer)
    self.pivot = copy(pivot)

  def step(self, timestep):
      pass

  def get_pivot_point(self):
    return copy(self.pivot)

  def get_inner_mass_point(self):
    return Point(
        x=
    )

  def _get_potential_engergy(self):
    return (
        -(self.inner.mass+self.outer.mass)
        *GRAVITY*self.inner.length* math.cos(self.inner.rotation)
        -self.outer.mass
        *GRAVITY*self.outer.mass*math.cos(self.outer.rotation)
    )

  def _get_kinetic_energy(self):




class State(object):
  def __init__(self, num_pendulums:int):


def main(
    canvas_width=800,
    canvas_height=600,
):
  image = Image.new(
      "RGBA",
      (canvas_width, canvas_height)
  )
  image.show()

if __name__=="__main__":
  Fire(main)
