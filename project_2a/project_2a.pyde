# Object Modeling Example Code

from __future__ import division
import traceback

time = 0   # time is used to move objects from one frame to another

def setup():
    size (800, 800, P3D)
    try:
        frameRate(120)       # this seems to be needed to make sure the scene draws properly
        perspective (60 * PI / 180, 1, 0.1, 1000)  # 60-degree field of view
    except Exception:
        traceback.print_exc()

def draw():
    try:
        global time
        time += 0.01

        camera (0, 0, 100, 0, 0, 0, 0,  1, 0)  # position of the virtual camera
        rotateY(time/2)        
        background (200, 200, 255)  # clear screen and set background to light blue
        
        # set up the lights
        ambientLight(50, 50, 50);
        lightSpecular(255, 255, 255)
        directionalLight (100, 100, 100, -0.3, 0.5, -1)
        
        # set some of the surface properties
        noStroke()
        specular (10, 10, 10)
        shininess (15.0)

        headHeight = -20

        #BALLS
        fill (204, 124, 74)
        pushMatrix()
        translate (0, headHeight, 0)
        sphereDetail(60)
        sphere(10)
        popMatrix()
        
        pushMatrix()
        translate (6,headHeight-8,0)
        sphereDetail(30)
        sphere(5)
        popMatrix()
        
        pushMatrix()
        translate (-6,headHeight-8,0)
        sphereDetail(30)
        sphere(5)
        popMatrix()
        
        pushMatrix()
        translate (0,headHeight+25,0)
        sphereDetail(60)
        sphere(20)
        popMatrix()
        
        fill (0, 0, 0)
        pushMatrix()
        translate (5, headHeight-5,5)
        sphereDetail(60)
        sphere(2)
        popMatrix()
        
        pushMatrix()
        translate (-5, headHeight-5,5)
        sphereDetail(60)
        sphere(2)
        popMatrix()
        
        pushMatrix()
        translate (0, headHeight-2,9)
        sphereDetail(60)
        sphere(2)
        popMatrix()
        
        fill(250, 0, 0)
        pushMatrix()
        translate (6, headHeight-2,6)
        sphereDetail(60)
        sphere(2)
        popMatrix()
        
        pushMatrix()
        translate (-6, headHeight-2,6)
        sphereDetail(60)
        sphere(2)
        popMatrix()

        #CYLINDERS
        fill (204, 124, 74)
        
        #LEFT LEG
        pushMatrix()
        translate (-6, headHeight+40, 0)
        rotateX (90)
        scale (5, 5, 15)
        cylinder()
        popMatrix()
        
        #RIGHT LEG
        pushMatrix()
        translate (6, headHeight+40, 0)
        rotateX (90)
        scale (5, 5, 15)
        cylinder()
        popMatrix()
        
        #RIGHT ARM
        pushMatrix()
        translate (20, headHeight+20, 0)
        rotateX (90)
        rotateY (90)
        scale (5, 5, 15)
        cylinder()
        popMatrix()
        
        #LEFT ARM
        pushMatrix()
        translate (-20, headHeight+20, 0)
        rotateX (90)
        rotateY (-90)
        scale (5, 5, 15)
        cylinder()
        popMatrix()
        
    except Exception:
        traceback.print_exc()

# cylinder with radius = 1, z range in [-1,1]
def cylinder(sides = 50):
    # first endcap
    beginShape()
    for i in range(sides):
        theta = i * 2 * PI / sides
        x = cos(theta)
        y = sin(theta)
        vertex ( x,  y, -1)
    endShape(CLOSE)
    # second endcap
    beginShape()
    for i in range(sides):
        theta = i * 2 * PI / sides
        x = cos(theta)
        y = sin(theta)
        vertex ( x,  y, 1)
    endShape(CLOSE)
    # round main body
    x1 = 1
    y1 = 0
    for i in range(sides):
        theta = (i + 1) * 2 * PI / sides
        x2 = cos(theta)
        y2 = sin(theta)
        beginShape()
        normal (x1, y1, 0)
        vertex (x1, y1, 1)
        vertex (x1, y1, -1)
        normal (x2, y2, 0)
        vertex (x2, y2, -1)
        vertex (x2, y2, 1)
        endShape(CLOSE)
        x1 = x2
        y1 = y2
