import bpy
from mathutils import Vector

### functions ###
# helper functions
def calcCentreOfMeshes():
    meshObjects = 0
    newBoundCentre = Vector((0, 0, 0))
    for obj in bpy.context.scene.objects:
        if (obj.type == "MESH"):
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            newBoundCentre += obj.location
            meshObjects += 1
    newBoundCentre /= meshObjects
    # print("Center of objects: " + str(newBoundCentre))

    return newBoundCentre

def findCamera():
    foundCamera = []
    for obj in bpy.context.view_layer.objects:
        if (obj.type == 'CAMERA'):
            foundCamera.append(obj)
            
    if (len(foundCamera) == 0):
        print('NO CAMERA FOUND!!')
    elif (len(foundCamera) >= 2):
        print('MORE THAN 1 CAMERA FOUND!!')
    
    return foundCamera[0]