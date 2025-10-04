import glfw
from OpenGL.GL import (
  glClearColor,
  glEnable,
  glDisable,
  glClear,
  glGetString,
  GL_DEPTH_TEST,
  GL_CULL_FACE,
  GL_COLOR_BUFFER_BIT,
  GL_DEPTH_BUFFER_BIT,
  GL_VERSION,
  GL_TRUE,
)
import glm
import math
from pathlib import Path
from camera3d import Camera3D
from light import Light
from shader import Shader
from material import Material
from transform import Transform
from node import Node
from scene import Scene
from disk import Disk
from texture import * 
from solar_system_engine import SolarSystemEngine

def initialize():
  
  glClearColor(0.0, 0.0, 0.0, 0.0)
  glEnable(GL_DEPTH_TEST)
  glDisable(GL_CULL_FACE)

  global camera
  camera = Camera3D(0, 15, 0)
  camera.SetCenter(0, 0, 0)
  camera.SetUpDir(0, 0, -1)
  camera.SetAngle(45)
  camera.SetOrtho(True)

  light = Light(0.0, 1.0, 0.0, 1.0, "world")

  shader = Shader(light, "world")
  root_dir = Path(__file__).resolve().parent.parent
  shader.AttachVertexShader(str(root_dir / "shaders/ilum_vert/vertex.glsl"))
  shader.AttachFragmentShader(str(root_dir / "shaders/ilum_vert/fragment.glsl"))
  shader.Link()

  shd_tex = Shader(light, "world")
  shd_tex.AttachVertexShader(root_dir / "shaders/ilum_vert/vertex_texture.glsl")
  shd_tex.AttachFragmentShader(root_dir / "shaders/ilum_vert/fragment_texture.glsl")
  shd_tex.Link()

  sun_mat = Material(1.0, 1.0, 1.0)
  earth_mat = Material(1.0, 1.0, 1.0)
  moon_mat = Material(1.0, 1.0, 1.0)
  venus_mat = Material(1.0, 1.0, 1.0)

  sun_tex = Texture("decal", root_dir / "images/sun_image.png")
  earth_tex = Texture("decal", root_dir / "images/NASA_earth.jpg")
  venus_tex = Texture("decal", root_dir / "images/venus.jpg")
  moon_tex = Texture("decal", root_dir / "images/moon.jpg")

  sun_radius = 2.0
  earth_radius = 0.6
  moon_radius = 0.3
  venus_radius = 0.5
  sun_disk = Disk(96, sun_radius)
  earth_disk = Disk(64, earth_radius)
  moon_disk = Disk(48, moon_radius)
  venus_disk = Disk(56, venus_radius)

  sun_trf = Transform()
  earth_orbit = Transform()
  earth_orbit_radius = 6.0
  earth_offset = Transform(); earth_offset.Translate(earth_orbit_radius, 0.0, 0.0)
  venus_orbit = Transform()
  venus_orbit_radius = 3.8
  venus_offset = Transform(); venus_offset.Translate(venus_orbit_radius, 0.0, 0.0)
  earth_spin = Transform()
  earth_tilt = Transform()
  earth_tilt.Rotate(23.5, 0, 0, 1)
  moon_orbit = Transform()
  moon_orbit_radius = 1.5
  moon_offset = Transform(); moon_offset.Translate(moon_orbit_radius, 0.0, 0.0)
  moon_spin = Transform()

  dist = glm.distance(camera.GetEye(), camera.GetCenter())
  half_extent = max(sun_radius, earth_orbit_radius + max(earth_radius, moon_orbit_radius + moon_radius)) * 1.2
  angle_rad = 2.0 * math.atan(float(half_extent) / float(dist))
  camera.SetAngle(math.degrees(angle_rad))

  sun_node = Node(trf=sun_trf, apps=[sun_mat, sun_tex], shps=[sun_disk])
  venus_node = Node(apps=[venus_mat, venus_tex], shps=[venus_disk])
  venus_branch = Node(trf=venus_orbit, nodes=[Node(trf=venus_offset, nodes=[venus_node])])
  earth_node = Node(trf=earth_tilt, nodes=[Node(trf=earth_spin, apps=[earth_mat, earth_tex], shps=[earth_disk])])
  moon_node = Node(trf=moon_spin, apps=[moon_mat, moon_tex], shps=[moon_disk])
  earth_offset_node = Node(trf=earth_offset, nodes=[
    earth_node,
    Node(trf=moon_orbit, nodes=[Node(trf=moon_offset, nodes=[moon_node])])
  ])
  earth_branch = Node(trf=earth_orbit, nodes=[earth_offset_node])

  root = Node(shd_tex, nodes=[sun_node, venus_branch, earth_branch])

  global scene
  scene = Scene(root)
  scene.AddEngine(SolarSystemEngine(earth_orbit, earth_spin, moon_orbit, moon_spin,
                                    earth_orbit_speed_deg_per_sec=15.0,
                                    earth_spin_speed_deg_per_sec=60.0,
                                    moon_orbit_speed_deg_per_sec=60.0,
                                    moon_spin_speed_deg_per_sec=120.0,
                                    venus_orbit_trf=venus_orbit,
                                    venus_orbit_speed_deg_per_sec=20.0))


def update(dt):
  scene.Update(dt)


def display():
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  scene.Render(camera)


def keyboard(win, key, scancode, action, mods):
  if key == glfw.KEY_Q and action == glfw.PRESS:
    glfw.set_window_should_close(win, glfw.TRUE)


def main():
  if not glfw.init():
    return
  glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
  glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
  glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
  glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
  win = glfw.create_window(800, 800, "sun-earth-moon-venus", None, None)
  if not win:
    glfw.terminate()
    return
  glfw.set_key_callback(win, keyboard)
  glfw.make_context_current(win)
  print("OpenGL version:", glGetString(GL_VERSION))

  initialize()

  t0 = glfw.get_time()
  while not glfw.window_should_close(win):
    t = glfw.get_time()
    dt = t - t0
    t0 = t
    update(dt)
    display()
    glfw.swap_buffers(win)
    glfw.poll_events()

  glfw.terminate()

if __name__ == "__main__":
  main()
