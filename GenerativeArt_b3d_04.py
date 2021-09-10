import bpy
from random import *

materialList = [
    bpy.data.materials['White'],
    bpy.data.materials['LightBlue'],
    bpy.data.materials['Blue'],
    bpy.data.materials['LightPink'],
    bpy.data.materials['Pink']
]

count = 6
startPos = [0, 0, 0]

def map(v, min1, max1, min2, max2) :
  return min2 + (v - min1) * (max2 - min2) / (max1 - min1)

def makeBuilding(pos, size, n) :
    height = map(n, count, 0, 0.2, 1.2)
    height += uniform(0.05, 0.1)
    scale = (size * .99, size * .99, height)
    loc = (pos[0] + size/2, pos[1] + size/2, pos[2] + height/2)
    bpy.ops.mesh.primitive_cube_add(location = loc, size = 1.0)
    bpy.ops.transform.resize(value=(scale))

    mat = materialList[0]

    if n < count :
        r = random()
        if r < 0.45 :
            mat = materialList[0]            
        elif r < 0.62 :
            mat = materialList[1]            
        elif r < 0.83 :
            mat = materialList[2]   
        elif r < 0.92 :
            mat = materialList[3]         
        else :
            mat = materialList[4]
    
    bpy.context.object.data.materials.append(mat)
                      
def divideSpace(pos, size, n) :
    makeBuilding(pos, size, n)
    
    n -= 1
    
    if n >= 0 :
        p = map(n, 0.0, count - 1, 0.5, 0.0)
        
        ns = size / 2.0
        nz = 0.0
        p0 = pos[0]
        p1 = pos[1]
        
        if(random() > p) :
            np = (p0, p1, nz)
            divideSpace(np, ns, n)

        if(random() > p) :
            np = (p0 + ns, p1, nz)
            divideSpace(np, ns, n)

        if(random() > p) :
            np = (p0 + ns, p1 + ns, nz)
            divideSpace(np, ns, n)

        if(random() > p) :
            np = (p0, p1 + ns, nz)
            divideSpace(np, ns, n)
            

def main() :
    divideSpace(startPos, 10, count)
        
if __name__ == '__main__':
    main()
