#version 410 core

// Input from vertex shader
in vec3 fPosition;  // Position in lighting space
in vec3 fNormal;    // Normal in lighting space
in vec2 fTexCoord;  // Texture coordinates

// Light uniforms
uniform vec4 lpos;  // Light position in lighting space
uniform vec4 lamb;  // Light ambient color
uniform vec4 ldif;  // Light diffuse color
uniform vec4 lspe;  // Light specular color

// Material uniforms
uniform vec4 mamb;  // Material ambient color
uniform vec4 mdif;  // Material diffuse color
uniform vec4 mspe;  // Material specular color
uniform float mshi; // Material shininess
uniform float mopacity; // Material opacity

// Camera uniform
uniform vec4 cpos;  // Camera position in lighting space

// Output
out vec4 FragColor;

uniform sampler2D decal;

void main()
{
    // Normalize interpolated normal
    vec3 N = normalize(fNormal);
    
    // Light direction
    vec3 L;
    if (lpos.w == 0.0) {
        // Directional light
        L = normalize(lpos.xyz);
    } else {
        // Point light
        L = normalize(lpos.xyz - fPosition);
    }
    
    // View direction
    vec3 V = normalize(cpos.xyz - fPosition);
    
    // Reflection vector
    vec3 R = reflect(-L, N);
    
    // Ambient component
    vec4 ambient = lamb * mamb;
    
    // Diffuse component
    float diff = max(dot(N, L), 0.0);
    vec4 diffuse = ldif * mdif * diff;
    
    // Specular component
    float spec = pow(max(dot(R, V), 0.0), mshi);
    vec4 specular = lspe * mspe * spec;
    
    // Combine all components
    vec4 baseColor = (ambient + diffuse) * texture(decal, fTexCoord) + specular;
    
    vec3 tex = texture(decal, fTexCoord).rgb;
    float lum = dot(tex, vec3(0.2126, 0.7152, 0.0722));

    float e = smoothstep(0.0, 0.90, lum);   
    vec3  glowColor = vec3(0.5, 0.3, 0.0);  
    float glowStrength = 0.8;                             

    vec3 color = baseColor.rgb + glowStrength * e * glowColor;

    FragColor = vec4(color, mopacity);
}
