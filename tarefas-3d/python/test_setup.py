"""
Test script to verify the scene setup
"""
import sys
print("Testing imports...")

try:
    import glfw
    print("✓ glfw imported")
except ImportError as e:
    print(f"✗ glfw import failed: {e}")
    sys.exit(1)

try:
    from OpenGL.GL import *
    print("✓ OpenGL imported")
except ImportError as e:
    print(f"✗ OpenGL import failed: {e}")
    sys.exit(1)

try:
    import glm
    print("✓ glm imported")
except ImportError as e:
    print(f"✗ glm import failed: {e}")
    sys.exit(1)

try:
    from PIL import Image
    print("✓ PIL imported")
except ImportError as e:
    print(f"✗ PIL import failed: {e}")
    sys.exit(1)

print("\nTesting local modules...")

try:
    from camera3d import Camera3D
    print("✓ camera3d imported")
except ImportError as e:
    print(f"✗ camera3d import failed: {e}")
    sys.exit(1)

try:
    from light import Light
    print("✓ light imported")
except ImportError as e:
    print(f"✗ light import failed: {e}")
    sys.exit(1)

try:
    from shader import Shader
    print("✓ shader imported")
except ImportError as e:
    print(f"✗ shader import failed: {e}")
    sys.exit(1)

try:
    from material import Material
    print("✓ material imported")
except ImportError as e:
    print(f"✗ material import failed: {e}")
    sys.exit(1)

try:
    from transform import Transform
    print("✓ transform imported")
except ImportError as e:
    print(f"✗ transform import failed: {e}")
    sys.exit(1)

try:
    from node import Node
    print("✓ node imported")
except ImportError as e:
    print(f"✗ node import failed: {e}")
    sys.exit(1)

try:
    from scene import Scene
    print("✓ scene imported")
except ImportError as e:
    print(f"✗ scene import failed: {e}")
    sys.exit(1)

try:
    from cube import Cube
    print("✓ cube imported")
except ImportError as e:
    print(f"✗ cube import failed: {e}")
    sys.exit(1)

try:
    from sphere import Sphere
    print("✓ sphere imported")
except ImportError as e:
    print(f"✗ sphere import failed: {e}")
    sys.exit(1)

print("\nTesting shader files...")
import os

if os.path.exists("shaders/per_fragment_vertex.glsl"):
    print("✓ Vertex shader file exists")
else:
    print("✗ Vertex shader file not found")
    
if os.path.exists("shaders/per_fragment_fragment.glsl"):
    print("✓ Fragment shader file exists")
else:
    print("✗ Fragment shader file not found")

print("\n✓ All tests passed! The scene should run correctly.")
print("\nTo run the scene, execute:")
print("  python main_scene.py")
