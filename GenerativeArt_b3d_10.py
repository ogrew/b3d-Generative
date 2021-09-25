import bpy
import bmesh
from random import *
from math import *

n =0.17
l = 14
materials = [
    bpy.data.materials["m4"], # white
    bpy.data.materials["m1"],
    bpy.data.materials["m2"],
    bpy.data.materials["m3"]
]

def AddBasePrimitve() :
        bpy.ops.mesh.primitive_ico_sphere_add(
            subdivisions = 3,
            radius = 1.0,
            enter_editmode=False,
            location=(0, 0, 0)
        )

def ApplySubSurfModifier(me) :
    sub = me.modifiers.new(type='SUBSURF', name = "Subdivision")
    sub.levels = 4
    sub.render_levels = 4
    sub.quality = 4
    # bpy.ops.object.modifier_apply(modifier = "Subdivision")

def ApplySimpleDeformModifier(me) :
    sd = me.modifiers.new(type='SIMPLE_DEFORM', name = "Deform")
    sd.deform_method = 'STRETCH'
    sd.factor = 3
    sd.deform_axis = 'Z'
    # bpy.ops.object.modifier_apply(modifier = "Deform")

def main() :
    AddBasePrimitve()
    ob = bpy.context.object
    me = ob.data
    me.materials.append(materials[0])
    me.materials.append(materials[1])
    me.materials.append(materials[2])
    me.materials.append(materials[3])
    count = len(me.polygons)

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type="FACE")
    bm = bmesh.from_edit_mesh(bpy.context.object.data)
    
    tList = [
        [0, 0, n],
        [n, 0, n],
        [-n, 0, n],
        [n/2, 0, n],
        [-n/2, 0, n],
        [n, 0, n],
        [-n, 0, n],
        [n/2, 0, n],
        [-n/2, 0, n],
        [0, 0, n],
    ]
    m = 1/(l/2)
    tLen =len(tList)
    
    for i in range( count ) :
        bpy.ops.mesh.select_all(action='DESELECT')
        bm.faces.ensure_lookup_table()
        bm.faces[index].select = True
        midx = floor(uniform(1, 4))
        face = bm.faces[index]
        face.material_index = midx
    
        for j in range(l) :
            t = tList[j % tLen]
            bpy.ops.mesh.extrude_region_move(
                TRANSFORM_OT_translate={
                    "value": t,
                    "constraint_axis": (True, True, True),
                    "orient_type": 'NORMAL'
                }
            )
            
            if j < l / 3 :
                s = 0.8
            elif j < l/2 :
                s = 3.2
            elif j < l -2 :
                s = 0.75
            else :
                s =  2.0
            
            bpy.ops.transform.resize(
                value = (s, s, s), 
                orient_matrix = ((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
                orient_type='GLOBAL', 
            )

    bpy.ops.object.mode_set(mode='OBJECT')
    ApplySubSurfModifier(bpy.context.object)
    ApplySimpleDeformModifier(bpy.context.object)
    #bpy.ops.transform.resize(value=(1, 1, 1.5))

if __name__ == "__main__":
    main()
