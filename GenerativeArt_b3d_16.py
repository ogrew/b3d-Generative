import bpy, math, random
import numpy as np
from mathutils import Color

rows, cols, offset, size = 14, 22, 0.1, 1.0

def DeleteMaterials() :
    for m in bpy.data.materials:
        if m.name == 'blue' or m.name == 'red' or m.name == 'yellow' :
            continue
        else :
            bpy.data.materials.remove( m )

def SelectObjects(name) :
    for item in bpy.data.objects :
        if name in item.name :
            item.select_set(True)
        else :
            item.select_set(False)

def DeleteObjects(name) :
    SelectObjects(name)
    bpy.ops.object.delete()

def map(v, min1, max1, min2, max2) :
    return min2 + (v - min1) * (max2 - min2) / (max1 - min1)

def ChangeMatProperties(mat) :
    node_tree = mat.node_tree
    nodes = node_tree.nodes

    ramp = nodes['ColorRamp']
    c = Color()
    hue = random.uniform(0.56, 0.6)
    sat = random.uniform(0.85, 1.0)
    val = random.uniform(0.66, 0.98)
    c.hsv = (hue, sat, val)
    ramp.color_ramp.elements[0].color = (c.r, c.g, c.b, 1.0)
    ramp.color_ramp.elements[1].position = random.uniform(0.75, 0.95)
    tex = nodes['Wave Texture']
    scale = tex.inputs[1]
    scale.default_value = random.uniform(1.4, 2.2)

def Generate() :
    total = rows * cols

    p, q, s, t = np.empty(0), np.empty(0), np.empty(0), np.empty(0)
    for i in range( 2 ) :
        c = math.floor( random.uniform(rows*4, total-rows*4) )
        arr1 = np.array( [c, c + 1, c + cols, c + cols + 1] )
        p = np.concatenate([p, arr1])
        arr2 = np.unique( [n % cols for n in arr1] )
        q = np.concatenate([q, arr2])
        
    for i in range( 4 ) :
        c = math.floor( random.uniform(rows, total-rows) )
        arr1 = np.array( [c, c + 1] )
        s = np.concatenate([s, arr1])
        arr2 = np.unique( [n % cols for n in arr1] )
        t = np.concatenate([t, arr2])
    
    for y in range( rows ) :
        tz = -offset * y
        for x in range( cols ) :
            tx, ty = x, y
            if tx % 2 == 0 :
                tz -= offset * 0.3
                ty += size / 2
            else :
                tz += offset * 0.3
                
            bpy.ops.mesh.primitive_circle_add(
                vertices = 80,
                radius = size,
                fill_type = 'NGON', 
                location = (tx, ty, tz)
            )
            
            index = cols * ( y - 1 ) + x
            
            copyMat = bpy.data.materials['blue']
            if index in p and x in q :
                baseMat = bpy.data.materials['red']
                copyMat = baseMat.copy()
            else :
                if index in s and x in t :
                    baseMat = bpy.data.materials['yellow']
                    copyMat = baseMat.copy()
                else :
                    baseMat = bpy.data.materials['blue']
                    copyMat = baseMat.copy()
                    ChangeMatProperties(copyMat)
            
            bpy.context.object.data.materials.append(copyMat)
        

def main() :
    DeleteObjects('Circle')
    DeleteMaterials()
    Generate()

if __name__ == "__main__":
    main()
