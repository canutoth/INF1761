import glm
from engine import Engine
from transform import Transform

class CameraEngine(Engine):
    def __init__(self, camera, earth_node, moon_node):
        self.camera = camera
        self.earth_node = earth_node 
        self.moon_node = moon_node   

    def Update(self, dt):
        try:
            earth_matrix = self.earth_node.GetModelMatrix()
            moon_matrix = self.moon_node.GetModelMatrix()
        except Exception as e:
            print(f"Erro ao obter matrizes para CameraEngine: {e}")
            return

        earth_pos = glm.vec3(earth_matrix[3])
        moon_pos = glm.vec3(moon_matrix[3])

        self.camera.SetEye(earth_pos.x, earth_pos.y, earth_pos.z)
        self.camera.SetCenter(moon_pos.x, moon_pos.y, moon_pos.z)
        
        self.camera.SetUpDir(0, 1, 0)