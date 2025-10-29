"""
Projeto 2 - Sistema Solar 3D com Iluminação por Fragmento
- Sol, Terra, Lua e Vênus como esferas 3D
- Iluminação por fragmento com luz posicionada no Sol
- Movimentos de translação e rotação dos astros
"""

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
from pathlib import Path
from shader import Shader
from color import Color
from transform import Transform
from node import Node
from scene import Scene
from sphere import Sphere
from texture import Texture
from camera3d import Camera3D
from light import Light
from material import Material
from skybox import SkyBox
from texcube import TexCube
from solar_system_engine_proj2 import SolarSystemEngineProj2
from camera_engine import CameraEngine

global camera_global, camera_earth, active_camera
global earth_frame_node, moon_frame_node

def initialize():
  """Inicializa a cena 3D do sistema solar"""
  glClearColor(0.0, 0.0, 0.05, 1.0)  # Cor de fundo escura (espaço)
  glEnable(GL_DEPTH_TEST)
  glEnable(GL_CULL_FACE)

  # Câmeras
  global camera_global, camera_earth, active_camera
  
  # Câmera 1: Global
  camera_global = Camera3D(0, 15, 30)  # Posição da câmera
  camera_global.SetCenter(0, 0, 0)     # Olhando para o centro (Sol)
  camera_global.SetUpDir(0, 1, 0)

  # Câmera 2: Na Terra 
  camera_earth = Camera3D(0, 0, 0)
  camera_earth.SetUpDir(0, 1, 0)
  
  # Define a câmera ativa inicial como a global
  active_camera = camera_global

  root_dir = Path(__file__).resolve().parent.parent

  # Shader de iluminação por fragmento (para planetas)
  global shd_light
  shd_light = Shader(space="world")  # Iluminação em espaço mundial
  shd_light.AttachVertexShader(root_dir / "shaders/ilum_vert/per_fragment_vertex.glsl")
  shd_light.AttachFragmentShader(root_dir / "shaders/ilum_vert/per_fragment_fragment.glsl")
  shd_light.Link()

  # Shader customizado para o Sol
  global shd_sun
  shd_sun = Shader(space="world")
  shd_sun.AttachVertexShader(root_dir / "shaders/ilum_vert/sun_vertex.glsl")
  shd_sun.AttachFragmentShader(root_dir / "shaders/ilum_vert/sun_fragment.glsl")
  shd_sun.Link()

  # Shader customizado para o SkyBox
  global shd_skybox
  shd_skybox = Shader(space="world")
  shd_skybox.AttachVertexShader(root_dir / "shaders/ilum_vert/skybox_vertex.glsl")
  shd_skybox.AttachFragmentShader(root_dir / "shaders/ilum_vert/skybox_fragment.glsl")
  shd_skybox.Link()

  # Luz posicionada no Sol
  global light
  light = Light(0, 0, 0, 1, "world")  # Luz pontual na posição do Sol
  light.SetAmbient(0.3, 0.3, 0.3)  # Ambiente mais forte para ver o Sol
  light.SetDiffuse(1.0, 1.0, 0.9)
  light.SetSpecular(1.0, 1.0, 1.0)

  # Texturas
  sun_tex = Texture("decal", root_dir / "images/sun_texture.jpg")
  earth_tex = Texture("decal", root_dir / "images/earth.jpg")
  venus_tex = Texture("decal", root_dir / "images/venus_texture.jpg")
  moon_tex = Texture("decal", root_dir / "images/moon_texture.jpg")

  # Esferas (geometria 3D)
  sun_sphere = Sphere(64, 64)
  earth_sphere = Sphere(48, 48)
  venus_sphere = Sphere(48, 48)
  moon_sphere = Sphere(32, 32)

  # Materiais dos astros
  # Sol - emissor de luz (alta componente ambiente, mas com algum contraste)
  sun_material = Material()
  sun_material.SetAmbient(0.9, 0.8, 0.3)  # Amarelo/laranja intenso
  sun_material.SetDiffuse(1.0, 0.9, 0.4)   # Cor quente
  sun_material.SetSpecular(1.0, 1.0, 0.8)
  sun_material.SetShininess(50.0)

  # Terra - material padrão
  earth_material = Material()
  earth_material.SetAmbient(0.3, 0.3, 0.4)
  earth_material.SetDiffuse(0.7, 0.7, 0.8)
  earth_material.SetSpecular(0.5, 0.5, 0.5)
  earth_material.SetShininess(32.0)

  # Vênus - material com tom dourado
  venus_material = Material()
  venus_material.SetAmbient(0.4, 0.35, 0.25)
  venus_material.SetDiffuse(0.8, 0.7, 0.5)
  venus_material.SetSpecular(0.6, 0.6, 0.4)
  venus_material.SetShininess(64.0)

  # Lua - material menos reflexivo
  moon_material = Material()
  moon_material.SetAmbient(0.3, 0.3, 0.3)
  moon_material.SetDiffuse(0.6, 0.6, 0.6)
  moon_material.SetSpecular(0.2, 0.2, 0.2)
  moon_material.SetShininess(16.0)

  # Transformações e dimensões
  sun_radius = 3.0
  earth_radius = 0.8
  venus_radius = 0.7
  moon_radius = 0.3

  # Sol (centro)
  sun_trf = Transform()
  sun_trf.Scale(sun_radius, sun_radius, sun_radius)
  sun_spin = Transform()  # Rotação do Sol

  # Vênus (entre Sol e Terra)
  venus_orbit_radius = 8.0
  venus_orbit = Transform()
  venus_offset = Transform()
  venus_offset.Translate(venus_orbit_radius, 0.0, 0.0)
  venus_scale = Transform()
  venus_scale.Scale(venus_radius, venus_radius, venus_radius)
  venus_spin = Transform()

  # Terra
  earth_orbit_radius = 15.0
  earth_orbit = Transform()
  earth_offset = Transform()
  earth_offset.Translate(earth_orbit_radius, 0.0, 0.0)
  earth_scale = Transform()
  earth_scale.Scale(earth_radius, earth_radius, earth_radius)
  earth_spin = Transform()
  
  # Inclinação do eixo da Terra (23.5 graus)
  earth_tilt = Transform()
  earth_tilt.Rotate(23.5, 0, 0, 1)

  # Lua (orbita a Terra)
  moon_orbit_radius = 2.0
  moon_orbit = Transform()
  moon_offset = Transform()
  moon_offset.Translate(moon_orbit_radius, 0.0, 0.0)
  moon_scale = Transform()
  moon_scale.Scale(moon_radius, moon_radius, moon_radius)
  moon_spin = Transform()

  # Hierarquia de nós da cena
  global earth_frame_node, moon_frame_node

  # Sol (com shader customizado para mostrar manchas)
  sun_node = Node(
    shader=shd_sun,
    trf=sun_trf,
    nodes=[
      Node(
        trf=sun_spin,
        apps=[sun_material, sun_tex],
        shps=[sun_sphere]
      )
    ]
  )

  # Vênus
  venus_node = Node(
    trf=venus_orbit,
    nodes=[
      Node(
        trf=venus_offset,
        nodes=[
          Node(
            trf=venus_spin,
            nodes=[
              Node(
                trf=venus_scale,
                apps=[venus_material, venus_tex],
                shps=[venus_sphere]
              )
            ]
          )
        ]
      )
    ]
  )

  # Terra com Lua
  moon_frame_node = Node(
                      trf=moon_offset,
                      nodes=[
                        Node(
                          trf=moon_spin,
                          nodes=[
                            Node(
                              trf=moon_scale,
                              apps=[moon_material, moon_tex],
                              shps=[moon_sphere]
                            )
                          ]
                        )
                      ]
                    )
  
  earth_frame_node = Node(
                      trf=earth_offset,
                      nodes=[
                        # Terra
                        Node(
                          trf=earth_tilt,
                          nodes=[
                            Node(
                              trf=earth_spin,
                              nodes=[
                                Node(
                                  trf=earth_scale,
                                  apps=[earth_material, earth_tex],
                                  shps=[earth_sphere]
                                )
                              ]
                            )
                          ]
                        ),
                        # Lua
                        Node(
                          trf=moon_orbit,
                          nodes=[ 
                            moon_frame_node
                          ]
                        )
                      ]
                    )

  earth_branch = Node(
    trf=earth_orbit,
    nodes=[ 
      earth_frame_node
    ]
  )

  # Montando o SkyBox
  skybox = SkyBox()

  skybox_tex = TexCube("skybox", root_dir / "images/a.jpg")
  skybox_branch = Node(
                        shader = shd_skybox,
                        apps=[
                          skybox_tex
                        ], 
                        shps=[skybox]
                      )

  # Raiz da cena
  root = Node(shd_light, nodes=[skybox_branch, sun_node, venus_node, earth_branch])

  # Cena e engine
  global scene
  scene = Scene(root)
  scene.SetLight(light)
  
  scene.AddEngine(
    SolarSystemEngineProj2(
      sun_spin_trf=sun_spin,
      earth_orbit_trf=earth_orbit,
      earth_spin_trf=earth_spin,
      moon_orbit_trf=moon_orbit,
      moon_spin_trf=moon_spin,
      venus_orbit_trf=venus_orbit,
      venus_spin_trf=venus_spin,
      sun_spin_speed_deg_per_sec=10.0,
      earth_orbit_speed_deg_per_sec=15.0,
      earth_spin_speed_deg_per_sec=50.0,
      moon_orbit_speed_deg_per_sec=80.0,
      moon_spin_speed_deg_per_sec=80.0,
      venus_orbit_speed_deg_per_sec=25.0,
      venus_spin_speed_deg_per_sec=40.0
    )
  )

  scene.AddEngine(
      CameraEngine(
          camera=camera_earth,
          earth_node=earth_frame_node,
          moon_node=moon_frame_node
      )
  )


