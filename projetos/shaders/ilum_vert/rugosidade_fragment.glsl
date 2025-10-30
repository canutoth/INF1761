#version 410 core

in vec3 dirLight; 
in vec2 mapCoord;
in mat3 TBN;

uniform vec4 lpos; 
uniform vec4 lamb; 
uniform vec4 ldif;  
uniform vec4 lspe; 

uniform vec4 mamb;  
uniform vec4 mdif;  
uniform vec4 mspe;  
uniform float mshi; 
uniform float mopacity; 

uniform vec4 cpos; 

out vec4 FragColor;

uniform sampler2D decal;
uniform sampler2D normalMap;

void main()
{
    vec3 N_tan = texture(normalMap, mapCoord).rgb;
    N_tan = N_tan * 2.0 - 1.0;  
    
    vec3 N = normalize(TBN * N_tan);

    vec3 L = (lpos.w == 0.0)
            ? normalize(lpos.xyz)                     
            : normalize(lpos.xyz - dirLight); 

    vec3 V = normalize(cpos.xyz - dirLight);
    vec3 R = reflect(-L, N);

    vec4 ambient = lamb * mamb;
    float diff = max(dot(N, L), 0.0);
    vec4 diffuse = ldif * mdif * diff;
    float spec = pow(max(dot(R, V), 0.0), mshi);
    vec4 specular = lspe * mspe * spec;

    vec4 albedo = texture(decal, mapCoord);
    FragColor = (ambient + diffuse) * albedo + specular;
    FragColor.a = mopacity;
}
