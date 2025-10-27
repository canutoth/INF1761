import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import *
from PIL import Image
import numpy as np
import time

import glm
from camera3d import *
from light import *
from shader import *
from material import *
from transform import *
from node import *
from scene import *
from cube import * 
from sphere import * 

def main():
    
    if not glfw.init():
        return
    
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR,4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR,1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT,GL_TRUE)
    win = glfw.create_window(800, 800, "first 3d scene", None, None)

    if not win:
        glfw.terminate()
        return
    glfw.set_key_callback(win,keyboard)

    glfw.make_context_current(win)
    print("OpenGL version: ",glGetString(GL_VERSION))
    print("Controls:")
    print(">> Mouse: Click and drag to rotate the scene (arcball)")
    print(">> S key: Take screenshot")
    print(">> Q key: Quit")

    fb_w, fb_h = glfw.get_framebuffer_size(win)
    glViewport(0, 0, fb_w, fb_h)

    def on_fb_resize(win, w, h):
        glViewport(0, 0, w, h)

    glfw.set_framebuffer_size_callback(win, on_fb_resize)

    initialize(win)
    
    while not glfw.window_should_close(win):
        display(win)
        glfw.swap_buffers(win)
        glfw.poll_events()

    glfw.terminate()

viewer_pos = glm.vec3(2.0, 3.5, 4.0)

def initialize (win):
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)

    global scene
    global camera
    camera = Camera3D(viewer_pos[0], viewer_pos[1], viewer_pos[2])
    camera.CreateArcball().Attach(win)

    light = Light(0.0, 0.0, 0.0, 1.0, "camera")
    light.SetAmbient(0.25, 0.25, 0.25)
    light.SetDiffuse(0.9, 0.9, 0.9)
    light.SetSpecular(1.0, 1.0, 1.0)

    base_mat = Material(0.95, 0.95, 0.95)
    base_mat.SetSpecular(0.0, 0.0, 0.0)
    base_mat.SetShininess(8.0)

    cubo_mat = Material(0.90, 0.75, 0.25)
    cubo_mat.SetSpecular(0.9, 0.8, 0.5)
    cubo_mat.SetShininess(48.0)

    esfera_g = Material(0.65, 0.90, 0.65)
    esfera_g.SetSpecular(1.0, 1.0, 1.0)
    esfera_g.SetShininess(64.0)

    esfera_r = Material(0.95, 0.55, 0.55)
    esfera_r.SetSpecular(1.0, 1.0, 1.0)
    esfera_r.SetShininess(64.0)

    cube = Cube()
    sphere = Sphere(32, 32)

    shader = Shader(light, "camera")
    shader.AttachVertexShader("shaders/per_fragment_vertex.glsl")
    shader.AttachFragmentShader("shaders/per_fragment_fragment.glsl")
    shader.Link()

    t_base = Transform()
    t_base.Scale(4.0, 0.4, 3.0)
    t_base.Translate(0.0, -1.2, 0.0)

    t_cubo = Transform()
    t_cubo.Scale(1.4, 0.5, 1.0)
    t_cubo.Translate(-0.15, -0.15, 0.0)

    t_esf_verde = Transform()
    t_esf_verde.Scale(0.35, 0.35, 0.35)
    t_esf_verde.Translate(0.0, 2, 0.0)

    t_esf_verm = Transform()
    t_esf_verm.Scale(0.70, 0.70, 0.70)
    t_esf_verm.Translate(1.9, 0.8, 1.5)

    root = Node(shader, nodes=[
        Node(None, t_base, [base_mat], [cube]),
        Node(None, t_cubo, [cubo_mat], [cube]),
        Node(None, t_esf_verde, [esfera_g], [sphere]),
        Node(None, t_esf_verm,  [esfera_r], [sphere]),
    ])

    scene = Scene(root)


def display (win):
    global scene
    global camera
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
    scene.Render(camera)

def save_screenshot():
    viewport = glGetIntegerv(GL_VIEWPORT)
    x, y, width, height = viewport[0], viewport[1], viewport[2], viewport[3]
    
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    pixels = glReadPixels(x, y, width, height, GL_RGB, GL_UNSIGNED_BYTE)
    
    image = Image.frombytes("RGB", (width, height), pixels)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    
    image.save(filename)
    print(f"Screenshot saved as: {filename}")

def keyboard (win, key, scancode, action, mods):
    if key == glfw.KEY_Q and action == glfw.PRESS:
        glfw.set_window_should_close(win, glfw.TRUE)
    elif key == glfw.KEY_S and action == glfw.PRESS:
        save_screenshot()

if __name__ == "__main__":
    main()
