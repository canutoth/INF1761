#version 410 core

// Shader para renderização de depth map (shadow map)

layout (location = 0) in vec3 aPosition;

uniform mat4 Mvp;  // Light's Model-View-Projection matrix

void main()
{
    gl_Position = Mvp * vec4(aPosition, 1.0);
}
