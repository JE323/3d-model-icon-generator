import bpy
import bpy_extras
from mathutils import Vector
from math import pi

scene = bpy.context.scene

print("\nStarting script")

camRot = Vector((65,0,55))
obj_camera = bpy.data.objects["Camera"]

cameraAspRatio = bpy.context.scene.render.resolution_x/bpy.context.scene.render.resolution_y
#print(cameraAspRatio)


#calculate bound center
meshObjects = 0
boundCentre = Vector((0,0,0))

for obj in scene.objects:
    if (obj.type == "MESH"):
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        boundCentre += obj.location
        meshObjects+=1
boundCentre /= meshObjects

#move camera to centre and set rotation
obj_camera.location = boundCentre
obj_camera.rotation_euler = camRot * pi / 180

#move camera back by the z amount it needs to
furtherBackBound = 0
extraShiftAmount = 0.2

for ob in scene.objects:
    if (ob.type == "MESH"):
        bbox_corners = [ob.matrix_world * Vector(corner) for corner in ob.bound_box]
        for corner in bbox_corners:
            if (corner.z < furtherBackBound):
                furtherBackBound = corner.z

bpy.ops.object.select_all(action='DESELECT')
obj_camera.select = True
############### line below causing invalid context convertviewvec but is needed
#bpy.ops.transform.translate(value=(0, 0, -furtherBackBound + extraShiftAmount), constraint_axis=(False, False, True), constraint_orientation='LOCAL')

#calculate positions the bound box corners are on the 2d camera plane
for ob in scene.objects:
    if (ob.type == "MESH"):
        bbox_corners = [ob.matrix_world * Vector(corner) for corner in ob.bound_box]
        for corner in bbox_corners:
            #print("Bound point: (" + str(corner.x) + ", " + str(corner.y) + ", " + str(corner.z) + ")")
            
            co_2d = bpy_extras.object_utils.world_to_camera_view(scene, obj_camera, corner)
            #print("2D Coords:",co_2d)
              