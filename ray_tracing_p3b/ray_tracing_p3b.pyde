from __future__ import division
import traceback
import math

debug_flag = False

vertices = []
shapes = []
lightSources = []
uvw =[(1,0,0), (0,1,0), (0,0,1)]

backgroundColor = (0, 0, 0)
fov = 0
specularColor = (0,0,0)
diffuseColor = (0,0,0)
ambientColor = (0,0,0)
spec_power = 0
k_refl = 0
eye = (0, 0, 0)

p = 0

def setup():
    size(320, 320) 
    noStroke()
    colorMode(RGB, 1.0)  # Processing color values will be in [0, 1]  (not 255)
    background(0, 0, 0)
    frameRate(30)
    
def keyPressed():
    try:
        handleKeyPressed()
    except Exception:
        traceback.print_exc()
    
def handleKeyPressed():
    if key == '1':
        interpreter("01_one_sphere.cli")
    elif key == '2':
        interpreter("02_three_spheres.cli")
    elif key == '3':
        interpreter("03_shiny_sphere.cli")
    elif key == '4':
        interpreter("04_many_spheres.cli")
    elif key == '5':
        interpreter("05_one_triangle.cli")
    elif key == '6':
        interpreter("06_icosahedron_and_sphere.cli")
    elif key == '7':
        interpreter("07_colorful_lights.cli")
    elif key == '8':
        interpreter("08_reflective_sphere.cli")
    elif key == '9':
        interpreter("09_mirror_spheres.cli")
    elif key == '0':
        interpreter("10_reflections_in_reflections.cli")

##INTERPRETER
def interpreter(fname):
    global shapes, vertices, lightSources, uvw, backgroundColor, fov, specularColor, diffuseColor, ambientColor, spec_power, k_refl, eye, p
    reset_scene()
    
    fname = "data/" + fname
    with open(fname) as f:
        lines = f.readlines()
    
    for line in lines:
        words = line.split()  # split up the line into individual tokens
        
        if len(words) == 0:   # skip empty lines
            continue
        if words[0] == 'sphere':
            x = float(words[2])
            y = float(words[3])
            z = float(words[4])
            center = Vertex(x, y, z)
            radius = float(words[1])
            shapes.append(Sphere(radius, center, diffuseColor, ambientColor, specularColor, spec_power, k_refl))
        elif words[0] == 'fov':
            fov = float(words[1])
            pass
        elif words[0] == 'eye':
            x = float(words[1])
            y = float(words[2])
            z = float(words[3])
            eye = Vertex(x,y,z)
            pass
        elif words[0] == 'uvw':
            uvw1 = PVector(float(words[1]), float(words[2]), float(words[3]))
            uvw2 = PVector(float(words[4]), float(words[5]), float(words[6]))
            uvw3 = PVector(float(words[7]), float(words[8]), float(words[9]))
            uvw = [uvw1, uvw2, uvw3]
            pass
        elif words[0] == 'background':
            r = float(words[1])
            g = float(words[2])
            b = float(words[3])
            backgroundColor = PVector(r,g,b)
            pass
        elif words[0] == 'light':
            x = float(words[1])
            y = float(words[2])
            z = float(words[3])
            r = float(words[4])
            g = float(words[5])
            b = float(words[6])
            v = Vertex(x,y,z)
            light = Light(v,r,g,b)
            lightSources.append(light)
            pass
        elif words[0] == 'surface':
            dr = float(words[1])
            dg = float(words[2])
            db = float(words[3])
            diffuseColor = PVector(dr,dg,db)
            
            ar = float(words[4])
            ag = float(words[5])
            ab = float(words[6])
            ambientColor = PVector(dr, dg, db)
            
            sr = float(words[7])
            sg = float(words[8])
            sb = float(words[9])
            specularColor = PVector(dr, dg, db)
            
            spec_power = float(words[10])
            k_refl = float(words[11])
        elif words[0] == 'begin':
            vertices = []
        elif words[0] == 'vertex':
            vertices.append(PVector(float(words[1]), float(words[2]), float(words[3])))
        elif words[0] == 'end':
            shapes.append(Triangle(vertices, diffuseColor, ambientColor, specularColor,
                                 spec_power, k_refl))
        elif words[0] == 'render':
            render_scene()
            reset_scene()
            pass    # render the scene (this is where most of the work happens)
        elif words[0] == '#':
            pass  # ignore lines that start with the comment symbol (pound-sign)
        else:
            print ("unknown command: " + word[0])

