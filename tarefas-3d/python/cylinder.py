from OpenGL.GL import *
from shape import Shape
import numpy as np
import math

class Cylinder(Shape):
    def __init__(self, nslices=32, nstacks=32):

        self.nslices = nslices
        self.nstacks = nstacks
        
        vertices = []
        normals = []
        texcoords = []
        indices = []

        for i in range(nstacks + 1):
            v = i / nstacks
            y = v - 0.5
            
            for j in range(nslices + 1):
                u = j / nslices
                theta = u * 2 * math.pi
                
                x = math.cos(theta)
                z = math.sin(theta)
                vertices.extend([x, y, z])
                
                normals.extend([x, 0, z])
                
                texcoords.extend([u, v])
        
        for i in range(nstacks):
            for j in range(nslices):
                first = i * (nslices + 1) + j
                second = first + nslices + 1
                
                indices.extend([first, second, first + 1])
                indices.extend([second, second + 1, first + 1])
        
        base_vertex_index = len(vertices) // 3
        
        center_bottom_index = len(vertices) // 3
        vertices.extend([0, -0.5, 0])
        normals.extend([0, -1, 0])
        texcoords.extend([0.5, 0.5])
        
        for j in range(nslices + 1):
            u = j / nslices
            theta = u * 2 * math.pi
            x = math.cos(theta)
            z = math.sin(theta)
            
            vertices.extend([x, -0.5, z])
            normals.extend([0, -1, 0])
            texcoords.extend([0.5 + 0.5 * x, 0.5 + 0.5 * z])
        
        for j in range(nslices):
            indices.extend([center_bottom_index, center_bottom_index + j + 1, center_bottom_index + j + 2])
        
        center_top_index = len(vertices) // 3
        vertices.extend([0, 0.5, 0])
        normals.extend([0, 1, 0])
        texcoords.extend([0.5, 0.5])
        
        for j in range(nslices + 1):
            u = j / nslices
            theta = u * 2 * math.pi
            x = math.cos(theta)
            z = math.sin(theta)
            
            vertices.extend([x, 0.5, z])
            normals.extend([0, 1, 0])
            texcoords.extend([0.5 + 0.5 * x, 0.5 + 0.5 * z])
        
        for j in range(nslices):
            indices.extend([center_top_index, center_top_index + j + 2, center_top_index + j + 1])
        
        vertices = np.array(vertices, dtype='float32')
        normals = np.array(normals, dtype='float32')
        texcoords = np.array(texcoords, dtype='float32')
        indices = np.array(indices, dtype='uint32')
        
        self.nind = len(indices)
        
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        
        buffers = glGenBuffers(4)
        
        glBindBuffer(GL_ARRAY_BUFFER, buffers[0])
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
        
        glBindBuffer(GL_ARRAY_BUFFER, buffers[1])
        glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(1)
        
        glBindBuffer(GL_ARRAY_BUFFER, buffers[2])
        glBufferData(GL_ARRAY_BUFFER, texcoords.nbytes, texcoords, GL_STATIC_DRAW)
        glVertexAttribPointer(3, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(3)
        
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, buffers[3])
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        
        glBindVertexArray(0)
    
    def Draw(self, st):
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self.nind, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
