import bpy
import random
import math

unit = 5
amount = 24
prefix = "cp"
scene = bpy.context.scene
base = bpy.context.object
co = bpy.context.collection
objs = [scene.objects['Capsule_01'],scene.objects['Capsule_02'],scene.objects['Capsule_03'],scene.objects['Capsule_04']]

def delete_copy() :
    for obj in bpy.context.scene.objects :
        if obj.name.startswith(prefix) :
            obj.select_set(state = True)
        else :
            obj.select_set(state = False)
    bpy.ops.object.delete()

def copy_obj(cnt) :
    index = 0
    for x in range(cnt) :
        for z in range(cnt) :
            target = objs[0]
            r = random.random()
            if r < .2 :
                continue
            elif r < 0.4 :
                target = objs[0]
            elif r < 0.6 :
                target = objs[1]
            elif r < 0.8 :
                target = objs[2]
            else :
                target = objs[3]
            obj = target.copy()
            obj.name = prefix + str(index).zfill(4)
            co.objects.link(obj)
            obj.location = [x * unit, 0, z * unit]
            
            s = random.uniform(0.998, 1.002)
            ss = (s, s, 1)
            obj.scale = ss
            rot = (0, 0, 0)
            if r < 0.25 :
                rot = (0, math.radians(90.0), 0)                
            elif r < 0.5 :
                rot = (0, math.radians(180.0), 0)
            obj.rotation_euler = rot

def main() :
    delete_copy()
    copy_obj(amount)
        
if __name__ == '__main__':
    main()
