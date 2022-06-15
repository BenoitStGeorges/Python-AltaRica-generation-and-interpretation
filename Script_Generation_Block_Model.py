# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 16:25:27 2020

"""
#%%

# This scrypt has been created by Benoit Saint-Georges in the context of a 
# student project at Ecole polytechnique in cooperation with Thales Alenia
# Space (TAS).
# 
# This scrypt generates a "block" object in the AltaRica 3.0 language modeling 
# a 60 satellite constellation from the model described in the "Satellite 
# Constellation End-of-Life Dependability assessment with AltaRica 3.0" 
# article published in Les Techniques de l'Ingénieur.


#%%

#Defintion of the macro parameters 
Nsat = 60               #satellites number in the constellation
Ner_sat=30              #radiative elements per satellite


#first lines to create a block in AltaRica grammar
txt = str("block Constellation\n    Integer tot_prod (reset=0);\n\n")

#initialisation of the loop variables
cpt = 1
cpt2 = 1
cpt3 = 1
cpt4 = 1
cpt5 = 1
cpt6 = 1
cpt7 = 1 

#main loop creating the 60 satellites
for i in range(Nsat):
    txt = txt +str("    block Monosatellite") +str(i+1) +str(" \n        ER ")

    # loops creating the variables for the 3 different components, ER, EPC, S2
    for j in range(1,Ner_sat+1+10):
        txt = txt + str("er"+str(cpt)+",")
        cpt+=1
    txt = txt[:-1]+"; \n        EPC "
    for j in range(1,11):
        txt = txt + str("epc"+str(cpt2)+",")
        cpt2+=1
    txt = txt[:-1]+"; \n        S2 "
    for j in range(1,3):
        txt = txt + str("s2"+str(cpt3)+",")
        cpt3+=1
    txt = txt[:-1]+";"
    txt = txt + str("\n \n")
    
    # creation of the final satellite variables
    txt = txt + str("        Integer tot_prod")+str(i+1)+str(" (reset=0);\n\n")
    txt = txt + str("        assertion\n\n")
    
    # creation of the flow lows (power alimentation) for the satellite
    for j in range(1,11):
        for k in range(1,5):
            txt = txt + str("            er")+str(cpt4)+str(".alim := epc")+str(cpt5)+str(".working;\n")
            cpt4+=1
        txt = txt + str("\n")
        cpt5+=1
        
    # creation of the flow low (common parts) for the satellite
    txt = txt + str("            tot_prod")+str(i+1)+str(" := if ") 
    txt = txt + str("s2"+str(cpt6)+".working==false and ")
    cpt6+=1
    txt = txt + str("s2"+str(cpt6)+".working==false then 0 else ")
    cpt6+=1
    
    # creation of the capacity variable for the satellite
    for k in range(1,11):
        txt = txt + str("min(")
        for j in range(1,5):
            txt = txt + str("er"+str(cpt7)+".prod+")
            cpt7+=1
        txt = txt[:-1] + str(",3)+")
    txt = txt[:-1]+"; \n\n    end \n\n"
    
# creation of the final constellation variables
txt = txt+str("    assertion\n")
txt = txt+str("        tot_prod := ")
for i in range(Nsat):
    txt = txt + str("Monosatellite")+str(i+1)+str(".tot_prod")+str(i+1)+str("+")
txt = txt[:-1]+str(";\n")
   
txt= txt + str("\n \n")


# creation of the final constellation observers (used to print the varibales 
# values)
for i in range(Nsat*Ner_sat+1):
    txtp = txt + str("    observer Boolean prod"+str(i)+" = if tot_prod=="+str(i)+" then true else false;\n")
    txt = txtp

lines = txt +str("\nend")


# save the file as a .txt
new_path = "PATH"
file = open(new_path,'w')
file.write(lines)