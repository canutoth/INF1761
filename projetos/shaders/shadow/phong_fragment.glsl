#version 410 core

// Fragment shader com iluminação Phong (sem sombras)

in vec3 fPosition;
in vec3 fNormal;
in vec2 fTexcoord;

// Light uniforms
uniform vec4 lpos;
uniform vec4 lamb;
uniform vec4 ldif;
uniform vec4 lspe;

// Material uniforms
uniform vec4 mamb;
uniform vec4 mdif;
uniform vec4 mspe;
uniform float mshi;
uniform float mopacity;

// Camera uniform
uniform vec4 cpos;

uniform sampler2D decal;

out vec4 FragColor;

void main()
{
    vec3 N = normalize(fNormal);
    vec3 L = normalize(lpos.xyz - fPosition);
    vec3 V = normalize(cpos.xyz - fPosition);
    vec3 R = reflect(-L, N);
    
    // Ambient
    vec4 ambient = lamb * mamb;
    
    // Diffuse
    float diff = max(dot(N, L), 0.0);
    vec4 diffuse = ldif * mdif * diff;
    
    // Specular
    float spec = pow(max(dot(R, V), 0.0), mshi);
    vec4 specular = lspe * mspe * spec;
    
    FragColor = ambient + diffuse + specular;
    FragColor.a = mopacity;
}
