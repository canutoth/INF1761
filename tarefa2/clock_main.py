from OpenGL.GL import *
import glfw
from pathlib import Path

from clock import Clock
from shader import Shader

global clock_obj, shd

def keyboard(win, key, scancode, action, mods):
    if key == glfw.KEY_Q and action == glfw.PRESS:
        glfw.set_window_should_close(win, glfw.TRUE)

def initialize():
    global clock_obj, shd
    glClearColor(156/255, 207/255, 255/255, 1)
    clock_obj = Clock()
    shd = Shader()
    base_dir = Path(__file__).resolve().parent
    vsh = base_dir / "shaders" / "vertex.glsl"
    fsh = base_dir / "shaders" / "fragment.glsl"
    if not vsh.exists() or not fsh.exists():
        print("shader files not found:", vsh, fsh)
    shd.AttachVertexShader(str(vsh))
    shd.AttachFragmentShader(str(fsh))
    shd.Link()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    shd.UseProgram()
    clock_obj.Draw()

def main():

    if not glfw.init():
        return
    
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    
    win = glfw.create_window(800, 800, "clock", None, None)
    if not win:
        glfw.terminate()
        return
    
    glfw.set_key_callback(win, keyboard)
    
    glfw.make_context_current(win)
    glfw.swap_interval(1)
    
    initialize()
    
    while not glfw.window_should_close(win):
        display()
        
        glfw.swap_buffers(win)
        
        glfw.poll_events()
    
    glfw.terminate()

if __name__ == '__main__':
    main()
