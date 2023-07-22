'''

__Presentation__:

Ce scrip permet de lire un fichier JSON contenant les données de toutes les stations du réseau infoclimat
et stocke la liste des stations avec leur nom, code, pays, departement, coordoonees dans un fichier CSV

__Prérequis__:
Python 3


__Dependances__:


__Imports__: requests.get, csv



__Input Data__: [liste des stations en open data](https://www.infoclimat.fr/opendata/stations_xhr.php?format=geojson)



__Author__: Steve Caron

__Contact email__: steve.caron.59@gmail.com

__Create at__: 2023-07-21



'''



import requests
import csv

def requeteAPI(code,date_debut,date_fin,token):
    '''
    Cette fonction fait une requete API sur la plateforme infoclimat
    Elle execute egalement la fonction testConnexion pour vérifier si la requete est réussie.
    
    @param : code: str, date_debut : str, date_fin : str
    @retrun : contenu de la page
    '''
    URL="https://www.infoclimat.fr/opendata/?method=get&format=csv&stations[]="+code+"&start="+date_debut+"&end="+date_fin+"&token="+token
    
    reponse = requests.get(URL)
    testConnexion(reponse)
    
    return reponse

def ecritureCSV(nomFichier,reponse):


    with open("./Data_brut/"+nomFichier,'w',newline='') as fichier:
        writer = csv.writer(fichier,delimiter=" ")
        writer.writerow(reponse.text.splitlines(True))

def testConnexion(reponse):

    
    if reponse.status_code == 200:
        print("Code :{}, la connexion api est établie".format(reponse.status_code))
    else:
        print("Code:{}, la connxeion api n'est pas établie".format(reponse.status_code))

def main(code,date_debut,date_fin,token):

    nomFichier = code+"_"+date_debut+"_"+date_fin+".csv"

    reponse = requeteAPI(code,date_debut,date_fin,token)
    
    ecritureCSV(nomFichier,reponse)



if __name__ == "__main__":

    code = "000QW"
    date_debut ="2020-01-01"
    date_fin = "2020-12-31"
    token = "Emp8A4J9Pk587RT3M5SwlhQ4jk3VtHVt0Qlq4XritihpvshdM7BVg"

    main(code,date_debut,date_fin,token)