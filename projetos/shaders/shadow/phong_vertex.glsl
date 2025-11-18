#version 410 core

// Vertex shader simples com iluminação Phong

layout (location = 0) in vec3 aPosition;
layout (location = 1) in vec3 aNormal;
layout (location = 3) in vec2 aTexcoord;

uniform mat4 Mvp;  // Model-View-Projection matrix
uniform mat4 M;    // Model matrix
uniform mat4 Mn;   // Normal matrix

out vec3 fPosition;  // Position in world space
out vec3 fNormal;    // Normal in world space
out vec2 fTexcoord;

void main()
{
    fTexcoord = aTexcoord;
    
    // Transform to world space
    vec4 worldPos = M * vec4(aPosition, 1.0);
    fPosition = worldPos.xyz;
    
    // Transform normal to world space
    fNormal = normalize((Mn * vec4(aNormal, 0.0)).xyz);
    
    // Transform to clip space
    gl_Position = Mvp * vec4(aPosition, 1.0);
}
