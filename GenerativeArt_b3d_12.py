import bpy
from random import *
from mathutils import *

materials = [
    bpy.data.materials['m1'],
    bpy.data.materials['m2'],
    bpy.data.materials['m3']
]
count = 14
radius = 0.7
noise_scale = 0.4
noise_height = 1.0

def SelectObjects(name) :
    active = True
    for item in bpy.data.objects :
        if name in item.name :
            item.select_set(True)
            if active :
                bpy.context.view_layer.objects.active = item
                active = False
        else :
            item.select_set(False)

def DeleteObjects(name) :
    SelectObjects(name)
    bpy.ops.object.delete()

def main() :
    DeleteObjects('Icosphere')
    
    for mat in materials :
        
        node_tree = mat.node_tree
        nodes = node_tree.nodes

        tx = nodes['tx']
        scale = nodes['scale']

        u = uniform(0.0, 2.0)
        tx.outputs['Value'].default_value = u
        u = uniform(0.7, 3.8)
        scale.outputs['Value'].default_value = u

        r = uniform(0.0, 0.7)
        g = uniform(0.1, 0.8)
        b = uniform(0.2, 0.9)
        color = [r, g, b]
        shuffle( color )
        color = color + [ 1.0 ]
        ramp = nodes['ColorRamp']
        ramp.color_ramp.elements[1].color = color
        
    for i in range( count ) :
        for j in range( count ) :
            v = Vector((i*noise_scale, j*noise_scale, 0))
            h = 0
            # h = noise.noise(v)
            # h *= noise_height
            angle = uniform(0, 180)

            bpy.ops.mesh.primitive_ico_sphere_add(
                subdivisions = 5,
                radius = radius,
                location = (i, j, h)
            )
            bpy.ops.object.shade_smooth()
            
            r = random()
            if r < 1/3 :
                bpy.ops.transform.rotate(value=angle, orient_axis = 'X')
            elif r < 2/3 :
                bpy.ops.transform.rotate(value=angle, orient_axis = 'Y')
            else :
                bpy.ops.transform.rotate(value=angle, orient_axis = 'Z')

            r = random()
            if r < 1/3 :
                bpy.context.object.data.materials.append(materials[0])
            elif r < 2/3 :
                bpy.context.object.data.materials.append(materials[1])
            else :
                bpy.context.object.data.materials.append(materials[2])

if __name__ == "__main__":
    main()
