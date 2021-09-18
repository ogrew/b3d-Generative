import bpy
import math
from random import random

rad = 0.78539816339745
sqrt2 = 1.41421356237
DEPTH = 4
SIZE = 0.5
MIN_RATE = 0.7
VERTS = 32

materials = [
    bpy.data.materials["m0"],
    bpy.data.materials["m1"],
    bpy.data.materials["m2"],
    bpy.data.materials["m3"]
]

def map(v, min1, max1, min2, max2) :
    return min2 + (v - min1) * (max2 - min2) / (max1 - min1)

def SelectObjects(name) :
    for item in bpy.data.objects :
        if name in item.name :
            item.select_set(True)
        else :
            item.select_set(False)

def JoinObjects(name1, name2) :
    SelectObjects(name1)
    bpy.ops.object.join()
    bpy.context.view_layer.objects.active.name = name2
    
def DeleteObjects(name) :
    SelectObjects(name)
    bpy.ops.object.delete()

def DeleteParent(name) :
    objects = bpy.data.objects
    found = name in bpy.data.objects
    if found:
        objects.remove(objects[name])

def SetMaterial(data) :
    p = random()
    if p < 0.7 :
        data.materials.append(materials[0])
    elif p < 0.8 :
        data.materials.append(materials[1])
    elif p < 0.9 :
        data.materials.append(materials[2])
    else :
        data.materials.append(materials[3])
        
def MakeCone(size, height,pos) :
        bpy.ops.mesh.primitive_cone_add(
            vertices = VERTS,
            radius1 = size, 
            radius2 = 0,
            depth = height,
            location=(pos[0], pos[1], pos[2]),
            rotation=(0, 0, rad)
        )
        bpy.ops.object.shade_smooth()

def Sierpinski(parent, size, height, count) :

    if count < 0 :
        return
    
    count -= 1
    pos = parent.location
    hh = height/2

    # make 5 children
    r = random()
    p = map(count, 0, DEPTH-2, MIN_RATE, 1.0)    
    pName = parent.name

    if r < p :
        pos1 = (pos[0]-hh, pos[1]-hh, pos[2]-hh)
        MakeCone(size, height,pos1)
        c1 = bpy.context.object
        c1.name = "CONE-" + str(count) + "(" + pName+ ").c1" 
        SetMaterial(c1.data)
        Sierpinski(c1, size/2, height/2, count)

        pos2 = (pos[0]+hh, pos[1]-hh, pos[2]-hh)
        MakeCone(size, height,pos2)
        c2 = bpy.context.object
        c2.name = "CONE-" + str(count) + "(" + pName+ ").c2" 
        SetMaterial(c2.data)
        Sierpinski(c2, size/2, height/2, count)

        pos3 = (pos[0]-hh, pos[1]+hh, pos[2]-hh)
        MakeCone(size, height,pos3)
        c3 = bpy.context.object
        c3.name = "CONE-" + str(count) + "(" + pName+ ").c3" 
        SetMaterial(c3.data)
        Sierpinski(c3, size/2, height/2, count)

        pos4 = (pos[0]+hh, pos[1]+hh, pos[2]-hh)
        MakeCone(size, height,pos4)
        c4 = bpy.context.object
        c4.name = "CONE-" + str(count) + "(" + pName+ ").c4" 
        SetMaterial(c4.data)
        Sierpinski(c4, size/2, height/2, count)

        pos5 = (pos[0], pos[1], pos[2]+hh)
        MakeCone(size, height,pos5)
        c5 = bpy.context.object
        c5.name = "CONE-" + str(count) + "(" + pName+ ").c5" 
        SetMaterial(c5.data)
        Sierpinski(c5, size/2, height/2, count)

        DeleteParent(pName)

def ApplyMirrorModifier(me, empty) :
    mirror = me.modifiers.new(type='MIRROR', name = "Mirror")
    mirror.mirror_object = empty
    mirror.use_axis = (False, False, True)
    bpy.ops.object.modifier_apply(modifier="Mirror")

def main():
    DeleteObjects("CONE")
    DeleteObjects("SIERPINSKI")
    DeleteObjects("Empty")

    height = SIZE * sqrt2
    # make parent
    bpy.ops.mesh.primitive_cone_add(
        vertices = VERTS,
        radius1 = SIZE * 2, 
        radius2 = 0,
        depth = height * 2,
        location = (0, 0, height),
        rotation = (0, 0, rad)
    )
    p = bpy.context.object
    p.name = "CONE.p" 
    
    parent = bpy.context.object
    Sierpinski(parent, SIZE, height, DEPTH)
    
    JoinObjects("CONE", "SIERPINSKI")
    obj = bpy.context.object
    
    bpy.ops.object.empty_add(location = (0, 0, height))
    empty = bpy.context.object
    
    ApplyMirrorModifier(obj, empty)
    
if __name__ == "__main__":
    main()
