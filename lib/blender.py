import sys
import json
import pathlib

try:
    import bpy
except ImportError:
    print("\nRobocraft Assembler needs to be ran inside blender, "
          "try invoking with blender --python " + sys.argv[0] + "\n")

sys.path.append(str(pathlib.Path().absolute()))
from lib.roboDictionaries import cubeColours
from lib.parser import Parser




class Blender():

    def __init__(self):
        pass

    def unselectEverything(self):
        selected = bpy.context.selected_objects
        if len(selected) > 0:
            for obj in selected:
                obj.select = False

    def displayPercentageCompleted(self, x, cubeCount):
        if (x / 100 - int(x / 100) == 0) and (x > 0):
            percentage_completed = int((x / cubeCount) * 100)
            print(percentage_completed, "% complete")

    def deleteCubes(self, cubesinuse):
        print("Removing " + str(len(cubesinuse)) + " datums now...")
        for obj in cubesinuse:
            bpy.data.objects[obj].select = True
            bpy.ops.object.delete()

    def build(self, cubeData, cubedatabase):
        unknowncube = list()
        cubesinuse = list()
        coloursinuse = list()

        for x in range(0, cubeData["cubeCount"]):
            self.parser = Parser()
            self.displayPercentageCompleted(x, cubeData["cubeCount"])
            cube = self.parser.getCubeData(cubeData["cubeHex"], cubeData["colourHex"], x)

            if cube["ID"] not in cubedatabase:
                if cube["ID"] not in unknowncube:
                    print("Replacing cube", cube["ID"], "with Spotter-Mace-0000")
                    unknowncube.append(cube["ID"])
                cube["name"] = "#" + cube["ID"]
                cube["ID"] = "Spotter-Mace-0000"
            else:
                cube["name"] = cube["ID"]
            if not cube["ID"] in cubedatabase:
                print("\nError: cannot find ID#", cube["ID"], "in cubes.csv\n")

            cubeimportdetails = json.loads(cubedatabase[cube["ID"]])
            objectlist = json.loads(cubeimportdetails["object"]) 
            section = "\\Object\\"
            cubeimportdetails["blendfile"] = "assets/blends/" + cubeimportdetails["blendfile"]
            filepath = cubeimportdetails["blendfile"] + section + cubeimportdetails["object"]
            directory = cubeimportdetails["blendfile"] + section
            

            for filename in objectlist: 
                colourOverride=cube["Colour"]
                if "ColourOverride" in filename: 
                        filename, rubbish, colourOverride = filename.split("=") 
                        colourOverride = int(colourOverride)
                datum = cube["name"] + "." + filename 
                
                if datum not in cubesinuse:  
                    print("Importing", datum, "now...")
                    bpy.ops.wm.append(
                        filepath = filepath, 
                        filename = filename, 
                        directory = directory
                    )
                    bpy.data.objects[filename].name = datum  
                    cubesinuse.append(datum) 

                self.unselectEverything() 

                bpy.data.objects.get(datum).select = True
                bpy.ops.object.duplicate(linked = True) 

                selected = bpy.context.selected_objects 
                if len(selected) > 0:
                    newcube = selected.pop()
                    newcube.location = (cube["X"], cube["Y"], cube["Z"])
                    newcube.material_slots[0].link = 'OBJECT' 

                    if cube["O"] == 0:
                        bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    
                    if cube["O"] == 1:
                        bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                        bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    
                    if cube["O"] == 2:
                        bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                        bpy.ops.transform.rotate(value=3.14159, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    
                    if cube["O"] == 3:
                        bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                        bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    
                    if cube["O"] == 4:
                        bpy.ops.transform.rotate(value=3.14159, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    
                    if cube["O"] == 5:
                        bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                        bpy.ops.transform.rotate(value=3.14159, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    
                    if cube["O"] == 6:
                        bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    
                    if cube["O"] == 7:
                        bpy.ops.transform.rotate(value=3.14159, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                        bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    
                    if cube["O"] == 8:
                        bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    
                    if cube["O"] == 9:
                        bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    
                    if cube["O"] == 10:
                        bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    
                    if cube["O"] == 11:
                        bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                        bpy.ops.transform.rotate(value=3.14159, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    
                    if cube["O"] == 12:
                        bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                        bpy.ops.transform.rotate(value=-3.14159, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)        
                    
                    if cube["O"] == 13:
                        bpy.ops.transform.rotate(value=3.14159, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    
                    if cube["O"] == 14:
                        bpy.ops.transform.rotate(value=1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    
                    if cube["O"] == 15:
                        bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                        bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    
                    if cube["O"] == 16:
                        bpy.ops.transform.rotate(value=1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                        bpy.ops.transform.rotate(value=3.14159, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    
                    if cube["O"] == 17:
                        bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                        bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    
                    if cube["O"] == 18:
                        pass     
                    
                    if cube["O"] == 19:
                        bpy.ops.transform.rotate(value=3.14159, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    
                    if cube["O"] == 20:
                        bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                        bpy.ops.transform.rotate(value=-1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    
                    if cube["O"] == 21:
                        bpy.ops.transform.rotate(value=1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                        bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    
                    if cube["O"] == 22:
                        bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                        bpy.ops.transform.rotate(value=1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                    
                    if cube["O"] == 23:
                        bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                        bpy.ops.transform.rotate(value=1.5708, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)


                    textureandcolour = str(datum) + "." + str(colourOverride) 
                    if textureandcolour not in coloursinuse: 
                        redValue = cubeColours[str(colourOverride)][0]
                        greenValue = cubeColours[str(colourOverride)][1]
                        blueValue = cubeColours[str(colourOverride)][2]

                        newMaterial = bpy.data.objects[datum].active_material.copy()
                        newMaterial.diffuse_color = (redValue, greenValue,
                                                         blueValue)    
                        newMaterial.specular_color = newMaterial.diffuse_color              
                        newMaterial.name = textureandcolour                         
                        coloursinuse.append(textureandcolour)
                    newcube.active_material = bpy.data.materials[textureandcolour]
                else:
                   
                    print("error, object ", cube["ID"], "didn't import properly")

        self.deleteCubes(cubesinuse)

