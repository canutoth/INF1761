#version 410 core

// Fragment shader para sombras planares
// Renderiza uma cor escura semitransparente

uniform float mopacity;

out vec4 FragColor;

void main()
{
    FragColor = vec4(0.0, 0.0, 0.0, mopacity);
}
