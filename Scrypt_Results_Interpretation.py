# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 16:25:27 2020

"""
#%%

# This scrypt has been created by Benoit Saint-Georges in the context of a 
# student project at Ecole polytechnique in cooperation with Thales Alenia
# Space (TAS).
# 
# This scrypt reads the results from the stochastic simulation. It enables to 
# interpret the row results into formalised statistics. The studied model is a
# a 60 satellite constellation from the model described in the "Satellite 
# Constellation End-of-Life Dependability assessment with AltaRica 3.0" 
# article published in Les Techniques de l'Ingénieur.


#%% libraries

import matplotlib.pyplot as plt
import numpy as np

#%%

def variables(lines): # get the variables defined in the .csv ie the 
                      # observers 
    tab = []
    ind = 7
    n = 0
    while lines[ind+1][0]=='0' or lines[ind+1][0]=='1' or lines[ind+1][0]=='2' or lines[ind+1][0]=='3'or lines[ind+1][0]=='4'or lines[ind+1][0]=='5'or lines[ind+1][0]=='6'or lines[ind+1][0]=='7'or lines[ind+1][0]=='8'or lines[ind+1][0]=='9':
        line = lines[ind+1][:-2]
        temp = line.split("\t")
        tab.append(temp)
        n+=1
        ind+=1
    return(n,tab)
        
def debut(lines): #get the first line of the results 
    for i in range(7,len(lines)):
        if lines[i][:9]=="Indicator":
            return i

def tailledonnees(lines,dbt): #get the size of the number of lines to be readen
    i = dbt+2
    cpt = 0
    while lines[i][:9]!="Indicator" and i<len(lines)-1:
        cpt+=1
        i+=1
    return cpt-1

def debutvar(lines,dbt):  #get the id of variables
    n = variables(lines)[0]
    tab = [dbt+2]
    for i in range(1,n):
        tab.append(dbt+2+i*(tailledonnees(lines,dbt)+3))
    return(tab)

def donnees(lines,dbt): #get the data
    dbtvar = debutvar(lines,dbt)
    tab = []
    for i in range(len(dbtvar)):
        temp = [lines[dbtvar[i]-2][10:-2]]
        for j in range(tailledonnees(lines,dbt)):
            line =  lines[dbtvar[i]+j][:-2].split("\t")
            inf = line[4].split("e")
            if len(inf)>1:
                inf_float = float(inf[0])*10**float(inf[1])
            else:
                inf_float = float(inf[0])
            sup = line[5].split("e")
            if len(sup)>1:
                sup_float = float(sup[0])*10**float(sup[1])
            else:
                sup_float = float(sup[0])
            temp.append([lines[dbtvar[i]-2][10:-2],float(line[2]),inf_float,sup_float])
        tab.append(temp)
    return(tab)
    
def distrib(data,tps): #reorganise the data into distributions
    tab = []
    for i in range(len(data)):
        temp = [int(data[i][1+tps][0])]
        for j in range(1,len(data[i][1+tps])):
            temp.append(data[i][1+tps][j])
        tab.append(temp)
                        
    return(tps,tab)

def distribution_finale(variable_n,taille,data): #generate the final plots
    
    for i in range(taille):
        plt.figure(dpi=300)
        distribfinale = distrib(data,i)[1]

        distribfinale.sort(key=lambda x: x[0])

        #Mean value
        plt.plot([i  for i in range(0,variable_n)],[distribfinale[i][1] for i in range(0,len(distribfinale))],color="red",label="Value")
        #trust interval
        plt.plot([i  for i in range(0,variable_n)],[distribfinale[i][2] for i in range(0,len(distribfinale))],"--",color="grey",label="95% interval")
        plt.plot([i  for i in range(0,variable_n)],[distribfinale[i][3] for i in range(0,len(distribfinale))],"--",color="grey")
        #mean value so it's above the grey lines
        plt.plot([i  for i in range(0,variable_n)],[distribfinale[i][1] for i in range(0,len(distribfinale))],color="red")
        titre = "Distribution after "+str(i)+" months"
        plt.title(titre)
        plt.legend(loc="best")
        plt.xlabel("Radiating elements")
        plt.ylabel("Probability")
        plt.grid()
        plt.show()
        
def heatmap(variable_n,taille,data): #genrating the final heatmap ie the life matrice 
    
    Zxx = []
    for i in range(taille):
        distribfinale = distrib(data,i)[1]

        distribfinale.sort(key=lambda x: x[0])

        Zxx.append([distribfinale[i][1] for i in range(0,len(distribfinale))])
        
    plt.figure(dpi=300)    
    c = plt.pcolormesh([i for i in range(0,variable_n+1)],[i for i in range(taille)], np.abs(Zxx),cmap ='gist_stern')
    plt.colorbar(c)
    plt.title('Life Matrice')
    plt.ylabel('Time [months]')
    plt.xlabel('Radiating elements')
    plt.show()

def val_temp3(data,seuil,variable_n): #print probability function over a certain level
    Val = []
    Valinf = []
    Valsup = []
    for j in range(len(data)):
        
        if int(data[j][0])>=seuil:
            tab = []
            tabinf = []
            tabsup = []
            for i in range(1,len(data[j])):
                tab.append(data[j][i][1])
                tabinf.append(data[j][i][2])
                tabsup.append(data[j][i][3])
            Val.append(tab)
            Valinf.append(tabinf)
            Valsup.append(tabsup)
    Sum = [sum([Val[i][j] for i in range(len(Val))]) for j in range(len(Val[0]))]
    Suminf = [sum([Valinf[i][j] for i in range(len(Val))]) for j in range(len(Val[0]))]
    Sumsup = [sum([Valsup[i][j] for i in range(len(Val))]) for j in range(len(Val[0]))]
    plt.figure(dpi=300) 
    plt.plot(Sum,color="red",label="Value")
    plt.plot(Suminf,"--",color="grey",label="95% interval")
    plt.plot(Sumsup,"--",color="grey")
    titre = "Probability of n > "+str(int(seuil*100/variable_n))+str("%")
    plt.title(titre)
    plt.grid()
    plt.legend(loc="best")
    plt.xlabel("Time [months]")
    plt.ylabel("Probability")
    plt.show()
    
def main(): # plot all the results

    #File path corresponding to the .csv output
    adresse = "P:/Polytechnique/Projet Thales/AltaRica/OARPlatform-win64-v1.1.0/OARPlatform-win64-v1.1.0/AltaRicaWizard/TAS - Monosatellite - Copie/Monosatellite_realistic_results.csv"
    
    file = open(adresse,"r")
    lines = file.readlines()
    
    variable_n = variables(lines)[0]
    
    dbt = debut(lines)
    
    taille = tailledonnees(lines,dbt)
    
    data = donnees(lines,dbt)
    
    distribution_finale(variable_n,taille,data)
    
    print("Month duration")
    print(taille-1)
    
    heatmap(variable_n,taille,data)
    
    s_50 = int(0.5*(variable_n+1))
    print(s_50)
    if s_50<variable_n:
        val_temp3(data,s_50,variable_n)

    s_90 = int(0.9*(variable_n+1))
    print(s_90)
    if s_90<variable_n:
        val_temp3(data,s_90,variable_n)

    s_95 = int(0.95*(variable_n+1))
    print(s_95)
    if s_95<variable_n:
        val_temp3(data,s_95,variable_n)

    s_98 = int(0.98*(variable_n+1))
    print(s_98)
    if s_98<variable_n:
        val_temp3(data,s_98,variable_n)