# Capstone '25: Pro-Bone-O
Members: Vithusha (Metha) Tharmarasa, MinYoung Park, Victoria Purcell, Adora Dong

## What is Pro-Bone-O
Our project aims to resolve some of the issues currently faced within the healthcare industry - specifically for diagnosing bone fractures. The end-result is a device that utilizes microwaves and ML to gauge whether the patient has a fracture and if so, what type of fracture.

## Software (Automation + App)
The software component of our project consists of 2 things - automated scripts and an app. 

### Automation
As we need large amounts of data to train the DNN to diagnose fractures, we need to perform virtual and real-life simulations. The simulation process can essentially be boiled down to the following steps: 
1. Create a 3D model 
2. Apply a fracture to the model 
3. Create dipoles within CST Studio 
4. Get S-parameter values 

To expedite the process, we created scripts. We did run simulations just purely within CST with simple models. To expose our DNN to more diverse and perhaps "realistic" data, we made specifically 2 scripts: 
* SOLIDWORKS + CST Studio Suite (coded in Python)
* CST Studio Suite (coded in MATLAB)

### App
To help patients and health practioners better understand the results, we developed an app that explains what the results mean. This is also to help encourage trust between our DNN and users.