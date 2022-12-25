# Object Modeling Example Code

from __future__ import division
import traceback

time = 0   # time is used to move objects from one frame to another

#PImage img

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
        #img = loadImage("toyshopBG.png")
        
        camera (0, -20, 120, 0, 0, 0, 0,  1, 0)  # position of the virtual camera  
        #rotateY(time)      
        background (158, 219, 255)  # clear screen and set background to light blue
        #background(img)
        
        
        pointLight(255, 250, 200, -300, -300, 144);

        lightSpecular(5, 240, 255)
        directionalLight (100, 100, 100, -0.3, 0.5, -1)
        
        pushMatrix()
        fill(50, 200, 70)
        translate(0,20,0)
        box(400, 25, 400)
        popMatrix()
        
        noStroke()
        specular (10, 10, 10)
        shininess (15.0)
        
        if (time < 15):
            pushMatrix()
            fill(255, 160, 235)
            translate(0,10,-10)
            box(80, 15, 30)
            popMatrix()
    
            pushMatrix()
            translate(-40+time*10, -2 * sin(4 * time) - 22, 40)
            person(5)
            popMatrix()
            
            pushMatrix()
            translate(-120+time*15, -2 * sin(4 * time) - 6, 40)
            person(2)
            popMatrix()

            pushMatrix()
            translate(0,-2,-10)
            rotateY(time)
            bear(5, -25)
            popMatrix()
            
            pushMatrix()
            translate(250-time*15, -2 * sin(4 * time) - 6, 40)
            person(2)
            popMatrix()
            
            pushMatrix()
            tree(0, -70)
            tree(-50, -70)
            tree(50, -70)
            tree(-100, -70)
            tree(100, -70)
            
            tree(-70, -100)
            tree(-20, -100)
            tree(20, -100)
            tree(70, -100)
            popMatrix()
            
        if(time >= 15) and (time < 20):
            camera (time, -5, 60, 0, 0, 0, 0,  1, 0)  # position of the virtual camera
            
            pushMatrix()
            fill(255, 160, 235)
            translate(0,10,-10)
            box(80, 15, 30)
            popMatrix()
            
            pushMatrix()
            translate(0,-2,-10)
            rotateY(time)
            bear(5, -25)
            popMatrix()
            
            pushMatrix()
            translate(0,-3,40)
            person(2)
            popMatrix()
            
            pushMatrix()
            tree(0, -70)
            tree(-50, -70)
            tree(50, -70)
            tree(-100, -70)
            tree(100, -70)
            
            tree(-70, -100)
            tree(-20, -100)
            tree(20, -100)
            tree(70, -100)
            popMatrix()
            
        if(time >= 20) and (time < 25):
            camera (0, -5, time, 0, 0, 50, 0,  1, 0)

            pushMatrix()
            translate(0,-4,40)
            person(2)
            popMatrix()
            
            pushMatrix()
            tree(0, 80)
            tree(-50, 80)
            tree(50, 80)
            tree(-100, 80)
            tree(100, 80)
            
            tree(-70, 100)
            tree(-20, 100)
            tree(20, 100)
            tree(70, 100)
            popMatrix()
        if (time >=25) and (time < 31):
            camera (0, -3, 20-(time-25)*25, 0, 0, 50, 0,  1, 0)
            
            pushMatrix()
            tree(-80, 70)
            tree(-30, 70)
            tree(30, 70)
            tree(80, 70)
            
            tree(-70, 100)
            tree(-20, 100)
            tree(20, 100)
            tree(70, 100)
            popMatrix()

            pushMatrix()
            translate(0,-2 * sin(4 * time) - 6,40-(time-25)*15)
            person(2)
            popMatrix()
            
            pushMatrix()
            translate (10,-2 * cos(4 * time)-22,20-(time-25)*15)
            person(5)  
            popMatrix()
            
            pushMatrix()
            fill(150, 160, 170)
            translate(0,-2 * sin(4 * time) - 25,40-(time-25)*15)
            rotateY(135)
            bear(5, -5)
            popMatrix()
        if (time >=31):
            background(70, 70, 70)
            
    except Exception:
        traceback.print_exc()

