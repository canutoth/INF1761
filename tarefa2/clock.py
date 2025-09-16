from OpenGL.GL import *
import numpy as np
import math
import time
import ctypes

class Clock():
    def __init__(self):
        # clock face (inner circle)
        self.clock_face_coords = []
        self.clock_face_colors = []
        
        # clock face (outer circle)
        center = (0.0, 0.0)
        radius = 0.8
        segments = 60
        
        # center
        self.clock_face_coords.append(center)
        self.clock_face_colors.append((240, 240, 240))
        
        # circle points
        for i in range(segments + 1):
            angle = 2 * math.pi * i / segments
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            self.clock_face_coords.append((x, y))
            self.clock_face_colors.append((240, 240, 240))
        
        # hour markers
        self.hour_markers_coords = []
        self.hour_markers_colors = []
        
        for hour in range(12):
            angle = math.pi/2 - (hour * 2 * math.pi / 12)  # start from 12 o'clock
            
            # outer point
            outer_radius = 0.75
            inner_radius = 0.65
            
            x_outer = center[0] + outer_radius * math.cos(angle)
            y_outer = center[1] + outer_radius * math.sin(angle)
            x_inner = center[0] + inner_radius * math.cos(angle)
            y_inner = center[1] + inner_radius * math.sin(angle)
            
            # create a thick line for hour marker
            marker_width = 0.02
            perpendicular_angle = angle + math.pi/2
            
            x_offset = marker_width * math.cos(perpendicular_angle)
            y_offset = marker_width * math.sin(perpendicular_angle)
            
            # 4 points for the rectangle marker
            self.hour_markers_coords.extend([
                (x_outer + x_offset, y_outer + y_offset),
                (x_outer - x_offset, y_outer - y_offset),
                (x_inner - x_offset, y_inner - y_offset),
                (x_inner + x_offset, y_inner + y_offset)
            ])
            
            # black color for markers
            for _ in range(4):
                self.hour_markers_colors.append((0, 0, 0))
        
        # minute markers
        self.minute_markers_coords = []
        self.minute_markers_colors = []
        
        for minute in range(60):
            if minute % 5 != 0:  # skip hour positions
                angle = math.pi/2 - (minute * 2 * math.pi / 60)
                
                outer_radius = 0.75
                inner_radius = 0.70
                
                x_outer = center[0] + outer_radius * math.cos(angle)
                y_outer = center[1] + outer_radius * math.sin(angle)
                x_inner = center[0] + inner_radius * math.cos(angle)
                y_inner = center[1] + inner_radius * math.sin(angle)
                
                marker_width = 0.005
                perpendicular_angle = angle + math.pi/2
                
                x_offset = marker_width * math.cos(perpendicular_angle)
                y_offset = marker_width * math.sin(perpendicular_angle)
                
                self.minute_markers_coords.extend([
                    (x_outer + x_offset, y_outer + y_offset),
                    (x_outer - x_offset, y_outer - y_offset),
                    (x_inner - x_offset, y_inner - y_offset),
                    (x_inner + x_offset, y_inner + y_offset)
                ])
                
                for _ in range(4):
                    self.minute_markers_colors.append((100, 100, 100))
        
        # clock numbers
        self.numbers_coords = []
        self.numbers_colors = []
        
        for hour in range(1, 13):
            angle = math.pi/2 - (hour * 2 * math.pi / 12)
            number_radius = 0.6
            
            x = center[0] + number_radius * math.cos(angle)
            y = center[1] + number_radius * math.sin(angle)
            
            # simple number representation using small rectangles
            self._create_number(hour, x, y)
        
        self._create_clock_buffers()
        
        # center dot
        self.center_coords = [(0.0, 0.0)]
        self.center_colors = [(0, 0, 0)]  # black center
        self._create_center_buffer()
        
        # hands
        self.hour_hand_coords = []
        self.hour_hand_colors = []
        self.minute_hand_coords = []
        self.minute_hand_colors = []
        self.second_hand_coords = []
        self.second_hand_colors = []
        
        self._create_hands_buffers()
    
    def _create_number(self, number, x, y):
        size = 0.03
        thickness = 0.008
        
        # [start_x, start_y, end_x, end_y] relative to center

        number_patterns = {
            1: [
                [-size*0.6, -size*0.8, -size*0.6, size*0.8],
            ],
            2: [
                [-size*0.7, size*0.7, size*0.7, size*0.7],
                [size*0.7, size*0.7, size*0.7, 0],
                [-size*0.7, 0, size*0.7, 0],
                [-size*0.7, 0, -size*0.7, -size*0.7],
                [-size*0.7, -size*0.7, size*0.7, -size*0.7],
            ],
            3: [
                [-size*0.7, size*0.7, size*0.7, size*0.7],
                [size*0.7, size*0.7, size*0.7, 0],
                [-size*0.7, 0, size*0.7, 0],
                [size*0.7, 0, size*0.7, -size*0.7],
                [-size*0.7, -size*0.7, size*0.7, -size*0.7],
            ],
            4: [
                [-size*0.7, size*0.7, -size*0.7, 0],
                [size*0.7, size*0.7, size*0.7, -size*0.7],
                [-size*0.7, 0, size*0.7, 0],
            ],
            5: [
                [-size*0.7, size*0.7, size*0.7, size*0.7],
                [-size*0.7, size*0.7, -size*0.7, 0],
                [-size*0.7, 0, size*0.7, 0],
                [size*0.7, 0, size*0.7, -size*0.7],
                [-size*0.7, -size*0.7, size*0.7, -size*0.7],
            ],
            6: [
                [-size*0.7, size*0.7, size*0.7, size*0.7],
                [-size*0.7, size*0.7, -size*0.7, -size*0.7],
                [-size*0.7, 0, size*0.7, 0],
                [size*0.7, 0, size*0.7, -size*0.7],
                [-size*0.7, -size*0.7, size*0.7, -size*0.7],
            ],
            7: [
                [-size*0.7, size*0.7, size*0.7, size*0.7],
                [size*0.7, size*0.7, size*0.7, -size*0.7],
            ],
            8: [
                [-size*0.7, size*0.7, size*0.7, size*0.7],
                [-size*0.7, size*0.7, -size*0.7, -size*0.7],
                [size*0.7, size*0.7, size*0.7, -size*0.7],
                [-size*0.7, 0, size*0.7, 0],
                [-size*0.7, -size*0.7, size*0.7, -size*0.7],
            ],
            9: [
                [-size*0.7, size*0.7, size*0.7, size*0.7],
                [-size*0.7, size*0.7, -size*0.7, 0],
                [size*0.7, size*0.7, size*0.7, -size*0.7],
                [-size*0.7, 0, size*0.7, 0],
                [-size*0.7, -size*0.7, size*0.7, -size*0.7],
            ],
            10: [  # 1 and 0
                # 1 part (left digit)
                [-size*0.6, -size*0.8, -size*0.6, size*0.8],
                # 0 part (right digit)
                [size*0.1, size*0.8, size*0.8, size*0.8],
                [size*0.1, size*0.8, size*0.1, -size*0.8],
                [size*0.8, size*0.8, size*0.8, -size*0.8],
                [size*0.1, -size*0.8, size*0.8, -size*0.8],
            ],
            11: [  # 1 and 1
                [-size*0.6, -size*0.8, -size*0.6, size*0.8], # left 1
                [size*0.4, -size*0.8, size*0.4, size*0.8], # right 1
            ],
            12: [  # 1 and 2
                # 1 part (left digit)
                [-size*0.6, -size*0.8, -size*0.6, size*0.8],
                # 2 part (right digit)
                [size*0.0, size*0.8, size*0.7, size*0.8], 
                [size*0.7, size*0.8, size*0.7, 0],
                [size*0.0, 0, size*0.7, 0], 
                [size*0.0, 0, size*0.0, -size*0.8],  
                [size*0.0, -size*0.8, size*0.7, -size*0.8],  
            ]
        }
        
        if number in number_patterns:
            segments = number_patterns[number]
            for segment in segments:
                # thick line for each segment
                start_x, start_y, end_x, end_y = segment
                
                # calculate line direction and perpendicular
                dx = end_x - start_x
                dy = end_y - start_y
                length = math.sqrt(dx*dx + dy*dy)
                
                if length > 0:
                    # normalize direction
                    dx /= length
                    dy /= length
                    
                    # perpendicular vector for thickness
                    perp_x = -dy * thickness
                    perp_y = dx * thickness
                    
                    # create rectangle for the line segment
                    self.numbers_coords.extend([
                        (x + start_x + perp_x, y + start_y + perp_y),
                        (x + start_x - perp_x, y + start_y - perp_y),
                        (x + end_x - perp_x, y + end_y - perp_y),
                        (x + end_x + perp_x, y + end_y + perp_y)
                    ])
                    
                    for _ in range(4):
                        self.numbers_colors.append((0, 0, 0))
    
    def _create_clock_buffers(self):
        # clock face VAO
        self.clock_face_vao = glGenVertexArrays(1)
        glBindVertexArray(self.clock_face_vao)
        
        coords_array = np.array(self.clock_face_coords, dtype=np.float32).reshape(-1, 2)
        colors_array = np.array(self.clock_face_colors, dtype=np.uint8).reshape(-1, 3)
        
        # vertices with position and color
        vertices = np.zeros((len(coords_array), 5), dtype=np.float32)
        vertices[:, :2] = coords_array
        vertices[:, 2:5] = colors_array / 255.0
        
        self.clock_face_vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.clock_face_vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(8))
        glEnableVertexAttribArray(1)
        
        self.clock_face_vertex_count = len(coords_array)
        
        # hour markers VAO
        if self.hour_markers_coords:
            self.hour_markers_vao = glGenVertexArrays(1)
            glBindVertexArray(self.hour_markers_vao)
            
            coords_array = np.array(self.hour_markers_coords, dtype=np.float32).reshape(-1, 2)
            colors_array = np.array(self.hour_markers_colors, dtype=np.uint8).reshape(-1, 3)
            
            vertices = np.zeros((len(coords_array), 5), dtype=np.float32)
            vertices[:, :2] = coords_array
            vertices[:, 2:5] = colors_array / 255.0
            
            self.hour_markers_vbo = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.hour_markers_vbo)
            glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
            
            glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(0))
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(8))
            glEnableVertexAttribArray(1)
            
            self.hour_markers_vertex_count = len(coords_array)
        
        # minute markers VAO
        if self.minute_markers_coords:
            self.minute_markers_vao = glGenVertexArrays(1)
            glBindVertexArray(self.minute_markers_vao)
            
            coords_array = np.array(self.minute_markers_coords, dtype=np.float32).reshape(-1, 2)
            colors_array = np.array(self.minute_markers_colors, dtype=np.uint8).reshape(-1, 3)
            
            vertices = np.zeros((len(coords_array), 5), dtype=np.float32)
            vertices[:, :2] = coords_array
            vertices[:, 2:5] = colors_array / 255.0
            
            self.minute_markers_vbo = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.minute_markers_vbo)
            glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
            
            glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(0))
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(8))
            glEnableVertexAttribArray(1)
            
            self.minute_markers_vertex_count = len(coords_array)
        
        # numbers VAO
        if self.numbers_coords:
            self.numbers_vao = glGenVertexArrays(1)
            glBindVertexArray(self.numbers_vao)
            
            coords_array = np.array(self.numbers_coords, dtype=np.float32).reshape(-1, 2)
            colors_array = np.array(self.numbers_colors, dtype=np.uint8).reshape(-1, 3)
            
            vertices = np.zeros((len(coords_array), 5), dtype=np.float32)
            vertices[:, :2] = coords_array
            vertices[:, 2:5] = colors_array / 255.0
            
            self.numbers_vbo = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.numbers_vbo)
            glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
            
            glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(0))
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(8))
            glEnableVertexAttribArray(1)
            
            self.numbers_vertex_count = len(coords_array)
    
    def _create_center_buffer(self):
        # create center dot as a small circle
        center_coords = []
        center_colors = []
        center = (0.0, 0.0)
        radius = 0.03
        segments = 12
        
        # center point
        center_coords.append(center)
        center_colors.append((0, 0, 0))
        
        # circle points
        for i in range(segments + 1):
            angle = 2 * math.pi * i / segments
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            center_coords.append((x, y))
            center_colors.append((0, 0, 0))
        
        self.center_vao = glGenVertexArrays(1)
        glBindVertexArray(self.center_vao)
        
        coords_array = np.array(center_coords, dtype=np.float32).reshape(-1, 2)
        colors_array = np.array(center_colors, dtype=np.uint8).reshape(-1, 3)
        
        vertices = np.zeros((len(coords_array), 5), dtype=np.float32)
        vertices[:, :2] = coords_array
        vertices[:, 2:5] = colors_array / 255.0
        
        self.center_vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.center_vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(8))
        glEnableVertexAttribArray(1)
        
        self.center_vertex_count = len(coords_array)
    
    def _create_hands_buffers(self):
        # empty VAOs for hands (updated each frame)
        self.hour_hand_vao = glGenVertexArrays(1)
        self.hour_hand_vbo = glGenBuffers(1)
        
        self.minute_hand_vao = glGenVertexArrays(1)
        self.minute_hand_vbo = glGenBuffers(1)
        
        self.second_hand_vao = glGenVertexArrays(1)
        self.second_hand_vbo = glGenBuffers(1)
    
    def _update_hand(self, angle, length, width, color, vao, vbo):
        """Update a clock hand with given parameters"""
        glBindVertexArray(vao)
        
        # hand shape (rectangle from center to tip)
        center = (0.0, 0.0)
        
        # calculate hand endpoints
        tip_x = center[0] + length * math.cos(angle)
        tip_y = center[1] + length * math.sin(angle)
        
        # calculate perpendicular for width
        perp_angle = angle + math.pi/2
        width_x = width * math.cos(perp_angle)
        width_y = width * math.sin(perp_angle)
        
        # hand coordinates (rectangle)
        coords = [
            (center[0] + width_x, center[1] + width_y),
            (center[0] - width_x, center[1] - width_y),
            (tip_x - width_x, tip_y - width_y),
            (tip_x + width_x, tip_y + width_y)
        ]
        
        coords_array = np.array(coords, dtype=np.float32).reshape(-1, 2)
        colors_array = np.array([color] * 4, dtype=np.uint8).reshape(-1, 3)
        
        vertices = np.zeros((4, 5), dtype=np.float32)
        vertices[:, :2] = coords_array
        vertices[:, 2:5] = colors_array / 255.0
        
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(8))
        glEnableVertexAttribArray(1)
    
    def update_time(self):
        """Update clock hands based on current time"""
        current_time = time.localtime()
        hours = current_time.tm_hour % 12
        minutes = current_time.tm_min
        seconds = current_time.tm_sec
        
        # calculate angles / clock coordinates
        second_angle = math.pi/2 - (seconds * 2 * math.pi / 60)
        # minute_angle = math.pi/2 - (minutes * 2 * math.pi / 60) # ticks every minute
        minute_angle = math.pi/2 - ((minutes + seconds/60.0) * 2 * math.pi / 60) # changes smoothly
        hour_angle = math.pi/2 - ((hours + minutes/60.0) * 2 * math.pi / 12)
        
        # update hands
        self._update_hand(hour_angle, 0.4, 0.02, (0, 0, 0), self.hour_hand_vao, self.hour_hand_vbo)
        self._update_hand(minute_angle, 0.6, 0.015, (0, 0, 0), self.minute_hand_vao, self.minute_hand_vbo)
        self._update_hand(second_angle, 0.65, 0.005, (255, 0, 0), self.second_hand_vao, self.second_hand_vbo)
    
    def Draw(self):
        # update time before drawing
        self.update_time()
        
        # draw clock face
        glBindVertexArray(self.clock_face_vao)
        glDrawArrays(GL_TRIANGLE_FAN, 0, self.clock_face_vertex_count)
        
        # draw hour markers
        if hasattr(self, 'hour_markers_vao'):
            glBindVertexArray(self.hour_markers_vao)
            for i in range(12):
                glDrawArrays(GL_TRIANGLE_FAN, i * 4, 4)
        
        # draw minute markers
        if hasattr(self, 'minute_markers_vao'):
            glBindVertexArray(self.minute_markers_vao)
            marker_count = len(self.minute_markers_coords) // 4
            for i in range(marker_count):
                glDrawArrays(GL_TRIANGLE_FAN, i * 4, 4)
        
        # draw numbers
        if hasattr(self, 'numbers_vao'):
            glBindVertexArray(self.numbers_vao)
            number_count = len(self.numbers_coords) // 4
            for i in range(number_count):
                glDrawArrays(GL_TRIANGLE_FAN, i * 4, 4)
        
        # draw hands (hour hand, then minute, then second)
        glBindVertexArray(self.hour_hand_vao)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        
        glBindVertexArray(self.minute_hand_vao)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        
        glBindVertexArray(self.second_hand_vao)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        
        # draw center dot
        glBindVertexArray(self.center_vao)
        glDrawArrays(GL_TRIANGLE_FAN, 0, self.center_vertex_count)