def update(dt):
  """Atualiza a cena"""
  scene.Update(dt)


def display():
  """Renderiza a cena"""
  global active_camera
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  scene.Render(active_camera)


def keyboard(win, key, scancode, action, mods):
  """Tratamento de teclado"""
  global active_camera, camera_global, camera_earth

  if key == glfw.KEY_Q and action == glfw.PRESS:
    glfw.set_window_should_close(win, glfw.TRUE)
  elif key == glfw.KEY_ESCAPE and action == glfw.PRESS:
    glfw.set_window_should_close(win, glfw.TRUE)
  elif key == glfw.KEY_C and action == glfw.PRESS:
    # Realiza a troca das câmeras
    if active_camera == camera_global:
      active_camera = camera_earth
      print("Câmera: Visão da Terra -> Lua")
    else:
      active_camera = camera_global
      print("Câmera: Visão Global")


def main():
  """Função principal"""
  if not glfw.init():
    return
  
  glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
  glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
  glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
  glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
  
  win = glfw.create_window(1024, 768, "Projeto 2 - Sistema Solar 3D", None, None)
  if not win:
    glfw.terminate()
    return
  
  glfw.set_key_callback(win, keyboard)
  glfw.make_context_current(win)

  #print("OpenGL version:", glGetString(GL_VERSION).decode('utf-8'))

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
