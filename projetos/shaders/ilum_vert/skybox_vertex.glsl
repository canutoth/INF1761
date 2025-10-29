#version 410

layout(location = 0) in vec3 coord;
layout(location = 1) in vec3 normal;
layout(location = 3) in vec3 texcoord;

uniform mat4 Mv; 
uniform mat4 Mn; 
uniform mat4 Mvp;

uniform vec4 lpos;  // light pos in eye space
uniform vec4 lamb;
uniform vec4 ldif;
uniform vec4 lspe;

uniform vec4 mamb;
uniform vec4 mdif;
uniform vec4 mspe;
uniform float mshi;

out data {
  vec4 color;
  vec3 texcoord;
} v;

void main (void) 
{
  v.texcoord = coord;
  v.color = vec4(0.20, 0.30, 0.70, 0.50);
  gl_Position = Mvp * vec4(coord, 1.0); 
}

