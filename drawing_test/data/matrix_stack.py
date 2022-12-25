import math

# Your Matrix Stack Library
stack = list()

#HELPER FUNCTIONS
def createIdentity():
    return [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]]
def createZero():
    return [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
def multiply(transformationM, stackM):
    newArr = createZero()
    for i in range(4):
        for j in range(4):
            for k in range(4):
                newArr[i][j] = newArr[i][j] + stackM[i][k] * transformationM[k][j]
    return newArr
def add(a, b):
    newArr = createZero()
    for i in range(4):
        for j in range(4):
            newArr[i][j] = a[i][j] + b[i][j]
    return newArr
def peek(s):
    if s:
        return s[-1]

# you should modify the provided empty routines to complete the assignment
def gtInitialize():
    del stack[:]
    arr = createIdentity()
    stack.append(arr)

def gtPopMatrix():
    if len(stack) == 1:
        print("cannot pop the matrix stack")
    else:
        stack.pop()

def gtPushMatrix():
    arr = peek(stack)
    stack.append(arr)

def gtScale(x,y,z):
    scaleM = createIdentity()
    if x%1==0 or y%1==0 or z%1==0:
        scaleM[0][0] = x
        scaleM[1][1] = y
        scaleM[2][2] = z
    else:
        scaleM[0][0] = float(x)
        scaleM[1][1] = float(y)
        scaleM[2][2] = float(z)
    arr = multiply(scaleM, stack.pop())
    stack.append(arr)

def gtTranslate(x,y,z):
    translateM = createIdentity()
    if x%1==0 or y%1==0 or z%1==0:
        translateM[0][3] = x
        translateM[1][3] = y
        translateM[2][3] = z
    else:
        translateM[0][3] = float(x)
        translateM[1][3] = float(y)
        translateM[2][3] = float(z)
    arr = multiply(translateM, stack.pop())
    stack.append(arr) 

def gtRotateX(theta):
    theta = math.radians(theta)
    rotationM = createIdentity()
    rotationM[1][1] = math.cos(theta)
    rotationM[1][2] = math.sin(theta)
    rotationM[2][1] = -1*math.sin(theta)
    rotationM[2][2] = -1*math.cos(theta)
    
    arr = multiply(rotationM, stack.pop())
    stack.append(arr) 

def gtRotateY(theta):
    theta = math.radians(theta)
    rotationM = createIdentity()
    rotationM[0][0] = math.cos(theta)
    rotationM[0][2] = math.sin(theta)
    rotationM[2][0] = -1*math.sin(theta)
    rotationM[2][2] = math.cos(theta)
    
    arr = multiply(rotationM, stack.pop())
    stack.append(arr) 

def gtRotateZ(theta):
    theta = math.radians(theta)
    rotationM = createIdentity()
    rotationM[0][0] = math.cos(theta)
    rotationM[0][1] = -1*math.sin(theta)
    rotationM[1][0] = math.sin(theta)
    rotationM[1][1] = math.cos(theta)
    
    arr = multiply(rotationM, stack.pop())
    stack.append(arr) 

def print_ctm():
    arr = peek(stack)
    for line in arr:
        print(line)
        print('')
