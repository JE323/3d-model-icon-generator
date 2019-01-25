import bpy
from bpy_extras.object_utils import world_to_camera_view
import time
import sys
import os.path
from mathutils import Vector
from math import pi
import json


### class ###
class RenderSettings:
    def __init__(self):
        self.cameraType = "ORTHO" # PERSP or ORTHO
        self.renderSize = Vector((256,256))
        self.pixelBorder = Vector((10,10))
        self.cameraRotation = Vector((60,0,0))
        self.sampleNumber = 10
        # post processing settings
        self.bgColour = Vector((1,1,1,1))
        self.useVignette = False

#### variables ###
#references
scene = bpy.context.scene

# loading
objectToLoad = "ERROR"

# render settings
renderSettings = RenderSettings()

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
        print(argv)
    except:
        argv = [] 
    
    print("Additional Arguments Specified:")
    
    #get file to load
    try:
        global objectToLoad
        objectToLoad = argv[argv.index("-file") + 1]
        print("Object File Specified: " + objectToLoad)
    except:
        print("No object provided.")
        pass
        
    try:
        renderFileLocation = argv[argv.index("-settings") + 1]

        #import json settings file
        global importedRenderSettings
        with open(renderFileLocation) as f:
            importedData = f.read()
            importedRenderSettings = json.loads(importedData)
        
        print("Imported settings file.")
        
        
        global renderSettings
        ### adjust global parameters
        print(importedRenderSettings)
        
        
        print(importedRenderSettings['pixBorder'])
        print(importedRenderSettings['camRot'])
        print(importedRenderSettings['samples'])
        print(importedRenderSettings['bgColour'])
        print(importedRenderSettings['vignette'])
        
        
        #get camera type
        try:
            if (importedRenderSettings['camType'] != ""):
                renderSettings.cameraType = importedRenderSettings['camType']
                print("Camera Type Specified: " + renderSettings.cameraType)
            else:
                raise Exception('Setting not found!')
        except:
            print("No camera type provided. Using default perspective.")
            pass

        #get render size
        try:
            if (importedRenderSettings['renderSize'] != ""):
                renderSizeStr = importedRenderSettings['renderSize'].replace('(','').replace(')','').split(',')
                if (len(renderSizeStr) == 2):
                    renderSettings.renderSize = Vector((float(renderSizeStr[0]),float(renderSizeStr[1])))
                    print("Render Size Specified: " + str(int(renderSettings.renderSize.x)) + " x " + str(int(renderSettings.renderSize.y)))
            else:
                raise Exception('Setting not found!')
        except:
            print("No render size provided. Using default 512 x 512.")
            pass
            
        try:
            if (importedRenderSettings['pixBorder'] != ""):
                renderSettings.pixelBorder = Vector((importedRenderSettings['pixBorder'],importedRenderSettings['pixBorder']))
                print("Pixel Border Specified: " + str(renderSettings.pixelBorder))
            else:
                raise Exception('Setting not found!')
        except:
            print("No pixel border provided. Using default 0px.")
            pass
        
        #get camera rotation
        try:
            if (importedRenderSettings['camRot'] != ""):
                cameraRotationStr = importedRenderSettings['camRot'].replace('(','').replace(')','').split(',')
                if (len(cameraRotationStr) == 3):
                    renderSettings.cameraRotation = Vector((float(cameraRotationStr[0]),float(cameraRotationStr[1]),float(cameraRotationStr[2])))
                    print("Camera Rotation Specified: (" + str(renderSettings.cameraRotation.x) + ", " + str(renderSettings.cameraRotation.y) + ", " + str(renderSettings.cameraRotation.z) + ")")
            else:
                raise Exception('Setting not found!')
        except:
            print("No camera rotation. Using default 65,0,55.")
            pass
                
        #get sample amount
        try:
            if (importedRenderSettings['samples'] != ""):
                renderSettings.sampleNumber = int(float(importedRenderSettings['samples']))
                print("Sample Number Specified: " + str(renderSettings.sampleNumber))
            else:
                raise Exception('Setting not found!')
        except:
            print("No sample number provided. Using default 10 samples.")
            pass
                
        #get background colour
        try:
            if (importedRenderSettings['bgColour'] != ""):
                bgColourStr = importedRenderSettings['bgColour'].replace('(','').replace(')','').split(',')
                if (len(bgColourStr) == 4):
                    renderSettings.bgColour = Vector((float(bgColourStr[0]),float(bgColourStr[1]),float(bgColourStr[2]),float(bgColourStr[3])))
                    print("Background Colour Specified: (" + str(renderSettings.bgColour.x) + ", " + str(renderSettings.bgColour.y) + ", " + str(renderSettings.bgColour.z) + ", " + str(renderSettings.bgColour.w) + ")")
            else:
                raise Exception('Setting not found!')
        except:
            print("No background colour provided. Using default (1,1,1,0).")
            pass
                
        #get vignette state
        try:
            if (importedRenderSettings['vignette'] != ""):
                renderSettings.useVignette = bool(int(importedRenderSettings['vignette']))
                print("Vignettte Specified: " + str(renderSettings.useVignette))
            else:
                raise Exception('Setting not found!')
        except:
            print("No vignette setting provided. Using default false.")
            pass

    except:
        print("No render settings provided.")
        pass
        
    #space out next set of outputs    
    print("")
        
def importObject():
    print("importing object")
    
    #import object depending on the type - .fbx, .obj
    print(objectToLoad)
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
    scene.render.resolution_x = int(renderSettings.renderSize.x)
    scene.render.resolution_y = int(renderSettings.renderSize.y)
    scene.render.pixel_aspect_x = 1
    scene.render.pixel_aspect_y = 1
    scene.render.resolution_percentage = 100
    
    #set sample number
    scene.cycles.samples = renderSettings.sampleNumber
    
def setupCamera():
    print("setting up camera")
    
    #create camera
    rotationRad = renderSettings.cameraRotation *pi / 180
    bpy.ops.object.camera_add(enter_editmode=False, location=Vector((0,0,0)), rotation=rotationRad, layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.ops.transform.translate(value=(0, 0, 2), constraint_axis=(False, False, True), constraint_orientation='LOCAL')

    #find camera
    cam = bpy.context.scene.objects.active
    bpy.context.scene.camera = cam
    
    #set camera type
    cam.data.type = renderSettings.cameraType
    cam.data.clip_start = 0.01
    cam.data.clip_end = 100
    
    scene.render.pixel_aspect_x = 1
    scene.render.pixel_aspect_y = 1
    bpy.context.scene.render.resolution_percentage = 100
      
    #set camera rotation
    cam.rotation_euler = renderSettings.cameraRotation * pi / 180    
    bpy.ops.wm.redraw_timer(type='DRAW', iterations=1) # redraw to use new camera information

    # Select objects that will be rendered and move camera position to the correct place
    for obj in scene.objects:
        obj.select = False
    for obj in bpy.context.visible_objects:
        if not (obj.hide or obj.hide_render):
            obj.select = True
    bpy.ops.view3d.camera_to_view_selected()
        
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

