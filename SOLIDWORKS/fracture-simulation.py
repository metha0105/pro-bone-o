# Author: Vithusha (Metha) Tharmarasa
# Note: Could make script more efficient using parallelization

# imports
import win32com.client as win32
import os
import csv
import simulation_helper_functions as shf

# set up connection to SOLIDWORKS API
def connect_to_solidworks():
    try:
        sw_app = win32.Dispatch("SldWorks.Application")
        sw_app.Visible = True

        print("Connected to SOLIDWORKS API successfully")
        return sw_app
    except Exception as e:
        print(f"Failed to connect to SOLIDWORKS API: {e}")
        return None

# set up connection to CST Studio Suite API 
def connect_to_cst():
    try:
        cst = win32.Dispatch("CSTStudio.Application")
        project = cst.NewMWSProject()

        print("Connected to CST Studio Suite API successfully")
        return cst, project
    except Exception as e:
        print(f"Failed to connect to CST Studio Suite API: {e}")
        return None, None
    
# parameters
bone_thickness = [5, 10, 15, 20, 25]
skin_thickness = [0.75, 1.5, 2]
fat_thickness = [3, 12, 22]
muscle_thickness = [30, 50, 70]

# SOLIDWORKS only function -> will modify to include CST and make it the main function
# uses recursion to create multiple models with different fractures
def create_cylinder_models_with_fractures(sw_app, bone_thickness, skin_thickness, fat_thickness, muscle_thickness, index = 0):
    if index >= len(bone_thickness):
        print("All models created successfully")
        return
    
    (model, bone) = shf.create_baseline_model(sw_app, bone_thickness[index], skin_thickness[index], fat_thickness[index], muscle_thickness[index])

    # create fractures
    shf.create_transverse_fracture(model, bone, sw_app)
    shf.create_oblique_fracture(model, bone, sw_app)
    shf.create_greenstick_fracture(model, bone, sw_app, bone_thickness[index])
    shf.create_hairline_fracture(model, bone, sw_app)

    create_cylinder_models_with_fractures(sw_app, bone_thickness, skin_thickness, fat_thickness, muscle_thickness, index + 1)