##RENDER SCENE
def render_scene():    
    d = 1/(tan(radians(fov/2)))
    
    for j in range(height):
        for i in range(width):
            U = 2.0 * i / width - 1
            #V = -1*(2.0 * j / height - 1)
            V = float(2*(height-j)/height)-1
            
            p1 = eye
            
            RD1 = -d * uvw[2]
            RD2 = V * uvw[1]
            RD3 = U * uvw[0]
            sum = RD1 + RD2 + RD3
            p2 = sum.normalize()
            ray = Ray(p1, p2)
            
            minTVal = 5000
            h = rayIntersectScene(shapes, ray, minTVal)
            
            pixColor = shade(h, ray, 10)
            #print(pixColor)
            if pixColor != None:
                pix_color = color(*pixColor)
                set(i, j, pix_color)
            else:
                pix_color = color(*backgroundColor)
                set(i, j, pix_color)
            continue
            pix_color = color(0.8, 0.2, 0.4)
            set(i, height - j, pix_color)
        pass

def createReflectionRay(intersectionPt, hit, ray):
    myScalar = scalarMultiply(0.0001, hit.normal)
    RROrigin = (intersectionPt.x + myScalar[0],
                intersectionPt.y + myScalar[1],
                intersectionPt.z + myScalar[2])

    N = hit.normal
    D = ray.slope
    sm = scalarMultiply(-1, D)    
    
    innerDotProduct = N.x * sm[0] + N.y * sm[1] + N.z * sm[2]    
    innerProduct = 2*innerDotProduct
    product = scalarMultiply(innerProduct, N)
    
    RRSlope =  ray.slope + product
    RRSlope = normalize(RRSlope)
    
    RR = Ray(RROrigin, RRSlope)
    return RR

def shade(hit, ray, max_depth):
    if hit == None:
        return None
    else:
        shadeR = 0
        shadeG = 0
        shadeB = 0
        
        #material = hit.object.material
        
        if max_depth > 0 and hit.object.material.k_refl > 0:
            reflection_ray = createReflectionRay(hit.intersectPt, hit, ray)
            #print(type(reflection_ray))
            reflect_hit = rayIntersectScene(shapes, reflection_ray, 5000)
            
            max_depth -= 1
            
            # print(type(reflection_ray))
            # print(type(reflect_hit))
            
            # print(type(shade(reflect_hit, reflection_ray, max_depth)))
            # print(type(hit.object.material.k_refl))
            
            reflect_color = scalarMultiply(hit.object.material.k_refl, shade(reflect_hit, reflection_ray, max_depth))
            
            shadeR += reflect_color[0]
            shadeG += reflect_color[1]
            shadeB += reflect_color[2]
        
        material = hit.object.material
        intersectionPt = hit.intersectPt
        specularPower = material.specularPower
        
        ##SHADOWS
        for light in lightSources:
            intersectionPt = getElement(intersectionPt)
            l = (light.v.x - intersectionPt[0], light.v.y - intersectionPt[1], light.v.z - intersectionPt[2])
                
            d = ray.slope
            h = (l[0]- d[0], l[1]- d[1], l[2]- d[2])
            h = normalize(h)
            lightColor = (light.r, light.g, light.b)
            
            SM = scalarMultiply(0.0001, hit.normal)
            shadowOrigin = (intersectionPt[0] + SM[0], intersectionPt[1] + SM[1], intersectionPt[2] + SM[2])
                
            shadowDirection = normalize(l)
            shadowRay = Ray(shadowOrigin, shadowDirection)
            
            shadowHit = rayIntersectScene(shapes, shadowRay, 5000)
            
            if shadowHit != None and shadowHit.tValue < l:
                continue
            else:
                newNormal = getElement(hit.normal)
                myDotProductS = h[0]*newNormal[0] + h[1]*newNormal[1] + h[2]*newNormal[2]

                specCoefficient = max(0, myDotProductS)**specularPower
            
                specCR = specCoefficient * lightColor[0] * material.specularColor[0]
                specCG = specCoefficient * lightColor[1] * material.specularColor[1]
                specCB = specCoefficient * lightColor[2] * material.specularColor[2]
                
                newNormal = getElement(hit.normal)
                myDotProductD = l[0]*newNormal[0] + l[1]*newNormal[1] + l[2]*newNormal[2]
                
                diffCoefficient = max(0, myDotProductD)**specularPower
                
                diffCR = diffCoefficient * lightColor[0] * material.diffuseColor[0]
                diffCG = diffCoefficient * lightColor[1] * material.diffuseColor[1]
                diffCB = diffCoefficient * lightColor[2] * material.diffuseColor[2]
                
                shadeR += specCR + diffCR
                shadeG += specCG + diffCG
                shadeB += specCB + diffCB
                
                # shadeR += specCR
                # shadeG += specCG
                # shadeB += specCB
        
        shadeR += material.ambientColor[0]
        shadeG += material.ambientColor[1]
        shadeB += material.ambientColor[2]
        
        myShade = (shadeR, shadeG, shadeB)
        
        return myShade
    
