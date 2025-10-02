from OpenGL.GL import *
from shape import Shape
import numpy as np
import math

class Disk(Shape):
  def __init__(self, slices: int = 64, radius: float = 1.0):
    # Generate a triangle fan: center + circle points (repeat first at end)
    slices = max(3, int(slices))
    nverts = slices + 2  # center + slices + repeat

    coord = np.empty((nverts, 3), dtype='float32')
    texco = np.empty((nverts, 2), dtype='float32')

    # center
    coord[0] = [0.0, 0.0, 0.0]
    texco[0] = [0.5, 0.5]

    # circle points on XZ plane (top view: Y up)
    for i in range(slices + 1):
      ang = (i % slices) * 2.0 * math.pi / slices
      x = radius * math.cos(ang)
      z = radius * math.sin(ang)
      coord[i + 1] = [x, 0.0, z]
      # map to texture [0,1]x[0,1] with center at (0.5,0.5)
      texco[i + 1] = [0.5 + 0.5 * (x / radius), 0.5 + 0.5 * (z / radius)]

    # create VAO and buffers
    self.count = nverts
    self.vao = glGenVertexArrays(1)
    glBindVertexArray(self.vao)

    ids = glGenBuffers(2)
    # positions (layout 0)
    glBindBuffer(GL_ARRAY_BUFFER, ids[0])
    glBufferData(GL_ARRAY_BUFFER, coord.nbytes, coord, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)

    # texcoords (layout 3)
    glBindBuffer(GL_ARRAY_BUFFER, ids[1])
    glBufferData(GL_ARRAY_BUFFER, texco.nbytes, texco, GL_STATIC_DRAW)
    glVertexAttribPointer(3, 2, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(3)

  def Draw(self, st):
    glBindVertexArray(self.vao)
    # constant normal (Y up) and tangent (X axis) for all vertices
    glVertexAttrib3f(1, 0.0, 1.0, 0.0)  # normal
    glVertexAttrib3f(2, 1.0, 0.0, 0.0)  # tangent
    glDrawArrays(GL_TRIANGLE_FAN, 0, self.count)
