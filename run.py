# Import flask library
from flask import Flask, jsonify,render_template, request, redirect, url_for
from functions import *
import numpy as np
import pandas as pd
import pickle
from datetime import datetime

import pandas as pd
df = pd.read_excel("data/dfMarque.xlsx")
Marque1 = list(df[df.SegMarque=="Marque 1"].Marque.drop_duplicates())
Marque2 = list(df[df.SegMarque=="Marque 2"].Marque.drop_duplicates())
Marque3 = list(df[df.SegMarque=="Marque 3"].Marque.drop_duplicates())
Marque4 = list(df[df.SegMarque=="Marque 4"].Marque.drop_duplicates())
Marque5 = list(df[df.SegMarque=="Marque 5"].Marque.drop_duplicates())
MarqueListe = list(df.Marque.drop_duplicates())

# create flask object application

# import models 
model1 = pickle.load(open('model/rfc.pkl', 'rb'))
model2 = pickle.load(open('model/log.pkl', 'rb'))
#model3 = pickle.load(open('model/xgb.pkl', 'rb'))
app = Flask(__name__)
#...
@app.route('/', methods=['post', 'get'])
def home():

    return render_template('login.html')

@app.route('/form',methods=['POST','GET'])
def form():
    
    Marque = MarqueListe
    if request.method == 'GET':
        return render_template('form.html',Marque=Marque)
    if request.method == 'POST':
        username = request.form.get('username')  
        password = request.form.get('password')
        if username == 'yara' and password == 'yara3796':
            return render_template('form.html',Marque=Marque)
        else:
            message = "Nom d'utilsateure ou Mot de passe incorrect "
            return render_template('login.html', message=message)

@app.route('/prediction',methods=['POST','GET'])
def prediction():
    
    if request.method == 'GET':
        df = pd.read_excel("data/tabExp.xlsx")
        dfRecap = pd.read_excel("data/Recap.xlsx")
        shape = df.shape[0]
        Classe = list(df.Classe)[0]
        FreqMoy = list(df.Frequence)[0]
        CoutMoy = list(df.CoutMoyen)[0]
        Prime_pure = list(df.Prime)[0]
        response = request.args
        Exposition = response['id_duree']
        Prime_ajustee = round(float(Prime_pure) * float(Exposition))
        garanties = list(request.args.values())
        Keys = list(request.args.keys())
        garantie = [gar for gar in garanties if gar!=Exposition]
        civilie = dfRecap.Values[0]

        return render_template('prediction.html',Keys=Keys,Prime_ajustee=Prime_ajustee,Exposition=Exposition,garantie=garantie,shape=shape,
        Classe=Classe,Prime_pure = Prime_pure,CoutMoy=CoutMoy,FreqMoy=FreqMoy,tables=dfRecap.values, titles=df.columns.values)
    
    elif request.method == 'POST':
      
        # first par
        civilite_val = MapGneder(request.form.get('form_Civilite') )
        civilite_recap = request.form.get('form_Civilite') 
        Place_val = request.form.get('formplaces') 
        Puissance_val = request.form.get('form_puissance')
  
        # second part 
        AgeAssure_val = request.form.get('form_ageassure')
        date_actuel = datetime.now().year
        print(f"L'année actuel : {date_actuel}")
        annee_naissance = AgeAssure_val.split("-")[0]
        AgeAssure_val = int(date_actuel) - int(annee_naissance)

        print(f"Age de l'assuré : {AgeAssure_val}")


        Aciennete_val = request.form.get('form_Anciennete')

        date_entree = Aciennete_val.split("-")[0]

        Aciennete_val = int(date_actuel) - int(date_entree)

        AgePermis_val = request.form.get('form_permis')
      
        # third part
        AgeVehicule_val = request.form.get('form_Agevehicule')
        Categorie_val = MapCategorie(request.form.get('form_categorie'))
        Energie_val = MapEnergie(request.form.get('form_energie'))
        
        Energie_recap = request.form.get('form_energie')
        Categorie_recap = request.form.get('form_categorie')
      
            # fourth part
        Profession_val = MapProfession(request.form.get('form_profession'))
        Marque_val = MapMarque(request.form.get('form_Marque'))
        Usage_val = MapUsage(request.form.get('form_Usage'))
        ValeurVenale_val = MapValuerVenale(request.form.get('id_ValeurVenale'))

        
        Profession_recap = request.form.get('form_profession')
        Marque_recap = request.form.get('form_Marque')
        Usage_recap = request.form.get('form_Usage')
    
        features = [civilite_val,Place_val,Puissance_val, AgeAssure_val,Aciennete_val ,AgePermis_val,
        AgeVehicule_val,ValeurVenale_val,Marque_val,Categorie_val,Energie_val,Usage_val,Profession_val]
        int_features = [int(x) for x in features]
        final_features = [np.array(int_features)]
        
        #prediction = model.predict(final_features)
        predicproba = model2.predict_proba(final_features)
        n_cluster = 5
        proba = [predicproba[0][i] for i in range(n_cluster)]
        
        Frequence=[0.12,0.29,0.19,0.01,0.10]
        FreqMoy = Frequence[np.argmax(proba)]
        
        Cout = [644971,886777,1256883,1277586,872572]
        CoutMoy = Cout[np.argmax(proba)]

        #Prime = [Cout[i]*Frequence[i] for i in range(n_cluster)]
        Prime = [41088.20,38908.65,36107.18,12775.86,51029.88]

        Classe = np.argmax(proba)+1
        probaL = [round(proba[i],2) for i in range(n_cluster)] 
        Prime_pure = round(sum([probaL[i]*Prime[i] for i in range(n_cluster)]))

        A= list(range(n_cluster))
        Prob= A + ["Prime"]
        
        df_ = pd.DataFrame({"Classe":[Classe],"Frequence":[FreqMoy],"CoutMoyen":[CoutMoy],"Prime":[Prime_pure]})
        val = probaL+[Prime_pure]
        dfproba = pd.DataFrame({"CLASSE":Prob,"Probabilite":val})
       
        dfproba.to_excel("data/tab.xlsx",index=False)
        df_.to_excel("data/tabExp.xlsx",index=False)
        Keys = []
        label=["Civilite","NbrePlace","Puissance","AgeAssure","Anciennete","AgePermis", "AgeVehicule","CategorieContrat","Energie","Profession","Marque","Usage"]
        Values = [civilite_recap,Place_val,Puissance_val,AgeAssure_val,Aciennete_val,AgePermis_val, AgeVehicule_val,Categorie_recap,Energie_recap,Profession_recap,Marque_recap,Usage_recap]
        dfRecap = pd.DataFrame({"Labels":label,"Values":Values})
        dfRecap.to_excel("data/Recap.xlsx",index=False)
        return render_template('prediction.html',Keys=Keys,ncluster=n_cluster,Classe=Classe,probaL = probaL,Prime_pure = Prime_pure,CoutMoy=CoutMoy,FreqMoy=FreqMoy)

# execute application
if __name__ == "__main__":
    app.run(debug=True)