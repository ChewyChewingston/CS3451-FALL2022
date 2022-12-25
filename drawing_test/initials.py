# The routine below should draw your initials in perspective

from matrix_stack import *
from drawlib import *

def persp_initials():
    gtInitialize()
    gtPerspective(50, -50, 50)
    gtPushMatrix()
    gtTranslate(-2, 0, -5)

    gtRotateX(30)
        
    gtBeginShape()

    gtVertex(0, 0, 1)
    gtVertex(0, 2, 1)

    gtVertex(0, 0, 1)
    gtVertex(2, 0, 1)
    
    gtVertex(1, 0, 1)
    gtVertex(1, 2, 1)
    
    gtVertex(2, 0, 1)
    gtVertex(2, 2, 1)
    
    gtVertex(0, 0, -0.05)
    gtVertex(0, 2, -0.05)

    gtVertex(0, 0, -0.05)
    gtVertex(2, 0, -0.05)
    
    gtVertex(1, 0, -0.05)
    gtVertex(1, 2, -0.05)
    
    gtVertex(2, 0, -0.05)
    gtVertex(2, 2, -0.05)

    gtEndShape()

    gtBeginShape()

    gtVertex(3, 0, 1)
    gtVertex(3, 2, 1)
    
    gtVertex(4, 0, 1)
    gtVertex(4, 2, 1)
    
    gtVertex(3, 1, 1)
    gtVertex(4, 1, 1)

    gtVertex(3, 0, -0.05)
    gtVertex(3, 2, -0.05)
    
    gtVertex(4, 0, -0.05)
    gtVertex(4, 2, -0.05)
    
    gtVertex(3, 1, -0.05)
    gtVertex(4, 1, -0.05)

    gtEndShape()
    gtPopMatrix()
