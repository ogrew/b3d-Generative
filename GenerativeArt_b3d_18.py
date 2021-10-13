import bpy, bmesh, math, random, requests, json
from mathutils import Vector
from perlin_noise import PerlinNoise
import numpy as np

# ref : https://gorillasun.de/blog/Smooth-Curves-with-Perlin-Noise-and-Recreating-the-Unknown-Pleasures-Album-Cover-in-P5

LENGTH = 100
COUNT = 200
NUM = 70
DEPTH = 2.0
HEIGHT = 60
materials = [ bpy.data.materials['white'], bpy.data.materials['black'] ]

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

def ApplySkinModifier(me) :
    skin = me.modifiers.new(type='SKIN', name = "Skin")

def ApplySubSurfModifier(me) :
    sub = me.modifiers.new(type='SUBSURF', name = "Subdivision")
    sub.levels = 3
    sub.render_levels = 3
    sub.quality = 4
    
def DeleteMaterials() :
    for m in bpy.data.materials:
        if 'white' in m.name or 'black' in m.name:
            continue
        bpy.data.materials.remove( m )

def main() :
    DeleteObjects('Wave')
    DeleteMaterials()
    
    colors = GetColors()
    random.shuffle( colors )
    
    s = math.floor(random.uniform(1, 65))
    xarr= np.linspace( 0, LENGTH, COUNT )
    xlist = xarr.tolist()
    
    noise = PerlinNoise(octaves = 28, seed = s)
    
    bm_vv1, bm_vv2, bm2_vv = None, None, None
    dist = 0
    half  = COUNT / 2
    x, y, z = 0, 0, 0
    w = 0.5
    r = round(random.random())
    pipeM = materials[r]
    
    for n in range( NUM ) :
        bm = bmesh.new()
        bm2 = bmesh.new()
        y = n * DEPTH
        
        for m in range( COUNT ) :
            d = w - abs(half - m) / half
            dist = max(0.035, d)
            x = xlist[m]
            z = abs(noise( [x / COUNT, y / NUM] ) * HEIGHT * dist)
            
            p1 = Vector(( x, y, 0 ))
            p2 = Vector(( x, y, z ))

            bm_v1 = bm.verts.new( p1 )
            bm_v2 = bm.verts.new( p2 )
            bm2_v = bm2.verts.new( p2 )
            
            if x > 0 :
                bm.edges.new( [ bm_vv1, bm_v1 ] )
                bm.edges.new( [ bm_vv2, bm_v2 ] )
                bm.faces.new( [ bm_vv1,bm_v1,bm_v2,bm_vv2 ] )
                bm2.edges.new( [ bm2_vv, bm2_v ] )

            bm_vv1 = bm_v1
            bm_vv2 = bm_v2
            bm2_vv = bm2_v

        color = colors[n % 5]
        mat = bpy.data.materials.new('Mat.' + str(n).zfill(2))
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs[0].default_value = (color[0] /255, color[1]/255, color[2]/255, 1.0)
        bsdf.inputs[7].default_value = 1.0

        m = bpy.data.meshes.new( 'WaveMesh' )
        bm.to_mesh( m )
        obj = bpy.data.objects.new( 'Wave', m )
        bpy.context.scene.collection.objects.link( obj )
        bpy.context.view_layer.objects.active = obj
        me =  bpy.context.object
        me.data.materials.append(mat)

        m2 = bpy.data.meshes.new( 'WavePipeMesh' )
        bm2.to_mesh( m2 )
        obj2 = bpy.data.objects.new( 'WavePipe', m2 )
        bpy.context.scene.collection.objects.link( obj2 )
        bpy.context.view_layer.objects.active = obj2
        ApplySkinModifier( obj2 )
        ApplySubSurfModifier( obj2 )
        me =  bpy.context.object
        me.data.materials.append(pipeM)
    
if __name__ == "__main__":
    main()
