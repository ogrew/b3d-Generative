import bpy
import random

GRID = 12
COUNT = 24
OFFSET = 2.4
RATE = 0.86
GAP = 0.24

materialList = [
    bpy.data.materials['c'],  # normal
    bpy.data.materials['m3'], # white
    bpy.data.materials['m2'], # red
    bpy.data.materials['m1'], # yellow
    bpy.data.materials['m0'], # black
]

scaleOffset = bpy.data.objects['A_Empty']
tex = bpy.data.textures['Stucci']

def ApplyDisplaceModifier(dir, power, count) :
    bpy.ops.object.modifier_add(type='DISPLACE')
    target = bpy.context.object
    disp = target.modifiers["Displace"]
    
    disp.texture = tex
    disp.strength = power
    disp.direction = dir
    disp.texture_coords = 'OBJECT'
    disp.texture_coords_object = scaleOffset
    
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Displace")
    
def ApplyArrayModifier(num, px, py) :
    bpy.ops.object.modifier_add(type='ARRAY')
    target = bpy.context.object
    array = target.modifiers["Array"]
    
    array.count = COUNT
    array.use_relative_offset = False
    array.use_object_offset = True
    
    gap = GAP/4
    px = px + random.uniform(-gap, gap)
    py = py + random.uniform(-gap, gap)
    
    bpy.ops.object.empty_add(
        type='PLAIN_AXES', location=(px, py, 0.3)
    )
    bpy.ops.transform.resize(value = (RATE, RATE, RATE))
    array.offset_object = bpy.context.active_object
    
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Array")

def MakeTrunks(px, py) :
    h = 2.0
    bpy.ops.mesh.primitive_cylinder_add(
        vertices = 12,
        radius = 0.15,
        depth = h,
        location = (px, py, -h/2)
    )

for i in range(GRID) :
    for j in range(GRID) :
        r = random.random()
        x = i * OFFSET
        y = j * OFFSET
        z = 0.0
        
        x += random.uniform(-GAP, GAP)
        y += random.uniform(-GAP, GAP)
        bpy.ops.mesh.primitive_circle_add(
            vertices = 128, radius = 1.3, fill_type='NGON', location=(x, y, z)
        )
        ApplyDisplaceModifier('X', 0.3, 0)
        ApplyDisplaceModifier('Y', 0.3, 1)
        ApplyArrayModifier(6, x, y)

        if r < 0.70 :
            mat = materialList[0]
        elif r < 0.83 :
            mat = materialList[1]
        elif r < 0.9 :
            mat = materialList[2]
        elif r < 0.96 :
            mat = materialList[3]
        else :
            mat = materialList[4]

        bpy.context.object.data.materials.append(mat)
        MakeTrunks(x, y)
