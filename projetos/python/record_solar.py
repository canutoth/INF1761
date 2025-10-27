from OpenGL.GL import *
import glfw
import cv2
import numpy as np
import time
from pathlib import Path

# Import the solar system components
from main_solar import initialize, update, display
import main_solar


def init_scene(window_width: int, window_height: int):
    glViewport(0, 0, window_width, window_height)
    
    # Call the solar system initialization
    initialize()
    
    # Access the global camera and scene from main_solar
    return main_solar.camera, main_solar.scene


def render_frame(camera, scene, dt: float):
    # Update animation
    scene.Update(dt)
    
    # Render the scene
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    scene.Render(camera)


def main(
    out_path: str = "solar_system_recording.mp4",
    duration_sec: float = 10.0,
    fps: int = 30,
    width: int = 800,
    height: int = 800,
):
    if not glfw.init():
        print("Failed to initialize GLFW")
        return 1

    # Match your existing context hints
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

    window = glfw.create_window(width, height, "sun-earth-moon", None, None)
    if not window:
        print("Failed to create window")
        glfw.terminate()
        return 1

    glfw.make_context_current(window)
    glfw.swap_interval(1)  # vsync

    # Initialize scene (shaders, geometry, etc.)
    camera, scene = init_scene(width, height)

    # Prepare video writer (MP4)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_writer = cv2.VideoWriter(out_path, fourcc, fps, (width, height))
    if not video_writer.isOpened():
        print("Failed to open video writer for:", out_path)
        glfw.terminate()
        return 1

    # Ensure tight packing to avoid row alignment issues
    glPixelStorei(GL_PACK_ALIGNMENT, 1)

    total_frames = int(duration_sec * fps)
    frame_duration = 1.0 / float(fps)

    start_time = time.perf_counter()
    prev_time = start_time
    
    for frame_idx in range(total_frames):
        if glfw.window_should_close(window):
            break

        frame_start = time.perf_counter()
        current_time = frame_start
        dt = current_time - prev_time
        prev_time = current_time

        # Draw the scene
        render_frame(camera, scene, dt)

        # Read pixels from framebuffer (origin is bottom-left in OpenGL)
        # We'll read RGB then convert to BGR and flip vertically for OpenCV
        pixels = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
        img = np.frombuffer(pixels, dtype=np.uint8).reshape((height, width, 3))
        img = np.flipud(img)  # flip vertically
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        video_writer.write(img_bgr)

        # Present and process events
        glfw.swap_buffers(window)
        glfw.poll_events()

        # Frame pacing to target fps (coarse)
        elapsed = time.perf_counter() - frame_start
        remaining = frame_duration - elapsed
        if remaining > 0:
            time.sleep(remaining)

    # Cleanup
    video_writer.release()

    # Keep the window open a bit after recording to verify visually (optional)
    end_grace = 0.25
    while time.perf_counter() - start_time < duration_sec + end_grace and not glfw.window_should_close(window):
        current_time = time.perf_counter()
        dt = current_time - prev_time
        prev_time = current_time
        render_frame(camera, scene, dt)
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()
    print(f"Saved recording to: {out_path}")
    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Record the solar system animation to a video file.")
    parser.add_argument("--out", default="solar_system_recording.mp4", help="Output video path (default: solar_system_recording.mp4)")
    parser.add_argument("--duration", type=float, default=10.0, help="Duration in seconds (default: 10)")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second (default: 30)")
    parser.add_argument("--width", type=int, default=800, help="Window/video width (default: 800)")
    parser.add_argument("--height", type=int, default=800, help="Window/video height (default: 800)")

    args = parser.parse_args()
    raise SystemExit(main(args.out, args.duration, args.fps, args.width, args.height))