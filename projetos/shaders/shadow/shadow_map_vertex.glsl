#version 410 core

// Vertex shader para shadow mapping (com posição em light space)

layout (location = 0) in vec3 aPosition;
layout (location = 1) in vec3 aNormal;
layout (location = 3) in vec2 aTexcoord;

uniform mat4 Mvp;        // Model-View-Projection matrix
uniform mat4 M;          // Model matrix (world space)
uniform mat4 Mn;         // Normal matrix
uniform mat4 lightVp;    // Light View-Projection matrix (sem model)

out vec3 fPosition;      // Position in world (lighting) space
out vec3 fNormal;        // Normal in lighting space
out vec2 fTexcoord;
out vec4 fPosLightSpace; // Position in light clip space

void main()
{
    fTexcoord = aTexcoord;
    
    // Transform to world space
    vec4 worldPos = M * vec4(aPosition, 1.0);
    fPosition = worldPos.xyz;
    
    // Normal in lighting space
    fNormal = normalize((Mn * vec4(aNormal, 0.0)).xyz);
    
    // Position in light's clip space
    fPosLightSpace = lightVp * worldPos;
    
    // To screen
    gl_Position = Mvp * vec4(aPosition, 1.0);
}
