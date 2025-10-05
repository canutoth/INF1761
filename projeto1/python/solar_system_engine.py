import glm
from engine import Engine
from transform import Transform

class SolarSystemEngine(Engine):
  def __init__(self,
               earth_orbit_trf: Transform,
               earth_spin_trf: Transform,
               moon_orbit_trf: Transform,
               moon_spin_trf: Transform,
               earth_orbit_speed_deg_per_sec=20.0,
               earth_spin_speed_deg_per_sec=60.0,
               moon_orbit_speed_deg_per_sec=120.0,
               moon_spin_speed_deg_per_sec=120.0,
               venus_orbit_trf: Transform | None = None,
               venus_orbit_speed_deg_per_sec: float = 30.0):

    self.earth_orbit_trf = earth_orbit_trf
    self.earth_spin_trf = earth_spin_trf
    self.moon_orbit_trf = moon_orbit_trf
    self.moon_spin_trf = moon_spin_trf
    self.eo = earth_orbit_speed_deg_per_sec
    self.es = earth_spin_speed_deg_per_sec
    self.mo = moon_orbit_speed_deg_per_sec
    self.ms = moon_spin_speed_deg_per_sec
    self.venus_orbit_trf = venus_orbit_trf
    self.vo = venus_orbit_speed_deg_per_sec

  def Update(self, dt: float):
    self.earth_orbit_trf.Rotate(self.eo * dt, 0, 0, 1)
    self.earth_spin_trf.Rotate(self.es * dt, 0, 0, 1)
    self.moon_orbit_trf.Rotate(self.mo * dt, 0, 0, 1)
    self.moon_spin_trf.Rotate(self.ms * dt, 0, 0, 1)
    self.venus_orbit_trf.Rotate(self.vo * dt, 0, 0, 1)
