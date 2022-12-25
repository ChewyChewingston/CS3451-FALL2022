# Provided code for Subdivison and Geodesic Spheres

from __future__ import division
import traceback
import random

def next(cornerNum):
    triangleNum = cornerNum // 3
    return 3*triangleNum + ((cornerNum + 1)%3)

def prev(cornerNum):
    triangleNum = cornerNum // 3
    return 3*triangleNum + ((cornerNum - 1)%3)

def opposite(cornerNum):
    global opposites
    return opposites[cornerNum]

def swing(cornerNum):
    return next(opposite(next(cornerNum)))

def inflateMesh(g):
    myNorm = []
    for vert in g:
        myNorm.append(vert.normalize())
    return myNorm

def createOppositesTable(g, v):
    newOTable = {}
    tripletList = []
    sortedtripletList = []
    temp = []
    
    for i in range(0, len(v)):
        temp.append(min(v[next(i)], v[prev(i)]))
        temp.append(max(v[next(i)], v[prev(i)]))
        temp.append(i)
        
        tripletList.append(temp) 
        temp = []
        
    maximum = 0
    
    for i in range(len(tripletList)):
         for j in range(len(tripletList[i])):
             if tripletList[i][j] > maximum:
                 maximum = tripletList[i][j]
                 
    for a in range(maximum + 1):
        buckets = []
        for b in range(len(tripletList)):
            if tripletList[b][0] == a:
                buckets.append(tripletList[b])
        for i in range(len(buckets)):
            for j in range(i, len(buckets)):
                if buckets[i][1]>buckets[j][1]:
                    swap = buckets[i]
                    buckets[i] = buckets[j]
                    buckets[j] = swap
                elif buckets[i][1] == buckets[j][1] and buckets[i][2] > buckets[j][2]:
                    swap = buckets[i]
                    buckets[i] = buckets[j]
                    buckets[j] = swap
        sortedtripletList.extend(buckets)
        
    for i in range(0, len(sortedtripletList), 2):
        cornerA = sortedtripletList[i][2]
        cornerB = sortedtripletList[i+1][2]
        newOTable[cornerA] = cornerB
        newOTable[cornerB] = cornerA
        
    return newOTable

def subdivide():
    global geometry, vertices
    numEdges = len(vertices)//2
    newGTable = []
    newVTable = []
    midpoints = {}
    
    for val in geometry:
        newGTable.append(val)
    
    for a,b in opposites.items():
        if a not in midpoints:
            endpoint1 = geometry[vertices[prev(a)]]
            endpoint2 = geometry[vertices[next(a)]]
            
            midpointX = (endpoint1[0] + endpoint2[0])/2
            midpointY = (endpoint1[1] + endpoint2[1])/2
            midpointZ = (endpoint1[2] + endpoint2[2])/2
    
            midpointIndex = len(newGTable)
            newGTable.append(PVector(midpointX, midpointY, midpointZ))
        
            midpoints[a] = midpointIndex
            midpoints[b] = midpointIndex
        
    for x in range(0, len(vertices), 3):
        y = x + 1
        z = x + 2
        newVTable.extend([vertices[x], midpoints[z], midpoints[y]])
        newVTable.extend([midpoints[z], vertices[y], midpoints[x]])
        newVTable.extend([midpoints[y], midpoints[x], vertices[z]])
        newVTable.extend([midpoints[x], midpoints[y], midpoints[z]])
        
    test = createOppositesTable(newGTable, newVTable)
    return newGTable, newVTable, createOppositesTable(newGTable, newVTable)

# parameters used for object rotation by mouse
mouseX_old = 0
mouseY_old = 0
rot_mat = PMatrix3D()

currCornerVisible = False
showRandomFlags = False
currentCorner = 0
geometry = []
vertices = []
colorCollection = []

# initalize things
def setup():
    size (800, 800, OPENGL)
    frameRate(30)
    noStroke()

