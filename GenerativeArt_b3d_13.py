import bpy
import math
import random

point = 360
two_pi = math.pi * 2.0
min = 2
max = 9
materials = [
    bpy.data.materials['m1'],
    bpy.data.materials['m2'],
    bpy.data.materials['m3']
]

def SelectObject(name) :
    for item in bpy.data.objects :
        if name == item.name :
            item.select_set(True)
        else :
            item.select_set(False)

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

def Move(pos):
    bpy.ops.transform.translate(
        value = (-1, 0, 0)
    )
  
def MakeCoords() :
    
    vx = math.floor(random.uniform(min, max))
    vy = math.floor(random.uniform(min, max))
    vz = vx * vy
    coords = []
    for i in range( point ) :
        ratio = float(i+1) / 360.0
        coords.append((
            math.sin( vx * ratio * two_pi ),
            math.cos( vy * ratio * two_pi ),
            math.sin( vz * ratio * two_pi )
        ))
    return coords

def AddCurve(n, m) :
    curve = bpy.data.curves.new(name = 'curve', type = 'CURVE')
    curve.dimensions = '3D'
    curve.resolution_u = 1
    
    spline = curve.splines.new('NURBS')
    coords = MakeCoords()
    spline.points.add( len( coords ) )
    
    for i, coord in enumerate( coords ) :
        x, y, z = coord
        spline.points[i].co = (x, y, z, 1)
        
    curveObj = bpy.data.objects.new('Curve', curve)
    
    scene = bpy.context.scene
    scene.collection.objects.link(curveObj)
    bpy.context.view_layer.objects.active = curveObj
    
    SelectObject(curveObj.name)
    
    bpy.ops.transform.translate(
        value = (n*2, 0, m*2)
    )
    
    obj = bpy.context.object
    obj.data.bevel_resolution = 6
    obj.data.bevel_depth = 0.05
    r = random.random()
    if r < 1/2 :
        bpy.context.object.data.materials.append(materials[0])
    elif r < 3/4 :
        bpy.context.object.data.materials.append(materials[1])
    else :
        bpy.context.object.data.materials.append(materials[2])
    
def main() :
    DeleteObjects('Curve')
    
    for i in range( 12 ) :
        for j in range( 6 ) :
            AddCurve(i, j)

if __name__ == "__main__":
    main()
