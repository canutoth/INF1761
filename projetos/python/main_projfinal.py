"""
Projeto Final - Implementação de Sombras
- Sombras Planares: projetadas no plano laranja
- Shadow Mapping: sombras em superfícies curvas (esferas)
- Cena: plano laranja + cubo azul + esfera vermelha + esfera verde
"""

import glfw
from nocull import NoCull
from polyoffset import PolygonOffset
from OpenGL.GL import (
  glClearColor,
  glEnable,
  glDisable,
  glClear,
  glGetString,
  glViewport,
  glCullFace,
  glPolygonOffset,
  glBlendFunc,
  GL_DEPTH_TEST,
  GL_CULL_FACE,
  GL_BLEND,
  GL_COLOR_BUFFER_BIT,
  GL_DEPTH_BUFFER_BIT,
  GL_VERSION,
  GL_TRUE,
  GL_FRONT,
  GL_BACK,
  GL_FILL,
  GL_POLYGON_OFFSET_FILL,
  GL_SRC_ALPHA,
  GL_ONE_MINUS_SRC_ALPHA,
)
import glm
from pathlib import Path
from shader import Shader
from color import Color
from transform import Transform
from node import Node
from scene import Scene
from sphere import Sphere
from cube import Cube
from quad import Quad
from camera3d import Camera3D
from light import Light
from material import Material
from texdepth import TexDepth
from framebuffer import Framebuffer

# Global variables
global active_camera
global scene
global light
global shadow_fb, shadow_texture
global width, height
global vp_var

# Shadow map resolution
SHADOW_WIDTH = 2048
SHADOW_HEIGHT = 2048

def initialize():
  """Inicializa a cena com objetos e sombras"""
  glClearColor(0.2, 0.2, 0.3, 1.0)
  glEnable(GL_DEPTH_TEST)
  glEnable(GL_CULL_FACE)
  glEnable(GL_BLEND)
  glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

  # Câmera
  global active_camera
  active_camera = Camera3D(5, 5, 8)
  active_camera.SetCenter(0, 1, 0)
  active_camera.SetUpDir(0, 1, 0)
  active_camera.SetAngle(45.0)
  active_camera.SetZPlanes(0.1, 100.0)
  
  # Criar arcball para rotação interativa
  arcball = active_camera.CreateArcball()

  # Luz posicional (simula luz do sol)
  global light
  light = Light(5.0, 8.0, 5.0, 1.0)  # Luz posicional
  light.SetDiffuse(1.0, 1.0, 1.0)
  light.SetSpecular(1.0, 1.0, 1.0)
  light.SetAmbient(0.2, 0.2, 0.2)

  root_dir = Path(__file__).resolve().parent.parent

  # ===== SHADERS =====
  
  # Shader para renderização normal com iluminação
  shd_phong = Shader(space="world")
  shd_phong.AttachVertexShader(root_dir / "shaders/shadow/phong_vertex.glsl")
  shd_phong.AttachFragmentShader(root_dir / "shaders/shadow/phong_fragment.glsl")
  shd_phong.Link()

  # Shader para renderizar depth map (shadow map)
  shd_depth = Shader()
  shd_depth.AttachVertexShader(root_dir / "shaders/shadow/depth_vertex.glsl")
  shd_depth.AttachFragmentShader(root_dir / "shaders/shadow/depth_fragment.glsl")
  shd_depth.Link()

  # Shader para sombras planares
  shd_planar_shadow = Shader(space="world")
  shd_planar_shadow.AttachVertexShader(root_dir / "shaders/shadow/planar_shadow_vertex.glsl")
  shd_planar_shadow.AttachFragmentShader(root_dir / "shaders/shadow/planar_shadow_fragment.glsl")
  shd_planar_shadow.Link()

  # Shader para renderização com shadow mapping
  shd_shadow_map = Shader(space="world")
  shd_shadow_map.AttachVertexShader(root_dir / "shaders/shadow/shadow_map_vertex.glsl")
  shd_shadow_map.AttachFragmentShader(root_dir / "shaders/shadow/shadow_map_fragment.glsl")
  shd_shadow_map.Link()
  
  # ===== MATERIAIS =====
  
  # Material laranja para o plano
  mat_orange = Material()
  mat_orange.SetAmbient(0.8, 0.4, 0.1)
  mat_orange.SetDiffuse(0.9, 0.5, 0.2)
  mat_orange.SetSpecular(0.3, 0.3, 0.3)
  mat_orange.SetShininess(32.0)

  # Material azul para o cubo
  mat_blue = Material()
  mat_blue.SetAmbient(0.1, 0.1, 0.5)
  mat_blue.SetDiffuse(0.2, 0.2, 0.8)
  mat_blue.SetSpecular(0.5, 0.5, 0.5)
  mat_blue.SetShininess(32.0)

  # Material vermelho para esfera grande
  mat_red = Material()
  mat_red.SetAmbient(0.5, 0.1, 0.1)
  mat_red.SetDiffuse(0.8, 0.2, 0.2)
  mat_red.SetSpecular(0.7, 0.7, 0.7)
  mat_red.SetShininess(64.0)

  # Material verde para esfera pequena
  mat_green = Material()
  mat_green.SetAmbient(0.1, 0.5, 0.1)
  mat_green.SetDiffuse(0.2, 0.8, 0.2)
  mat_green.SetSpecular(0.5, 0.5, 0.5)
  mat_green.SetShininess(32.0)

  # Material preto para sombras planares
  mat_shadow = Material()
  mat_shadow.SetAmbient(0.0, 0.0, 0.0)
  mat_shadow.SetDiffuse(0.0, 0.0, 0.0)
  mat_shadow.SetSpecular(0.0, 0.0, 0.0)
  mat_shadow.SetOpacity(0.5)
  
  # Variável para passar VP matrix para sombra planar
  from variable import Variable
  global vp_var
  vp_var = Variable("Vp", glm.mat4(1.0))

  # ===== CONSTRUÇÃO DA CENA =====
  global scene
  root = Node()

  # Plano laranja (no chão, y=0)
  plane_trans = Transform()
  plane_trans.Scale(4.0, 4.0, 4.0)
  plane_trans.Rotate(-90, 1, 0, 0)  # Plano horizontal
  plane_node = Node(
    shader=shd_shadow_map,
    trf=plane_trans,
    apps=[mat_orange],
    shps=[Quad(10, 10)]
  )
  root.AddNode(plane_node)

  # Cubo azul
  cube_trans = Transform()
  cube_trans.Translate(1.5, 0.2, -1.0)
  cube_trans.Scale(0.8, 0.8, 0.8)
  cube_node = Node(
    shader=shd_phong,
    trf=cube_trans,
    apps=[mat_blue],
    shps=[Cube()]
  )
  
  # Sombra planar do cubo
  cube_shadow_node = Node(
    shader=shd_planar_shadow,
    trf=cube_trans,
    apps=[mat_shadow, PolygonOffset(-1, -1), NoCull(), vp_var],
    shps=[Cube()]
  )
  root.AddNode(cube_shadow_node)
  root.AddNode(cube_node)

  # Esfera vermelha grande
  sphere_trans = Transform()
  sphere_trans.Translate(0.5, 0.8, -2.5)
  sphere_trans.Scale(0.8, 0.8, 0.8)
  sphere_red_node = Node(
    shader=shd_shadow_map,
    trf=sphere_trans,
    apps=[mat_red],
    shps=[Sphere(64, 64)]
  )
  root.AddNode(sphere_red_node)

  # Esfera verde pequena
  sphere_green_trans = Transform()
  sphere_green_trans.Translate(3, 0.3, -2.0)
  sphere_green_trans.Scale(0.3, 0.3, 0.3)
  sphere_green_node = Node(
    shader=shd_shadow_map,
    trf=sphere_green_trans,
    apps=[mat_green],
    shps=[Sphere(64, 64)]
  )
  root.AddNode(sphere_green_node)

  # Criar cena
  scene = Scene(root)
  scene.SetLight(light)

  # ===== SHADOW MAP SETUP =====
  global shadow_fb, shadow_texture
  # TexDepth expects a uniform name and size: (varname, width, height)
  shadow_texture = TexDepth("shadowMap", SHADOW_WIDTH, SHADOW_HEIGHT)
  # Enable depth comparison mode (useful if sampling shadow map as sampler2D)
  try:
    shadow_texture.SetCompareMode()
  except Exception:
    pass
  # Framebuffer takes depth and optional color textures
  shadow_fb = Framebuffer(depth=shadow_texture)

  print("OpenGL version:", glGetString(GL_VERSION).decode())
  print("Controles:")
  print("  Mouse: Rotacionar câmera")
  print("  Scroll: Zoom")
  print("  ESC: Sair")

