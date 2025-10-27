import glm
from engine import Engine
from transform import Transform

class SolarSystemEngineProj2(Engine):
  def __init__(self,
               sun_spin_trf: Transform,
               earth_orbit_trf: Transform,
               earth_spin_trf: Transform,
               moon_orbit_trf: Transform,
               moon_spin_trf: Transform,
               venus_orbit_trf: Transform,
               venus_spin_trf: Transform,
               sun_spin_speed_deg_per_sec=10.0,
               earth_orbit_speed_deg_per_sec=20.0,
               earth_spin_speed_deg_per_sec=60.0,
               moon_orbit_speed_deg_per_sec=120.0,
               moon_spin_speed_deg_per_sec=120.0,
               venus_orbit_speed_deg_per_sec=30.0,
               venus_spin_speed_deg_per_sec=50.0):

    # Transforms de rotação
    self.sun_spin_trf = sun_spin_trf
    self.earth_orbit_trf = earth_orbit_trf
    self.earth_spin_trf = earth_spin_trf
    self.moon_orbit_trf = moon_orbit_trf
    self.moon_spin_trf = moon_spin_trf
    self.venus_orbit_trf = venus_orbit_trf
    self.venus_spin_trf = venus_spin_trf
    
    # Velocidades (graus por segundo)
    self.ss = sun_spin_speed_deg_per_sec
    self.eo = earth_orbit_speed_deg_per_sec
    self.es = earth_spin_speed_deg_per_sec
    self.mo = moon_orbit_speed_deg_per_sec
    self.ms = moon_spin_speed_deg_per_sec
    self.vo = venus_orbit_speed_deg_per_sec
    self.vs = venus_spin_speed_deg_per_sec

  def Update(self, dt: float):
    # Rotação do Sol em torno do seu eixo (eixo Y)
    self.sun_spin_trf.Rotate(self.ss * dt, 0, 1, 0)
    
    # Translação da Terra em torno do Sol (eixo Y)
    self.earth_orbit_trf.Rotate(self.eo * dt, 0, 1, 0)
    
    # Rotação da Terra em torno do seu eixo (eixo Y)
    self.earth_spin_trf.Rotate(self.es * dt, 0, 1, 0)
    
    # Translação da Lua em torno da Terra (eixo Y)
    self.moon_orbit_trf.Rotate(self.mo * dt, 0, 1, 0)
    
    # Rotação da Lua em torno do seu eixo (eixo Y)
    self.moon_spin_trf.Rotate(self.ms * dt, 0, 1, 0)
    
    # Translação de Vênus em torno do Sol (eixo Y)
    self.venus_orbit_trf.Rotate(self.vo * dt, 0, 1, 0)
    
    # Rotação de Vênus em torno do seu eixo (eixo Y)
    self.venus_spin_trf.Rotate(self.vs * dt, 0, 1, 0)
