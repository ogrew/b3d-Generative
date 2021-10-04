import bpy; import requests; import json; import random; import math
from perlin_noise import PerlinNoise

def GetColors() :
    res = requests.post(
        'http://colormind.io/api/',
        data = '{"model":"default"}'
    )
    json_load = res.json()
    colors = json_load['result']
    return colors

def DeleteMaterials() :
    for m in bpy.data.materials:
        bpy.data.materials.remove( m )
        
def Rotate(val, axis) :
    bpy.ops.transform.rotate(value = val, orient_axis=axis)

def ApplyArrayModifier(me, num) :
    array = me.modifiers.new(type='ARRAY', name = "Array")
    array.count = num
    array.use_relative_offset = True
    array.relative_offset_displace = (0.0, 0.0, 2.7)
    bpy.ops.object.modifier_apply(modifier="Array")

def map(v, min1, max1, min2, max2) :
    return min2 + (v - min1) * (max2 - min2) / (max1 - min1)

def main() :
    DeleteMaterials()
    s = math.floor(random.uniform(1, 65))
    noise = PerlinNoise(octaves = 9, seed = s)
    for j in range( 30 ) :
        res = GetColors()
        colors = res
        colors.extend(res)
        colors.extend(res)
        random.shuffle(colors)
        l = len( colors )
        for i in range( l ) :
            mat = bpy.data.materials.new('Mat.' + str(i).zfill(2))
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            color = colors[i]
            bsdf.inputs[0].default_value = (color[0] /255, color[1]/255, color[2]/255, 1.0)
            bsdf.inputs[7].default_value = 1.0

            if j % 2 == 0 :
                tx = i
            else :
                tx = i + 0.5

            ty = j - (j / 2) * 0.35
            tz = 0
            vert = 6
            r = 0.5
            if random.random() < 0.05 :
                vert = 64
                r = 0.45
            bpy.ops.mesh.primitive_circle_add(
                vertices = vert, radius = r,
                enter_editmode=True, fill_type = 'NGON',
                align='WORLD',  location=(tx, ty, tz)
            )
            bpy.ops.mesh.extrude_region_move( TRANSFORM_OT_translate={
                    "value" : (0, 0, 0.03),
                    "constraint_axis" : (True, True, True),
                    "orient_matrix_type" : 'LOCAL'
            } )
            bpy.ops.object.mode_set(mode='OBJECT')

            me =  bpy.context.object
            me.data.materials.append(mat)
            n = noise([i/20.0, j/25.0])
            height = map(n, -0.5, 0.5, 2, 20)
            ApplyArrayModifier(me, height)    

if __name__ == "__main__":
    main()
