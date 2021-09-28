import bpy, bmesh
from random import uniform, random
from math import floor
from mathutils import Vector

rows = 18
cols = 9
rate = 0.235
materials = [
    bpy.data.materials["Red"],
    bpy.data.materials["Yellow"],
    bpy.data.materials["Blue"]
]

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
    
def JoinObjects(targetName, afterName) :
    SelectObjects(targetName)
    bpy.ops.object.join()
    bpy.context.view_layer.objects.active.name = afterName

def ApplySolidifyModifier(me) :
    sol = me.modifiers.new(type='SOLIDIFY', name = "Solidify")
    sol.solidify_mode = 'NON_MANIFOLD'
    sol.nonmanifold_boundary_mode = 'FLAT'
    sol.thickness = 0.06
    bpy.ops.object.modifier_apply(modifier = "Solidify")  
    
def AddBox(pos, name) :
    bpy.ops.mesh.primitive_cube_add(
        size = 0.999,
        enter_editmode = True,
        location = pos
    )
    obj = bpy.context.edit_object
    obj.name = name
    me = obj.data

    if random() < 0.1 :
        bpy.ops.object.mode_set(mode='OBJECT')
        ApplySolidifyModifier(obj)
        return

    bm = bmesh.from_edit_mesh(me)
    for f in bm.faces :
        f.select = False
        if f.normal == Vector((0.0, 0.0, 1.0)) :
            f.select = True
    faceUp = [f for f in bm.faces if f.select]
    bmesh.ops.delete(bm, geom=faceUp, context='FACES')

    edgeUpIndices = (2, 5, 8, 11)
    edgeUpIndex = edgeUpIndices[floor(uniform(0, 4))]
    
    for e in bm.edges :
        e.select = False
        if e.index == edgeUpIndex :
            e.select = True
    
    edgeUp = [e for e in bm.edges if e.select]
    bmesh.update_edit_mesh(me, True)
    z = uniform(0.1, 0.45)
    v = (0, 0, z)
    if random() < 0.3 :
        v = (0, 0, -z)
    bpy.ops.transform.translate(
        value = v, 
        orient_type = 'GLOBAL', 
        orient_matrix = ((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
        orient_matrix_type = 'GLOBAL', 
        constraint_axis = (False, False, True), 
    )
    bpy.ops.object.mode_set(mode='OBJECT')
    ApplySolidifyModifier(obj)

def AddHole(pos, name, size) :
    bpy.ops.mesh.primitive_cube_add(
        size = 1.0,
        enter_editmode = False,
        location = pos
    )
    bpy.ops.transform.resize(value = size)
    bpy.context.object.name = name
    
def AddSphere(pos, name, size) :
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions = 4,
        radius = size,
        location = pos
    )
    bpy.context.object.name = name
    bpy.ops.object.shade_smooth()
    
def ApplyBooleanModifier(me, target) :
    boolean = me.modifiers.new(type='BOOLEAN', name = "Boolean")
    boolean.operation = 'DIFFERENCE'
    boolean.object = target
    bpy.context.view_layer.objects.active = me
    bpy.ops.object.modifier_apply(modifier = "Boolean")

def main() :
    DeleteObjects('Cube')
    for i in range( rows ) :
        for j in range( cols ) :
            pos = [i, j, 0]
            AddBox(pos, 'Room')
            
            r = random()
            if r < rate :
                pos4 = [ pos[0] + 0.03, pos[1] + 0.05, pos[2] - 0.1 ]
                AddSphere(pos4, 'Cube_Sphere', 0.145)
                if r < rate/3 :
                    bpy.context.object.data.materials.append(materials[0])
                elif r < rate * 2/3 :
                    bpy.context.object.data.materials.append(materials[1])
                else :
                    bpy.context.object.data.materials.append(materials[2])
            
            if i < rows - 1 and j < cols - 1 :
                if random() < 0.9 :
                    pos2 = [pos[0] + 0.53, pos[1] + 0.5, pos[2] - 0.19]
                    AddHole(pos2, 'Joint', [0.35, 0.35, 0.2])
                if random() < 0.5 :
                    pos3 = [pos[0] + 1.05, pos[1] + 0.5, pos[2] - 0.105]
                    AddHole(pos3, 'Hole', [0.2, 0.5, 0.6])

    JoinObjects('Room', 'Cube_Room')
    JoinObjects('Joint', 'Cube_Joint')
    JoinObjects('Hole', 'Cube_Hole')
    ApplyBooleanModifier(bpy.data.objects['Cube_Room'], bpy.data.objects['Cube_Hole'])
    DeleteObjects('Cube_Hole')

if __name__ == "__main__":
    main()
