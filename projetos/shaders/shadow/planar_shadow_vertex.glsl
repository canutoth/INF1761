#version 410 core

// Vertex shader para sombras planares
// Projeta vértices no plano y=0 baseado na posição da luz

layout (location = 0) in vec3 aPosition;

uniform mat4 Mvp;   // Model-View-Projection matrix
uniform mat4 Mv;    // Model matrix (world space)
uniform vec4 lpos;  // Light position (world space)
uniform mat4 Vp;    // View-Projection matrix (sem model)

void main()
{
    // Transformar posição para world space
    vec4 worldPos = Mv * vec4(aPosition, 1.0);
    
    // Calcular projeção no plano y=0
    // A sombra é a interseção do raio (luz -> vértice) com o plano y=0
    vec3 lightToVertex = worldPos.xyz - lpos.xyz;
    float t = (0.0 - lpos.y) / lightToVertex.y;
    
    vec3 shadowPos = lpos.xyz + t * lightToVertex;
    shadowPos.y = 0.01;  // Ligeiramente acima do plano
    
    // Transformar shadowPos (já em world space) para clip space usando VP
    gl_Position = Vp * vec4(shadowPos, 1.0);
}
