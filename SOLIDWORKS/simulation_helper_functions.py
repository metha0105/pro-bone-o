## HELPER FUNCTIONS FOR SIMULATION AUTOMATION SCRIPT
import os

# create baseline model - cylinder
def create_baseline_model(sw_app, bone_radius, muscle_radius, fat_radius, skin_radius, length):
    # create new part from sw_app
    sw_model = sw_app.NewDocument(" ", 0, 0, 0)
    sw_app.ActivateDoc2(sw_model.GetTitle(), False, 0)

    sw_model.Extension.SelectByID2("Top Plane", "PLANE", 0, 0, 0, False, 0, None, 0)
    sw_model.SketchManager.InsertSketch(True)

    # create concentric circles for bone, muscle, fat, and skin respectively
    sw_model.SketchManager.CreateCircleByRadius(0, 0, 0, bone_radius, 0, 0)
    sw_model.SketchManager.CreateCircleByRadius(0, 0, 0, muscle_radius, 0, 0)
    sw_model.SketchManager.CreateCircleByRadius(0, 0, 0, fat_radius, 0, 0)
    sw_model.SketchManager.CreateCircleByRadius(0, 0, 0, skin_radius, 0, 0)

    # exit sketch
    sw_model.SketchManager.InsertSketch(False)

    # extrude bone separately and name it for fracture helper functions
    sw_model.FeatureManager.FeatureExtrusion(True, False, False, 0, 0, length, 0, False, False, False, False, 0, 0, False)
    bone_feature = sw_model.SelectionManager.GetSelectedObject6(1, -1)

    if not bone_feature:
        bone_feature.Name = "BoneExtrusion"

    # extrude surrounding layers of muscle, fat, and skin
    sw_model.FeatureManager.FeatureExtrusion(True, False, False, 0, 0, length, 0, False, False, False, False, 0, 0, False)

    # print message
    print("Created baseline model with bone, muscle, fat, and skin layers")
    return sw_model, bone_feature

# save and close document 
def save_and_close_document(sw_model, sw_app, part_name):
    part_path = os.path.join(os.getcwd(), "models", "cylinder", f"{part_name}.STEP")
    sw_model.SaveAs(part_path)
    print(f"Saved {part_name} model to {part_path}")
    sw_app.QuitDoc(sw_model.GetTitle())

# create transverse fracture
def create_transverse_fracture(sw_model, bone_feature, sw_app):
    # parameter to change = length
    length = [1, 6, 12, 18]

    if not bone_feature:
        print("Bone feature not found. Cannot create transverse fracture :(")
        return

    sw_model.Extension.SelectByID2(bone_feature.Name, "BODYFEATURE", 0, 0, 0, False, 0, None, 0)
    sw_model.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, None, 0)
    sw_model.SketchManager.InsertSketch(True)

    for i in range(len(length)):
        # create actual fracture
        sw_model.SketchManager.CreateRectangle(-15, -length[i]/2, 0, 15, length[i]/2, 0)
        sw_model.FeatureManager.FeatureCut(True, False, False, 0, 0, 5, 0, False, False, False, False, 
                                   0, 0, False, False, False, False, False, True, True, True, True, 
                                   False, 0, 0, False)
        
        # save part
        save_and_close_document(sw_model, sw_app, f"Transverse_{length[i]}")

