import bpy, bmesh, requests, json
from random import uniform, random, shuffle
from math import floor

LOOP = 9
WIDTH = 10
HEIGHT = 10
materials = []

def GetColors() :
    res = requests.post( 'http://colormind.io/api/', data = '{"model":"default"}' )
    json_load = res.json()
    colors = json_load['result']
    return colors

def SelectObjects(name) :
    for item in bpy.data.objects :
        if name in item.name :
            item.select_set(True)
        else :
            item.select_set(False)
            
def DeleteObjects(name) :
    SelectObjects(name)
    bpy.ops.object.delete()
    
def DeleteMaterials() :
    for m in bpy.data.materials:
        bpy.data.materials.remove( m )

def MakePlane(x, y, w, h, count, colors) :
    isLast = count == 0
    if not isLast :
        return
     
    cx = x + w/2
    cy = y + h/2
    cz = - count * 0.02
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD',
        location=(cx, cy, cz)
    )
    bpy.ops.transform.resize( value = (w*0.96, h*0.96, 1), constraint_axis=(True,True,True) )
    # bpy.ops.transform.resize( value = (w*1.001, h*1.001, 1), constraint_axis=(True,True,True) )
    
    obj = bpy.context.active_object

    bpy.context.view_layer.objects.active = obj
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_mode(type= 'VERT')

    bpy.ops.mesh.select_all(action = 'SELECT')

    param = (1+count) * 0.5
    bpy.ops.mesh.bevel(
        offset_type='OFFSET',
        offset = param,
        segments = 12,
        offset_pct = 0,
        vertex_only = True,
        clamp_overlap = True
    )

    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    index = floor( uniform(0, 5) )
    mat = materials[index]
    bpy.context.object.data.materials.append(mat)
    
def MakeMaterials( colors ) :
    global materials
    for i in range( len(colors) ) :
        color = colors[i]
        name = 'Mat.' + str(i).zfill(2)
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs[0].default_value = (color[0] /255, color[1]/255, color[2]/255, 1.0)
        bsdf.inputs[7].default_value = 1.0
        
        materials.append( mat )
    
def DivideSpace(x, y, w, h, count, colors) :
    MakePlane(x, y, w, h, count, colors)
    count -= 1
    if count >= 0 :
        
        if( w >= h ) :
            randomW = uniform(w * 0.2, w * 0.8)
            DivideSpace(x, y, randomW, h, count, colors)
            DivideSpace(x + randomW, y, w - randomW, h, count, colors)
        
        elif( w < h ) :
            randomH = uniform(h * 0.2, h *0.8)
            DivideSpace(x, y, w, randomH, count, colors)
            DivideSpace(x, y+randomH, w, h - randomH, count, colors)
    
def moveX(edge) :
    bpy.ops.object.select_all( action = 'DESELECT' )
    for item in bpy.data.objects :
        if item.location[0] > edge :
            item.select_set(True)
        else :
            item.select_set(False)
    bpy.ops.transform.translate(value=(0.5, 0, 0), constraint_axis=(True,True,True))

def moveY(edge) :
    bpy.ops.object.select_all( action = 'DESELECT' )
    for item in bpy.data.objects :
        if item.location[1] > edge :
            item.select_set(True)
        else :
            item.select_set(False)
    bpy.ops.transform.translate(value=(0, 0.5, 0), constraint_axis=(True,True,True))
    
def Move() :
    moveX(WIDTH/2)
    moveY(HEIGHT * 3/5)

def main() :
    DeleteObjects('Cube')
    DeleteMaterials()
    colors = GetColors()
    MakeMaterials( colors )
    DivideSpace(0, 0, WIDTH, HEIGHT, LOOP, colors)
    DeleteObjects('trash_')
    Move()

if __name__ == "__main__":
    main()
