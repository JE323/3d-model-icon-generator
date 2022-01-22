import bpy
from bpy_extras.object_utils import world_to_camera_view
import time
import sys
import os.path
from mathutils import Vector
from math import pi
import json

#add custom modules into script
sys.path.append(os.getcwd())
import blenderHelpers

#### variables ###
#references
scene = bpy.context.scene

# loading
objectToLoad = "ERROR"

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
        for i in range(argv.index("-file") + 2,len(argv)):
            objectToLoad += (" " + argv[i])

        print("Object File Specified: " + objectToLoad)
    except Exception as e:
        print(e)
        print("Error with object provided.")
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
    boundCentre = blenderHelpers.calcCentreOfMeshes()

    #move objects overall center back to origin
    bpy.ops.transform.translate(value=(-boundCentre.x, -boundCentre.y, -boundCentre.z))

    bpy.ops.object.select_all(action='DESELECT')

def setupCamera():
    print("setting up camera")

    #find camera
    cam = blenderHelpers.findCamera()
    bpy.context.scene.camera = cam
    
    #set camera settings for position calculation
    bpy.context.scene.render.pixel_aspect_x = 1
    bpy.context.scene.render.pixel_aspect_y = 1
    bpy.context.scene.render.resolution_percentage = 100
      
    #set camera rotation
    bpy.ops.wm.redraw_timer(type='DRAW', iterations=1) # redraw to use new camera information

    # Select objects that will be rendered and move camera position to the correct place
    for obj in bpy.context.view_layer.objects:
        obj.select_set(False)
    for obj in bpy.context.visible_objects:
        if not (obj.hide_viewport or obj.hide_render):
            obj.select_set(True)
    bpy.ops.view3d.camera_to_view_selected()
