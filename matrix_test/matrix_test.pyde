# Test the matrix transformation commands that you will write

from matrix_stack import *

def setup():
    size (500, 500)
    background (220, 220, 220)
    try:
        mat_test()
    except Exception:
        import traceback
        print(traceback.format_exc())
        
# test the various commands
def mat_test():
    
    print ("Initialize Matrix")
        
    gtInitialize()
    print("worms")
    print_ctm()
    
    print ("Test Stack Underflow")
    gtInitialize()
    gtPopMatrix()
    print ("")

    print ("Translate")
    gtInitialize()
    gtTranslate(3,2,1.5)
    print_ctm()

    print ("Translate and Matrix Stack")
    gtInitialize()
    gtTranslate(-1,4,-2)
    gtPushMatrix()
    gtTranslate(2,-2,5)
    print_ctm()
    gtPopMatrix()
    print_ctm()

    print ("Scale")
    gtInitialize()
    gtScale(2,3,4)
    print_ctm()

    print ("Rotate X")
    gtInitialize()
    gtRotateX(90)
    print_ctm()

    print ("Rotate Y")
    gtInitialize()
    gtRotateY(-15)
    print_ctm()

    print ("Rotate Z and Matrix Stack")
    gtInitialize()
    gtPushMatrix()
    gtRotateZ(45)
    print_ctm()
    gtPopMatrix()
    print_ctm()

    print ("Rotate and Translate")
    gtInitialize()
    gtRotateZ(90)
    gtTranslate(7,5,3)
    print_ctm()

    print ("Translate and Rotate")
    gtInitialize()
    gtTranslate(7,5,3)
    gtRotateZ(90)
    print_ctm()

    print ("Translate and Scale")
    gtInitialize()
    gtTranslate(1.5,2.5,3.5)
    gtScale(2,2,2)
    print_ctm()

    print ("Scale and Translate")
    gtInitialize()
    gtScale(4,2,0.5)
    gtTranslate(2,-2,10)
    print_ctm()

# not used
def draw():
    pass
