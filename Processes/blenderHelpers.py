import bpy
from mathutils import Vector

### functions ###
# helper functions
def moveLocal(obj, vec):
    inv = obj.matrix_world.copy()
    inv.invert()
    # vec aligned to local axis
    obj.location = obj.location + vec * inv
    bpy.ops.wm.redraw_timer(type='DRAW', iterations=1)


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