# create oblique fracture
def create_oblique_fracture(sw_model, bone_feature, sw_app):
    # parameters to change = angle and length
    angle = [30, 40, 50, 60]
    length = [1, 6, 12, 18]

    # check bone feature exists correctly
    if not bone_feature:
        print("Bone feature not found. Cannot create oblique fracture :(")
        return

    for i in range(len(angle)):
        for j in range(len(length)):
            # select bone extrusion specifically
            sw_model.Extension.SelectByID2(bone_feature.Name, "BODYFEATURE", 0, 0, 0, False, 0, None, 0)

            # create reference plane to create fracture at specified angle
            sw_model.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, None, 0)
            plane = sw_model.FeatureManager.InsertRefPlane(8, angle[i] * 0.0174533, 0, 0, 0, 0)

            if not plane:
                print(f"Failed to create reference plane for oblique fracture at {angle[i]} degrees")
                return

            plane_name = plane.Name

            # create actual fracture
            sw_model.Extension.SelectById2(plane_name, "PLANE", 0, 0, 0, False, 0, None, 0)
            sw_model.SketchManager.InsertSketch(True)

            # create fracture cut
            sw_model.SketchManager.CreateRectangle(-15, -length[j]/2, 0, 15, length[j]/2, 0)
            sw_model.FeatureManager.FeatureCut(True, False, False, 0, 0, 5, 0, 
                                  False, False, False, False, 0, 0, False, False, 
                                  False, False, False, True, True, True, True, False, 
                                  0, 0, False)
            
            # save part
            save_and_close_document(sw_model, sw_app, f"Oblique_{angle[i]}_{length[j]}")

# create comminuted fracture
# def create_comminuted_fracture(sw_model, sw_app):
#     # parameters to change = length and internal length
#     length = [1, 6, 12, 18]
#     internal_length = [0.1, 0.5, 1]

    # NEED TO CONFIRM HOW TO CREATE COMMINUTED FRACTURE

# create greenstick fracture
def create_greenstick_fracture(sw_model, bone_feature, sw_app, bone_thickness):
    # parameters to change = length and depth
    length = [1, 6, 12, 18]
    depth = [0, 0.25 * bone_thickness, 0.5 * bone_thickness, 0.75 * bone_thickness]

    if not bone_feature:
        print("Bone feature not found. Cannot create greenstick fracture :(")
        return

    # create actual greenstick fracture
    for i in range(len(length)):
        for j in range(len(depth)):
            sw_model.Extension.SelectByID2(bone_feature.Name, "BODYFEATURE", 0, 0, 0, False, 0, None, 0)            
            sw_model.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, None, 0)
            sw_model.SketchManager.InsertSketch(True)

            # create partial line
            sw_model.SketchManager.CreateLine(-length[i]/2, 0, 0, length[i], 0, 0)

            # exit sketch and create shallow cut
            sw_model.SketchManager.InsertSketch(False)
            sw_model.FeatureManager.FeatureCut(True, False, False, 0, 0, depth[j], 0, False, False, False, False, 0, 0, False, False, False, False, False, True, True, True, True, False, 0, 0, False)

            # save part
            save_and_close_document(sw_model, sw_app, f"Greenstick_{length[i]}_{depth[j]}")

# create hairline fracture
def create_hairline_fracture(sw_model, bone_feature, sw_app):
    # parameters to change = length
    length = [1, 5, 6, 8, 9]
    thickness = 0.2

    if not bone_feature:
        print("Bone feature not found. Cannot create hairline fracture :(")
        return

    # create actual hairline fracture
    for i in range(len(length)):
        sw_model.Extension.SelectByID2(bone_feature.Name, "BODYFEATURE", 0, 0, 0, False, 0, None, 0)            
        sw_model.Extension.SelectByID2("Front Plane", "PLANE", 0, 0, 0, False, 0, None, 0)
        sw_model.SketchManager.InsertSketch(True)

        # actual hairline fracture
        sw_model.SketchManager.CreateLine(-length[i]/2, 0, 0, length[i]/2, 0, 0)
        sw_model.SketchManager.InsertSketch(False)
        sw_model.FeatureManager.FeatureCut(True, False, False, 0, 0, thickness, 0, 
                                  False, False, False, False, 0, 0, False, False, 
                                  False, False, False, True, True, True, True, False, 
                                  0, 0, False)
    
        # save part
        save_and_close_document(sw_model, sw_app, f"Hairline_{length[i]}")