def reset_scene():
    global shapes, vertices, lightSources, uvw, backgroundColor, fov, specularColor, diffuseColor, ambientColor, spec_power, k_refl, eye, p
    shapes = []
    lightSources = []
    uvw =[(1,0,0), (0,1,0), (0,0,1)]

    backgroundColor = (0, 0, 0)
    fov = 0
    specularColor = (0,0,0)
    diffuseColor = (0,0,0)
    ambientColor = (0,0,0)
    spec_power = 0
    k_refl = 0
    eye = (0, 0, 0)
    p = 0
    
def rayIntersectScene(shapes, ray, minimum):
    h = None
    testH = None

    for s in shapes:
        testH = s.intersect(ray, minimum)
        if testH != None:
            h = testH
        else:
            continue
    if (h != None):
        return h
    else:
        return None
                
####################
class Vertex(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    def __repr__(self):
        return "{} {} {}".format(self.x, self.y, self.z)
    def scale(self, n):
        return Vertex(self.x * n, self.y * n, self.z * n)
    
    def distance(self, p):
        return sqrt((p.x - self.x) ** 2 + (p.y - self.y) ** 2 + (p.z - self.z) ** 2)

    def __sub__(self, p):
        return Vertex(self.x - p.x, self.y - p.y, self.z - p.z)

    def dotProduct(self, p):
        return self.x * p.x + self.y * p.y + self.z * p.z

    def __mul__(self, p):
        x = self.y * p.z - self.z * p.y
        y = self.z * p.x - self.x * p.z
        z = self.x * p.y - self.y * p.x
        return Vertex(x, y, z)

    def length(self):
        squared = (self.x) ** 2 + (self.y) ** 2 + (self.z) ** 2
        result = sqrt(squared)
        return result
    
    def normalize(self):
        absLen = self.length()
        return Vertex(self.x/absLen, self.y/absLen, self.z/absLen)
            
class Light(object):
    def __init__(self, v , r, g, b):
        self.v = v
        self.r = r
        self.g = g
        self.b = b
        
class Sphere(object):
    def __init__(self, radius, center, diff, amb, spec, specularPower, k_refl):
        self.radius = radius
        self.center = center
        self.material = Material(diff, amb, spec, specularPower, k_refl)
        self.surfaceN = None
        
    def intersect(self, ray, minimum):
        h = None
        
        newRS = getElement(ray.slope)
        dx = newRS[0]
        dy = newRS[1]
        dz = newRS[2]
        
        newRO = getElement(ray.origin)
        ox = newRO[0]
        oy = newRO[1]
        oz = newRO[2]
        
        cx = self.center.x
        cy = self.center.y
        cz = self.center.z
        radius = self.radius
        
        ux = ox - cx
        uy = oy - cy
        uz = oz - cz
        
        a = dx**2 + dy**2 + dz**2
        b = 2*(dx*ux + dy*uy + dz*uz)
        c = ux**2 + uy**2 + uz**2 - radius**2
        
        discriminant = b**2 - 4*a*c
        
        if discriminant >= 0:
            t1 = (-b + sqrt(discriminant))/(2*a)
            t2 = (-b - sqrt(discriminant))/(2*a)

            candidates = [t1, t2]
            solution = min(candidates)
                
            if solution > 0 and minimum > solution:
                minimum = solution
                IP = ray.getLocation(solution)
                newNormal = Vertex(IP.x - self.center.x, IP.y - self.center.y, IP.z - self.center.z).normalize()
                h = Hit(self, newNormal, solution, IP)
                
                self.surfaceN = (h.intersectPt - self.center).normalize()
        return h
    
class Triangle(object):
    def __init__(self, vertices, diff, amb, spec, specularPower, k_refl):
        self.a = vertices[0]
        self.b = vertices[1]
        self.c = vertices[2]
        
        self.ab = (self.b[0] - self.a[0], self.b[1] - self.a[1], self.b[2] - self.a[2])
        self.bc = (self.c[0] - self.b[0], self.c[1] - self.b[1], self.c[2] - self.b[2])
        
        self.material = Material(diff, amb, spec, specularPower, k_refl)
        
        self.surfaceN = crossProduct(self.ab, self.bc)
        self.surfaceN = normalize(self.surfaceN)
        
    def intersect(self, ray, minimum):
            N = normalize(self.surfaceN)
            o = ray.origin
            v1 = self.a
            d = normalize(ray.slope)
            
            denom = dotProduct(N, d)
            if denom != 0:
                newOrigin = getElement(o)
                
                v1ox = v1.x - newOrigin[0]
                v1oy = v1.y - newOrigin[1]
                v1oz = v1.z - newOrigin[2]
                
                numer = N[0]*v1ox + N[1]*v1oy + N[2]*v1oz
                
                t = numer/denom
            
                if t >= 0:
                    td = scalarMultiply(t, d)
                    p = (newOrigin[0] + td[0], newOrigin[1] + td[1], newOrigin[2] + td[2])
                    
                    ap = (p[0] - self.a.x, p[1] - self.a.y, p[2] - self.a.z)
                    ab = (self.b.x - self.a.x, 
                        self.b.y - self.a.y, 
                        self.b.z - self.a.z)
                    apab = crossProduct(ap, ab)
                    triple1 = dotProduct(N, apab)
                    
                    bp = (p[0] - self.b.x, p[1] - self.b.y, p[2] - self.b.z)
                    bc = (self.c.x - self.b.x, 
                        self.c.y - self.b.y, 
                        self.c.z - self.b.z)
                    bpbc = crossProduct(bp, bc)
                    triple2 = dotProduct(N, bpbc)
                    
                    cp = (p[0] - self.c.z, p[1] - self.c.y, p[2] - self.c.z)
                    ca = (self.a.x - self.c.x, 
                        self.a.y - self.c.y, 
                        self.a.z - self.c.z)
                    cpca = crossProduct(cp, ca)
                    triple3 = dotProduct(N, cpca)
                                        
                    triple1bool = triple1>0
                    triple2bool = triple2>0
                    triple3bool = triple3>0
                    
                    if triple1bool == triple2bool == triple3bool:
                        checkFlip = dotProduct(N, d)
                        if (checkFlip <= 0):
                            h = Hit(self, N, t, p)
                        else:
                            h = Hit(self, scalarMultiply(-1, N), t, p)
                        return h
                else:
                    return None
            else:
                return None
                
class Ray(object):
    def __init__(self, origin, slope):
        self.origin = origin
        self.slope = slope
        
    def getLocation(self, t):
        newSlope = getElement(self.slope)
        newOrigin = getElement(self.origin)
        
        x = newOrigin[0] + t * newSlope[0]
        y = newOrigin[1] + t * newSlope[1]
        z = newOrigin[2] + t * newSlope[2]
        
        return Vertex(x, y, z)

class Material(object):
    def __init__(self, diffuseColor, ambientColor, specularColor, specularPower, k_refl):
       self.diffuseColor = diffuseColor
       self.ambientColor = ambientColor
       self.specularColor = specularColor
       
       self.specularPower = specularPower
       self.k_refl = k_refl
       
class Hit(object):
    def __init__(self, object, normal, tValue, intersectPt):
        self.object = object
        self.normal = normal
        self.tValue = tValue
        self.intersectPt = intersectPt

def getElement(v1):
    try:
        return (v1.x, v1.y, v1.z)
    except:
        return (v1[0], v1[1], v1[2])

def crossProduct(v1, v2):
    cpx = v1[1]*v2[2] - v1[2]*v2[1]
    cpy = v1[2]*v2[0] - v1[0]*v2[2]
    cpz = v1[0]*v2[1] - v1[1]*v2[0]
    crossProduct = (cpx, cpy, cpz)
    return crossProduct

def dotProduct(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]

def scalarMultiply(s, v):
    newV = getElement(v)
    returnVal = (s * newV[0], s * newV[1], s * newV[2])
    return returnVal

def findMagnitude(v):
    newV = getElement(v)
    return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])

def normalize(v):
    myMagnitude = findMagnitude(v)
    if (myMagnitude == 0):
        return 0
    else:
        return (v[0]/myMagnitude, v[1]/myMagnitude, v[2]/myMagnitude)

def mousePressed():
    print ("You pressed the mouse at " + str(mouseX) + " " + str(mouseY))

def draw():
    pass
