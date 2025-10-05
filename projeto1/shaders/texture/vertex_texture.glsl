#version 410

layout(location = 0) in vec4 coord;
layout(location = 1) in vec3 normal;
layout(location = 3) in vec2 texcoord;

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
  vec2 texcoord;
} v;

void main (void) 
{
  v.texcoord = texcoord;
  v.color = vec4(1.0, 1.0, 1.0, 1.0);
  gl_Position = Mvp*coord; 
}

