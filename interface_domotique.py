#!/usr/bin/python3.8
#/home/f5gfe/tableau_de_bord/.venv/bin/python3
# -*- encoding: utf-8 -*-

''' 
#### Commande directe des objets de ma domotique dans une interface graphique. ###
Le but est d'avoir une interface de pilotage même si le serveur hébergeant Domoticz
est en panne
Attention: Il y a conflit entre cette interface et Domoticz si on les utilise
en parallèle. 
Il peut être nécessaire de lancer nmap afin de rafraîchir la table ARP du PC.

'''
import sys
from PySide6.QtWidgets import (
    QWidget, QLineEdit, QScrollArea, QMainWindow,
    QApplication, QVBoxLayout, QSpacerItem, QSizePolicy, QCompleter,
    QWidget, QLabel, QPushButton, QHBoxLayout)
from PySide6.QtCore import Qt
from pathlib import Path
import etat_sonoff
from etat_sonoff import sonoffIP, send_ordre_on, send_ordre_off, lecture_mesure

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.controls = QWidget()  # Controls main widget.
        self.controlsLayout = QVBoxLayout()   # Controls main layout.
        self.etat_actuel = 0
        self.modify_widgets()
        #la liste de noms des widgets isuues des clefs sont stockés dans une liste
        widget_names = []
        self.widgets = []
        
        # parcourir la liste en créant un nouveau OnOffWidget
        # pour chacun d'entre eux,déclencher la recherche de leur état l'ajouter au layout
        # + stocker sa référence dans la liste self.widgets
        for inter in etat_sonoff.sonoffIP:
            self.etat_actuel = (sonoffIP.get(inter)[1])
            item = OnOffWidget(inter)
            #print(inter, item)
            self.controlsLayout.addWidget(item)
            self.widgets.append(item)
            #print(self.widgets)
        
        
        # mise en page des éléments gestion de la taille des widgets
        spacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.controlsLayout.addItem(spacer)
        self.controls.setLayout(self.controlsLayout)
        
        # assenceur 
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.controls)

        # barre de recherche.
        self.searchbar = QLineEdit()
        self.searchbar.textChanged.connect(self.update_display)

        # Prédiction de texte de la barre de recherche
        self.completer = QCompleter(widget_names)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.searchbar.setCompleter(self.completer)

        # Ajouter des lignes info
        va = []
        self.alim = QLabel()
        try:
            va = lecture_mesure("192.168.1.220")
            #self.alim.setText(str(va))
            self.alim.setText(str(va[0])+"="+str(va[1])+"V   Courant="+str(va[3])+"A")
        except:
            self.alim.setText("Erreur de connexion")
            pass

        self.meteo = QLabel()
        tps = []
        try:
            tps = lecture_mesure("192.168.1.110")
            #self.meteo.setText(str(temps))
            self.meteo.setText(str(tps[0])+"="+str(tps[1])+"°   "\
                +str(tps[2])+"="+str(tps[3])+"%    "\
                +str(tps[4])+"="+str(tps[5])+"Hp")
        except:
            self.meteo.setText("Erreur de connexion")
            pass

        self.congel = QLabel()
        froid =[]
        try:
            froid = lecture_mesure("192.168.1.13", "5")# je vise le 5eme bloc de données
            self.congel.setText(str(froid[0])+" congélateur = "+ str(froid[1])+"°")
        except:
            self.congel.setText("Erreur de connexion")
            pass


        # Ajouter la ligne recherche VBoxLayout (appliqué au widget principal
        # qui englobe l'ensemble de la fenêtre).
        main = QWidget()
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.searchbar)
        mainLayout.addWidget(self.alim)
        mainLayout.addWidget(self.meteo)
        mainLayout.addWidget(self.congel)
        mainLayout.addWidget(self.scroll)

        main.setLayout(mainLayout)
        self.setCentralWidget(main)
        self.setGeometry(500, 100, 500, 700)
        self.setWindowTitle('Contrôle de la domotique')

    def update_display(self, text):
        '''
        rafraichit l'affichage de barre de recherche en 
        fonction de la recherche après conversion en minuscule
        '''
        for widget in self.widgets:
            if text.lower() in widget.name.lower():
                widget.show()
            else:
                widget.hide()

    def modify_widgets(self):
        css_file = Path.cwd() /"style.css"
        with open(css_file, "r") as f:
            self.setStyleSheet(f.read())
        
    def persit():
        ''' sauve l état des widgets '''
        # print("liste widgets ", self.widgets)


class OnOffWidget(QWidget):
    '''
    creation d'un widget personalisé d'un bouton en mode bistable
    '''
    def __init__(self, name):
        super(OnOffWidget, self).__init__()

        self.is_on = 0
        # print("le nom du widget ", name)
        self.name = name
        self.etat_actuel = (sonoffIP.get(self.name)[1])
        self.lbl = QLabel(self.name)
        self.btn_on = QPushButton("Marche")
        self.btn_on.setCheckable(True)
        self.btn_off = QPushButton("Arrêt ")
        self.btn_off.setCheckable(False)
        
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.lbl)
        self.hbox.addWidget(self.btn_on)
        self.hbox.addWidget(self.btn_off)

        self.btn_on.clicked.connect(self.on)
        self.btn_off.clicked.connect(self.off)
        self.setLayout(self.hbox)
        self.update_button_state()

    def show(self):
        """
        dans la recherche afficher ces widgets, et tous les widgets enfants.
        """
        for bidule in [self, self.lbl, self.btn_on, self.btn_off]:
            bidule.setVisible(True)

    def hide(self):
        """
        cacher ces widgets, et tous les widgets enfants.
        """
        for bidule in [self, self.lbl, self.btn_on, self.btn_off]:
            bidule.setVisible(False)

    def off(self):
        self.etat_actuel = 0
        send_ordre_off(self.name)
        self.update_button_state()
        print("etat_actuel après un clic off", self.etat_actuel)

    def on(self):
        self.etat_actuel = 1
        send_ordre_on(self.name)
        self.update_button_state()
        print("etat_actuel après un clic on", self.etat_actuel)

    def update_button_state(self):
        """
        Mettre à jour l'apparence des boutons de contrôle (On/Off)
        en fonction de l'état actuel.
        """
        if self.etat_actuel == 1:
            self.btn_on.setStyleSheet("background-color: #008000; color: #fff;")
            self.btn_off.setStyleSheet("background-color: none; color: #fff;")
        else:
            self.btn_on.setStyleSheet("background-color: none; color: #fff;")
            self.btn_off.setStyleSheet("background-color: #FF0000; color: #fff;")
            
    def persit(widgets):
        ''' sauve l état des widgets '''
        print(widgets)
        

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())

