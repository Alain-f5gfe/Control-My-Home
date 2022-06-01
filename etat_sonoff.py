#!/usr/bin/python3.8
# -*- encoding: utf-8 -*-
'''
But: tester si un sonoff a bien basculé d'état:
ce script est compatible avec ESPeasy.
requète demandant la valeur de l'état actuel du sonoff: 
http://192.168.1.142/json?view=sensorupdate&tasknr=1
on reçois un fichier Json.Ce fichier contient un dictionnaire qui contient 4 clefs. 
C'est la première clef "TaskValues" qu'on récupère. 
Cet élément contient une liste. je récupère son premier élément qui est un dico
j'en extrais la valeur liée à la clef "Value". C'est l'état du sonoff 1 = ON 0 = OFF

But N°2: 
je récupère les infos mesurées et transmisent par un NodeMCU/capteur de ma domotique
'''


import requests
import json

#liste de sonoff ou NodeMCU
sonoffIP = {
"Eclairage Salon":["http://192.168.1.26/json?view=sensorupdate&tasknr=1", "etat"],
"Pi-Star":["http://192.168.1.143/json?view=sensorupdate&tasknr=1", "etat"],
"Sonde Garage":["http://192.168.1.143/json?view=sensorupdate&tasknr=2", "etat"],
#"Cloture Electrique":["http://192.168.1.29/json?view=sensorupdate&tasknr=1", "etat"],
"Pompe Arrosage":["http://192.168.1.142/json?view=sensorupdate&tasknr=1", "etat"],
"NC":["http://192.168.1.142/json?view=sensorupdate&tasknr=2", "etat"],
"Lampe PC":["http://192.168.1.144/json?view=sensorupdate&tasknr=1", "etat"],
"NC Bureau":["http://192.168.1.144/json?view=sensorupdate&tasknr=2", "etat"]
} 

for inter in sonoffIP.keys():
    reponse = requests.get(sonoffIP.get(inter)[0]) #récupère la 1er valeur de la liste
    #reponse = requests.get("http://192.168.1.143/json?vi ew=sensorupdate&tasknr=1")
    donnes = reponse.json()
    value = ((donnes.get("TaskValues")).pop(0))["Value"]
    
    if value == 0:
        print(inter, " Etat OFF")
    else:
        print(inter, " Etat ON")

    sonoffIP[inter][1] = value #ajoute la valeur de l'état à la clef etat
    #print(sonoffIP.get(inter)[1])# affiche l'état du capteur avec 0 ou 1
    # forme de la requète: print("état pi-star ", sonoffIP.get("Pi-Star")[1])

def lecture_mesure(ip):
    '''
    Va lire les infos transmisent par un élément capteur de ma domotique
    ce déclenche en stipulant l'IP visé
    '''
    requete = "http://" + ip + "/json?view=sensorupdate&tasknr=1"
    print(requete)
    vap = requests.get(requete)
    valeurs = vap.json()
    for i in enumerate(valeurs.get("TaskValues")):
        val_capteur = (i[1])
        nom = val_capteur["Name"]
        valeur = val_capteur["Value"]
        print(nom, "=", valeur)
    '''
    # Etapes pas à pas laissées pour faciliter la compréhension de la lecture
    valeurs = vap.json()
    #volt = ((valeurs.get("TaskValues")).pop(0))["Value"]
    valeurs = vap.json()
    print(((valeurs.get("TaskValues")).pop(0))["Name"])
    valeurs = vap.json()
    print(((valeurs.get("TaskValues")).pop(0))["Value"])
    valeurs = vap.json()
    print(((valeurs.get("TaskValues")).pop(1))["Name"])
    valeurs = vap.json()
    print(((valeurs.get("TaskValues")).pop(1))["Value"])
    valeurs = vap.json()
    print(((valeurs.get("TaskValues")).pop(2))["Name"])
    valeurs = vap.json()
    print(((valeurs.get("TaskValues")).pop(2))["Value"])
    '''

def send_ordre_on(name):
    '''Envoie des commandes aux sonoff ou NodeMcu '''
    convert_name_ordre_on = {
    "Eclairage Salon":"http://192.168.1.26/control?cmd=gpio,12,1",
    "Pi-Star":"http://192.168.1.143/control?cmd=gpio,12,1",
    "Sonde Garage":"http://192.168.1.143/control?cmd=gpio,5,1",
    "Cloture Electrique":"http://192.168.1.29/control?cmd=gpio,12,1",
    "Pompe Arrosage":"http://192.168.1.142/control?cmd=gpio,12,1",
    "NC":"http://192.168.1.142/control?cmd=gpio,5,1",
    "Lampe PC":"http://192.168.1.144/control?cmd=gpio,12,1",
    "NC Bureau":"http://192.168.1.144/control?cmd=gpio,5,1"
    }
    cible = convert_name_ordre_on[name]
    requests.post(cible)

def send_ordre_off(name):
    convert_name_ordre_off = {
    "Eclairage Salon":"http://192.168.1.26/control?cmd=gpio,12,0",
    "Pi-Star":"http://192.168.1.143/control?cmd=gpio,12,0",
    "Sonde Garage":"http://192.168.1.143/control?cmd=gpio,5,0",
    "Cloture Electrique":"http://192.168.1.29/control?cmd=gpio,12,0",
    "Pompe Arrosage":"http://192.168.1.142/control?cmd=gpio,12,0",
    "NC":"http://192.168.1.142/control?cmd=gpio,5,0",
    "Lampe PC":"http://192.168.1.144/control?cmd=gpio,12,0",
    "NC Bureau":"http://192.168.1.144/control?cmd=gpio,5,0"
    }
    cible = convert_name_ordre_off[name]
    requests.post(cible)

#commande manuelle des fonctions
#lecture_mesure("192.168.1.220")
#send_ordre_on("Lampe PC")
#send_ordre_off("Lampe PC")