def setup():
    size(600, 600)
    
## x = x coordinate of parent's center    
## y = y coordinate of parent's center
## w = parent width
## level = how many levels are we from the first four satellite squares
## total = how many times to recurse
## r = ratio between the widths of the first four satellite squares and the central square
## colorVar = how much color deviation is applied
def drawRecSquare(x, y, w, level, total, offset, r, colorVar):
        
    fill(100+level*colorVar, 50+level*colorVar, 100+level*colorVar)
    testXA = x + offset*r
    testYA = y - w/2 - float((w*r)/2)
    rect(testXA, testYA, w*r, w*r)

    fill(150+level*colorVar, 100+level*colorVar, 100+level*colorVar)
    testXB = x - offset*r
    testYB = y + w/2 + float((w*r)/2)
    rect(testXB, testYB, w*r, w*r)

    
    fill(150+level*colorVar, 50+level*colorVar, 100+level*colorVar)
    testXC = x - w/2 - float((w*r)/2)
    testYC = y - offset*r
    rect(testXC, testYC, w*r, w*r)
    
    fill(100+level*colorVar, 50+level*colorVar, 150+level*colorVar)   
    testXD = x + w/2 + float((w*r)/2)
    testYD = y + offset*r
    rect(testXD, testYD, w*r, w*r)
    
    if level < total:
        level = level + 1
        drawRecSquare(testXA, testYA, w*r, level, total, offset*r, r, colorVar)
        drawRecSquare(testXB, testYB, w*r, level, total, offset*r, r, colorVar)
        drawRecSquare(testXC, testYC, w*r, level, total, offset*r, r, colorVar)
        drawRecSquare(testXD, testYD, w*r, level, total, offset*r, r, colorVar)
    
    
def draw():
    ##DRAW BACKGROUND
    background(10)
    noStroke()
    
    ##DRAW CENTRAL SQUARE
    fill(100, 50, 100)
    
    x = width/2
    y = height/2
    w = (height-mouseY)*2/3
    
    rectMode(CENTER)
    rect(x, y, height/3, height/3)
    
    ##CREATE FIRST FOUR SATELLITE SQUARES
    fill(120, 70, 120)
    
    newXA = mouseX
    newYA = y - height/6 - w/4
    rect(newXA, newYA, w/2, w/2)
    
    newXB = height-mouseX
    newYB = y + height/6 + w/4
    rect(newXB, newYB, w/2, w/2)
    
    newXC = y + height/6 + w/4
    newYC = mouseX
    rect(newXC, newYC, w/2, w/2)
    
    newXD = y - height/6 - w/4
    newYD = height - mouseX
    rect(newXD, newYD, w/2, w/2)

    ##CALL FUNCTION RECURSIVELY
    t = mouseX - width/2
    r = float(float(w/2)/(width/3))
    
    drawRecSquare(newXA, newYA, w/2, 1, 4, t, r, 25)
    drawRecSquare(newXB, newYB, w/2, 1, 4, t, r, 25)
    drawRecSquare(newXC, newYC, w/2, 1, 4, t, r, 25)
    drawRecSquare(newXD, newYD, w/2, 1, 4, t, r, 25)
    
    
    
