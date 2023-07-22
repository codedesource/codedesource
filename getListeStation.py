'''

__Presentation__:

Ce scrip permet de lire un fichier JSON contenant les données de toutes les stations du réseau infoclimat
et stocke la liste des stations avec leur nom, code, pays, departement, coordoonees dans un fichier CSV

__Prérequis__:
Python 3


__Dependances__:


__Imports__: pandas, Json



__Input Data__: [liste des stations en open data](https://www.infoclimat.fr/opendata/stations_xhr.php?format=geojson)



__Author__: Steve Caron

__Contact email__: steve.caron.59@gmail.com

__Create at__: 2023-07-21



'''

import pandas as pd
import json

chemin_fichier = "stations_xhr.json"

def ouvertureJson(chemin_fichier):
    ''' Cette fonction permet d'ouvrir un fichier de type Json '''

    with open(chemin_fichier, 'r') as file:
        data=json.load(file)
    
    return data

def SauvegardeCSV(pandasDataFrame):
    ''' Cette fonction sauvegarde le contenu d'un dataFramePandas dans un fichier csv'''
    pandasDataFrame.to_csv("liste_station.csv", index=False)

def stockageListe(dataJson):
    ''' Cette fonction parcours les elements d'un JSON et stocke
    le nom de la station, le code de la station, le département, le pays, la coordonnée x et la coordonnée y
    dans des listes
    Et retourne les listes'''

    #Initialise des listes vides
    liste_name = []
    liste_code = []
    liste_departement = []
    liste_pays = []
    liste_coordonnees_x = []
    liste_coordonnees_y = []
    liste_source = []

    #Parcours tous les features de mon Json, et extrait le nom, l'id, le département, le pays, les coordonées et les stocke dans des listes.
    for indice in range(len(dataJson["features"])):
        name = dataJson["features"][indice]["properties"]['name']
        liste_name.append(name)
        source = dataJson['features'][indice]['properties']['license']['source']
        liste_source.append(source)
        code = dataJson["features"][indice]["properties"]['id']
        liste_code.append(code)
        departement = dataJson["features"][indice]["properties"]['departement']
        liste_departement.append(departement)
        pays = dataJson["features"][indice]["properties"]['country']
        liste_pays.append(pays)
        coordonnees = dataJson["features"][indice]["geometry"]['coordinates']
        coordonnees_x = coordonnees[0]
        coordonnees_y = coordonnees[1]
        liste_coordonnees_x.append(coordonnees_x)
        liste_coordonnees_y.append(coordonnees_y)
    
    return liste_name,liste_code,liste_departement,liste_pays,liste_coordonnees_x,liste_coordonnees_y,liste_source

def transformeListesEnDataframe(liste_name,liste_code,liste_departement,liste_pays,liste_coordonnees_x,liste_coordonnees_y,liste_source):
    '''
    Cette fonction creer un dataFrame et insert dans mon dataFrame les listes en entrée.
    '''

    df = pd.DataFrame(list(zip(liste_name,liste_code,liste_departement,liste_pays,liste_coordonnees_x,liste_coordonnees_y,liste_source)),
                       columns = ['nom_station','code_station','departement','pays','coordonnees_x','coordonnees_y','source'])
    
    return df



if __name__ == "__main__":
    
    data = ouvertureJson(chemin_fichier)

    liste_name,liste_code,liste_departement,liste_pays,liste_coordonnees_x,liste_coordonnees_y,liste_source = stockageListe(data)

    dataFrame= transformeListesEnDataframe(liste_name,liste_code,liste_departement,liste_pays,liste_coordonnees_x,liste_coordonnees_y,liste_source)

    SauvegardeCSV(dataFrame)