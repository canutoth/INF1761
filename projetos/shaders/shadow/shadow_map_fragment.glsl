#version 410 core

// Fragment shader com shadow mapping

in vec3 fPosition;
in vec3 fNormal;
in vec2 fTexcoord;
in vec4 fPosLightSpace;

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

uniform sampler2D shadowMap;

out vec4 FragColor;

float ShadowCalculation(vec4 fragPosLightSpace)
{
        // perspective divide
        vec3 projCoords = fragPosLightSpace.xyz / fragPosLightSpace.w;
        // to [0,1]
        projCoords = projCoords * 0.5 + 0.5;
        // outside light frustum
        if(projCoords.z > 1.0)
                return 0.0;
        float currentDepth = projCoords.z;
        float bias = 0.005;
        // PCF 3x3
        float shadow = 0.0;
        vec2 texelSize = 1.0 / textureSize(shadowMap, 0);
        for(int x=-1;x<=1;++x){
            for(int y=-1;y<=1;++y){
                float pcfDepth = texture(shadowMap, projCoords.xy + vec2(x,y)*texelSize).r;
                shadow += currentDepth - bias > pcfDepth ? 1.0 : 0.0;
            }
        }
        shadow /= 9.0;
        return shadow;
}

void main()
{
        vec3 N = normalize(fNormal);
        vec3 L = normalize(lpos.xyz - fPosition);
        vec3 V = normalize(cpos.xyz - fPosition);
        vec3 R = reflect(-L, N);
    
        vec4 ambient = lamb * mamb;
        float diff = max(dot(N, L), 0.0);
        vec4 diffuse = ldif * mdif * diff;
        float spec = pow(max(dot(R, V), 0.0), mshi);
        vec4 specular = lspe * mspe * spec;

        float shadow = ShadowCalculation(fPosLightSpace);
        vec4 lighting = ambient + (1.0 - shadow) * (diffuse + specular);
        FragColor = lighting;
        FragColor.a = mopacity;
}
