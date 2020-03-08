import sys
import json
import pathlib

try:
    import bpy
except ImportError:
    print("\nRobocraft Assembler needs to be ran inside blender, "
          "try invoking with blender --python " + sys.argv[0] + "\n")

sys.path.append(str(pathlib.Path().absolute()))
from lib.parser import Parser
from lib.roboDictionaries import cubeColours


class Blender():

    def __init__(self):
        pass

    def unselectEverything(self):
        selected = bpy.context.selected_objects
        if len(selected) > 0:
            for obj in selected:
                obj.select = False

    def displayPercentageCompleted(self, currentCube, cubeCount):
        if (currentCube / 100 - int(currentCube / 100) == 0) and (currentCube > 0):
            percentage_completed = int((currentCube / cubeCount) * 100)
            print(percentage_completed, "% complete")

    def deleteCubes(self, cubesInUse):
        print("Removing " + str(len(cubesInUse)) + " datums now...")
        for obj in cubesInUse:
            bpy.data.objects[obj].select = True
            bpy.ops.object.delete()

    def build(self, cubeData, cubeDatabase):
        unknownCube = list()
        cubesInUse = list()
        coloursinuse = list()

        for x in range(0, cubeData["cubeCount"]):
            self.parser = Parser()
            self.displayPercentageCompleted(x, cubeData["cubeCount"])
            cube = self.parser.getCubeData(cubeData["cubeHex"], cubeData["colourHex"], x)

            if cube["ID"] not in cubeDatabase:
                if cube["ID"] not in unknownCube:
                    print("Replacing cube", cube["ID"], "with Spotter-Mace-0000")
                    unknownCube.append(cube["ID"])
                cube["name"] = "#" + cube["ID"]
                cube["ID"] = "Spotter-Mace-0000"
            else:
                cube["name"] = cube["ID"]
            if not cube["ID"] in cubeDatabase:
                print("\nError: cannot find ID#", cube["ID"], "in cubes.csv\n")

            cubeimportdetails = json.loads(cubeDatabase[cube["ID"]])
            objectList = json.loads(cubeimportdetails["object"]) 
            section = "\\Object\\"
            cubeimportdetails["blendfile"] = "assets/blends/" + cubeimportdetails["blendfile"]
            filepath = cubeimportdetails["blendfile"] + section + cubeimportdetails["object"]
            directory = cubeimportdetails["blendfile"] + section
            

            for filename in objectList: 
                colourOveride=cube["Colour"]
                if "ColourOveride" in filename: 
                        filename, rubbish, colourOveride = filename.split("=") 
                        colourOveride = int(colourOveride)
                datum = cube["name"] + "." + filename 
                
                if datum not in cubesInUse:  
                    print("Importing", datum, "now...")
                    bpy.ops.wm.append(
                        filepath = filepath, 
                        filename = filename, 
                        directory = directory
                    )
                    bpy.data.objects[filename].name = datum  
                    cubesInUse.append(datum) 

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


                    textureandcolour=str(datum)+"."+str(colourOveride) 
                    if textureandcolour not in coloursinuse:
                            newMaterial = bpy.data.objects[datum].active_material.copy()
                            if (str(colourOveride)) in cubeColours:
                                red = cubeColours[str(colourOveride)][0] 
                                blue = cubeColours[str(colourOveride)][1] 
                                green = cubeColours[str(colourOveride)][2] 
                                newMaterial.diffuse_color=(red, blue, green)
                            newMaterial.specular_color = newMaterial.diffuse_color              
                            newMaterial.name = textureandcolour                         
                            coloursinuse.append(textureandcolour)
                    newcube.active_material = bpy.data.materials[textureandcolour]
                else:
                   
                    print("error, object ", cube["ID"], "didn't import properly")

        self.deleteCubes(cubesInUse)

