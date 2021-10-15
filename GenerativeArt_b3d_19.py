import bpy, bmesh, random, math
from mathutils import Color, Vector

RADIUS = 15.0
VERTS = 180
DEPTH = 1.0
COLORS = 8
COUNT = 10
AREA = RADIUS * 9

# ref : https://blender.stackexchange.com/questions/1311/how-can-i-get-vertex-positions-from-a-mesh

def MakeMaterials() :
    materials = []
    for i in range( COLORS ) :
        mat = bpy.data.materials.new('Mat.' + str(i).zfill(2))
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
 
        c = Color()
        hue = random.random()
        sat = random.uniform( 0.9, 1.0 )
        val = random.uniform( 0.9, 1.0 )
        c.hsv = hue, sat, val
        
        bsdf.inputs[0].default_value = ( c.r, c.g, c.b, 1.0 )
        bsdf.inputs[4].default_value = 0.2
        bsdf.inputs[7].default_value = 0.7
        bsdf.inputs[18].default_value = random.uniform( 0.4, 0.9 )
        materials.append( mat )
    return materials

def DeleteObjects(name) :
    for item in bpy.data.objects :
        if name in item.name :
            item.select_set( True )
        else :
            item.select_set( False )
    bpy.ops.object.delete()

def DeleteMeshes() :
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)

def DeleteMaterials(exclude) :
    for m in bpy.data.materials:
        if m.name != exclude :
            bpy.data.materials.remove( m )

def ApplySkinModifier(me) :
    skin = me.modifiers.new( type='SKIN', name = "Skin" )
    bpy.ops.object.modifier_apply(modifier="Skin")
    bpy.ops.object.modifier_apply(modifier = "Skin")

def ApplySubSurfModifier(me) :
    sub = me.modifiers.new( type='SUBSURF', name = "Subdivision" )
    sub.levels = 3
    sub.render_levels = 3
    sub.quality = 4
    bpy.ops.object.modifier_apply( modifier = "Subdivision" )
    
def MakeNewCollection(index) :
    targetcollection = bpy.data.collections.get( "Master Collection" )
    name = "Collection " + str(index)
    if name in bpy.data.collections:
        return
    
    collection = bpy.data.collections.new( name )
    targetcollection.children.link( collection )
    return collection

def MakeFirework(index, l_min, l_max, radius, materials) :
    
    verts = random.uniform(32, VERTS)
    bpy.ops.mesh.primitive_circle_add(
        vertices = VERTS,
        radius = radius,
        enter_editmode = False,
        location = (0, 0, 0)
    )
    obj = bpy.context.active_object
    verts = obj.data.vertices
    locations = [ obj.matrix_world @ v.co for v in verts ]
    normals = [ v.normal for v in verts ]

    count = len( locations )
    m_count = len( materials )
    
    newCollection = MakeNewCollection( index )

    offset = radius * 0.015

    for i, t in enumerate( zip(locations, normals) ) :
        m = bpy.data.meshes.new('PipeMesh')
        bm = bmesh.new()

        l1 = random.uniform(- offset, offset)                
        l2 = random.uniform(l_min, l_max)
        
        loc1 = t[0] + l1 * t[1]
        loc2 = loc1 + l2 * t[1]
        #loc2 = loc1 + l2 * Vector((0.0, -1.0, 0.0))
            
        pos1 = bm.verts.new( loc1 )
        pos2 = bm.verts.new( loc2 )
        bm.edges.new( [ pos1, pos2 ] )
        
        if loc2[0] > 0.0 and loc2[1] > 0.0 :
            loc3 = loc2 + radius*5 * Vector((1.0, 1.0, 0.0))
            pos3 = bm.verts.new( loc3 )
            bm.edges.new( [ pos2, pos3 ] )
        elif loc2[0] < 0.0 and loc2[1] < 0.0 :
            loc3 = loc2 + radius*5 * Vector((-1.0, -1.0, 0.0))
            pos3 = bm.verts.new( loc3 )
            bm.edges.new( [ pos2, pos3 ] )
        elif loc2[0] > 0.0 and loc2[1] < 0.0 :
            loc3 = loc2 + radius*5 * Vector((1.0, -1.0, 0.0))
            pos3 = bm.verts.new( loc3 )
            bm.edges.new( [ pos2, pos3 ] )
        elif loc2[0] < 0.0 and loc2[1] > 0.0 :
            loc3 = loc2 + radius*5 * Vector((-1.0, 1.0, 0.0))
            pos3 = bm.verts.new( loc3 )
            bm.edges.new( [ pos2, pos3 ] )
    
        bm.to_mesh( m )
        pipe = bpy.data.objects.new( 'Pipe', m )
        newCollection.objects.link( pipe )
        bpy.context.view_layer.objects.active = pipe
        ApplySkinModifier( pipe )
        ApplySubSurfModifier( pipe )
        m_index = math.floor( random.uniform(0, m_count) )
        bpy.context.object.data.materials.append( materials[m_index] )

def main() :
    DeleteObjects( 'Pipe' )
    DeleteMaterials( 'eye' )
    mats = MakeMaterials()    
    l_max = RADIUS * 0.9
    l_min = RADIUS * 0.4
 
    center = [ 0, 0 ]
    hoge = random.uniform(0, 100)
    MakeFirework(hoge, l_min, l_max, RADIUS, mats)
    
    DeleteObjects( 'Circle' )

if __name__ == "__main__":
    main()
