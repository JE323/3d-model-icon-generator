import bpy
import bpy_extras
from mathutils import Vector

scene = bpy.context.scene

print("\nStarting script")

cameraAspRatio = bpy.context.scene.render.resolution_x/bpy.context.scene.render.resolution_y
#print(cameraAspRatio)

for ob in scene.objects:
    if (ob.type == "MESH"):
        bbox_corners = [ob.matrix_world * Vector(corner) for corner in ob.bound_box]
        for corner in bbox_corners:
            print("Bound point: (" + str(corner.x) + ", " + str(corner.y) + ", " + str(corner.z) + ")")
            
