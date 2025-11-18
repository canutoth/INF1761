from OpenGL.GL import *
from appearance import Appearance

class NoCull(Appearance):
  def Load(self, st):
    glDisable(GL_CULL_FACE)
  def Unload(self, st):
    glEnable(GL_CULL_FACE)
