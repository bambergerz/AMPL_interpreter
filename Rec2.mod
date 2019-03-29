set VERTICIES;
set EDGES within (VERTICIES cross VERTICIES);
param SOURCE in VERTICIES
param SINK in VERTICIES
param capacity {EDGES} >= 0;