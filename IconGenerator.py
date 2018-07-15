import bpy
import time
import sys
import os.path
from mathutils import Vector
from math import pi

#### variables ###
scene = bpy.context.scene

# loading
objectToLoad = "G://Blender Projects//blender-icon-generator//ExampleObjects//bolt.obj"

# render settings
cameraType = "PERSP" # PERSP or ORTHO
renderSize = Vector((1024,1024))
cameraRotation = Vector((60,0,30))
sampleNumber = 10

# post processing settings
bgColour = Vector((1,1,1,1))
useVignette = False

# output settings
outputName = ""

### functions ###

# main fucntions
def resetSceneFromFactory():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=True)

def parseArgs():
    argv = sys.argv

    try:
        argv = argv[argv.index("--") + 1:]  # get all args after "--"
        #print(argv)
    except:
        argv = [] 
    
    print("/nAdditional Arguments Specified:")
    
    #get file to load
    try:
        objectToLoad = argv[argv.index("-file") + 1]
        print("Object File Specified: " + objectToLoad)
    except:
        print("No object provided.")
        pass
        
    #get camera type
    try:
        cameraType = argv[argv.index("-camType") + 1]
        print("Camera Type Specified: " + cameraType)
    except Exception as e:

        print("No camera type provided. Using default perspective.")
        print("Exception caught as well:" + str(e))
        pass

    #get render size
    try:
        renderSizeStr = argv[argv.index("-renderSize") + 1]
        renderSizeStr = renderSizeStr.replace('(','').replace(')','').split(',')
        if (len(renderSizeStr) == 2):
            renderSize = Vector((float(renderSizeStr[0]),float(renderSizeStr[1])))
            print("Render Size Specified: " + str(int(renderSize.x)) + " x " + str(int(renderSize.y)))
    except:
        print("No render size provided. Using default 512 x 512.")
        pass
        
    #get pixel border amount
    try:
        pixelBorderAmount = int(float(argv[argv.index("-pixBorder") + 1]))
        print("Pixel Border Specified: " + str(pixelBorderAmount))
    except:
        print("No pixel border provided. Using default 10px.")
        pass
        
    #get camera rotation
    try:
        cameraRotationStr = argv[argv.index("-camRot") + 1]
        cameraRotationStr = cameraRotationStr.replace('(','').replace(')','').split(',')
        if (len(cameraRotationStr) == 3):
            cameraRotation = Vector((float(cameraRotationStr[0]),float(cameraRotationStr[1]),float(cameraRotationStr[2])))
            print("Camera Rotation Specified: (" + str(cameraRotation.x) + ", " + str(cameraRotation.y) + ", " + str(cameraRotation.z) + ")")
    except:
        print("No camera rotation. Using default 65,0,55.")
        pass
            
    #get sample amount
    try:
        sampleNumber = int(float(argv[argv.index("-samples") + 1]))
        print("Sample Number Specified: " + str(sampleNumber))
    except:
        print("No sample number provided. Using default 10 samples.")
        pass
            
    #get background colour
    try:
        bgColourStr = argv[argv.index("-bgColour") + 1]
        bgColourStr = bgColourStr.replace('(','').replace(')','').split(',')
        if (len(bgColourStr) == 4):
            bgColour = Vector((float(bgColourStr[0]),float(bgColourStr[1]),float(bgColourStr[2]),float(bgColourStr[3])))
            print("Background Colour Specified: (" + str(bgColour.x) + ", " + str(bgColour.y) + ", " + str(bgColour.z) + ", " + str(bgColour.w) + ")")
    except:
        print("No background colour provided. Using default (1,1,1,0).")
        pass
            
    #get vignette state
    try:
        useVignette = bool(argv[argv.index("-vignette") + 1])
        print("Vignettte Specified: " + str(useVignette))
    except:
        print("No vignette setting provided. Using default false.")
        pass 
    
    #space out next set of outputs    
    print("")
        
def importObject():
    print("importing object")
    
    #import object depending on the type - .fbx, .obj
    detectedFileTypeSplit = objectToLoad.split('.')
    detectedFileType = detectedFileTypeSplit[len(detectedFileTypeSplit)-1]
    
    if (detectedFileType == "obj"):
        importedObject = bpy.ops.import_scene.obj(filepath=objectToLoad)
    elif(detectedFileType == "fbx"):
        importedObject = bpy.ops.import_scene.fbx(filepath=objectToLoad)

    #recalculate all the origins so the boundary box dimensions are correct
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    boundCentre = Vector((0,0,0))
    for obj in scene.objects:
        boundCentre += obj.location
    boundCentre /= len(scene.objects)
    
    #print("Center of objects: " + str(boundCentre.x) + ", " + str(boundCentre.y) + ", " + str(boundCentre.z))
    
    #move objects overall center back to origin
    bpy.ops.transform.translate(value=(-boundCentre.x, -boundCentre.y, -boundCentre.z))

    bpy.ops.object.select_all(action='DESELECT')
    
def setupRenderSettings():
    print("setting render settings")
    
    #set standard setup
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.film_transparent = True

    #render size
    bpy.context.scene.render.resolution_x = int(renderSize.x)
    bpy.context.scene.render.resolution_y = int(renderSize.y)
    bpy.context.scene.render.resolution_percentage = 100
    
    #set sample number
    bpy.context.scene.cycles.samples = sampleNumber
    
def setupCamera():
    print("setting up camera")

    ######################### calculate distance away needed depending on all boundary boxes
    # some logic
    # some way to translate locally
    
    #create camera
    rotationRad = cameraRotation *pi / 180
    bpy.ops.object.camera_add(enter_editmode=False, location=Vector((0,0,0)), rotation=rotationRad, layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.ops.transform.translate(value=(0, 0, 2), constraint_axis=(False, False, True), constraint_orientation='LOCAL')

    #find camera
    cam = bpy.context.scene.objects.active
    
    bpy.context.scene.camera = cam
    
    #set camera type
    cam.data.type = cameraType

def setupPostprocessing():
    print("setting up postprocessing")
    
    # make sure compositing is setup
    bpy.context.scene.render.use_compositing = True
    
    ######################### bgColour
    
    
    ######################### useVignette
    
    
def setupRender():
    print("starting to render out")
    print("current render dir: " + bpy.context.scene.render.filepath)
    
    objPathSplit = objectToLoad.split('/')
    outputName = objPathSplit[len(objPathSplit)-1].split('.')[0]    
    
    bpy.context.scene.render.filepath = bpy.context.scene.render.filepath + "//" + outputName

### main ###
def main():
    print("\nStarting Icon Generator")
    resetSceneFromFactory()
    parseArgs()
    importObject()
    setupRenderSettings()
    setupCamera()
    setupPostprocessing()
    setupRender()
    #render is then handled from process information by the blender api

### main loop ###  
try:
    main()
except Exception as e:
    print(e)

input("Press Enter to continue...")

