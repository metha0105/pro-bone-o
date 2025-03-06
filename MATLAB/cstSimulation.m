% Pro-Bone-O - CST Simulations
% Author: Vithusha (Metha) Tharmarasa
% Link to Repo used as foundation: https://github.com/simos421/CST-MATLAB-API/blob/master/Examples/TwoDipolesExample.m
% NOTE: NEED TO CONFIRM PARAMETERS AND MATERIALS USED WITH TEAM

% connect to CST API - may need to modify based on actual computer
addpath("...\cst api")

cst = actxserver('CSTStudio.application');
project = cst.invoke('NewMWS');

% set units
project.invoke('StoreDoubleParameter', 'Frequency', 2.45); % GHz
project.invoke('StoreDoubleParameter', 'Length', 1); % mm
project.invoke('StoreDoubleParameter', 'Time', 1e-9);

% background material
minfrequency = 2.4;
x = "expanded open";
CstDefineOpenBoundary(mws, minfrequency, x, x, x, x, x, x);
XminSpace = 0; 
XmaxSpace = 0; 
YminSpace = 0; 
YmaxSpace = 0; 
ZminSpace = 0;
ZmaxSpace = 0;
CstDefineBackroundMaterial(mws,XminSpace,XmaxSpace, YminSpace, YmaxSpace, ZminSpace, ZmaxSpace)

% define materials for dipoles
material = "tbd"; 

% dipole #1 
Name = "Dipole 1";
OuterRadius = 0; 
InnerRadius = 0;
Xcenter = 0; 
Ycenter = 0;
Zrange = [0, 0]; 
Cstcylinder(mws, Name, ComponentList, material, 'Z', OuterRadius, InnerRadius, Xcenter, Ycenter, Zrange)

% dipole #2
Name = "Dipole 2";
OuterRadius = 0;
InnerRadius = 0;
Xcenter = 0;
Ycenter = 0;
Zrange = [0, 0];
Cstcylinder(mws, Name, ComponentList, material, 'Z', OuterRadius, InnerRadius, Xcenter, Ycenter, Zrange)

% define gaps btwn dipoles

% bone thicknesses we want to test with
bone_thickness = [5, 10, 15, 20, 25];

for i = 1:length(bone_thickness)
    % bone parameters
    Name = "bone";
    ComponentList = "human_bones";
    Material = "Bone"; % need to have this defined beforehand within CST
    OuterRadius = bone_thickness(i);
    InnerRadius = 0; 
    Xcenter = 0; 
    Ycenter = 0;
    Zrange = [0, 200];

    Cstcylinder(mws, Name, ComponentList, Material, 'Z', OuterRadius, InnerRadius, Xcenter, Ycenter, Zrange);
end