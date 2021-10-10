import bpy, random, bmesh, requests, json
import numpy as np

# ref: https://blender.stackexchange.com/questions/135963/how-to-add-a-line-between-two-moving-objects-with-python

COUNT = 250
SIZE = 2
AREA = 100
TOTAL_LIMIT = 250
EACH_LIMIT = 5

def GetColors() :
    res = requests.post( 'http://colormind.io/api/', data = '{"model":"default"}' )
    json_load = res.json()
    colors = json_load['result']
    return colors

def DeleteMaterials(exclude) :
    for m in bpy.data.materials:
        if m.name != exclude :
            bpy.data.materials.remove( m )

def SelectObjects(name) :
    for item in bpy.data.objects :
        if name in item.name :
            item.select_set(True)
        else :
            item.select_set(False)
            
def MakeMaterials(colors) :
    materials = []
    for i in range( len(colors) ) :
        mat = bpy.data.materials.new('Mat.' + str(i).zfill(2))
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        color = colors[i]
        bsdf.inputs[0].default_value = (color[0] /255, color[1]/255, color[2]/255, 1.0)
        # bsdf.inputs[17].default_value = (color[0] /255, color[1]/255, color[2]/255, 1.0)
        bsdf.inputs[4].default_value = 0.8
        bsdf.inputs[7].default_value = 0.2
        materials.append( mat )
    return materials
        
def DeleteObjects(name) :
    SelectObjects(name)
    bpy.ops.object.delete()

def SetCubes(materials) :
    posArr = np.array([ ])
    posList = posArr.tolist()
    l = len(materials)
    for i in range( COUNT ) :
        tx = random.uniform(-AREA, AREA)
        ty = random.uniform(-AREA, AREA)
        tz = random.uniform(-AREA, AREA)
        pos = [tx, ty, tz]
        posList.append(pos)
        r = random.uniform(SIZE, SIZE*1.5)
        bpy.ops.mesh.primitive_ico_sphere_add( subdivisions = 3, radius = r, location = pos )
        bpy.ops.object.shade_smooth()
        mat = materials[ i % l ]
        bpy.context.object.data.materials.append( mat )
        
    posArr = np.asarray(posList)
    return posArr

def ApplySkinModifier(me) :
    skin = me.modifiers.new(type='SKIN', name = "Skin")
    bpy.ops.object.modifier_apply(modifier="Skin")
    bpy.ops.object.modifier_apply(modifier = "Skin")

def ApplySubSurfModifier(me) :
    sub = me.modifiers.new(type='SUBSURF', name = "Subdivision")
    sub.levels = 3
    sub.render_levels = 3
    sub.quality = 4
    bpy.ops.object.modifier_apply(modifier = "Subdivision")

def main() :
    DeleteObjects('Icosphere')
    DeleteObjects('Pipe')
    DeleteMaterials('line')

    colors = GetColors()
    materials = MakeMaterials( colors )
    cubes = SetCubes( materials )

    maxDist = AREA/2
    minDist = AREA/8
    offset = AREA/30
    total = 0
    pairs = []
    
    for i in range( COUNT ) :
        each = 0
        p1 = cubes[i]
        
        if random.random() < 0.1 :
            continue
        
        for j in range( COUNT ) :
            if i == j :
                continue
            p2 = cubes[j]
             
            dist = np.linalg.norm(p1 - p2)
            if dist < maxDist and dist > minDist :

                k1, k2 = max(i, j), min(i, j)
                pair = [k1, k2]
                if (pair in pairs) or (total > TOTAL_LIMIT) or (each > EACH_LIMIT) :
                    continue
                
                pairs.append( pair )
                total += 1
                each += 1
                
                m = bpy.data.meshes.new('PipeMesh')
                bm = bmesh.new()
                p1List = p1.tolist()
                p2List = p2.tolist()

                v1 = bm.verts.new( p1List )
                v2 = bm.verts.new( p2List )
                
                o1 = random.uniform(-offset, offset)
                o2 = random.uniform(-offset, offset)
                o3 = random.uniform(-offset, offset)

                px = ( p1List[0] + 2 * p2List[0] ) / 3 + o1
                py = ( p1List[1] + 2 * p2List[1] ) / 3 + o2
                pz = ( p1List[2] + 2 * p2List[2] ) / 3 + o3
                p3List = (px, py, pz)            
                v3 = bm.verts.new( p3List )

                px = ( 2 * p1List[0] + p2List[0] ) / 3 + o3
                py = ( 2 * p1List[1] + p2List[1] ) / 3 + o1
                pz = ( 2 * p1List[2] + p2List[2] ) / 3 + o2
                p4List = (px, py, pz)            
                v4 = bm.verts.new( p4List )

                e = bm.edges.new( [ v1, v4 ] )
                e = bm.edges.new( [ v4, v3 ] )
                e = bm.edges.new( [ v3, v2 ] )
                
                bm.to_mesh( m )
                obj = bpy.data.objects.new( 'Pipe', m )
                bpy.context.scene.collection.objects.link( obj )
                ApplySkinModifier( obj )
                ApplySubSurfModifier( obj )
                bpy.context.view_layer.objects.active = obj
                bpy.context.object.data.materials.append( bpy.data.materials["line"] )

if __name__ == "__main__":
    main()
