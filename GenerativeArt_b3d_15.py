import bpy, bmesh, math, random
from mathutils import Vector
import numpy as np

w, h = 3.0, 4.5
count, end, loop, amp = 600, 50, 33, 2.5
freq = 1/30

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

def calcWave(v, amp, index):
    if index % 2 == 0 :
        return np.cos(v * 1/6 + np.pi/2) * amp/0.75
    else :
        return np.sin(v * 1/2) * amp

def setMat(index) :
    if index % 2 == 0:
        bpy.context.object.data.materials.append(bpy.data.materials['m1'])
    else :
        bpy.context.object.data.materials.append(bpy.data.materials['m2'])

def MakeSineWave(width, height, count, end, index, length) :
    bm    = bmesh.new()
    loops = []
    xMax = end * np.pi
    yOffset = (index - length/2) * w * 2.0
    x = np.linspace( 0, xMax, count )
    for zw, xw in zip( [1, 1, 0, 0], [-1, 1, 1, -1] ):
        loop = []
        z = calcWave( x, amp, index ) + zw * height
        y = calcWave( x, 0, index ) + xw * width + yOffset
        for xi, yi, zi in zip( x, y, z ) :
            vec = Vector(( xi, yi, zi ))
            loop.append( bm.verts.new( vec ) )
        loops.append( loop )
        
    for i in range( len( loops ) ) :
        for j in range( len( loops[i] ) - 1 ) :
            verts = []
            if i == len( loops ) - 1 :
                verts.append( loops[0][j] )
                verts.append( loops[0][j + 1] )
                verts.append( loops[i][j + 1] )
                verts.append( loops[i][j] )
            else:
                verts.append( loops[i][j] )
                verts.append( loops[i][j + 1] )
                verts.append( loops[i + 1][j + 1] )
                verts.append( loops[i + 1][j] )
            bm.faces.new(verts)

    for i in [0, len( loops[0] ) - 1 ] :
        fs = []
        for j in range( len(loops) ) :
            fs.append( loops[j][i] )
        bm.faces.new( fs )
        
    m = bpy.data.meshes.new( 'WavePatternMesh' )
    bm.to_mesh( m )
    obj = bpy.data.objects.new( 'WavePattern', m )
    bpy.context.scene.collection.objects.link( obj )
    bpy.context.view_layer.objects.active = obj
    bpy.data.objects[obj.name].select_set( True )
    bpy.ops.object.shade_smooth()
    bpy.context.object.data.use_auto_smooth = True
    setMat(index)

def MakeSphere(i, j) :
    edge = end * np.pi
    tx = i * 12 + 25
    ty = j * 9 - 36
    tz = random.uniform(20, 35)
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=3,
        radius = 1.25,
        location = [tx, ty, tz]
    )
    bpy.ops.object.shade_smooth()
    if j % 2 == 0 :
        bpy.context.object.data.materials.append(bpy.data.materials['m3'])
    else :
        bpy.context.object.data.materials.append(bpy.data.materials['m4'])
    bpy.ops.rigidbody.object_add()
    bpy.context.object.rigid_body.mass = 2
    bpy.context.object.rigid_body.collision_shape = 'MESH'


def main() :
    DeleteObjects('WavePattern')
    DeleteObjects('Icosphere')
    for i in range( loop ) :
        MakeSineWave(w, h, count, end, i, loop)
    
    JoinObjects('WavePattern', 'WavePatterns')

    SelectObjects('WavePatterns')    
    bpy.ops.rigidbody.object_add()
    waves = bpy.context.object 
    waves.rigid_body.type = 'PASSIVE'
    waves.rigid_body.friction = 0.3
    waves.rigid_body.collision_shape = 'MESH'

    for i in range( 10 ) :
        for j in range( 10 ) :
            MakeSphere(i, j)

if __name__ == "__main__":
    main()
