from OpenGL.GL import *
import glfw
from pathlib import Path
from shader import Shader
from polygon import Polygon

global poly, shd

def keyboard(win, key, scancode, action, mods):
    if key == glfw.KEY_Q and action == glfw.PRESS:
        glfw.set_window_should_close(win, glfw.TRUE)

def initialize():
    global poly, shd
    glClearColor(1, 1, 1, 1)

    colors, coords = None, None

    # heart
    coords = [
        (0.0, 0.5),
        (-0.5, 0.8),
        (-0.8, 0.5),
        (-0.6, 0.0),
        (0.0, -0.6),
        (0.6, 0.0),
        (0.8, 0.5),
        (0.5, 0.8),
    ]
    colors = [
        (255, 0, 0),
        (255, 100, 100),
        (255, 50, 50),
        (200, 0, 0),
        (255, 0, 0),
        (255, 50, 50),
        (255, 100, 100),
        (255, 0, 0),
    ]

    # # star
    # coords = [
    #     (0.0, 0.6),
    #     (-0.2, 0.2),
    #     (-0.6, 0.2),
    #     (-0.3, -0.2),
    #     (-0.4, -0.6),
    #     (0.0, -0.4),
    #     (0.4, -0.6),
    #     (0.3, -0.2),
    #     (0.6, 0.2),
    #     (0.2, 0.2),
    # ]

    # colors = [
    #     (0, 0, 255),
    #     (75, 0, 130),
    #     (138, 43, 226),
    #     (148, 0, 211),
    #     (186, 85, 211),
    #     (216, 191, 216),
    #     (186, 85, 211),
    #     (148, 0, 211),
    #     (138, 43, 226),
    #     (75, 0, 130),
    # ]

    # # example showed
    # coords = [
    #     (-0.1, 0.2),
    #     (0.6,0.6),
    #     (0.4,-0.4),
    #     (-0.4,-0.6),
    #     (-0.4,0.6)
    # ]

    # colors = [
    #     (255, 0, 0),
    #     (0, 255, 0),
    #     (0, 0, 255),
    #     (255, 255, 0),
    #     (255, 0, 255)
    # ]

    poly = Polygon(coords=coords, colors=colors)
    shd = Shader()
    base_dir = Path(__file__).resolve().parent
    vsh = base_dir / "shaders" / "vertex.glsl"
    fsh = base_dir / "shaders" / "fragment.glsl"
    shd.AttachVertexShader(str(vsh))
    shd.AttachFragmentShader(str(fsh))
    shd.Link()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    shd.UseProgram()
    poly.Draw()

def main():
    if not glfw.init():
        return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    win = glfw.create_window(800, 600, "concave polygon", None, None)
    if not win:
        glfw.terminate()
        return
    glfw.set_key_callback(win, keyboard)
    glfw.make_context_current(win)
    print("OpenGL version: ", glGetString(GL_VERSION))

    initialize()

    while not glfw.window_should_close(win):
        display()
        glfw.swap_buffers(win)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
