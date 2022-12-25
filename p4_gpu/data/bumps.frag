// Fragment shader
// The fragment shader is run once for every pixel
// It can change the color and transparency of the fragment.

#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

#define PROCESSING_TEXLIGHT_SHADER

// Set in Processing
uniform sampler2D texture;

// These values come from the vertex shader
varying vec4 vertColor;
varying vec3 vertNormal;
varying vec3 vertLightDir;
varying vec4 vertTexCoord;

varying float offset;  //  your surface offset amount should be here (from your vertex shader)

void main() { 
  vec4 diffuse_color = texture2D(texture, vertTexCoord.xy);
  diffuse_color = vec4(offset, offset, offset, 1);
  gl_FragColor = vec4(diffuse_color.rgb, 1.0);
}
