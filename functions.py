# import data
import pandas as pd
df = pd.read_excel("data/dfMarque.xlsx")
Marque1 = list(df[df.SegMarque=="Marque 1"].Marque.drop_duplicates())
Marque2 = list(df[df.SegMarque=="Marque 2"].Marque.drop_duplicates())
Marque3 = list(df[df.SegMarque=="Marque 3"].Marque.drop_duplicates())
Marque4 = list(df[df.SegMarque=="Marque 4"].Marque.drop_duplicates())
Marque5 = list(df[df.SegMarque=="Marque 5"].Marque.drop_duplicates())
MarqueListe = list(df.Marque.drop_duplicates())

def MapValuerVenale(x):
    if int(x)<12000000:
        val = 2

    elif  int(x)<=25000000:
        val = 1

    elif  int(x)<40000000:
        val = 5

    elif  int(x)<90000000:
        val = 3

    elif int(x)<110000000:
        val =  0
    else:
        val = 4
    return val

def Model(model1,model2,model3,i,final_features):
    if i==1:
        predictions = model1.predict_proba(final_features)
        n_cluster=4
    elif i==2:
        n_cluster=4
        predictions = model2.predict_proba(final_features)
    else: 
        predictions = model3.predict_proba(final_features)
        n_cluster=3
    return predictions,n_cluster

def FrequenceCout(i):
    if i==1:
        frequence = [0.13,0.13,0.12,0.15]
        coutmoyen = [598455,549443,581034,581034]
    elif i==2:
        frequence = [0.190,0.210,0.100,0.070]
        coutmoyen = [1189889,1222377,1042983,1282302]
    else: 
        frequence = [0.550,0.370,0.330]
        coutmoyen = [863243,1161345,1203498]
    return frequence, coutmoyen

def MapFormula(x):
    if x=='formule1':
        x=0
    elif x=='formule2':
        x=1
    elif x=='formule3':
        x=2
    elif x=='formule4':
        x=3
    elif x=='formule5':
        x=4
    elif x=='formule6':
        x=5
    elif x=='formuleLibre':
            x=6
    return x


def MapGneder(x):
    if x=='Personne Morale':
        x=0
    elif x=='Monsieur':
        x=1
    elif x=='Madame':
        x=2
    return x

def MapEnergie(x):
    if x=='DIESEL':
        x=0
    else:
        x=1
    return x

def MapCategorie(x):
    if x=="Mono":
        x=1
    elif x=="Flotte":
        x= 0
    return x

def MapUsage(x):
    if x in ["Promenade et affaire","Promenade - trajet","Privé et Professionnel"]:
            x=1
    
    elif x in ["Trasport privé de marchandises","Transport public de marchandises"]:
        x=2
    elif x in ["Location avec chauffeur: Autobus","Location avec chauffeur: Utilitaire","Location Utilitaire"," Location avec chauffeur","Location véhicule de tourisme"]:
        x=3
    return x


def MapApporteur(x):
    if x=="Apporteur1":
            x=5
    elif x=="Apporteur2":
        x=1
    elif x=="Apporteur3":
        x=2
    elif x=="Apporteur4":
        x=3
    elif x=="Apporteur5":
        x=4
    elif x=="Apporteur6":
        x=5
    elif x=="Apporteur7":
        x=6
    elif x=="Apporteur8":
        x=7
    return x

def MapProfession(x):
    if x=="Salariés":
        x=5
    elif x=="VRP & autres professions":
        x=7
    elif x=="Profession inconnue":
        x=2
    elif x=="Fonctionnaires & assimilés":
        x=1
    elif x=="Sans profession":
        x=8
    elif x=="Profession libérale, médicale":
        x=3
    elif x=="Artisans":
        x=0
    elif x=="Agriculteurs":
        x=6
    elif x=="Retraité":
        x=4
    return x

def MapMarque(x):
    if x in Marque1:
        x=0
    elif x in Marque2:
        x=1
    elif x in Marque3:
        x=2
    elif x in Marque4:
        x=3
        
    elif x in Marque5:
        x=4
    return x	