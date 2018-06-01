import bpy

#### variables ###
# loading
objectToLoad = "//monkey.obj"

# render settings
cameraType = "ORTHO" # PERSP or ORTHO
renderSize = "(1024,1024)"
pixelBorderAmount = 10
cameraRotation = "(0,30,60)"
sampleNumber = 10

# post processing settings
bgColour = "(1,1,1,1)"
useVignette = False

# output settings
outputDirectory = "//Render"
outputName = ""

### functions ###
def importObject():
    print("importing object")
    
    #import object depending on the type - .fbx, .obj
    
def setupRenderSettings():
    print("setting render settings")
    #render size
    #set sample number
    
def calculateCameraPosition():
    print("setting camera position and rotation")
    
    #calculate center of all boundary boxes
    
    #set rotation
    
    #calculate distance away needed depending on all boundary boxes

def setupCamera():
    print("setting up camera")

    #find camera
    cam = bpy.data.cameras["Camera"]
    
    #set type
    cam.type = cameraType
    
    #camera type - persp or ortho

    calculateCameraPosition()
    

    
def setupPostprocessing():
    print("setting up postprocessing")
    # bgColour
    
    # useVignette
    
def render():
    print("starting to render out")

### main ###
def main():
    print("\nStarting Icon Generator")
    importObject()
    setupRenderSettings()
    setupCamera()
    setupPostprocessing()
    
    
### main loop ###    
main()