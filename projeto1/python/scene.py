
class Scene:
  def __init__ (self, root):
    self.root = root
    self.engines = []
    self.light = None

  def GetRoot (self):
    return self.root

  def AddEngine (self, engine):
    self.engines.append(engine)

  def SetLight (self, light):
    self.light = light

  def GetLight (self):
    return self.light

  def Update (self, dt):
    for e in self.engines:
      e.Update(dt)

  def Render (self, camera):
    from state import State
    st = State(camera)
    if self.light:
      st.SetLight(self.light)
    self.root.Render(st)
