#version 410

in data {
  vec4 color;
  vec3 texcoord;
} f;

out vec4 color;

uniform samplerCube skybox;

void main (void)
{
  color = f.color * texture(skybox, f.texcoord);
}

