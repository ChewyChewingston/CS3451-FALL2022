# Drawing Routines that are similar to those in OpenGL

from matrix_stack import *
prevVertex = []

k = -1
isOrtho = 0

leftVar = 0
rightVar = 0
topVar = 0
bottomVar = 0
fovVar = 0
nearVar = 0
farVar = 0

def gtOrtho(left, right, bottom, top, near, far):
    global leftVar, rightVar, topVar, bottomVar, isOrtho
    
    leftVar = left
    rightVar = right
    bottomVar = bottom
    topVar = top
    
    isOrtho = 1

def gtPerspective(fov, near, far):
    global isOrtho, fovVar, nearVar, farVar
    
    fovVar = fov
    nearVar = near
    farVar = farVar
    
    isOrtho = 0

def gtVertex(x, y, z):
    global isOrtho, prevVertex
    
    if len(prevVertex) == 0:
        prevVertex = [x,y,z,1]
        return
        
    prevV = multiplyV(peek(stack), prevVertex)
    currV = multiplyV(peek(stack), [x,y,z,1])
        
    if isOrtho:
        scaler = createIdentity()
        
        scaler[0][0] = float(width) / (rightVar - leftVar)
        scaler[0][3] = float(-leftVar) * width / (rightVar - leftVar)
        scaler[1][1] = float(height)/(topVar - bottomVar)
        scaler[1][3] = float(-bottomVar) * height / (topVar - bottomVar)
        
        prevV = multiplyV(scaler, prevV)
        currV = multiplyV(scaler, currV)
        
        line(prevV[0], height-prevV[1], currV[0], height-currV[1])
    else:
        radFov = fovVar * math.pi/180
        scaler = tan(radFov/2)
        
        newPV = [0,0,0,0]
        newCV = [0,0,0,0]
        
        scalePts(newPV, prevV, scaler)
        scalePts(newCV, currV, scaler)
        
        line(newPV[0], height-newPV[1], newCV[0], height-newCV[1])

    prevVertex = []

def gtBeginShape():
    pass

def gtEndShape():
    pass
    
def scalePts(result, v, k):
    x = 0
    y = 0
    
    for j in range(1):
        x = float(v[j]) / abs(v[2])
        y = float(v[j+1]) / abs(v[2])
    
    for i in range(1):
        result[i] = (float(x + k)) * (width / float(2*k))
        result[i+1] = (float(y + k)) * (width / float(2*k))
    
def multiplyV(m, v):
    result = []
    for i in range(4):
        result.append(m[i][0]*v[0] + m[i][1]*v[1] + m[i][2]*v[2] + m[i][3]*v[3])
    return result
