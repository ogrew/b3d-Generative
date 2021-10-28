import bpy, math, random, bmesh, requests, json
import numpy as np

# ref : https://sabopy.com/py/matplotlib-3d-49/

num = 400
R1 = 5
R2 = 20
S1 = 1.0 # sphere-radius
S2 = 2.0 # torus-radius

def GetColors() :
    res = requests.post( 'http://colormind.io/api/', data = '{"model":"default"}' )
    json_load = res.json()
    colors = json_load['result']
    return colors

def DeleteMaterials() :
    for m in bpy.data.materials:
        bpy.data.materials.remove( m )
    
def DeleteMeshes() :    
    for m in bpy.data.meshes:
        bpy.data.meshes.remove( m )
        
def DeleteObjects() :
    for item in bpy.data.objects :
        if "Camera" in item.name :
            item.select_set(False)
        else :
            item.select_set(True)
    bpy.ops.object.delete()

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

def map(v, min1, max1, min2, max2) :
  return min2 + (v - min1) * (max2 - min2) / (max1 - min1)

def ApplySkinModifier(me) :
    skin = me.modifiers.new(type='SKIN', name = "Skin")

def ApplySubSurfModifier(me) :
    sub = me.modifiers.new(type='SUBSURF', name = "Subdivision")
    sub.levels = 4
    sub.render_levels = 5
    sub.quality = 4

def AddSphere(vec, size, mat) :
   
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions = 4,
        radius = size,
        location = (vec[0], vec[1], vec[2])
    )
    bpy.ops.object.shade_smooth()
    bpy.context.object.data.materials.append( mat )    

def main() :
    DeleteObjects()
    DeleteMeshes()
    DeleteMaterials()
    colors = GetColors()
    materials = MakeMaterials( colors )

    u = np.linspace(0, 2*np.pi, num)   
    p = math.floor( random.uniform(6, 14) )
    q = math.floor( random.uniform(2, 7) )
    print("p, q = " + str(p) + "," + str(q))
    
    for i in range( 1 ) :
        r1 = R1 / (i + 1)
        r2 = R2 / (i + 1)
        
        offset = math.pi if i % 2 == 0 else 0
        nx = (r2 + r1*np.cos(p*u + offset)) * np.cos(q*u)
        ny = (r2 + r1*np.cos(p*u + offset)) * np.sin(q*u)
        nz = r1 * np.sin(p*u)
            
        li = list(zip(nx, ny, nz))
        ll = len( li )
                
        for i, pos in enumerate( li ) :
            c = map(i, 0, ll, 0, 8 * math.pi)
            size = S2 * abs( math.cos(c) ) + 0.1
            loc = [ pos[0], pos[1], pos[2] ]
            m = materials[i % 5]
            AddSphere(loc, size, m)
           
if __name__ == "__main__":
    main()
