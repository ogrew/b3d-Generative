import bpy
from random import random

STEPS = 18
LENGTH = 22
SIZE  = 1.0
materialList = [
    bpy.data.materials['m0'], # white
    bpy.data.materials['m1'], # red
    bpy.data.materials['m2'], # yellow
    bpy.data.materials['m3'], # black
]

def setScale(values) :
    bpy.ops.transform.resize(value = values)
    
def setRandomMat(m) :
    if m < 0.9 :
        mat = materialList[0]
    elif m < 0.94 :
        mat = materialList[1]
    elif m < 0.98 :
        mat = materialList[2]
    else :
        mat = materialList[3]

    bpy.context.object.data.materials.append(mat)
    
def makeChild(pos, pSize, v, edge) :
    cSize = pSize * 0.5
    of1 = pSize * 0.75
    of2 = pSize * 0.25
    
    e = edge / 3

    if v < e :
        bpy.ops.mesh.primitive_cube_add(size = cSize, location = (pos[0] + of1, pos[1] + of2, pos[2] - of2))
    elif v < e*2 :
        bpy.ops.mesh.primitive_cube_add(size = cSize, location = (pos[0] + of2, pos[1] - of1, pos[2] - of2))
    else :
        bpy.ops.mesh.primitive_cube_add(size = cSize, location = (pos[0] + of1, pos[1] + of2, pos[2] + of2))

    m = random()   
    setRandomMat(m)

    if m < 0.5 :
        name = bpy.context.active_object.name
        target = bpy.data.objects[name]
        makeChild(target.location, cSize, m, 0.5)         

for s in range(STEPS) :
    for l in range(LENGTH) :
        r = random()

        if r < 0.1 :
    
            scale = 2.0
            v = scale / 4
            r2 = random()
            if r2 < 0.3 :
                scale = 3.0
                v = scale / 3
                
            o = 1.001
            
            if r < 0.05 :
                bpy.ops.mesh.primitive_cube_add(size = SIZE, location = (l - s + s, l + s - v, s))
                setScale((o, scale * o, o))
            else :
                bpy.ops.mesh.primitive_cube_add(size = SIZE, location = (l - s + s, l + s, s + v))
                setScale((o, o, scale * o))
        else :
            bpy.ops.mesh.primitive_cube_add(size = SIZE, location = (l - s + s, l + s, s))

        m = random()
        setRandomMat(m)          
        
        r3 = random()
        edge = 0.4
        if r3 < edge :
            name = bpy.context.active_object.name
            target = bpy.data.objects[name]
            makeChild(target.location, SIZE, r3, edge)    
        
    s += 1.0