def person(inputSize):
    fill (240, 200, 150)
        
    pushMatrix()
    translate (0, 0, 0)
    sphereDetail(20)
    sphere(inputSize*2)
    popMatrix()
        
    fill (inputSize*25, 82, 255)
        
    pushMatrix()
    translate (0, inputSize*3, 0)
    box(inputSize*2, inputSize*5, inputSize*2)
    popMatrix()
    
def bear(inputSize, headHeight):

    #BALLS
    fill (204, 124, 74)
    pushMatrix()
    translate (0, headHeight, 0)
    sphereDetail(30)
    sphere(inputSize)
    popMatrix()
        
    pushMatrix()
    translate ((float(inputSize/5)*3), headHeight-(float(inputSize/5)*4),0)
    sphereDetail(10)
    sphere(float(inputSize/2))
    popMatrix()
        
    pushMatrix()
    translate (-(float(inputSize/5)*3), headHeight-(float(inputSize/5)*4),0)
    sphereDetail(10)
    sphere(float(inputSize/2))
    popMatrix()
        
    pushMatrix()
    translate (0, headHeight+(float(inputSize/2)*5),0)
    sphereDetail(30)
    sphere(inputSize*2)
    popMatrix()
        
    fill (0, 0, 0)
    pushMatrix()
    translate (float(inputSize/2), headHeight-float(inputSize/2),float(inputSize/2))
    sphereDetail(10)
    sphere(float(inputSize/5))
    popMatrix()
        
    pushMatrix()
    translate (-float(inputSize/2), headHeight-float(inputSize/2),float(inputSize/2))
    sphereDetail(10)
    sphere(float(inputSize/5))
    popMatrix()
        
    pushMatrix()
    translate (0, headHeight-float(inputSize/5),float(inputSize/10)*9)
    sphereDetail(10)
    sphere(float(inputSize/5))
    popMatrix()
        
    fill(250, 0, 0)
    pushMatrix()
    translate (float(inputSize/5)*3, headHeight-float(inputSize/5),float(inputSize/5)*3)
    sphereDetail(10)
    sphere(float(inputSize/5))
    popMatrix()
        
    pushMatrix()
    translate (-float(inputSize/5)*3, headHeight-float(inputSize/5),float(inputSize/5)*3)
    sphereDetail(10)
    sphere(float(inputSize/5))
    popMatrix()

    #CYLINDERS
    fill (204, 124, 74)
        
    #LEFT LEG
    pushMatrix()
    translate (-float(inputSize/5)*3, headHeight+inputSize*4, 0)
    rotateX (90)
    scale (float(inputSize/2), float(inputSize/2), float(inputSize/2)*3)
    cylinder()
    popMatrix()
        
    #RIGHT LEG
    pushMatrix()
    translate (float(inputSize/5)*3, headHeight+inputSize*4, 0)
    rotateX (90)
    scale (float(inputSize/2), float(inputSize/2), float(inputSize/2)*3)
    cylinder()
    popMatrix()
        
    #RIGHT ARM
    pushMatrix()
    translate (inputSize*2, headHeight+inputSize*2, 0)
    rotateX (90)
    rotateY (90)
    scale (float(inputSize/2), float(inputSize/2), float(inputSize/2)*3)
    cylinder()
    popMatrix()
        
    #LEFT ARM
    pushMatrix()
    translate (-inputSize*2, headHeight+inputSize*2, 0)
    rotateX (90)
    rotateY (-90)
    scale (float(inputSize/2), float(inputSize/2), float(inputSize/2)*3)
    cylinder()
    popMatrix()
    
def tree(xInput, yInput):
    
    pushMatrix()
    fill(70, 50, 35)
    translate(xInput,-20,yInput)
    box(10, 70, 10)
    popMatrix()
    
    pushMatrix()
    fill(45, 90, 40)
    translate(xInput,-50,yInput)
    sphere(20)
    popMatrix()
    
    pushMatrix()
    translate(xInput+20,-60,yInput)
    sphere(12)
    popMatrix()
    
    pushMatrix()
    translate(xInput-10,-60,yInput)
    sphere(15)
    popMatrix()
    
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