# draw the current mesh (you will modify parts of this routine)
def draw():
    global geometry, vertices, showRandomColors, currCornerVisible, currentCorner, opposites
    
    background (100, 100, 180)    # clear the screen to black

    perspective (PI*0.2, 1.0, 0.01, 1000.0)
    camera (0, 0, 6, 0, 0, 0, 0, 1, 0)    # place the camera in the scene
    
    # create an ambient light source
    ambientLight (102, 102, 102)

    # create two directional light sources
    lightSpecular (202, 202, 202)
    directionalLight (100, 100, 100, -0.7, -0.7, -1)
    directionalLight (152, 152, 152, 0, 0, -1)
    
    pushMatrix();

    stroke (0)                    # draw polygons with black edges
    fill (200, 200, 200)          # set the polygon color to white
    ambient (200, 200, 200)
    specular (0, 0, 0)            # turn off specular highlights
    shininess (1.0)
    
    applyMatrix (rot_mat)   # rotate the object using the global rotation matrix
    for corner in vertices:
        myRand = random.randrange(0,255)
        colorCollection.append(myRand)

    # THIS IS WHERE YOU SHOULD DRAW YOUR MESH
    p = 0
    for c in range(0, len(vertices), 3):
        beginShape()
        if showRandomFlags:
            fill(colorCollection[p], colorCollection[p+1], colorCollection[p+2])
            p+=3
        else:
            fill(255,255,255)
        
        vertex(geometry[vertices[c]][0], geometry[vertices[c]][1], geometry[vertices[c]][2])
        vertex(geometry[vertices[c+1]][0], geometry[vertices[c+1]][1], geometry[vertices[c+1]][2])
        vertex(geometry[vertices[c+2]][0], geometry[vertices[c+2]][1], geometry[vertices[c+2]][2])
        
        endShape(CLOSE)
            
        if currCornerVisible:
            pushMatrix()
            
            currentVertex = geometry[vertices[currentCorner]]
            myCurrVX = geometry[vertices[currentCorner]][0]*0.8 + geometry[vertices[next(currentCorner)]][0]*0.1+ geometry[vertices[prev(currentCorner)]][0]*0.1
            myCurrVY = geometry[vertices[currentCorner]][1]*0.8 + geometry[vertices[next(currentCorner)]][1]*0.1 + geometry[vertices[prev(currentCorner)]][1]*0.1
            myCurrVZ = geometry[vertices[currentCorner]][2]*0.8 + geometry[vertices[next(currentCorner)]][2]*0.1+ geometry[vertices[prev(currentCorner)]][2]*0.1
            translate(myCurrVX, myCurrVY, myCurrVZ)
            
            fill(255,0,0)
            noStroke()
            sphere(0.1)
            stroke(0)
            
            popMatrix()
    popMatrix()

# read in a mesh file (this needs to be modified)
def read_mesh(filename):
    global geometry, vertices, opposites
    currCornerVisible = False
    fname = "data/" + filename
    # read in the lines of a file
    with open(fname) as f:
        lines = f.readlines()

    # determine number of vertices (on first line)
    words = lines[0].split()
    num_vertices = int(words[1])

    # determine number of faces (on first second)
    words = lines[1].split()
    num_faces = int(words[1])
    
    # read in the vertices
    geometry = []
    for i in range(num_vertices):
        words = lines[i+2].split()
        x = float(words[0])
        y = float(words[1])
        z = float(words[2])
        geometry.append(PVector(x, y, z))

    # read in the faces
    vertices = []
    for i in range(num_faces):
        j = i + num_vertices + 2
        words = lines[j].split()
        nverts = int(words[0])
        if (nverts != 3):
            print "error: this face is not a triangle"
            exit()

        index1 = int(words[1])
        index2 = int(words[2])
        index3 = int(words[3])
        vertices += [index1, index2, index3]
        
    opposites = createOppositesTable(geometry, vertices)

# make sure proper error messages get reported when handling key presses
def keyPressed():
    try:
        handleKeyPressed()
    except Exception:
        traceback.print_exc()

# process key presses (call your own routines!)
def handleKeyPressed():
    global showRandomFlags, geometry, currentCorner, currCornerVisible, vertices, opposites
    
    if key == '1':
        read_mesh ('tetra.ply')
    elif key == '2':
        read_mesh ('octa.ply')
    elif key == '3':
        read_mesh ('icos.ply')
    elif key == '4':
        read_mesh ('star.ply')
    elif key == 'n': # next
        currentCorner= next(currentCorner)
    elif key == 'p': # previous
        currentCorner= prev(currentCorner)
    elif key == 'o': # opposite
        currentCorner= opposite(currentCorner)
    elif key == 's': # swing
        currentCorner= swing(currentCorner)
    elif key == 'd': # subdivide mesh
        geometry, vertices, opposites = subdivide()
    elif key == 'i': # inflate mesh
        geometry = inflateMesh(geometry)
    elif key == 'r': # toggle random colors
        if showRandomFlags:
            showRandomFlags = false
        else:
            showRandomFlags = True
    elif key == 'c': # toggle showing current corner
        currCornerVisible = True
    elif key == 'q': # quit the program
        exit()

# remember where the user first clicked
def mousePressed():
    global mouseX_old, mouseY_old
    mouseX_old = mouseX
    mouseY_old = mouseY

# change the object rotation matrix while the mouse is being dragged
def mouseDragged():
    global rot_mat
    global mouseX_old, mouseY_old
    
    if (not mousePressed):
        return
    
    dx = mouseX - mouseX_old
    dy = mouseY - mouseY_old
    dy *= -1

    len = sqrt (dx*dx + dy*dy)
    if (len == 0):
        len = 1
    
    dx /= len
    dy /= len
    rmat = PMatrix3D()
    rmat.rotate (len * 0.005, dy, dx, 0)
    rot_mat.preApply (rmat)

    mouseX_old = mouseX
    mouseY_old = mouseY
