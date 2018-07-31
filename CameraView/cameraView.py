import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
from math import pi

scene = bpy.context.scene

def moveLocal(obj, vec):
    inv = obj.matrix_world.copy()
    inv.invert()
    # vec aligned to local axis
    obj.location = obj.location + vec * inv



#variables
camRot = Vector((65,0,55))
extraShiftAmount = 3
pixelBorder = Vector((20,20))


print("\nStarting script")

obj_camera = bpy.data.objects["Camera"]


camRes = Vector((bpy.context.scene.render.resolution_x, bpy.context.scene.render.resolution_y))


cameraAspRatio = camRes.x / camRes.y
bpy.context.scene.render.resolution_percentage = 100

lowerBorderLimit = Vector((pixelBorder.x / camRes.x, pixelBorder.y / camRes.y))
upperBorderLimit = Vector(((camRes.x - pixelBorder.x) / camRes.x, (camRes.y - pixelBorder.y) / camRes.y))
print("lower border limit: " + str(lowerBorderLimit))
print("upper border limit: " + str(upperBorderLimit))

#calculate bound center
meshObjects = 0
boundCentre = Vector((0,0,0))
for obj in scene.objects:
    if (obj.type == "MESH"):
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        boundCentre += obj.location
        meshObjects+=1
boundCentre /= meshObjects
print("Center of objects: " + str(boundCentre))

#move camera to centre and set rotation
obj_camera.location = boundCentre
obj_camera.rotation_euler = camRot * pi / 180

#calculate positions the bound box corners are on the 2d camera plane
min2DPlane = Vector((1000,1000,1000))
max2DPlane = Vector((-1000,-1000,-1000))

for ob in scene.objects:
    if (ob.type == "MESH"):
        bbox_corners = [ob.matrix_world * Vector(corner) for corner in ob.bound_box]
        for corner in bbox_corners:
            #print("Bound point: (" + str(corner.x) + ", " + str(corner.y) + ", " + str(corner.z) + ")")
            
            co_2d = world_to_camera_view(scene, obj_camera, corner)
            #print("2D Coords:",co_2d)
            
            #adjust the x plane info
            if (co_2d.x < min2DPlane.x):
                min2DPlane.x = co_2d.x
            elif (co_2d.x > max2DPlane.x):
                max2DPlane.x = co_2d.x
                
            #adjust the y plane info
            if (co_2d.y < min2DPlane.y):
                min2DPlane.y = co_2d.y
            elif (co_2d.y > max2DPlane.y):
                max2DPlane.y = co_2d.y
                
            #adjust the z plane info
            if (co_2d.z < min2DPlane.z):
                min2DPlane.z = co_2d.z
            elif (co_2d.z > max2DPlane.z):
                max2DPlane.z = co_2d.z

print("Projected x plane: min " + str(min2DPlane.x) + ", max " + str(max2DPlane.x))
print("Projected y plane: min " + str(min2DPlane.y) + ", max " + str(max2DPlane.y))
print("Projected z plane: min " + str(min2DPlane.z) + ", max " + str(max2DPlane.z))

#move camera back by the z amount it needs to
moveLocal(obj_camera, Vector((0.0, 0.0, extraShiftAmount)))
'''
if (min2DPlane.z < 0):
    moveLocal(obj_camera, Vector((0.0, 0.0, (-min2DPlane.z + extraShiftAmount))))
else:
    moveLocal(obj_camera, Vector((0.0, 0.0, (max2DPlane.z + extraShiftAmount))))
'''
