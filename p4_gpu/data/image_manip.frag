// Fragment shader
// The fragment shader is run once for every pixel
// It can change the color and transparency of the fragment.

#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

#define PROCESSING_TEXLIGHT_SHADER

// Set in Processing
uniform sampler2D my_texture;
uniform sampler2D my_mask;
uniform float blur_flag;

// These values come from the vertex shader
varying vec4 vertColor;
varying vec3 vertNormal;
varying vec3 vertLightDir;
varying vec4 vertTexCoord;

void main() { 
  // grab the color values from the texture and the mask
  vec4 diffuse_color = texture2D(my_texture, vertTexCoord.xy);
  vec4 mask_color = texture2D(my_mask, vertTexCoord.xy);

  // half sheep, half mask
  if (blur_flag == 1) {
    vec4 blur_col = vec4(0,0,0,0);
    int blur_radius = 1;
    float texl_size = 1.0/768.0;

    if (mask_color.x < 0.1) {
      blur_radius = 6;
    } else if (mask_color.x < 0.5) {
      blur_radius = 3;
    }
    
    for (int i = (-1*blur_radius); i < blur_radius; i++) {
      for (int j = (-1*blur_radius); j < blur_radius; j++) {
        vec2 myXY = vec2(vertTexCoord.x + i*texl_size, vertTexCoord.y + j*texl_size);
        vec4 newCol = texture2D (my_texture, myXY.xy);

        blur_col.x += newCol.x;
        blur_col.y += newCol.y;
        blur_col.z += newCol.z;
    }
  }
    blur_col.x = blur_col.x/(4*blur_radius*blur_radius);
    blur_col.y = blur_col.y/(4*blur_radius*blur_radius);
    blur_col.z = blur_col.z/(4*blur_radius*blur_radius);
    diffuse_color = blur_col;
  }

  // simple diffuse shading model
  float diffuse = clamp(dot (vertNormal, vertLightDir), 0.0, 1.0);

  gl_FragColor = vec4(diffuse * diffuse_color.rgb, 1.0);
}
