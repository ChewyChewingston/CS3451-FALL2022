// Fragment shader

#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

#define PROCESSING_LIGHT_SHADER

// These values come from the vertex shader
varying vec4 vertColor;
varying vec3 vertNormal;
varying vec3 vertLightDir;
varying vec4 vertTexCoord;

//varying int var;

void main() { 
  vec4 coord = vertTexCoord;
  coord.x -= 0.5;
  coord.y -= 0.5;

  float angle = radians(45);

  float s = sin(angle);
  float c = cos(angle);

  mat2 matrix = mat2(c,s,-s,c);
  vec2 temp = matrix * vec2(coord.x, coord.y);

  coord.x = temp.x + 0.5;
  coord.y = temp.y + 0.5;

  int alpha = 1;
  
  int centerCol = 0;
  while (centerCol < 5) {
    bool ISX0 = abs(coord.x - 0.5) <= .07;
    bool ISY0 = abs(coord.y - (0.1 + 0.2*centerCol)) <= .07;
    bool IS0 = ISX0 && ISY0;
    if (IS0) {
      alpha = 0;
    }
    centerCol += 1;
  }

  int sideCol1 = 0;
  while (sideCol1 < 3) {
    bool ISX1 = abs(coord.x - 0.3) <= .07;
    bool ISY1 = abs(coord.y - (0.3 + 0.2*sideCol1)) <= .07;
    bool IS1 = ISX1 && ISY1;
    if (IS1) {
      alpha = 0;
    }

    bool ISX2 = abs(coord.x - 0.7) <= .07;
    bool ISY2 = abs(coord.y - (0.3 + 0.2*sideCol1)) <= .07;
    bool IS2 = ISX2 && ISY2;
    if (IS2) {
      alpha = 0;
    }
    sideCol1 += 1;
  }

  bool ISX = abs(coord.x - 0.1) <= .07;
  bool ISY = abs(coord.y - 0.5) <= .07;
  bool IS = ISX && ISY;
  if (IS) {
    alpha = 0;
  }

  ISX = abs(coord.x - 0.9) <= .07;
  ISY = abs(coord.y - 0.5) <= .07;
  IS = ISX && ISY;
  if (IS) {
    alpha = 0;
  }

  gl_FragColor = vec4(0.0, 1.0, 2.0, alpha);
}

