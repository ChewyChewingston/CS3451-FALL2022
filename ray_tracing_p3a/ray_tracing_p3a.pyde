from __future__ import division
import traceback

debug_flag = False

spheres = []
lightSources = []
uvw =[(1,0,0), (0,1,0), (0,0,1)]

backgroundColor = (0, 0, 0)
fov = 0
diffuseColor = (0,0,0)
currentMaterial = (0,0,0,0,0,0,0,0,0,0,0)
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
    global diffuseColor, spheres, lightSources, uvw, backgroundColor, fov, currentMaterial, eye, p
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
            spheres.append(Sphere(radius, center, diffuseColor[0], diffuseColor[1], diffuseColor[2], currentMaterial))
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
        elif words[0] == 'begin':
            pass
        elif words[0] == 'vertex':
            pass
        elif words[0] == 'end':
            pass
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
            pixColor = intersect(spheres, ray, minTVal)
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

def diffuseShading(hit):
    normVector = (hit.intersectPt - hit.sphere.center).normalize()

    redV = 0
    greenV = 0
    blueV = 0
    
    for light in lightSources:
        LVector = (light.v - hit.intersectPt).normalize()
        proportion = max(normVector.dotProduct(LVector),0)
        
        redV += hit.sphere.red * light.r * proportion
        greenV += hit.sphere.green * light.g * proportion
        blueV += hit.sphere.blue * light.b * proportion
        
    output = (redV, greenV, blueV)
    return output
    
def reset_scene():
    global spheres, lightSources, uvw, backgroundColor, fov, currentMaterial, eye, p
    spheres = []
    lightSources = []
    uvw =[(1,0,0), (0,1,0), (0,0,1)]
    backgroundColor = (0, 0, 0)
    fov = 0
    currentMaterial = (0,0,0,0,0,0,0,0,0,0,0)
    eye = (0, 0, 0)
    p = 0

def intersect(spheres, ray, minimum):
    
    dx = ray.slope.x
    dy = ray.slope.y
    dz = ray.slope.z
    
    ox = ray.origin.x
    oy = ray.origin.y
    oz = ray.origin.z
    
    for s in spheres:
        cx = s.center.x
        cy = s.center.y
        cz = s.center.z
        radius = s.radius
        
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
                IP = ray.getLocation(solution)
                newNormal = Vertex(IP.x - s.center.x, IP.y - s.center.y, IP.z - s.center.z).normalize()
                h = Hit(s, newNormal, solution, IP)
                pixColor = diffuseShading(h)
                return pixColor
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
    def __init__(self, radius, center, red, green, blue, material):
        self.radius = radius
        self.center = center
        self.red = red
        self.green = green
        self.blue = blue
        self.material = material
                
class Ray(object):
    def __init__(self, origin, slope):
        self.origin = origin
        self.slope = slope
        
    def getLocation(self, t):
        x = self.origin.x + t * self.slope.x
        y = self.origin.y + t * self.slope.y
        z = self.origin.z + t * self.slope.z
        return Vertex(x, y, z)

class Material(object):
    def __init__(self, diffR, diffG, diffB, ambR, ambG, ambB, specR, specG, specB, specPower, k_refl):
       self.diffR = diffR
       self.diffG = diffG
       self.diffB = diffB
       self.ambR = ambR
       self.ambG = ambG
       self.ambB = ambB
       self.specR = specR
       self.specG = specG
       self.specB = specB
       self.specPower = specPower
       self.k_refl = k_refl
       
class Hit(object):
    def __init__(self, sphere, normal, tValue, intersectPt):
        self.sphere = sphere
        self.normal = normal
        self.tValue = tValue
        self.intersectPt = intersectPt
        
def mousePressed():
    print ("You pressed the mouse at " + str(mouseX) + " " + str(mouseY))

def draw():
    pass
