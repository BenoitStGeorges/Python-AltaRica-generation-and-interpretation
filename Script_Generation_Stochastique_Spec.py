# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 16:25:27 2020

"""
#%%

# This scrypt has been created by Benoit Saint-Georges in the context of a 
# student project at Ecole polytechnique in cooperation with Thales Alenia
# Space (TAS).
# 
# This scrypt generates the stochastique simulation specification file for 
# AltaRica 3.0 corresponding to the model generated for the project. The 
# corresponding model is a 60 satellite constellation from the model described 
# in the "Satellite Constellation End-of-Life Dependability assessment with 
# AltaRica 3.0" article published in Les Techniques de l'Ingénieur.


#%%

#number of observers generated in Script_Generation_Block_Model.py
Nobs = 1800  

# beginning of the file corresponding to the grammar
txt = str("<?xml version=")+str("\"1.0\"")+str(" ?>\n<!DOCTYPE ar3ccp>\n<ar3ccp>\n")

# specifications of the observer considered in the simulation
for i in range(Nobs+1):
    txt = txt + str(" <calculation observer=")+str("\"prod")+str(i)+str("\">\n")
    txt = txt + str("  <indicator type=\"has-value\" name=\"")+str(i)+str("\" value=\"true\">\n")
    txt = txt +str("   <mean/>\n")
    txt = txt +str("   <confidence-range/>\n")
    txt = txt + str("  </indicator>\n")
    txt = txt + str(" </calculation>\n")

txt = txt + str("</ar3ccp>\n")

# save the file as a .txt
lines = txt 
new_path = "PATH"
file = open(new_path,'w')
file.write(lines)