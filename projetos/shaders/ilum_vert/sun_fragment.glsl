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
    FragColor = texture(decal, fTexCoord);
}
