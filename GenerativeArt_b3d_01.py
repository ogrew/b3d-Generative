import bpy
import random

materials = [
    bpy.data.materials["m1"],
    bpy.data.materials["m2"],
    bpy.data.materials["m3"],
    bpy.data.materials["c"]
]
spacing = 2.2

for x in range(40) :
    for y in range(40) :
        
        pos = (x * spacing, y * spacing, random.random() * 2)
        g = random.random()
        if g < .05 :
            bpy.ops.mesh.primitive_cylinder_add(location=pos, radius=1, depth=6)
        else :        
            bpy.ops.mesh.primitive_cube_add(location=pos, size=2)
        
        item = bpy.context.object
        if g < 0.1 :
              item.data.materials.append(materials[3])      
        else :
            r = random.random()
                    
            if r < .15 :
                item.data.materials.append(materials[0])
            elif r < .95 :
                item.data.materials.append(materials[1])
            else :
                item.data.materials.append(materials[2])
