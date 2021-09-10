import bpy
import bmesh
from random import *

bpy.ops.mesh.primitive_plane_add()
orange = (246/255, 189/255, 96/255, 1.0)
white = (247/255, 237/255, 226/255, 1.0)
pink = (245/255, 202/255, 195/255, 1.0)
blue = (132/255, 165/255, 157/255, 1.0)
red = (242/255, 132/255, 130/255, 1.0)

context = bpy.context
obj = context.object
if obj == None:
    print("not found Plane")
me = obj.data

bm = bmesh.new()
bm.from_mesh(me)
bmesh.ops.subdivide_edges(
    bm,
    edges = bm.edges,
    cuts = 65,
    use_grid_fill = True,
)
bm.to_mesh(me)
me.update()

tex = bpy.data.textures.new("OriginalNoiseTex", 'STUCCI')

bpy.ops.object.modifier_add(type='DISPLACE')
disp = bpy.context.object.modifiers["Displace"]
disp.texture = tex

bpy.ops.object.mode_set(mode='EDIT')

bm = bmesh.from_edit_mesh(me)

for m in bpy.data.materials:
    bpy.data.materials.remove(m)

index = 1
for f in bm.faces:
    bpy.ops.mesh.select_all(action='DESELECT')
    f.select=True
    name="Material.%03d" % index
    m = bpy.data.materials.new(name)
    r = random()
    if r < 0.12 :
        m.diffuse_color = orange
    elif r < 0.33 :
        m.diffuse_color = pink
    elif r < 0.56 :
        m.diffuse_color = blue
    elif r < 0.73 :
        m.diffuse_color = red
    else :
        m.diffuse_color = white
    
    bpy.context.object.data.materials.append(m)
    
    f.material_index = index
    index = index + 1
