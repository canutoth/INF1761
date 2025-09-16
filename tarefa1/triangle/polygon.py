from OpenGL.GL import *
import numpy as np
from shape import Shape

class Polygon (Shape):

    def __init__(self, coords=None, colors=None):

        # in case user doesnt provide color or coords, default is drawing an arrow
        
        if coords is None:
            coords = [
                (-0.8, -0.2),
                (0.0, -0.2),
                (0.0, -0.6),
                (0.8, 0.0),
                (0.0, 0.6),
                (0.0, 0.2),
                (-0.8, 0.2),
            ]
        if colors is None:
            
            colors = [
                (255, 0, 0),
                (255, 165, 0),
                (255, 255, 0),
                (0, 128, 0),
                (0, 0, 255),
                (75, 0, 130),
                (238, 130, 238),
            ]

        if len(coords) < 3:
            raise ValueError("Polygon needs at least 3 vertices")
        if len(colors) != len(coords):
            raise ValueError("colors must have the same length as coords")

        self._coords2 = np.array(coords, dtype=np.float32).reshape(-1, 2)
        self._colors3 = np.array(colors, dtype=np.uint8).reshape(-1, 3)

        indices = self._ear_clip(self._coords2)
        self._index_count = len(indices)
        self._indices = np.array(indices, dtype=np.uint32)

        self._create_buffers()

    def _create_buffers(self):
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        vbo_pos, vbo_col, ebo = glGenBuffers(3)
        self._vbo_pos = vbo_pos
        self._vbo_col = vbo_col
        self._ebo = ebo

        glBindBuffer(GL_ARRAY_BUFFER, self._vbo_pos)
        glBufferData(
            GL_ARRAY_BUFFER,
            self._coords2.nbytes,
            self._coords2,
            GL_STATIC_DRAW,
        )
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, self._vbo_col)
        glBufferData(
            GL_ARRAY_BUFFER,
            self._colors3.nbytes,
            self._colors3,
            GL_STATIC_DRAW,
        )
        glVertexAttribPointer(1, 3, GL_UNSIGNED_BYTE, GL_TRUE, 0, None)
        glEnableVertexAttribArray(1)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._ebo)
        glBufferData(
            GL_ELEMENT_ARRAY_BUFFER,
            self._indices.nbytes,
            self._indices,
            GL_STATIC_DRAW,
        )

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def Draw(self):
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, self._index_count, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

    @staticmethod
    def _area(poly):
        x = poly[:, 0]
        y = poly[:, 1]
        return 0.5 * np.sum(x * np.roll(y, -1) - y * np.roll(x, -1))

    @staticmethod
    def _is_convex(a, b, c, ccw):
        cross = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        return cross > 1e-10 if ccw else cross < -1e-10

    @staticmethod
    def _point_in_triangle(p, a, b, c):
        v0 = c - a
        v1 = b - a
        v2 = p - a
        den = v0[0] * v1[1] - v0[1] * v1[0]
        if abs(den) < 1e-12:
            return False
        u = (v2[0] * v1[1] - v2[1] * v1[0]) / den
        v = (v0[0] * v2[1] - v0[1] * v2[0]) / den
        return u >= -1e-12 and v >= -1e-12 and (u + v) <= 1 + 1e-12

    def _ear_clip(self, poly):
        n = poly.shape[0]
        if n == 3:
            return [0, 1, 2]

        ccw = self._area(poly) > 0

        idx = list(range(n))
        triangles = []

        guard = 0
        while len(idx) > 3 and guard < 5 * n * n:
            ear_found = False
            for i in range(len(idx)):
                i0 = idx[(i - 1) % len(idx)]
                i1 = idx[i]
                i2 = idx[(i + 1) % len(idx)]
                a, b, c = poly[i0], poly[i1], poly[i2]

                if not self._is_convex(a, b, c, ccw):
                    continue

                any_inside = False
                for j in idx:
                    if j in (i0, i1, i2):
                        continue
                    if self._point_in_triangle(poly[j], a, b, c):
                        any_inside = True
                        break
                if any_inside:
                    continue

                triangles.extend([i0, i1, i2])
                del idx[i]
                ear_found = True
                break

            if not ear_found:
                triangles = []
                for k in range(1, n - 1):
                    triangles.extend([0, k, k + 1])
                return triangles

            guard += 1

        if len(idx) == 3:
            triangles.extend(idx)
        return triangles
