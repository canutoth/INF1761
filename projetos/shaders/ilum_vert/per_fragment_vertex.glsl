#version 410 core

// Input vertex attributes
layout (location = 0) in vec3 aPosition;
layout (location = 1) in vec3 aNormal;
layout (location = 3) in vec2 aTexcoord;

// Uniforms
uniform mat4 Mvp;  // Model-View-Projection matrix
uniform mat4 Mv;   // Model-View matrix (to lighting space)
uniform mat4 Mn;   // Normal matrix

// Output to fragment shader
out vec3 fPosition;  // Position in lighting space
out vec3 fNormal;    // Normal in lighting space
out vec2 fTexcoord;  

void main()
{
    fTexcoord = aTexcoord;
    // Transform position to lighting space for fragment shader
    vec4 pos = Mv * vec4(aPosition, 1.0);
    fPosition = pos.xyz;
    
    // Transform normal to lighting space
    fNormal = normalize((Mn * vec4(aNormal, 0.0)).xyz);
    
    // Transform position to clip space
    gl_Position = Mvp * vec4(aPosition, 1.0);
}
