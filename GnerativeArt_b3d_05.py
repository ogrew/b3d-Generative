import bpy
import math
import random

COUNT = 25
R1 = 10.0
R2 = 2.0
HEIGHT = 0.0

materialList = [
    bpy.data.materials['m1'],
    bpy.data.materials['m2'],
    bpy.data.materials['m3'],
    bpy.data.materials['m4'],
    bpy.data.materials['m5']
]

def map(v, min1, max1, min2, max2) :
  return min2 + (v - min1) * (max2 - min2) / (max1 - min1)

def copySphere(offset, depth, sign, loop) :
    for i in range(COUNT):

        r1 = R1 * map(i, 0, COUNT, 1, 0.5)
        r2 = R2 * map(i, 0, COUNT, 1, 0.5)

        rad = sign * loop * (2 * math.pi * (i /COUNT + offset))

        x = r1 * math.cos(rad)
        y = r1 * math.sin(rad)
        
        z = depth * i
 
        bpy.ops.mesh.primitive_ico_sphere_add(
            location=(x, y, z),
            radius= r2,
            subdivisions = 4
        )
        
        r = random.random()
        if r < 0.65 :
            mat = materialList[4]    
        elif r < 0.76 :
            mat = materialList[3]            
        elif r < 0.87 :
            mat = materialList[2]            
        elif r < 0.93 :
            mat = materialList[1]   
        else :
            mat = materialList[0]
            
        bpy.context.object.data.materials.append(mat)     
        
        global HEIGHT
        HEIGHT  = z

def setCenterSphere() :
    bpy.ops.mesh.primitive_ico_sphere_add(
        location=(0, 0, HEIGHT),
        radius= R1/1.5,
        subdivisions = 6
    )    
    bpy.context.object.data.materials.append(materialList[3])  

def setParticleObjs(num) :
    for i in range(num) :
        x = random.uniform(-10.0, 30.0)
        y = random.uniform(-20.0, 20.0)
        z = random.uniform( 0.0, 35.0)

        rx = random.uniform(-90.0, 90.0)
        ry = random.uniform(-90.0, 90.0)
        rz = random.uniform(-90.0, 90.0)

        ss = random.uniform(0.1, 0.4)
        bpy.ops.mesh.primitive_cube_add(
            location=(x, y, z),
            rotation=(rx, ry, rz),
            size= ss
        )
        
        r = random.random()
        if r < 0.5 :
            mat = materialList[4]    
        elif r < 0.8 :
            mat = materialList[0]                        
        else :
            mat = materialList[2]
        bpy.context.object.data.materials.append(mat)  

def main() :
    d = 1
    ll = 1
    copySphere(0.0,  d, 1, ll)
    copySphere(0.25, d, 1, ll)
    copySphere(0.5,  d, 1, ll)
    copySphere(0.75, d, 1, ll)
    setCenterSphere()
    setParticleObjs(150)
    
if __name__ == '__main__':
    main()
