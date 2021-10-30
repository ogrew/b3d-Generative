import bpy, random, math, requests, json

COUNT = 4
LENGTH = 8
PI = math.pi

materials = [
    bpy.data.materials['m0'],
    bpy.data.materials['m1'],
    bpy.data.materials['m2'],
    bpy.data.materials['m3'],
    bpy.data.materials['m4'],
]

def GetColors() :
    res = requests.post( 'http://colormind.io/api/', data = '{"model":"default"}' )
    json_load = res.json()
    colors = json_load['result']
    return colors

def ChangeMaterialColor( colors ) :
    for i, mat in enumerate( materials ) :
        color = colors[i]
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs[0].default_value = (color[0] /255, color[1]/255, color[2]/255, 1.0)
        bsdf.inputs[4].default_value = 0.7
        bsdf.inputs[7].default_value = 0.4

def DeleteObjects(name) :
    for item in bpy.data.objects :
        if name in item.name :
            item.select_set( True )
        else :
            item.select_set( False )
    bpy.ops.object.delete()

def main() :
    colors = GetColors()
    ChangeMaterialColor( colors )
    
    DeleteObjects('Cube')
    size = LENGTH / COUNT
    base01 =  bpy.data.objects['Base01']
    base02 =  bpy.data.objects['Base02']
    base03 =  bpy.data.objects['Base03']
    base04 =  bpy.data.objects['Base04']
    base05 =  bpy.data.objects['Base05']
    base06 =  bpy.data.objects['Base06']
    base07 =  bpy.data.objects['Base07']
    base08 =  bpy.data.objects['Base08']
    co = bpy.context.collection
    scene = bpy.context.scene
    
    if base01 is None:
        print("not found <Base01> ...")
        return
    if base02 is None:
        print("not found <Base02> ...")
        return
    if base03 is None:
        print("not found <Base03> ...")
        return
    if base04 is None:
        print("not found <Base04> ...")
        return
    if base05 is None:
        print("not found <Base05> ...")
        return
    if base06 is None:
        print("not found <Base06> ...")
        return
    if base07 is None:
        print("not found <Base07> ...")
        return
    if base08 is None:
        print("not found <Base08> ...")
        return

    for i in range( COUNT ) :
        for j in range( COUNT ) :
            for k in range( COUNT ) :
                colorType = random.random()

                data = base01.data
                if colorType < 0.21 :
                    data = base02.data
                elif colorType < 0.42 :
                    data = base03.data
                elif colorType < 0.63 :
                    data = base04.data
                elif colorType < 0.84 :
                    data = base05.data
                elif colorType < 0.88 :
                    data = base06.data
                elif colorType < 0.92 :
                    data = base07.data
                elif colorType < 0.96 :
                    data = base08.data
                
                cube = bpy.data.objects.new( "Cube", data )
                co.objects.link( cube )
                cube.location = [i * size, j * size , k * size]

                    
if __name__ == '__main__':
    main()
