import bpy, bmesh, math, sys, random, requests, json
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
        
def MakeMaterials( colors ) :
    global materials
    for i in range( len(colors) ) :
        color = colors[i]
        name = 'Mat.' + str(i).zfill(2)
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs[0].default_value = (color[0] /255, color[1]/255, color[2]/255, 1.0)
        bsdf.inputs[4].default_value = 0.6
        bsdf.inputs[7].default_value = 0.4
        materials.append( mat )

def AddLine(r, px, py, pz, rate, length) :
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius = r,
        segments = 32,
        ring_count = 14,
        align = 'WORLD',
        location = (px, py, pz)
    )
    obj = bpy.context.object
    matrix =obj.matrix_world
    data = obj.data
    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.mesh.select_mode(type = 'VERT')
    bm = bmesh.from_edit_mesh(data)
    bm.verts.ensure_lookup_table()
    
    for v in bm.verts :
        pos = v.co
        if abs(pos.z) <= 0.0001 :
            v.select_set(True)
        else :
            v.select_set(False)
    bpy.ops.mesh.edge_face_add()
    bpy.ops.mesh.extrude_region_move( TRANSFORM_OT_translate={ "value" : [length, 0, 0] })
    bpy.ops.transform.resize(
        value=(rate, rate, rate),
        orient_type='GLOBAL', 
        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
        orient_matrix_type='GLOBAL'
    )

    bpy.ops.object.mode_set(mode = 'OBJECT')
    
    bpy.ops.object.shade_smooth()
    data.use_auto_smooth = True
    
    index = math.floor( random.uniform(0, 5) )
    mat = materials[index]
    data.materials.append(mat)
    
def main() :
    DeleteObjects('Sphere')
    DeleteMaterials()
    colors = GetColors()
    MakeMaterials( colors )
    
    for i in range(6) :
        pz = i*0.02
        for j in range(60) :
            pz += 0.001

            px1 = i * 10 + random.uniform(-2.0, 2.0)
            py1 = j * 2.1 + random.uniform(-1.0, 0.5)
            r1 = random.uniform(0.7, 2.1)
            l1 = random.uniform(30, 60)

            AddLine(r1, px1, py1, pz, 1, l1)

            pz += 0.001

            r2 = random.uniform(0.3, 1.2)
            rate = random.uniform(0.9, 1.5)
            l2 = random.uniform(20, 40)
            px2 = 5 + i * 10 + random.uniform(-1.0, 1.0)
            py2 = j * 2.1 + random.uniform(-0.8, 0.8)

            AddLine(r2, px2, py2, pz, rate, l2)
            
if __name__ == "__main__":
    main()
