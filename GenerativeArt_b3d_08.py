import bpy
from random import uniform
from random import shuffle
from random import random

materials = [
    bpy.data.materials["m1"],
    bpy.data.materials["m2"],
    bpy.data.materials["m3"],
    bpy.data.materials["m4"]
]

GRID = 12
RATE = 0.7
ARRAY_NUM = 16
ARRAY_OFFSET = 2.0
RADIUS = 0.3
HEIGHT = 3.0
THICKNESS = 20

def deleteObjects(s) :
    for item in bpy.data.objects :
        if s in item.name :
            item.select_set(True)
        else :
            item.select_set(False)
    bpy.ops.object.delete()

def resize(ratios) :
    bpy.ops.transform.resize(value=ratios)

def applyTransform() :
    bpy.ops.object.transform_apply(scale = True)

def makePyramid(pos, scale, rot) :
    z = pos[2] + HEIGHT / 2.5
    bpy.ops.mesh.primitive_cone_add(
        vertices = 4,
        radius1 = 0.0,
        radius2 = scale,
        depth = HEIGHT,
        end_fill_type = 'NGON',
        rotation = rot,
        location = (pos[0], pos[1], z)
    )
    me = bpy.context.object
    return me

def makeSphere(pos, scale) :
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions = 5,
        radius = scale,
        location = pos
    )
    bpy.ops.object.shade_smooth()
    
    me = bpy.context.object
    return me

def ApplyArrayModifier(me, scale) :
    array = me.modifiers.new(type='ARRAY', name = "Array")
    array.count = ARRAY_NUM
    array.use_relative_offset = True
    array.relative_offset_displace = (0.0, 0.0, ARRAY_OFFSET)
    bpy.ops.object.modifier_apply(modifier="Array")
    
def ApplyBooleanModifier(me, target) :
    boolean = me.modifiers.new(type='BOOLEAN', name = "Boolean")
    boolean.operation = 'DIFFERENCE'
    boolean.object = target
    bpy.context.view_layer.objects.active = me
    bpy.ops.object.modifier_apply(modifier = "Boolean")
    
def makeBlocks(pos, scale) :
    bpy.ops.mesh.primitive_cube_add(
       size = 3.0,
       location = (pos[0], pos[1], pos[2])
    )
    
    ratios = (1.0, 1.0, scale)
    resize(ratios)
    applyTransform()
    me = bpy.context.object
    return me
    
def main() :
    deleteObjects('Cone')
    deleteObjects('Icosphere')
    
    thickness = HEIGHT/THICKNESS
    
    list = [materials[1], materials[2], materials[3]]

    for i in range(GRID) :
        for j in range(GRID) :
            x = -i * 6 + uniform(-0.1, 0.1)
            y = j * 6  + uniform(-0.1, 0.1)
            z = uniform(10, 30)
            pos = [x, y, z]
        
            rz = uniform(0, 90)
            rot = (0, 0, rz)
            radius = HEIGHT/3
            
            pyramid1 = makePyramid(pos, radius, rot)
            bpy.context.object.data.materials.append(materials[0])
            pos[2] += thickness
            pyramid2 = makePyramid(pos, radius, rot)
            
            blocks = makeBlocks(pos, scale = 0.02)

            ApplyArrayModifier(me = blocks, scale = radius)
            ApplyBooleanModifier(me = pyramid1,target = blocks)
            ApplyBooleanModifier(me = pyramid1,target = pyramid2)

            bpy.data.objects[pyramid2.name].select_set(True)
            bpy.ops.object.delete()

            shuffle(list)
            pos[2] += HEIGHT/1.2
            makeSphere(pos, RADIUS)
            bpy.context.object.data.materials.append(list[0])
            
            pos[2] += HEIGHT/4.5
            makeSphere(pos, RADIUS)
            bpy.context.object.data.materials.append(list[1])
            
            pos[2] += HEIGHT/4.5
            makeSphere(pos, RADIUS)
            bpy.context.object.data.materials.append(list[2])
            
        deleteObjects('Cube')
            
main()
