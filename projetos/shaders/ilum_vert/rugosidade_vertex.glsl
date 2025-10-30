#version 410 core

layout (location = 0) in vec3 aPosition;
layout (location = 1) in vec3 aNormal;
layout (location = 1) in vec3 aTangent;
layout (location = 3) in vec2 aTexcoord;

uniform vec3 posLight; 

uniform mat4 Mvp;  
uniform mat4 Mv;   
uniform mat4 Mn; 

out vec3 dirLight;
out vec2 mapCoord;
out mat3 TBN;

void main()
{
    vec3 nVS = normalize((Mn * vec4(aNormal, 0.0)).xyz);
    vec3 tVS = normalize((mat3(Mv) * aTangent));     
    vec3 bVS = normalize(cross(nVS, tVS));

    TBN = mat3(tVS, bVS, nVS);
    dirLight = (Mv * vec4(aPosition, 1.0)).xyz;

    gl_Position = Mvp * vec4(aPosition, 1.0);
    
    mapCoord = aTexcoord;
}
