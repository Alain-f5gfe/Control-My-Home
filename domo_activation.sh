#!/usr/bin/python
# -*- encoding: utf-8 -*-

#dans windows installer cmder et ouvrir une console cmder
#installez python 3.8 sur le PC

mkdir ~/tableau_de_bord
cd ~/tableau_de_bord

# copiez tous les fichiers que je vous aie envoyé dans ce dossier
# modifiez le fichier etat_sonoff.py avec vos propres noms d'actionneurs (sonoff ou NodeMcu) et leurs IP

python3.8 -m venv .venv
source ~/tableau_de_bord/.venv/bin/activate

# le prompt doit être précédé par (.venv) ce qui indique que vous êtes
# maintenant dans un environnement virtuel

pip install -r requirements.txt

# va installer les dépendances nécessaires au script.
# faire un scanne du réseau pour mètre à jour la table arp de votre PC

nmap -sP 192.168.1.* # adaptez IP en fonction de votre box

# vous pouvez éditer votre table arp avec la commande

arp -a

python3.8 interface_domotique.py # lance l'interface
 