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
    vec4 baseColor = ambient + diffuse + specular;
    
    // Adicionar manchas solares procedurais
    // Usar coordenadas de textura para criar padrões
    float u = fTexCoord.x;
    float v = fTexCoord.y;
    
    // Mancha 1 - grande perto do equador
    float spot1 = smoothstep(0.05, 0.0, length(vec2(u - 0.3, v - 0.5)));
    
    // Mancha 2 - média
    float spot2 = smoothstep(0.08, 0.0, length(vec2(u - 0.7, v - 0.6)));
    
    // Mancha 3 - pequena
    float spot3 = smoothstep(0.04, 0.0, length(vec2(u - 0.5, v - 0.3)));
    
    // Mancha 4 - outra pequena
    float spot4 = smoothstep(0.06, 0.0, length(vec2(u - 0.85, v - 0.4)));
    
    // Linha vertical para visualizar rotação
    float line = smoothstep(0.015, 0.0, abs(u - 0.5));
    
    // Combinar todas as manchas
    float spots = spot1 + spot2 + spot3 + spot4 + line * 0.5;
    spots = clamp(spots, 0.0, 1.0);
    
    // Escurecer as manchas (manchas solares são mais escuras)
    vec3 spotColor = vec3(0.6, 0.4, 0.1); // Cor marrom/escura
    FragColor.rgb = mix(baseColor.rgb, spotColor, spots * 0.6);
    FragColor.a = mopacity;
}
