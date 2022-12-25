// Fragment shader

#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

#define PROCESSING_LIGHT_SHADER

uniform float cx;
uniform float cy;

// These values come from the vertex shader
varying vec4 vertColor;
varying vec3 vertNormal;
varying vec3 vertLightDir;
varying vec4 vertTexCoord;

void main() { 
  float pi = 3.14;
  vec2 c = vec2(cx, cy);
  vec2 z = vec2(vertTexCoord.x*2*pi - pi, vertTexCoord.y*2*pi - pi);  
  
  for (int i=0; i<20; i++) {
    vec2 complexIV = vec2 (sin(z.x) * cosh(z.y), cos(z.x) * sinh(z.y));
    z.x = c.x * complexIV.x - c.y * complexIV.y;
    z.y = c.x * complexIV.y + c.y * complexIV.x;
  }

  vec4 diff_color = vec4 (1.0, 0.0, 0.0, 1.0);
  float diff = clamp(dot (vertNormal, vertLightDir), 0.0, 1.0);
  
  if (length(z) < 2500) {
    diff_color = vec4 (1.0, 1.0, 1.0, 0.0);
  } 
  gl_FragColor = vec4(diff * diff_color.rgb, 1.0);
}