def display():
  """Renderiza a cena com sombras"""
  
  # Atualizar VP matrix para sombras planares
  vp_matrix = active_camera.GetProjMatrix() * active_camera.GetViewMatrix()
  vp_var.SetValue(vp_matrix)
  
  glViewport(0, 0, width, height)
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  glCullFace(GL_BACK)
  
  # Renderizar cena
  scene.Render(active_camera)
  
def keyboard(window, key, scancode, action, mods):
  """Trata eventos de teclado"""
  if action == glfw.PRESS or action == glfw.REPEAT:
    if key == glfw.KEY_ESCAPE:
      glfw.set_window_should_close(window, GL_TRUE)

def mouse_button(window, button, action, mods):
  """Trata eventos de botão do mouse"""
  arcball = active_camera.GetArcball()
  if arcball and button == glfw.MOUSE_BUTTON_LEFT:
    if action == glfw.PRESS:
      xpos, ypos = glfw.get_cursor_pos(window)
      arcball.StartMotion(xpos, ypos)
    elif action == glfw.RELEASE:
      arcball.StopMotion()

def cursor_pos(window, xpos, ypos):
  """Trata movimentação do mouse"""
  arcball = active_camera.GetArcball()
  if arcball:
    arcball.Move(xpos, ypos)

def scroll(window, xoffset, yoffset):
  """Trata scroll do mouse (zoom)"""
  arcball = active_camera.GetArcball()
  if arcball:
    arcball.Zoom(yoffset * 0.5)

def main():
  """Função principal"""
  global width, height
  width, height = 1024, 768

  # Inicializar GLFW
  if not glfw.init():
    return
  
  # Configurar contexto OpenGL
  glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
  glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
  glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
  glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
  
  # Criar janela
  window = glfw.create_window(width, height, "Projeto Final - Sombras", None, None)
  if not window:
    glfw.terminate()
    return
  
  glfw.make_context_current(window)
  
  # Registrar callbacks básicos
  glfw.set_key_callback(window, keyboard)
  
  # Inicializar cena (cria câmera e arcball)
  initialize()
  
  # Conectar arcball aos eventos do GLFW
  arc = active_camera.GetArcball()
  if arc:
    arc.Attach(window)
  
  # Loop principal
  while not glfw.window_should_close(window):
    display()
    glfw.swap_buffers(window)
    glfw.poll_events()
  
  glfw.terminate()

if __name__ == "__main__":
  main()
