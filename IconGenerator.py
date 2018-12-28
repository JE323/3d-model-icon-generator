import bpy
from bpy_extras.object_utils import world_to_camera_view
import time
import sys
import os.path
from mathutils import Vector
from math import pi

#class references
class Plane2DProjection:
    min2DPlane = Vector((4000,4000,4000))
    max2DPlane = Vector((-4000,-4000,-4000))
    
    camRef = None
    
    def __init__(self, cam):
        self.camRef = cam
        for ob in scene.objects:
            if (ob.type == "MESH"):
                bbox_corners = [ob.matrix_world * Vector(corner) for corner in ob.bound_box]
                for corner in bbox_corners:
                    #print("Bound point: (" + str(corner.x) + ", " + str(corner.y) + ", " + str(corner.z) + ")")
                    
                    co_2d = world_to_camera_view(scene, cam, corner)
                    #print("2D Coords:",co_2d)
                    
                    #adjust the x plane info
                    if (co_2d.x < self.min2DPlane.x):
                        self.min2DPlane.x = co_2d.x
                    elif (co_2d.x > self.max2DPlane.x):
                        self.max2DPlane.x = co_2d.x
                        
                    #adjust the y plane info
                    if (co_2d.y < self.min2DPlane.y):
                        self.min2DPlane.y = co_2d.y
                    elif (co_2d.y > self.max2DPlane.y):
                        self.max2DPlane.y = co_2d.y
                        
                    #adjust the z plane info
                    if (co_2d.z < self.min2DPlane.z):
                        self.min2DPlane.z = co_2d.z
                    elif (co_2d.z > self.max2DPlane.z):
                        self.max2DPlane.z = co_2d.z
                        
    def CalculateOrthoCameraScale(self, xBound, yBound):
        xScale = self.camRef.data.ortho_scale * (self.max2DPlane.x - self.min2DPlane.x) #/ xBound
        yScale = self.camRef.data.ortho_scale * (self.max2DPlane.y - self.min2DPlane.y) #/ yBound
        
        if (yScale > xScale):
            return yScale
        else:
            return xScale
        
    def CalculateLocalZMovement(self, adjustment):
        return adjustment - self.min2DPlane.z
        
    def PrintProjectionInformation(self):
        print("Projected x plane: min " + str(self.min2DPlane.x) + ", max " + str(self.max2DPlane.x))
        print("Projected y plane: min " + str(self.min2DPlane.y) + ", max " + str(self.max2DPlane.y))
        print("Projected z plane: min " + str(self.min2DPlane.z) + ", max " + str(self.max2DPlane.z))

#### variables ###
#references
scene = bpy.context.scene

# loading
objectToLoad = "G://Blender Projects//blender-icon-generator//ExampleObjects//bolt.obj"

# render settings
cameraType = "ORTHO" # PERSP or ORTHO
renderSize = Vector((1024,1024))
pixelBorder = Vector((10,10))
cameraRotation = Vector((60,0,0))
sampleNumber = 10

# post processing settings
bgColour = Vector((1,1,1,1))
useVignette = False

# output settings
outputName = ""

### functions ###
#helper functions
def moveLocal(obj, vec):
    inv = obj.matrix_world.copy()
    inv.invert()
    # vec aligned to local axis
    obj.location = obj.location + vec * inv
    bpy.ops.wm.redraw_timer(type='DRAW', iterations=1)

def calcCentreOfMeshes():
    meshObjects = 0
    newBoundCentre = Vector((0,0,0))
    for obj in scene.objects:
        if (obj.type == "MESH"):
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            newBoundCentre += obj.location
            meshObjects+=1
    newBoundCentre /= meshObjects
    #print("Center of objects: " + str(newBoundCentre))
    
    return newBoundCentre
    
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
        pixelBorder = Vector((pixelBorderAmount,pixelBorderAmount))
        print("Pixel Border Specified: " + str(pixelBorderAmount))
    except:
        print("No pixel border provided. Using default 0px.")
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
    boundCentre = calcCentreOfMeshes()

    #move objects overall center back to origin
    bpy.ops.transform.translate(value=(-boundCentre.x, -boundCentre.y, -boundCentre.z))

    bpy.ops.object.select_all(action='DESELECT')
    
def setupRenderSettings():
    print("setting render settings")
    
    #set standard setup
    scene.render.engine = 'CYCLES'
    scene.cycles.film_transparent = True

    #render size
    scene.render.resolution_x = int(renderSize.x)
    scene.render.resolution_y = int(renderSize.y)
    scene.render.pixel_aspect_x = 1
    scene.render.pixel_aspect_y = 1
    scene.render.resolution_percentage = 100
    
    #set sample number
    scene.cycles.samples = sampleNumber
    
def setupCamera():
    print("setting up camera")
    
    #create camera
    rotationRad = cameraRotation *pi / 180
    bpy.ops.object.camera_add(enter_editmode=False, location=Vector((0,0,0)), rotation=rotationRad, layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.ops.transform.translate(value=(0, 0, 2), constraint_axis=(False, False, True), constraint_orientation='LOCAL')

    #find camera
    cam = bpy.context.scene.objects.active
    bpy.context.scene.camera = cam
    
    #set camera type
    cam.data.type = cameraType
    cam.data.clip_start = 0.01
    cam.data.clip_end = 100
    
    scene.render.pixel_aspect_x = 1
    scene.render.pixel_aspect_y = 1
    bpy.context.scene.render.resolution_percentage = 100
    
    if (cameraType == 'ORTHO'):
        cam.data.ortho_scale = 5
        
    #move camera to centre and set rotation
    boundCentre = calcCentreOfMeshes()
    cam.location = boundCentre
    cam.rotation_euler = cameraRotation * pi / 180    
    bpy.ops.wm.redraw_timer(type='DRAW', iterations=1) # redraw to use new camera information
    
    #calculate border limits
    camRes = Vector((bpy.context.scene.render.resolution_x, bpy.context.scene.render.resolution_y))
    lowerBorderLimit = Vector((pixelBorder.x / camRes.x, pixelBorder.y / camRes.y))
    upperBorderLimit = Vector(((camRes.x - pixelBorder.x) / camRes.x, (camRes.y - pixelBorder.y) / camRes.y))
    
    print("lower border limit: " + str(lowerBorderLimit))
    print("upper border limit: " + str(upperBorderLimit))

    #calculate positions the bound box corners are on the 2d camera plane
    projectionPlane = Plane2DProjection(cam)
    projectionPlane.PrintProjectionInformation()
    
    if (cameraType == 'ORTHO'):
        newCameraScale = projectionPlane.CalculateOrthoCameraScale(upperBorderLimit.x - lowerBorderLimit.x, upperBorderLimit.y - lowerBorderLimit.y)
        print("New camera scale: " + str(newCameraScale))
        cam.data.ortho_scale = newCameraScale
        
        #move camera back by the z amount it needs to
        moveLocal(cam, Vector((0.0, 0.0, projectionPlane.CalculateLocalZMovement(0.1))))
        
def setupLighting():
    bpy.data.node_groups["Shader Nodetree"].nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)

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
    #setupLighting()
    #setupPostprocessing()
    #setupRender()
    #render is then handled from process information by the blender api

### main loop ###  
try:
    main()
except Exception as e:
    print(e)

#input("Press Enter to continue...")

