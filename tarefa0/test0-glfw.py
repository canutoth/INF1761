from OpenGL.GL import *
import glfw

def initialize (win):
    glClearColor(1,1,1,1)

def display (win):
    glClear(GL_COLOR_BUFFER_BIT)

def keyboard (win, key, scancode, action, mods):
   if key == glfw.KEY_Q and action == glfw.PRESS:
      glfw.set_window_should_close(win,glfw.TRUE)

def resize (win, width, height):
    glViewport(0,0,width,height)

def cursorpos (win, xpos, ypos):
    wn_w, wn_h = glfw.get_window_size(win)
    fb_w, fb_h = glfw.get_framebuffer_size(win)
    x = xpos * fb_w / wn_w
    y = (wn_h - ypos) * fb_w / wn_w
    print("(x,y): ",x,", ",y)

def dummy (win, xpos, ypos):
    pass

def mousebutton (win, button, action, mods):
    if action == glfw.PRESS:
        if button == glfw.MOUSE_BUTTON_1:
            print("button 1")
        elif button == glfw.MOUSE_BUTTON_2:
            print("button 2")
        elif button == glfw.MOUSE_BUTTON_3:
            print("button 3")
        glfw.set_cursor_pos_callback(win,cursorpos)
    else:
        glfw.set_cursor_pos_callback(win,dummy)

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR,4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR,1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT,GL_TRUE)
    win = glfw.create_window(640, 480, "Test", None, None)
    if not win:
        glfw.terminate()
        return
    glfw.set_key_callback(win,keyboard)
    glfw.set_mouse_button_callback(win,mousebutton)

    # Make the window's context current
    glfw.make_context_current(win)
    print("OpenGL version: ",glGetString(GL_VERSION))

    initialize(win)

    # Loop until the user closes the window
    while not glfw.window_should_close(win):
        # Render here, e.g. using pyOpenGL
        display(win)

        # Swap front and back buffers
        glfw.swap_buffers(win)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()